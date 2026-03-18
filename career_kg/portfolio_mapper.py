"""
Portfolio image mapper — Dynamic KG-based portfolio page selection.

Queries Neo4j PortfolioPage nodes linked to Projects, Skills, and Achievements
to dynamically select relevant portfolio images for chatbot answers.
"""

MAX_IMAGES = 6


class PortfolioMapper:
    def __init__(self, graph_rag=None):
        self.graph = graph_rag

    def get_images(self, tool: str, graph_data, params: dict) -> list[dict]:
        """Dynamically select portfolio images based on KG graph traversal."""
        if not self.graph:
            return []

        project_ids, project_titles = self._extract_project_ids(tool, graph_data)
        skill_ids = self._extract_skill_ids(tool, graph_data)

        seen_pages = set()
        images = []

        # Priority 1a: pages linked to matched projects (by ID)
        if project_ids:
            try:
                for row in self.graph.get_portfolio_pages_for_projects(project_ids):
                    if row["page"] not in seen_pages:
                        seen_pages.add(row["page"])
                        images.append({
                            "page": row["page"],
                            "url": row["url"],
                            "caption": row["caption"],
                        })
            except Exception:
                pass

        # Priority 1b: pages linked to matched projects (by title)
        if project_titles and len(images) < MAX_IMAGES:
            try:
                for row in self.graph.get_portfolio_pages_for_project_titles(list(project_titles)):
                    if row["page"] not in seen_pages:
                        seen_pages.add(row["page"])
                        images.append({
                            "page": row["page"],
                            "url": row["url"],
                            "caption": row["caption"],
                        })
            except Exception:
                pass

        # Priority 2: pages linked to matched skills (supplement if needed)
        if skill_ids and len(images) < MAX_IMAGES:
            try:
                for row in self.graph.get_portfolio_pages_for_skills(skill_ids):
                    if row["page"] not in seen_pages:
                        seen_pages.add(row["page"])
                        images.append({
                            "page": row["page"],
                            "url": row["url"],
                            "caption": row["caption"],
                        })
            except Exception:
                pass

        # Priority 3: fallback to profile page
        if not images:
            try:
                for row in self.graph.get_portfolio_fallback("profile"):
                    images.append({
                        "page": row["page"],
                        "url": row["url"],
                        "caption": row["caption"],
                    })
            except Exception:
                pass

        return images[:MAX_IMAGES]

    def _extract_project_ids(self, tool: str, graph_data) -> tuple[list[str], set[str]]:
        """Extract project IDs and titles from graph_data. Returns (ids, titles)."""
        ids = set()
        titles = set()
        if isinstance(graph_data, list):
            for item in graph_data:
                if isinstance(item, dict):
                    # search_projects: "id", match_jd: "project_id"
                    for key in ("id", "project_id"):
                        val = item.get(key)
                        if val:
                            ids.add(val)
                    # query_achievements: "project" field is a title
                    if "project" in item and "achievement" in item:
                        titles.add(item["project"])
                    elif "project" in item and "achievement" not in item:
                        ids.add(item["project"])
        elif isinstance(graph_data, dict):
            # candidate_overview: career_timeline has project IDs
            for item in graph_data.get("career_timeline", []):
                if isinstance(item, dict) and item.get("project"):
                    ids.add(item["project"])
            # candidate_overview: achievements have project titles
            for item in graph_data.get("achievements", []):
                if isinstance(item, dict) and item.get("project"):
                    titles.add(item["project"])
            for item in graph_data.get("explicit_evolution", []):
                if isinstance(item, dict):
                    if item.get("from_project"):
                        ids.add(item["from_project"])
                    if item.get("to_project"):
                        ids.add(item["to_project"])
            for item in graph_data.get("evolution_chains", []):
                if isinstance(item, dict):
                    for key in ("project_1", "project_2", "project_3"):
                        if item.get(key):
                            ids.add(item[key])
        return list(ids), titles

    def _extract_skill_ids(self, tool: str, graph_data) -> list[str]:
        """Extract skill names from graph_data (used to match SHOWS_SKILL relationships)."""
        ids = set()
        if isinstance(graph_data, list):
            for item in graph_data:
                if isinstance(item, dict) and "skill" in item:
                    ids.add(item["skill"])
        elif isinstance(graph_data, dict):
            for item in graph_data.get("top_skills", []):
                if isinstance(item, dict) and "skill" in item:
                    ids.add(item["skill"])
        return list(ids)
