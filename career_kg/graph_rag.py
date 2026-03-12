"""
Career KG — Graph RAG Engine
HybridRetriever (vector + fulltext) + 4 Cypher analysis queries.
Pattern adapted from content_factory/graph_rag.py.
"""
import ast
import os
from pathlib import Path
from neo4j import GraphDatabase
from neo4j_graphrag.retrievers import HybridRetriever
from dotenv import load_dotenv
from llm_client import LLMClient

load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")


class GeminiEmbeddings:
    """Wrapper to match neo4j-graphrag embedder interface."""
    def __init__(self):
        self.client = LLMClient()

    def embed_query(self, text: str) -> list[float]:
        return self.client.get_embedding(text)


class CareerGraphRAG:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.auth = (os.getenv("NEO4J_USERNAME", "neo4j"), os.getenv("NEO4J_PASSWORD"))
        self.driver = GraphDatabase.driver(self.uri, auth=self.auth)

        # HybridRetriever for project search
        self.embedder = GeminiEmbeddings()
        self.retriever = HybridRetriever(
            driver=self.driver,
            vector_index_name="project_embedding_index",
            fulltext_index_name="project_fulltext_index",
            embedder=self.embedder,
            return_properties=[
                "id", "title", "title_kr", "summary",
                "description", "category", "scale_metrics",
            ],
        )

    def close(self):
        self.driver.close()

    # ─── Tool 1: search_projects ───────────────────────────────
    def search_projects(self, query: str, top_k: int = 5) -> list[dict]:
        """Hybrid search (vector + fulltext) over projects."""
        try:
            results = self.retriever.search(query_text=query, top_k=top_k)
            matched = []
            for item in results.items:
                raw = item.content
                if isinstance(raw, dict):
                    props = raw
                elif isinstance(raw, str):
                    try:
                        props = ast.literal_eval(raw)
                    except (ValueError, SyntaxError):
                        props = {}
                else:
                    props = {}
                matched.append({
                    "id": props.get("id"),
                    "title": props.get("title"),
                    "summary": props.get("summary"),
                    "description": props.get("description"),
                    "category": props.get("category"),
                    "scale_metrics": props.get("scale_metrics"),
                    "score": item.metadata.get("score") if item.metadata else None,
                })
            return matched
        except Exception as e:
            print(f"Search error: {e}")
            return []

    # ─── Tool 2: analyze_skills ────────────────────────────────
    def analyze_skills(self, top_n: int = 10) -> list[dict]:
        """Which skills are used across the most projects?"""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (p:Project)-[:USES_SKILL]->(s:Skill)
            RETURN s.name AS skill, s.category AS category, count(p) AS project_count
            ORDER BY project_count DESC
            LIMIT $top_n
            """, parameters={"top_n": top_n})
            return [dict(r) for r in result]

    # ─── Tool 3: match_jd ─────────────────────────────────────
    def match_jd(self, requirement_id: str) -> list[dict]:
        """Find projects that best demonstrate a JD requirement, ranked by strength."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (p:Project)-[r:DEMONSTRATES]->(j:JDRequirement {id: $req_id})
            RETURN p.id AS project_id, p.title AS title, p.summary AS summary,
                   r.strength AS strength, r.weight AS weight
            ORDER BY r.weight DESC
            """, parameters={"req_id": requirement_id})
            return [dict(r) for r in result]

    # ─── Tool 4: query_achievements ────────────────────────────
    def query_achievements(self, min_value: float = None) -> list[dict]:
        """Retrieve numeric achievements, optionally filtered by minimum value."""
        with self.driver.session() as session:
            if min_value is not None:
                result = session.run("""
                MATCH (p:Project)-[:PRODUCED]->(a:Achievement)
                WHERE a.metric_value IS NOT NULL AND a.metric_value >= $min_val
                RETURN p.title AS project, a.text AS achievement,
                       a.metric_value AS value, a.metric_unit AS unit
                ORDER BY a.metric_value DESC
                """, parameters={"min_val": min_value})
            else:
                result = session.run("""
                MATCH (p:Project)-[:PRODUCED]->(a:Achievement)
                WHERE a.metric_value IS NOT NULL
                RETURN p.title AS project, a.text AS achievement,
                       a.metric_value AS value, a.metric_unit AS unit
                ORDER BY a.metric_value DESC
                """)
            return [dict(r) for r in result]

    # ─── Bonus: career_timeline ────────────────────────────────
    def career_timeline(self) -> list[dict]:
        """Chronological view of projects with companies."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (p:Project)
            OPTIONAL MATCH (p)-[:AT_COMPANY]->(c:Company)
            RETURN p.title AS project, p.category AS category,
                   c.name AS company, p.start_date AS start_date, p.end_date AS end_date
            ORDER BY p.start_date
            """)
            return [dict(r) for r in result]

    # ─── HR Queries ──────────────────────────────────────────────
    def get_candidate_summary(self) -> dict:
        """Person info + aggregate stats for profile card."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (p:Person)
            OPTIONAL MATCH (p)-[:HELD_POSITION]->(pos:Position)
            OPTIONAL MATCH (p)-[:LED_PROJECT]->(proj:Project)
            OPTIONAL MATCH (p)-[:HAS_SKILL]->(s:Skill)
            RETURN p {.name, .name_kr, .title, .summary, .email, .linkedin} AS person,
                   count(DISTINCT pos) AS position_count,
                   count(DISTINCT proj) AS project_count,
                   count(DISTINCT s) AS skill_count
            """)
            record = result.single()
            if not record:
                return {}
            return {
                "person": dict(record["person"]),
                "position_count": record["position_count"],
                "project_count": record["project_count"],
                "skill_count": record["skill_count"],
            }

    def get_jd_fit_overview(self) -> list[dict]:
        """Aggregate JD match across all 6 requirements."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (p:Project)-[r:DEMONSTRATES]->(j:JDRequirement)
            RETURN j.id AS requirement_id, j.name AS name, j.name_kr AS name_kr,
                   sum(r.weight) AS total_weight, count(p) AS project_count
            ORDER BY total_weight DESC
            """)
            return [dict(r) for r in result]

    def get_project_with_relationships(self, project_id: str) -> dict:
        """Return a project with all connected nodes for visualization."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (p:Project {id: $pid})
            OPTIONAL MATCH (p)-[:USES_SKILL]->(s:Skill)
            OPTIONAL MATCH (p)-[:PRODUCED]->(a:Achievement)
            OPTIONAL MATCH (p)-[:AT_COMPANY]->(c:Company)
            OPTIONAL MATCH (p)-[d:DEMONSTRATES]->(j:JDRequirement)
            RETURN p {.id, .title, .title_kr, .summary, .category, .scale_metrics} AS project,
                   collect(DISTINCT s {.id, .name, .category}) AS skills,
                   collect(DISTINCT a {.id, .text, .metric_value, .metric_unit}) AS achievements,
                   c {.id, .name, .name_kr} AS company,
                   collect(DISTINCT {jd_id: j.id, jd_name: j.name, weight: d.weight, strength: d.strength}) AS jd_matches
            """, parameters={"pid": project_id})
            record = result.single()
            if not record:
                return {}
            return {
                "project": dict(record["project"]),
                "skills": [dict(s) for s in record["skills"] if s.get("id")],
                "achievements": [dict(a) for a in record["achievements"] if a.get("id")],
                "company": dict(record["company"]) if record["company"] else None,
                "jd_matches": [dict(j) for j in record["jd_matches"] if j.get("jd_id")],
            }

    # ─── Multi-Hop Evolution Queries ─────────────────────────────
    def skill_evolution_paths(self, skill_name: str = None) -> list[dict]:
        """Find chronological project chains connected by shared skills."""
        with self.driver.session() as session:
            if skill_name:
                result = session.run("""
                MATCH (p1:Project)-[:USES_SKILL]->(s:Skill)<-[:USES_SKILL]-(p2:Project)
                WHERE toLower(s.name) CONTAINS toLower($skill_name)
                  AND p1.start_date < p2.start_date
                RETURN s.name AS skill, s.category AS skill_category,
                       p1.title AS from_project, p1.start_date AS from_date, p1.category AS from_category,
                       p2.title AS to_project, p2.start_date AS to_date, p2.category AS to_category
                ORDER BY s.name, p1.start_date
                """, parameters={"skill_name": skill_name})
            else:
                result = session.run("""
                MATCH (p1:Project)-[:USES_SKILL]->(s:Skill)<-[:USES_SKILL]-(p2:Project)
                WHERE p1.start_date < p2.start_date
                WITH s, collect(DISTINCT p1.title) AS earlier_projects,
                     collect(DISTINCT p2.title) AS later_projects,
                     count(*) AS connection_count
                RETURN s.name AS skill, s.category AS skill_category,
                       earlier_projects, later_projects, connection_count
                ORDER BY connection_count DESC
                LIMIT 15
                """)
            return [dict(r) for r in result]

    def project_evolution_chains(self) -> list[dict]:
        """Find 3-hop project chains connected through shared skills chronologically."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (p1:Project)-[:USES_SKILL]->(s1:Skill)<-[:USES_SKILL]-(p2:Project),
                  (p2)-[:USES_SKILL]->(s2:Skill)<-[:USES_SKILL]-(p3:Project)
            WHERE p1.start_date <= p2.start_date
              AND p2.start_date <= p3.start_date
              AND p1.id <> p2.id AND p2.id <> p3.id AND p1.id <> p3.id
              AND s1.id <> s2.id
            RETURN p1.title AS project_1, p1.start_date AS date_1,
                   s1.name AS bridging_skill_1,
                   p2.title AS project_2, p2.start_date AS date_2,
                   s2.name AS bridging_skill_2,
                   p3.title AS project_3, p3.start_date AS date_3
            ORDER BY p1.start_date
            LIMIT 20
            """)
            return [dict(r) for r in result]

    def skill_timeline(self, category: str = None) -> list[dict]:
        """When each skill was first used and how adoption deepened over time."""
        with self.driver.session() as session:
            where_clause = "WHERE s.category = $category" if category else ""
            params = {"category": category} if category else {}
            result = session.run(f"""
            MATCH (p:Project)-[:USES_SKILL]->(s:Skill)
            {where_clause}
            WITH s, p ORDER BY p.start_date
            WITH s,
                 collect(p.title) AS projects_chronological,
                 collect(p.start_date) AS dates,
                 min(p.start_date) AS first_used,
                 count(p) AS total_projects
            WHERE total_projects >= 1
            RETURN s.name AS skill, s.category AS category,
                   first_used, total_projects,
                   projects_chronological, dates
            ORDER BY first_used, total_projects DESC
            """, parameters=params)
            return [dict(r) for r in result]

    def project_skill_overlap(self) -> list[dict]:
        """Find project pairs with the most shared skills (technology transfer density)."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (p1:Project)-[:USES_SKILL]->(s:Skill)<-[:USES_SKILL]-(p2:Project)
            WHERE p1.id < p2.id
            WITH p1, p2, collect(s.name) AS shared_skills, count(s) AS overlap_count
            WHERE overlap_count >= 2
            RETURN p1.title AS project_a, p1.start_date AS date_a, p1.category AS cat_a,
                   p2.title AS project_b, p2.start_date AS date_b, p2.category AS cat_b,
                   shared_skills, overlap_count
            ORDER BY overlap_count DESC
            """)
            return [dict(r) for r in result]

    def get_evolution_graph(self) -> list[dict]:
        """Return explicit project evolution chains via EVOLVED_INTO relationships."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (p1:Project)-[r:EVOLVED_INTO]->(p2:Project)
            RETURN p1.title AS from_project, p1.start_date AS from_date,
                   p2.title AS to_project, p2.start_date AS to_date,
                   r.evolution_type AS evolution_type,
                   r.description AS evolution_description
            ORDER BY p1.start_date
            """)
            return [dict(r) for r in result]

    def get_jd_descriptions(self) -> list[dict]:
        """Return all JD requirement definitions with full descriptions."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (j:JDRequirement)
            RETURN j.id AS id, j.name AS name, j.name_kr AS name_kr, j.description AS description
            ORDER BY j.id
            """)
            return [dict(r) for r in result]

    # ─── Candidate Gaps ──────────────────────────────────────────
    def get_candidate_gaps(self) -> list[dict]:
        """Return candidate gaps mapped to JD requirements."""
        with self.driver.session() as session:
            result = session.run("""
            MATCH (g:CandidateGap)
            OPTIONAL MATCH (g)-[:GAP_FOR]->(j:JDRequirement)
            RETURN g.id AS id, g.gap_description AS gap, g.mitigation AS mitigation,
                   g.severity AS severity, j.id AS requirement_id, j.name AS requirement_name
            ORDER BY
                CASE g.severity WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END
            """)
            return [dict(r) for r in result]

    # ─── Graph stats ───────────────────────────────────────────
    def get_stats(self) -> dict:
        """Return node/relationship counts."""
        with self.driver.session() as session:
            nodes = session.run("""
            MATCH (n)
            RETURN labels(n)[0] AS label, count(n) AS count
            ORDER BY count DESC
            """)
            node_stats = {r["label"]: r["count"] for r in nodes}

            rels = session.run("MATCH ()-[r]->() RETURN count(r) AS count")
            rel_count = rels.single()["count"]

            return {"nodes": node_stats, "total_relationships": rel_count}


if __name__ == "__main__":
    rag = CareerGraphRAG()
    print("Career Graph RAG initialized.")
    stats = rag.get_stats()
    print(f"Nodes: {stats['nodes']}")
    print(f"Relationships: {stats['total_relationships']}")
    rag.close()
