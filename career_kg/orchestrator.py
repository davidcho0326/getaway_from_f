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

5. "candidate_overview" — Comprehensive overview of the candidate (JD fit, skills, timeline)
   Parameters: {}
   Examples: "이 후보자에 대해 전반적으로 알려줘", "JD 요구사항과 얼마나 맞나요?", "후보자 종합 평가"

6. "skill_evolution" — Trace how a specific skill/technology evolved across projects over time
   Parameters: {"skill_name": "optional skill name filter, null for all"}
   Examples: "Python이 프로젝트 간 어떻게 발전했어?", "Neo4j 사용이 어떻게 진화했어?", "기술 진화 패턴 보여줘"

7. "project_evolution" — Show multi-hop project chains and how one project's technology feeds into the next
   Parameters: {}
   Examples: "프로젝트 간 기술 전이 보여줘", "프로젝트가 서로 어떻게 연결돼?", "기술 융합 패턴", "가장 큰 장점이 뭐야?"

8. "skill_timeline" — Show when each skill was first adopted and how usage deepened over time
   Parameters: {"category": "optional: AI/LLM, Production, Development, Cloud, Data, Language"}
   Examples: "기술 습득 타임라인", "AI 스킬 언제부터 썼어?", "스킬 성장 과정"

9. "general_qa" — General questions about career, motivation, strategy
   Parameters: {}
   Examples: "왜 Anthropic에 지원하나?", "자기소개 해줘"

10. "generate_resume" — Generate a resume section (summary, experience, skills, achievements) from KG data
    Parameters: {"section": "one of: summary, experience, skills, achievements, full"}
    Examples: "레쥬메 써줘", "Professional Summary 생성해줘", "경력 섹션 작성해줘", "이력서 만들어줘"

Respond with ONLY valid JSON (no markdown):
{"tool": "tool_name", "parameters": {...}}
"""

# ─── Synthesizer Prompt ───────────────────────────────────────
SYNTHESIZER_SYSTEM = """You are a career assessment assistant evaluating candidate Hansol Cho for the **Anthropic Account Executive (Startups), Seoul** position.

TARGET JD REQUIREMENTS — Always frame every answer through this lens:
1. B2B Startup Sales: 3+ years prospecting/closing startup leads, consultative solutions-oriented approach
2. Technical Stakeholder Sales: Selling to technical stakeholders, complex sales cycles, tailored solutions
3. Strategic Business Advisor: Deeply understanding startup founders' needs, creating innovative aligned solutions
4. AI Passion & Safety: Passion for AI, interest in safe/responsible AI development, frontier AI experience
5. Analytical + Creative Execution: Strategic market assessment + creative tactical execution, analytical customer understanding
6. Korean Market Expansion: Win new business, drive revenue in Korea, pinpoint new customer segments and use cases

CRITICAL RULES:
- Every answer MUST be evaluated through the lens of these 6 JD requirements
- Strengths → explain how each connects to specific JD requirements
- Weaknesses → identify gaps ONLY against these JD requirements (do NOT mention irrelevant technical gaps like ML/DL, Kubernetes, etc. — this is a sales/BD role, not an engineering role)
- Projects → frame how they demonstrate JD-relevant competencies
- Be balanced and evidence-based, grounded in the Knowledge Graph data
- Present in structured, scannable format with specific numbers
- Answer in the same language as the question (Korean if Korean, English if English)

If the graph data is insufficient, say so honestly rather than hallucinating.
"""


class RAGOrchestrator:
    def __init__(self):
        self.llm = LLMClient()
        self.graph = CareerGraphRAG()

    def close(self):
        self.graph.close()

    def _get_jd_context(self) -> dict:
        """Common JD context to inject into all tool results."""
        return {
            "jd_fit": self.graph.get_jd_fit_overview(),
            "jd_requirements": self.graph.get_jd_descriptions(),
            "candidate_gaps": self.graph.get_candidate_gaps(),
        }

    def process_query(self, query: str) -> str:
        """3-stage pipeline: Route → Retrieve → Synthesize."""
        result = self.process_query_with_metadata(query)
        return result["answer"]

    def process_query_with_metadata(self, query: str) -> dict:
        """3-stage pipeline returning answer + metadata for visualization."""
        # Stage 1: Intent Router
        tool, params = self._route(query)

        # Stage 2: Graph Engine
        graph_result_str = self._execute(tool, params)

        # Stage 3: Synthesize
        answer = self._synthesize(query, tool, graph_result_str)

        try:
            graph_data = json.loads(graph_result_str) if graph_result_str != "{}" else {}
        except json.JSONDecodeError:
            graph_data = {}

        return {
            "answer": answer,
            "tool": tool,
            "params": params,
            "graph_data": graph_data,
        }

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

        elif tool == "candidate_overview":
            jd_fit = self.graph.get_jd_fit_overview()
            timeline = self.graph.career_timeline()
            skills = self.graph.analyze_skills(top_n=10)
            summary = self.graph.get_candidate_summary()
            achievements = self.graph.query_achievements()
            evolution_chains = self.graph.project_evolution_chains()
            evolution_graph = self.graph.get_evolution_graph()
            context = {
                "candidate_summary": summary,
                "jd_fit": jd_fit,
                "career_timeline": timeline,
                "top_skills": skills,
                "achievements": achievements[:10],
                "evolution_chains": evolution_chains[:10],
                "explicit_evolution": evolution_graph,
                "candidate_gaps": self.graph.get_candidate_gaps(),
            }
            return json.dumps(context, ensure_ascii=False, indent=2)

        elif tool == "skill_evolution":
            skill_name = params.get("skill_name")
            paths = self.graph.skill_evolution_paths(skill_name=skill_name)
            overlap = self.graph.project_skill_overlap()
            evolution_graph = self.graph.get_evolution_graph()
            context = {
                "skill_evolution_paths": paths,
                "project_skill_overlap": overlap[:10],
                "explicit_evolution": evolution_graph,
                **self._get_jd_context(),
            }
            return json.dumps(context, ensure_ascii=False, indent=2)

        elif tool == "project_evolution":
            chains = self.graph.project_evolution_chains()
            overlap = self.graph.project_skill_overlap()
            evolution_graph = self.graph.get_evolution_graph()
            timeline = self.graph.career_timeline()
            context = {
                "evolution_chains": chains,
                "skill_overlap_matrix": overlap,
                "explicit_evolution": evolution_graph,
                "career_timeline": timeline,
                **self._get_jd_context(),
            }
            return json.dumps(context, ensure_ascii=False, indent=2)

        elif tool == "skill_timeline":
            category = params.get("category")
            results = self.graph.skill_timeline(category=category)
            context = {
                "skill_timeline": results,
                **self._get_jd_context(),
            }
            return json.dumps(context, ensure_ascii=False, indent=2)

        elif tool == "general_qa":
            stats = self.graph.get_stats()
            timeline = self.graph.career_timeline()
            skills = self.graph.analyze_skills(top_n=5)
            overlap = self.graph.project_skill_overlap()
            evolution_graph = self.graph.get_evolution_graph()
            context = {
                "graph_stats": stats,
                "career_timeline": timeline[:10],
                "top_skills": skills,
                "technology_connections": overlap[:5],
                "explicit_evolution": evolution_graph,
                **self._get_jd_context(),
            }
            return json.dumps(context, ensure_ascii=False, indent=2)

        elif tool == "generate_resume":
            section = params.get("section", "full")
            context = {
                "requested_section": section,
                "candidate_summary": self.graph.get_candidate_summary(),
                "career_timeline": self.graph.career_timeline(),
                "top_skills": self.graph.analyze_skills(top_n=15),
                "achievements": self.graph.query_achievements(),
                "jd_fit": self.graph.get_jd_fit_overview(),
                "evolution_chains": self.graph.project_evolution_chains()[:5],
                "candidate_gaps": self.graph.get_candidate_gaps(),
            }
            return json.dumps(context, ensure_ascii=False, indent=2)

        return "{}"

    def process_query_with_stream(self, query: str) -> dict:
        """Stage 1+2 synchronous, Stage 3 returns streaming generator."""
        tool, params = self._route(query)
        graph_result_str = self._execute(tool, params)

        try:
            graph_data = json.loads(graph_result_str) if graph_result_str != "{}" else {}
        except json.JSONDecodeError:
            graph_data = {}

        collected_text = []

        def logging_stream():
            for chunk in self._synthesize_stream(query, tool, graph_result_str):
                collected_text.append(chunk)
                yield chunk

        return {
            "stream": logging_stream(),
            "tool": tool,
            "params": params,
            "graph_data": graph_data,
            "get_full_answer": lambda: "".join(collected_text),
        }

    def _synthesize_stream(self, query: str, tool: str, graph_result: str):
        """Stage 3 (streaming): yield text chunks from Claude."""
        path_hint = ""
        if tool in ("skill_evolution", "project_evolution", "skill_timeline", "candidate_overview"):
            path_hint = """
IMPORTANT: The graph data below contains MULTI-HOP PATH data showing connections between projects through shared skills over time.
Do NOT just list projects and skills flatly. Instead, narrate the EVOLUTION STORY:
- How skills transferred from one project to the next, deepened, and fused across projects chronologically
- Identify patterns: skill deepening (same skill used more sophisticatedly), technology fusion (combining skills from different domains), adaptive transfer (repurposing a skill in a new context)
- Use temporal language: "started with...", "which then evolved into...", "culminating in..."
- The 'explicit_evolution' field shows confirmed project-to-project evolution links with descriptions
"""
        elif tool == "generate_resume":
            path_hint = """
IMPORTANT: You are generating a PROFESSIONAL RESUME section. Follow these rules:
- Write in English, polished and ATS-optimized
- Use strong action verbs (Led, Drove, Scaled, Architected, Negotiated)
- Include specific metrics: revenue (KRW/USD), percentages, team sizes, user counts
- Frame everything through the Anthropic AE (Startups) JD lens
- For "summary": 3-4 sentence professional summary highlighting B2B sales + AI expertise
- For "experience": bullet points per position, most impactful first, max 6 bullets per role
- For "skills": categorized list (AI/LLM, Production, Development, Cloud, Data, Languages)
- For "achievements": top 10 quantified achievements ranked by impact
- For "full": complete resume in markdown format with all sections
- Output in clean markdown format ready to copy-paste
"""

        prompt = f"""User Question: {query}

Tool Used: {tool}
{path_hint}
Knowledge Graph Data:
{graph_result}

Based on the graph data above, provide a comprehensive answer to the user's question.
Be specific with numbers, project names, and technologies.
Answer in the same language as the question (Korean if Korean, English if English).
"""
        yield from self.llm.generate_response_stream(prompt, system_instruction=SYNTHESIZER_SYSTEM)

    def _synthesize(self, query: str, tool: str, graph_result: str) -> str:
        """Stage 3: Combine graph data + original question → natural language answer."""
        path_hint = ""
        if tool in ("skill_evolution", "project_evolution", "skill_timeline", "candidate_overview"):
            path_hint = """
IMPORTANT: The graph data below contains MULTI-HOP PATH data showing connections between projects through shared skills over time.
Do NOT just list projects and skills flatly. Instead, narrate the EVOLUTION STORY:
- How skills transferred from one project to the next, deepened, and fused across projects chronologically
- Identify patterns: skill deepening (same skill used more sophisticatedly), technology fusion (combining skills from different domains), adaptive transfer (repurposing a skill in a new context)
- Use temporal language: "started with...", "which then evolved into...", "culminating in..."
- The 'explicit_evolution' field shows confirmed project-to-project evolution links with descriptions
"""
        elif tool == "generate_resume":
            path_hint = """
IMPORTANT: You are generating a PROFESSIONAL RESUME section. Follow these rules:
- Write in English, polished and ATS-optimized
- Use strong action verbs (Led, Drove, Scaled, Architected, Negotiated)
- Include specific metrics: revenue (KRW/USD), percentages, team sizes, user counts
- Frame everything through the Anthropic AE (Startups) JD lens
- For "summary": 3-4 sentence professional summary highlighting B2B sales + AI expertise
- For "experience": bullet points per position, most impactful first, max 6 bullets per role
- For "skills": categorized list (AI/LLM, Production, Development, Cloud, Data, Languages)
- For "achievements": top 10 quantified achievements ranked by impact
- For "full": complete resume in markdown format with all sections
- Output in clean markdown format ready to copy-paste
"""

        prompt = f"""User Question: {query}

Tool Used: {tool}
{path_hint}
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
