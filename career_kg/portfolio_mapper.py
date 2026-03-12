"""
Portfolio image mapper — KG 프로젝트 ID ↔ 포트폴리오 PDF 페이지 매핑.

챗봇 답변에 관련 포트폴리오 장표 이미지를 함께 표시하기 위한 모듈.
"""
import json
from pathlib import Path

# 프로젝트 ID → 대표 페이지 (최대 4장, UI 과부하 방지)
PROJECT_PAGE_MAP: dict[str, list[dict]] = {
    "fashion-image-tagging": [
        {"page": 4, "caption": "VARCO for F&F — System Overview"},
        {"page": 10, "caption": "VLM 데이터 전처리"},
    ],
    "fnf-studio": [
        {"page": 13, "caption": "AI Content Studio — Overview"},
        {"page": 14, "caption": "AI 화보 — 비용 99% 절감"},
        {"page": 23, "caption": "FNF STUDIO — Product Planning"},
        {"page": 25, "caption": "AI Video Workflow"},
    ],
    "linn-custom-nodes": [
        {"page": 13, "caption": "AI Content Studio"},
        {"page": 22, "caption": "Claude Code for ComfyUI"},
    ],
    "fnf-knowledge-graph-bi": [
        {"page": 3, "caption": "AI Content Generation Pipeline"},
        {"page": 12, "caption": "지식 그래프 기반 컨텐츠 기획"},
    ],
    "content-factory": [
        {"page": 12, "caption": "지식 그래프 기반 컨텐츠 기획"},
        {"page": 29, "caption": "Influencer Seeding Platform"},
    ],
    "entertainment-dashboard-grok": [
        {"page": 11, "caption": "SNS 트렌드 소셜 리스닝"},
        {"page": 34, "caption": "Grok Search API 트렌드 분석"},
    ],
    "fnco-influencer-seeding": [
        {"page": 29, "caption": "뷰티 인플루언서 시딩 플랫폼"},
        {"page": 30, "caption": "Influencer Seeding Dashboard"},
        {"page": 31, "caption": "93% 마케팅 업무 자동화"},
    ],
    "enterprise-ai-education": [
        {"page": 35, "caption": "전사 AI 교육"},
        {"page": 36, "caption": "AI 육성 프로그램 & CEO 리포팅"},
    ],
    "context-architect-training": [
        {"page": 35, "caption": "전사 AI 교육"},
    ],
    "brand-collaboration": [
        {"page": 40, "caption": "CJ ENM 디지털 광고 캠페인"},
    ],
    "gamecon": [
        {"page": 40, "caption": "CJ ENM 광고 캠페인"},
        {"page": 41, "caption": "CJ ENM 현장"},
    ],
    "china-ip-development": [
        {"page": 40, "caption": "CJ ENM 캠페인"},
    ],
    "ax-team-claude-code-skills": [
        {"page": 22, "caption": "Claude Code for ComfyUI"},
    ],
    "autoskill": [
        {"page": 22, "caption": "Claude Code Agentic Coding"},
    ],
}

# tool 레벨 폴백 (프로젝트 ID 추출 불가 시)
TOOL_PAGE_MAP: dict[str, list[int]] = {
    "candidate_overview": [2],
    "general_qa": [2],
    "analyze_skills": [2],
    "generate_resume": [2],
    "skill_timeline": [2],
}

MAX_IMAGES = 6


class PortfolioMapper:
    def __init__(self, pages_json_path: str = None):
        if pages_json_path is None:
            pages_json_path = str(Path(__file__).parent / "portfolio_pages.json")
        try:
            with open(pages_json_path) as f:
                pages = json.load(f)
            self.page_urls = {p["page"]: p["url"] for p in pages}
        except FileNotFoundError:
            self.page_urls = {}

    def get_images(self, tool: str, graph_data, params: dict) -> list[dict]:
        """tool + graph_data에서 관련 프로젝트를 추출하고 매핑된 포트폴리오 이미지 반환."""
        project_ids = self._extract_project_ids(tool, graph_data)

        seen_pages = set()
        images = []

        for pid in project_ids:
            for entry in PROJECT_PAGE_MAP.get(pid, []):
                if entry["page"] not in seen_pages:
                    seen_pages.add(entry["page"])
                    url = self.page_urls.get(entry["page"])
                    if url:
                        images.append({
                            "page": entry["page"],
                            "url": url,
                            "caption": entry["caption"],
                        })

        # 프로젝트 매칭 없으면 tool 레벨 폴백
        if not images:
            for page in TOOL_PAGE_MAP.get(tool, []):
                url = self.page_urls.get(page)
                if url:
                    images.append({"page": page, "url": url, "caption": "Candidate Profile"})

        return images[:MAX_IMAGES]

    def _extract_project_ids(self, tool: str, graph_data) -> list[str]:
        """graph_data 구조에 따라 프로젝트 ID 추출."""
        ids = []
        if isinstance(graph_data, list):
            for item in graph_data:
                if isinstance(item, dict):
                    pid = item.get("id") or item.get("project_id")
                    if pid:
                        ids.append(pid)
        elif isinstance(graph_data, dict):
            for key in ("career_timeline", "evolution_chains"):
                for item in graph_data.get(key, []):
                    if isinstance(item, dict):
                        pid = item.get("project") or item.get("from_project")
                        if pid:
                            ids.extend(self._title_to_ids(pid))
        return ids

    def _title_to_ids(self, title: str) -> list[str]:
        """프로젝트 제목에서 ID 추정 (부분 매칭)."""
        title_lower = title.lower()
        matched = []
        for pid in PROJECT_PAGE_MAP:
            keywords = pid.replace("-", " ").split()
            if any(kw in title_lower for kw in keywords if len(kw) > 3):
                matched.append(pid)
        return matched
