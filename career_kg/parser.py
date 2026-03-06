"""
Career KG — Parser
Extracts structured entities from markdown career documents using Claude Opus 4.6.
Outputs career_data.json for Neo4j ingestion.
"""
import json
from pathlib import Path
from llm_client import LLMClient

# Source files (relative to for_move/)
BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILES = {
    "resume": BASE_DIR / "resume_fin.md",
    "portfolio": BASE_DIR / "project_portfolio.md",
    "strategy": BASE_DIR / "st.md",
    "essays": BASE_DIR / "greenhouse_essays.md",
    "jd": BASE_DIR / "jd.md",
}

OUTPUT_FILE = Path(__file__).resolve().parent / "career_data.json"

EXTRACTION_SCHEMA = """
You are a structured data extractor. Given a markdown document about a person's career,
extract ALL entities and relationships into the following JSON schema.

Be thorough — extract every project, skill, achievement, and company mentioned.
For achievements, always include numeric metrics when available.

{
  "person": {
    "name": "string",
    "name_kr": "string",
    "email": "string",
    "phone": "string",
    "linkedin": "string",
    "title": "string — current professional title",
    "philosophy_major": true,
    "summary": "string — 1-2 sentence professional summary"
  },
  "companies": [
    {
      "id": "company_slug",
      "name": "string",
      "name_kr": "string or null",
      "industry": "string",
      "description": "string — brief description"
    }
  ],
  "positions": [
    {
      "id": "position_slug",
      "title": "string",
      "title_kr": "string or null",
      "company_id": "company_slug — references companies[].id",
      "start_date": "YYYY-MM or YYYY",
      "end_date": "YYYY-MM or 'Present'",
      "is_current": true/false,
      "key_responsibilities": ["string"]
    }
  ],
  "projects": [
    {
      "id": "project_slug",
      "title": "string",
      "title_kr": "string or null",
      "summary": "string — 1 sentence",
      "description": "string — detailed description, 2-4 sentences",
      "category": "claude_mastery | enterprise_ai | ecosystem",
      "company_id": "company_slug or null",
      "start_date": "YYYY-MM or YYYY or null",
      "end_date": "YYYY-MM or 'Present' or null",
      "scale_metrics": "string — key scale numbers",
      "skills_used": ["skill_slug"],
      "jd_requirements_demonstrated": [
        {"requirement_id": "jd_slug", "strength": "★★★ | ★★ | ★"}
      ]
    }
  ],
  "skills": [
    {
      "id": "skill_slug",
      "name": "string",
      "category": "AI/LLM | Production | Development | Cloud | Data | Language"
    }
  ],
  "achievements": [
    {
      "id": "achievement_slug",
      "text": "string — the achievement statement",
      "metric_value": "number or null",
      "metric_unit": "string or null — e.g. %, KRW, people, tools",
      "context": "string — brief context",
      "project_id": "project_slug or null",
      "position_id": "position_slug or null"
    }
  ],
  "jd_requirements": [
    {
      "id": "jd_slug",
      "name": "string",
      "name_kr": "string",
      "description": "string"
    }
  ]
}

IMPORTANT RULES:
- Use lowercase slugs with hyphens for all IDs (e.g. "fnf-studio", "neo4j", "b2b-sales")
- Every project must link to at least 2 jd_requirements
- Extract ALL numeric achievements (revenue, cost savings, team sizes, accuracy rates)
- For the JD requirements, use these 6 from the portfolio document:
  1. b2b-sales — B2B startup sales, consultative approach
  2. tech-sales — Selling to technical stakeholders
  3. strategic-advisor — Strategic business advisor to founders
  4. ai-passion — Passion for AI, especially safe AI
  5. analytical-execution — Analytical + creative execution
  6. korean-market — Korean market expansion
- Category mapping:
  - claude_mastery: Projects showing Claude/MCP expertise (Part 1 in portfolio)
  - enterprise_ai: Enterprise AI systems at F&F (Part 2 in portfolio)
  - ecosystem: AI ecosystem literacy, teaching, news (Part 3 in portfolio)
"""


def read_source(file_key: str) -> str:
    """Read a source markdown file."""
    path = SOURCE_FILES[file_key]
    if not path.exists():
        print(f"⚠ File not found: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def extract_from_sources(llm: LLMClient) -> dict:
    """Extract structured career data from all source markdown files."""
    # Combine key sources into one extraction prompt
    resume = read_source("resume")
    portfolio = read_source("portfolio")
    strategy = read_source("strategy")
    jd = read_source("jd")

    combined = f"""
=== RESUME (resume_fin.md) ===
{resume}

=== PROJECT PORTFOLIO (project_portfolio.md) ===
{portfolio}

=== STRATEGY DOCUMENT (st.md — first 3000 chars) ===
{strategy[:3000]}

=== JOB DESCRIPTION (jd.md) ===
{jd}
"""

    prompt = f"""Extract ALL structured career data from the following documents.
Return ONLY valid JSON matching the schema — no markdown fences, no explanation.

{combined}
"""

    print("⏳ Extracting entities with Claude Opus 4.6...")
    response = llm.generate_response(prompt, system_instruction=EXTRACTION_SCHEMA)

    # Strip markdown fences if present
    text = response.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    text = text.strip()

    try:
        data = json.loads(text)
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        print("Raw response (first 500 chars):", text[:500])
        # Save raw response for debugging
        debug_path = OUTPUT_FILE.with_suffix(".raw.txt")
        debug_path.write_text(text, encoding="utf-8")
        print(f"  Raw response saved to {debug_path}")
        raise


def validate_data(data: dict) -> list[str]:
    """Basic validation of extracted data."""
    issues = []

    if not data.get("person"):
        issues.append("Missing person data")
    if not data.get("companies"):
        issues.append("No companies extracted")
    if not data.get("positions"):
        issues.append("No positions extracted")

    projects = data.get("projects", [])
    if len(projects) < 5:
        issues.append(f"Only {len(projects)} projects (expected 10+)")

    skills = data.get("skills", [])
    if len(skills) < 10:
        issues.append(f"Only {len(skills)} skills (expected 20+)")

    achievements = data.get("achievements", [])
    if len(achievements) < 5:
        issues.append(f"Only {len(achievements)} achievements (expected 15+)")

    jd_reqs = data.get("jd_requirements", [])
    if len(jd_reqs) != 6:
        issues.append(f"{len(jd_reqs)} JD requirements (expected 6)")

    return issues


def print_summary(data: dict):
    """Print extraction summary."""
    print("\n📊 Extraction Summary")
    print("─" * 40)
    print(f"  Person:          {data.get('person', {}).get('name', 'N/A')}")
    print(f"  Companies:       {len(data.get('companies', []))}")
    print(f"  Positions:       {len(data.get('positions', []))}")
    print(f"  Projects:        {len(data.get('projects', []))}")
    print(f"  Skills:          {len(data.get('skills', []))}")
    print(f"  Achievements:    {len(data.get('achievements', []))}")
    print(f"  JD Requirements: {len(data.get('jd_requirements', []))}")
    print("─" * 40)

    issues = validate_data(data)
    if issues:
        print("\n⚠ Validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ All validations passed")


def main():
    llm = LLMClient()
    data = extract_from_sources(llm)
    print_summary(data)

    OUTPUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n💾 Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
