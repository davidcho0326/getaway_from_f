"""
Career KG — RAG Orchestrator
3-Stage pipeline: Intent Router → Graph Engine → Synthesizer
Pattern adapted from content_factory/rag_orchestrator.py.
"""
import json
from graph_rag import CareerGraphRAG
from llm_client import LLMClient

# ─── Router Prompt ────────────────────────────────────────────
ROUTER_PROMPT = """You are an intent router for a Career Knowledge Graph system.
Given a user question about Hansol Cho's career, classify it into ONE tool.

Available tools:
1. "search_projects" — Find projects by topic, keyword, or technology
   Parameters: {"query": "search terms"}
   Examples: "MCP 관련 프로젝트 알려줘", "Neo4j 쓴 프로젝트는?", "이미지 생성 관련 작업"

2. "analyze_skills" — Analyze skill distribution across projects
   Parameters: {"top_n": 10}
   Examples: "가장 많이 쓴 기술은?", "스킬 프로파일 보여줘", "어떤 기술을 가지고 있어?"

3. "match_jd" — Find projects matching a JD requirement
   Parameters: {"requirement_id": "one of: b2b-sales, tech-sales, strategic-advisor, ai-passion, analytical-execution, korean-market"}
   Examples: "B2B 영업 역량을 증명하는 프로젝트는?", "기술 세일즈 관련 경험은?", "AI 열정을 보여주는 사례"

4. "query_achievements" — Retrieve numeric achievements and metrics
   Parameters: {"min_value": null}
   Examples: "수치로 된 성과 보여줘", "매출 실적은?", "ROI 숫자 알려줘"

5. "general_qa" — General questions about career, motivation, strategy
   Parameters: {}
   Examples: "왜 Anthropic에 지원하나?", "자기소개 해줘", "강점이 뭐야?"

Respond with ONLY valid JSON (no markdown):
{"tool": "tool_name", "parameters": {...}}
"""

# ─── Synthesizer Prompt ───────────────────────────────────────
SYNTHESIZER_SYSTEM = """You are a career knowledge assistant for Hansol Cho,
who is applying for Account Executive (Startups) at Anthropic Korea.

When answering:
- Be specific and cite actual project names, metrics, and technologies
- Frame answers in the context of the Anthropic AE role when relevant
- Use both Korean and English naturally as appropriate
- For interview prep, structure answers with clear evidence points
- Always ground responses in the Knowledge Graph data provided

If the graph data is insufficient, say so honestly rather than hallucinating.
"""


class RAGOrchestrator:
    def __init__(self):
        self.llm = LLMClient()
        self.graph = CareerGraphRAG()

    def close(self):
        self.graph.close()

    def process_query(self, query: str) -> str:
        """3-stage pipeline: Route → Retrieve → Synthesize."""
        # Stage 1: Intent Router
        tool, params = self._route(query)

        # Stage 2: Graph Engine
        graph_result = self._execute(tool, params)

        # Stage 3: Synthesize
        answer = self._synthesize(query, tool, graph_result)
        return answer

    def _route(self, query: str) -> tuple[str, dict]:
        """Stage 1: Classify user intent into a tool call."""
        response = self.llm.generate_response(query, system_instruction=ROUTER_PROMPT)

        # Parse JSON response
        text = response.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        text = text.strip()

        try:
            parsed = json.loads(text)
            tool = parsed.get("tool", "general_qa")
            params = parsed.get("parameters", {})
        except json.JSONDecodeError:
            tool = "general_qa"
            params = {}

        return tool, params

    def _execute(self, tool: str, params: dict) -> str:
        """Stage 2: Execute the appropriate graph query."""
        if tool == "search_projects":
            results = self.graph.search_projects(
                query=params.get("query", ""),
                top_k=params.get("top_k", 5),
            )
            return json.dumps(results, ensure_ascii=False, indent=2)

        elif tool == "analyze_skills":
            results = self.graph.analyze_skills(
                top_n=params.get("top_n", 10)
            )
            return json.dumps(results, ensure_ascii=False, indent=2)

        elif tool == "match_jd":
            req_id = params.get("requirement_id", "")
            # Map Korean terms to IDs
            id_map = {
                "b2b": "b2b-sales", "영업": "b2b-sales", "세일즈": "b2b-sales",
                "기술": "tech-sales", "technical": "tech-sales",
                "전략": "strategic-advisor", "어드바이저": "strategic-advisor",
                "ai": "ai-passion", "열정": "ai-passion",
                "분석": "analytical-execution", "실행": "analytical-execution",
                "한국": "korean-market", "시장": "korean-market",
            }
            if req_id not in [
                "b2b-sales", "tech-sales", "strategic-advisor",
                "ai-passion", "analytical-execution", "korean-market"
            ]:
                for key, val in id_map.items():
                    if key in req_id.lower():
                        req_id = val
                        break

            results = self.graph.match_jd(requirement_id=req_id)
            return json.dumps(results, ensure_ascii=False, indent=2)

        elif tool == "query_achievements":
            min_val = params.get("min_value")
            results = self.graph.query_achievements(min_value=min_val)
            return json.dumps(results, ensure_ascii=False, indent=2)

        elif tool == "general_qa":
            # For general QA, gather broad context from the graph
            stats = self.graph.get_stats()
            timeline = self.graph.career_timeline()
            skills = self.graph.analyze_skills(top_n=5)
            context = {
                "graph_stats": stats,
                "career_timeline": timeline[:10],
                "top_skills": skills,
            }
            return json.dumps(context, ensure_ascii=False, indent=2)

        return "{}"

    def _synthesize(self, query: str, tool: str, graph_result: str) -> str:
        """Stage 3: Combine graph data + original question → natural language answer."""
        prompt = f"""User Question: {query}

Tool Used: {tool}

Knowledge Graph Data:
{graph_result}

Based on the graph data above, provide a comprehensive answer to the user's question.
Be specific with numbers, project names, and technologies.
Answer in the same language as the question (Korean if Korean, English if English).
"""
        return self.llm.generate_response(prompt, system_instruction=SYNTHESIZER_SYSTEM)


if __name__ == "__main__":
    orch = RAGOrchestrator()
    test_queries = [
        "MCP 서버를 만든 프로젝트는?",
        "가장 많이 사용한 기술 TOP 5",
    ]
    for q in test_queries:
        print(f"\n❓ {q}")
        print(f"💡 {orch.process_query(q)}")
    orch.close()
