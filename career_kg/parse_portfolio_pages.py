"""
Portfolio page parsing with Gemini 3.1 Pro Vision API.
Analyzes each portfolio page image and extracts structured metadata
for integration into the Career Knowledge Graph.

Usage:
    pip install google-genai>=1.51.0
    python3 parse_portfolio_pages.py
"""
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# Load known entity IDs from career_data.json
DATA_DIR = Path(__file__).parent / "data"
CAREER_DATA_PATH = Path(__file__).parent / "career_data.json"
PAGES_JSON_PATH = Path(__file__).parent / "portfolio_pages.json"
OUTPUT_PATH = DATA_DIR / "portfolio_page_annotations.json"


def load_known_entities() -> dict:
    with open(CAREER_DATA_PATH) as f:
        data = json.load(f)
    return {
        "project_ids": [p["id"] for p in data.get("projects", [])],
        "skill_ids": [s["id"] for s in data.get("skills", [])],
        "achievement_ids": [a["id"] for a in data.get("achievements", [])],
        "company_ids": [c["id"] for c in data.get("companies", [])],
    }


def build_prompt(entities: dict) -> str:
    return f"""You are analyzing a Korean portfolio page image for a career knowledge graph.
Extract structured metadata about what this page shows.

IMPORTANT: For mentioned_projects, mentioned_skills, mentioned_achievements, and mentioned_companies,
you MUST ONLY use IDs from the known lists below. Do NOT invent new IDs.

Known project IDs: {json.dumps(entities["project_ids"])}

Known skill IDs: {json.dumps(entities["skill_ids"])}

Known achievement IDs: {json.dumps(entities["achievement_ids"])}

Known company IDs: {json.dumps(entities["company_ids"])}

Analyze the image and return a JSON object with these fields:
{{
    "title": "The main title or headline visible on the page (in original language)",
    "caption": "A concise 1-line English description of what this page shows",
    "page_type": "One of: cover, profile, project_overview, project_detail, achievement, education, section_divider",
    "content_summary": "2-3 sentence description of the page content and its significance",
    "mentioned_projects": ["Only IDs from the known project list that are depicted or referenced"],
    "mentioned_skills": ["Only IDs from the known skill list that are shown or referenced"],
    "mentioned_achievements": ["Only IDs from the known achievement list that are shown"],
    "mentioned_companies": ["Only IDs from the known company list that appear"],
    "visual_keywords": ["Free-form descriptive tags for the visual content, e.g. 'dashboard', 'architecture diagram', 'before-after comparison'"]
}}"""


def validate_ids(annotation: dict, entities: dict) -> dict:
    """Remove any IDs that aren't in the known lists (hallucination guard)."""
    valid_sets = {
        "mentioned_projects": set(entities["project_ids"]),
        "mentioned_skills": set(entities["skill_ids"]),
        "mentioned_achievements": set(entities["achievement_ids"]),
        "mentioned_companies": set(entities["company_ids"]),
    }
    for field, valid_ids in valid_sets.items():
        if field in annotation:
            original = annotation[field]
            annotation[field] = [x for x in original if x in valid_ids]
            removed = set(original) - set(annotation[field])
            if removed:
                print(f"    Removed invalid {field}: {removed}")
    return annotation


def parse_all_pages():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)
    entities = load_known_entities()
    prompt_text = build_prompt(entities)

    with open(PAGES_JSON_PATH) as f:
        pages = json.load(f)

    print(f"Parsing {len(pages)} portfolio pages with Gemini 3.1 Pro Vision...")
    annotations = []

    for page_info in pages:
        page_num = page_info["page"]
        url = page_info["url"]
        print(f"  Page {page_num}/{len(pages)}: {url[:60]}...")

        try:
            image_bytes = requests.get(url, timeout=30).content
            image_part = types.Part.from_bytes(
                data=image_bytes, mime_type="image/png"
            )

            response = client.models.generate_content(
                model="gemini-3.1-pro-preview",
                contents=[image_part, prompt_text],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )

            annotation = json.loads(response.text)
            annotation = validate_ids(annotation, entities)
            annotation["page"] = page_num
            annotation["url"] = url
            annotations.append(annotation)
            print(f"    OK: {annotation.get('caption', 'no caption')[:60]}")

        except Exception as e:
            print(f"    ERROR: {e}")
            annotations.append({
                "page": page_num,
                "url": url,
                "title": "",
                "caption": f"Parse error: {e}",
                "page_type": "unknown",
                "content_summary": "",
                "mentioned_projects": [],
                "mentioned_skills": [],
                "mentioned_achievements": [],
                "mentioned_companies": [],
                "visual_keywords": [],
            })

        time.sleep(1)  # Rate limit

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(annotations, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(annotations)} annotations to {OUTPUT_PATH}")


if __name__ == "__main__":
    parse_all_pages()
