"""
Career KG — HR Graph RAG Chatbot
Streamlit web app for HR recruiters to explore Hansol Cho's career knowledge graph.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import json
import time
import uuid
import streamlit as st
from streamlit_agraph import agraph
from hr_config import QUICK_QUESTIONS, CANDIDATE_PROFILE, THEME, JD_REQUIREMENTS_DISPLAY
from query_logger import QueryLogger
from portfolio_mapper import PortfolioMapper
from graph_viz import (
    build_project_graph,
    build_jd_match_graph,
    build_skill_chart,
    build_achievement_chart,
    build_jd_fit_radar,
    AGRAPH_CONFIG,
)

st.set_page_config(
    page_title="Career Profile | Hansol Cho",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def init_orchestrator():
    """Initialize RAGOrchestrator once (cached across reruns)."""
    try:
        from orchestrator import RAGOrchestrator
        return RAGOrchestrator()
    except Exception as e:
        return None


@st.cache_resource
def init_logger():
    """Initialize QueryLogger once (cached across reruns)."""
    return QueryLogger()


@st.cache_resource
def init_portfolio_mapper():
    """Initialize PortfolioMapper once (cached across reruns)."""
    return PortfolioMapper()


def render_sidebar():
    """Render the sidebar: profile card + quick questions + graph stats."""
    with st.sidebar:
        st.markdown("### Candidate Profile")
        p = CANDIDATE_PROFILE
        st.markdown(f"**{p['name']}** ({p['name_kr']})")
        st.markdown(f"_{p['title']}_ @ {p['company']}")
        st.markdown(f"Target: {p['target_role']}")

        col1, col2 = st.columns(2)
        col1.metric("Years", p["years"])
        col2.metric("Projects", p["projects"])
        col3, col4 = st.columns(2)
        col3.metric("Skills", p["skills"])
        col4.metric("Achievements", p["achievements"])

        st.divider()
        st.markdown("### Quick Questions")

        for category, questions in QUICK_QUESTIONS.items():
            with st.expander(category, expanded=False):
                for q in questions:
                    if st.button(q["label"], key=f"qq_{q['label']}", use_container_width=True):
                        st.session_state.pending_query = q["query"]
                        st.rerun()

        st.divider()

        # Graph stats (only if connected)
        orch = init_orchestrator()
        if orch:
            try:
                stats = orch.graph.get_stats()
                st.markdown("### Knowledge Graph")
                node_total = sum(stats["nodes"].values())
                st.markdown(f"**Nodes:** {node_total} | **Relationships:** {stats['total_relationships']}")
                for label, count in stats["nodes"].items():
                    st.caption(f"  {label}: {count}")
            except Exception:
                st.caption("Graph stats unavailable")

        st.divider()
        st.markdown("### Query Logs")
        logger = init_logger()
        stats = logger.get_stats()

        col_a, col_b = st.columns(2)
        col_a.metric("Total Queries", stats["total"])
        col_b.metric("Avg Response", f"{stats['avg_ms']}ms")

        if stats["top_tools"]:
            st.caption("Top tools: " + ", ".join(
                f"{t['tool']} ({t['count']})" for t in stats["top_tools"]
            ))

        with st.expander("Recent Queries", expanded=False):
            logs = logger.get_recent(20)
            for entry in logs:
                st.caption(
                    f"**{entry['timestamp']}** | {entry['tool']} | {entry['response_ms']}ms\n\n"
                    f"Q: {entry['question'][:80]}"
                )


def render_portfolio_images(images: list[dict]):
    """Display portfolio page images in a responsive grid."""
    if not images:
        return
    st.markdown("#### 📎 Portfolio Reference")
    cols = st.columns(min(len(images), 3))
    for idx, img in enumerate(images):
        with cols[idx % 3]:
            st.image(img["url"], caption=f"p.{img['page']} — {img['caption']}", use_container_width=True)


def render_visualization(tool: str, graph_data, params: dict):
    """Render charts/graphs based on which tool was used."""
    if not graph_data:
        return

    try:
        if tool == "search_projects" and isinstance(graph_data, list):
            nodes, edges = build_project_graph(graph_data)
            if nodes:
                st.markdown("#### Project Network")
                agraph(nodes=nodes, edges=edges, config=AGRAPH_CONFIG)

        elif tool == "analyze_skills" and isinstance(graph_data, list):
            fig = build_skill_chart(graph_data)
            st.plotly_chart(fig, use_container_width=True)

        elif tool == "match_jd" and isinstance(graph_data, list):
            req_id = params.get("requirement_id", "")
            req_name = JD_REQUIREMENTS_DISPLAY.get(req_id, req_id)
            nodes, edges = build_jd_match_graph(graph_data, req_name)
            if nodes:
                st.markdown("#### JD Match Graph")
                agraph(nodes=nodes, edges=edges, config=AGRAPH_CONFIG)

        elif tool == "query_achievements" and isinstance(graph_data, list):
            fig = build_achievement_chart(graph_data)
            st.plotly_chart(fig, use_container_width=True)

        elif tool == "candidate_overview" and isinstance(graph_data, dict):
            jd_fit = graph_data.get("jd_fit", [])
            if jd_fit:
                fig = build_jd_fit_radar(jd_fit)
                st.plotly_chart(fig, use_container_width=True)

            skills = graph_data.get("top_skills", [])
            if skills:
                fig = build_skill_chart(skills)
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.caption(f"Visualization unavailable: {e}")


def process_and_display(query: str, orch):
    """Process a query through the RAG pipeline and display results with streaming."""
    logger = init_logger()
    start = time.time()

    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant"):
        with st.status("Analyzing...", expanded=True) as status:
            st.write("Routing intent...")
            result = orch.process_query_with_stream(query)
            st.write(f"Queried graph ({result['tool']})")
            status.update(label="Complete", state="complete", expanded=False)

        full_text = st.write_stream(result["stream"])

        render_visualization(result["tool"], result["graph_data"], result["params"])

        mapper = init_portfolio_mapper()
        portfolio_images = mapper.get_images(result["tool"], result["graph_data"], result["params"])
        render_portfolio_images(portfolio_images)

    elapsed_ms = int((time.time() - start) * 1000)

    logger.log(
        session_id=st.session_state.session_id,
        question=query,
        tool=result["tool"],
        params=result["params"],
        answer=result["get_full_answer"](),
        response_ms=elapsed_ms,
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_text,
        "tool": result["tool"],
        "params": result["params"],
        "graph_data": result["graph_data"],
        "portfolio_images": portfolio_images,
    })


def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]

    render_sidebar()

    # Main area header
    st.title("Career Knowledge Graph Chat")
    st.caption("Ask questions about candidate Hansol Cho — powered by Graph RAG")

    orch = init_orchestrator()
    if orch is None:
        st.error(
            "Could not connect to Neo4j or initialize LLM clients. "
            "Please check your .env file has NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, "
            "antrophic_API_key, and GOOGLE_API_KEY configured."
        )
        return

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("tool"):
                render_visualization(msg["tool"], msg.get("graph_data"), msg.get("params", {}))
                if msg.get("portfolio_images"):
                    render_portfolio_images(msg["portfolio_images"])

    # Handle pending query from quick question buttons
    pending = st.session_state.pending_query
    if pending:
        st.session_state.pending_query = None
        process_and_display(pending, orch)
        return

    # Chat input
    if query := st.chat_input("Ask about the candidate..."):
        process_and_display(query, orch)


if __name__ == "__main__":
    main()
