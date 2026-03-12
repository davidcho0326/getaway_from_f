"""
Career KG — Neo4j Ingest
Loads career_data.json and creates nodes/relationships in Neo4j.
Pattern adapted from content_factory/migrate_to_neo4j.py.
"""
import os
import json
from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv
from llm_client import LLMClient

# Load env
load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME", "neo4j"), os.getenv("NEO4J_PASSWORD"))
DATA_FILE = Path(__file__).resolve().parent / "data" / "career_data.json"


class CareerKGMigrator:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)
        self.llm = LLMClient()

    def close(self):
        self.driver.close()

    def clear_database(self):
        print("🧹 Clearing existing database...")
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def create_indexes(self):
        print("📇 Creating indexes...")
        with self.driver.session() as session:
            # Vector index for project embeddings
            try:
                session.run("""
                CREATE VECTOR INDEX project_embedding_index IF NOT EXISTS
                FOR (p:Project) ON (p.embedding)
                OPTIONS {indexConfig: {
                    `vector.dimensions`: 768,
                    `vector.similarity_function`: 'cosine'
                }}
                """)
                print("  ✅ Vector index: project_embedding_index")
            except Exception as e:
                print(f"  ⚠ Vector index: {e}")

            # Fulltext index for project search
            try:
                session.run("""
                CREATE FULLTEXT INDEX project_fulltext_index IF NOT EXISTS
                FOR (p:Project) ON EACH [p.title, p.summary, p.description]
                """)
                print("  ✅ Fulltext index: project_fulltext_index")
            except Exception as e:
                print(f"  ⚠ Fulltext index: {e}")

            # Fulltext index for achievement search
            try:
                session.run("""
                CREATE FULLTEXT INDEX achievement_fulltext_index IF NOT EXISTS
                FOR (a:Achievement) ON EACH [a.text]
                """)
                print("  ✅ Fulltext index: achievement_fulltext_index")
            except Exception as e:
                print(f"  ⚠ Achievement fulltext index: {e}")

    def ingest_data(self, data: dict):
        print("🚀 Starting ingestion...")
        with self.driver.session() as session:
            self._ingest_person(session, data.get("person", {}))
            self._ingest_companies(session, data.get("companies", []))
            self._ingest_positions(session, data)
            self._ingest_jd_requirements(session, data.get("jd_requirements", []))
            self._ingest_skills(session, data.get("skills", []))
            self._ingest_projects(session, data.get("projects", []))
            self._ingest_achievements(session, data)
            self._ingest_candidate_gaps(session, data.get("candidate_gaps", []))
            self._ingest_project_evolution(session, data.get("project_evolution", []))
        print("✅ Ingestion complete")

    def _ingest_person(self, session, person: dict):
        if not person:
            return
        session.run("""
        MERGE (p:Person {name: $name})
        SET p.name_kr = $name_kr,
            p.email = $email,
            p.phone = $phone,
            p.linkedin = $linkedin,
            p.title = $title,
            p.philosophy_major = $philosophy_major,
            p.summary = $summary
        """, parameters={
            "name": person.get("name", ""),
            "name_kr": person.get("name_kr"),
            "email": person.get("email", ""),
            "phone": person.get("phone", ""),
            "linkedin": person.get("linkedin", ""),
            "title": person.get("title", ""),
            "philosophy_major": person.get("philosophy_major", True),
            "summary": person.get("summary", ""),
        })
        print(f"  👤 Person: {person.get('name')}")

    def _ingest_companies(self, session, companies: list):
        for c in companies:
            session.run("""
            MERGE (c:Company {id: $id})
            SET c.name = $name,
                c.name_kr = $name_kr,
                c.industry = $industry,
                c.description = $description
            """, parameters={
                "id": c["id"],
                "name": c.get("name", ""),
                "name_kr": c.get("name_kr"),
                "industry": c.get("industry", ""),
                "description": c.get("description", ""),
            })
        print(f"  🏢 Companies: {len(companies)}")

    def _ingest_positions(self, session, data: dict):
        person_name = data.get("person", {}).get("name", "")
        positions = data.get("positions", [])
        for pos in positions:
            session.run("""
            MERGE (pos:Position {id: $id})
            SET pos.title = $title,
                pos.title_kr = $title_kr,
                pos.start_date = $start_date,
                pos.end_date = $end_date,
                pos.is_current = $is_current
            """, parameters={
                "id": pos["id"],
                "title": pos.get("title", ""),
                "title_kr": pos.get("title_kr"),
                "start_date": pos.get("start_date", ""),
                "end_date": pos.get("end_date", ""),
                "is_current": pos.get("is_current", False),
            })
            # Person -[:HELD_POSITION]-> Position
            if person_name:
                session.run("""
                MATCH (p:Person {name: $person_name})
                MATCH (pos:Position {id: $pos_id})
                MERGE (p)-[:HELD_POSITION]->(pos)
                """, parameters={"person_name": person_name, "pos_id": pos["id"]})

            # Position -[:AT_COMPANY]-> Company
            company_id = pos.get("company_id")
            if company_id:
                session.run("""
                MATCH (pos:Position {id: $pos_id})
                MATCH (c:Company {id: $company_id})
                MERGE (pos)-[:AT_COMPANY]->(c)
                """, parameters={"pos_id": pos["id"], "company_id": company_id})

                # Person -[:WORKED_AT]-> Company
                if person_name:
                    session.run("""
                    MATCH (p:Person {name: $person_name})
                    MATCH (c:Company {id: $company_id})
                    MERGE (p)-[:WORKED_AT]->(c)
                    """, parameters={"person_name": person_name, "company_id": company_id})

        print(f"  💼 Positions: {len(positions)}")

    def _ingest_jd_requirements(self, session, jd_reqs: list):
        for jd in jd_reqs:
            session.run("""
            MERGE (j:JDRequirement {id: $id})
            SET j.name = $name,
                j.name_kr = $name_kr,
                j.description = $description
            """, parameters={
                "id": jd["id"],
                "name": jd.get("name", ""),
                "name_kr": jd.get("name_kr", ""),
                "description": jd.get("description", ""),
            })
        print(f"  📋 JD Requirements: {len(jd_reqs)}")

    def _ingest_skills(self, session, skills: list):
        for s in skills:
            session.run("""
            MERGE (s:Skill {id: $id})
            SET s.name = $name,
                s.category = $category
            """, parameters={
                "id": s["id"],
                "name": s.get("name", ""),
                "category": s.get("category", ""),
            })
        print(f"  🛠 Skills: {len(skills)}")

    def _ingest_projects(self, session, projects: list):
        person_name = ""
        # Try to get person name from the data file
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                person_name = d.get("person", {}).get("name", "")
        except Exception:
            pass

        for proj in projects:
            # Generate embedding for project
            embed_text = f"{proj.get('title', '')}. {proj.get('summary', '')} {proj.get('description', '')}"
            embedding = self.llm.get_embedding(embed_text)

            session.run("""
            MERGE (p:Project {id: $id})
            SET p.title = $title,
                p.title_kr = $title_kr,
                p.summary = $summary,
                p.description = $description,
                p.category = $category,
                p.start_date = $start_date,
                p.end_date = $end_date,
                p.scale_metrics = $scale_metrics,
                p.embedding = $embedding
            """, parameters={
                "id": proj["id"],
                "title": proj.get("title", ""),
                "title_kr": proj.get("title_kr"),
                "summary": proj.get("summary", ""),
                "description": proj.get("description", ""),
                "category": proj.get("category", ""),
                "start_date": proj.get("start_date"),
                "end_date": proj.get("end_date"),
                "scale_metrics": proj.get("scale_metrics", ""),
                "embedding": embedding,
            })

            # Person -[:LED_PROJECT]-> Project
            if person_name:
                session.run("""
                MATCH (p:Person {name: $person_name})
                MATCH (proj:Project {id: $proj_id})
                MERGE (p)-[:LED_PROJECT]->(proj)
                """, parameters={"person_name": person_name, "proj_id": proj["id"]})

            # Project -[:AT_COMPANY]-> Company
            company_id = proj.get("company_id")
            if company_id:
                session.run("""
                MATCH (proj:Project {id: $proj_id})
                MATCH (c:Company {id: $company_id})
                MERGE (proj)-[:AT_COMPANY]->(c)
                """, parameters={"proj_id": proj["id"], "company_id": company_id})

            # Project -[:USES_SKILL]-> Skill
            for skill_id in proj.get("skills_used", []):
                session.run("""
                MATCH (proj:Project {id: $proj_id})
                MATCH (s:Skill {id: $skill_id})
                MERGE (proj)-[:USES_SKILL]->(s)
                """, parameters={"proj_id": proj["id"], "skill_id": skill_id})

            # Project -[:DEMONSTRATES]-> JDRequirement
            for jd_map in proj.get("jd_requirements_demonstrated", []):
                strength = jd_map.get("strength", "★")
                # Convert stars to numeric weight
                weight = strength.count("★")
                session.run("""
                MATCH (proj:Project {id: $proj_id})
                MATCH (j:JDRequirement {id: $jd_id})
                MERGE (proj)-[r:DEMONSTRATES]->(j)
                SET r.strength = $strength, r.weight = $weight
                """, parameters={
                    "proj_id": proj["id"],
                    "jd_id": jd_map["requirement_id"],
                    "strength": strength,
                    "weight": weight,
                })

            # Person -[:HAS_SKILL]-> Skill (via projects)
            if person_name:
                for skill_id in proj.get("skills_used", []):
                    session.run("""
                    MATCH (p:Person {name: $person_name})
                    MATCH (s:Skill {id: $skill_id})
                    MERGE (p)-[:HAS_SKILL]->(s)
                    """, parameters={"person_name": person_name, "skill_id": skill_id})

            print(f"    📁 {proj['id']}")

        print(f"  📦 Projects: {len(projects)}")

    def _ingest_achievements(self, session, data: dict):
        achievements = data.get("achievements", [])
        for ach in achievements:
            session.run("""
            MERGE (a:Achievement {id: $id})
            SET a.text = $text,
                a.metric_value = $metric_value,
                a.metric_unit = $metric_unit,
                a.context = $context
            """, parameters={
                "id": ach["id"],
                "text": ach.get("text", ""),
                "metric_value": ach.get("metric_value"),
                "metric_unit": ach.get("metric_unit"),
                "context": ach.get("context", ""),
            })

            # Project -[:PRODUCED]-> Achievement
            project_id = ach.get("project_id")
            if project_id:
                session.run("""
                MATCH (proj:Project {id: $proj_id})
                MATCH (a:Achievement {id: $ach_id})
                MERGE (proj)-[:PRODUCED]->(a)
                """, parameters={"proj_id": project_id, "ach_id": ach["id"]})

            # Position -[:PRODUCED]-> Achievement
            position_id = ach.get("position_id")
            if position_id:
                session.run("""
                MATCH (pos:Position {id: $pos_id})
                MATCH (a:Achievement {id: $ach_id})
                MERGE (pos)-[:PRODUCED]->(a)
                """, parameters={"pos_id": position_id, "ach_id": ach["id"]})

        print(f"  🏆 Achievements: {len(achievements)}")

    def _ingest_candidate_gaps(self, session, gaps: list):
        for gap in gaps:
            session.run("""
            MERGE (g:CandidateGap {id: $id})
            SET g.gap_description = $gap_description,
                g.mitigation = $mitigation,
                g.severity = $severity
            """, parameters={
                "id": gap["id"],
                "gap_description": gap.get("gap_description", ""),
                "mitigation": gap.get("mitigation", ""),
                "severity": gap.get("severity", "medium"),
            })

            # CandidateGap -[:GAP_FOR]-> JDRequirement
            req_id = gap.get("requirement_id")
            if req_id and req_id != "general":
                session.run("""
                MATCH (g:CandidateGap {id: $gap_id})
                MATCH (j:JDRequirement {id: $req_id})
                MERGE (g)-[:GAP_FOR]->(j)
                """, parameters={"gap_id": gap["id"], "req_id": req_id})

        print(f"  ⚠️ Candidate Gaps: {len(gaps)}")

    def _ingest_project_evolution(self, session, evolutions: list):
        for evo in evolutions:
            session.run("""
            MATCH (p1:Project {id: $from_id})
            MATCH (p2:Project {id: $to_id})
            MERGE (p1)-[r:EVOLVED_INTO]->(p2)
            SET r.evolution_type = $evolution_type,
                r.description = $description
            """, parameters={
                "from_id": evo["from"],
                "to_id": evo["to"],
                "evolution_type": evo.get("evolution_type", ""),
                "description": evo.get("description", ""),
            })
        print(f"  🔗 Project Evolutions: {len(evolutions)}")


def print_stats(driver):
    """Print node/relationship counts from Neo4j."""
    print("\n📊 Neo4j Graph Statistics")
    print("─" * 40)
    with driver.session() as session:
        result = session.run("""
        MATCH (n)
        RETURN labels(n)[0] AS label, count(n) AS count
        ORDER BY count DESC
        """)
        total_nodes = 0
        for record in result:
            label = record["label"]
            count = record["count"]
            total_nodes += count
            print(f"  {label}: {count}")

        result = session.run("MATCH ()-[r]->() RETURN count(r) AS count")
        total_rels = result.single()["count"]

        print("─" * 40)
        print(f"  Total nodes: {total_nodes}")
        print(f"  Total relationships: {total_rels}")


def main():
    if not DATA_FILE.exists():
        print(f"❌ {DATA_FILE} not found. Run parser.py first.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    migrator = CareerKGMigrator(URI, AUTH)
    try:
        migrator.clear_database()
        migrator.create_indexes()
        migrator.ingest_data(data)
        print_stats(migrator.driver)
        print("\n🎉 Migration Complete!")
    except Exception as e:
        print(f"❌ Migration Failed: {e}")
        raise
    finally:
        migrator.close()


if __name__ == "__main__":
    main()
