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
