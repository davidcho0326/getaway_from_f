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

        project_ids = self._extract_project_ids(tool, graph_data)
        skill_ids = self._extract_skill_ids(tool, graph_data)

        seen_pages = set()
        images = []

        # Priority 1: pages linked to matched projects
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

    def _extract_project_ids(self, tool: str, graph_data) -> list[str]:
        """Extract project IDs from graph_data based on tool type."""
        ids = []
        if isinstance(graph_data, list):
            for item in graph_data:
                if isinstance(item, dict):
                    pid = item.get("id") or item.get("project_id")
                    if pid:
                        ids.append(pid)
        elif isinstance(graph_data, dict):
            for key in ("career_timeline", "evolution_chains", "explicit_evolution"):
                for item in graph_data.get(key, []):
                    if isinstance(item, dict):
                        pid = item.get("project") or item.get("from_project")
                        if pid:
                            ids.append(pid)
        return ids

    def _extract_skill_ids(self, tool: str, graph_data) -> list[str]:
        """Extract skill IDs from graph_data based on tool type."""
        ids = []
        if isinstance(graph_data, list):
            for item in graph_data:
                if isinstance(item, dict) and "skill" in item:
                    ids.append(item["skill"])
        elif isinstance(graph_data, dict):
            for item in graph_data.get("top_skills", []):
                if isinstance(item, dict) and "skill" in item:
                    ids.append(item["skill"])
        return ids
