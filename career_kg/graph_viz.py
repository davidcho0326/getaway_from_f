"""
Career KG — Graph Visualization Utilities
Converts Neo4j query results into streamlit-agraph nodes/edges and Plotly charts.
"""
from streamlit_agraph import Node, Edge, Config
import plotly.graph_objects as go
from hr_config import THEME

AGRAPH_CONFIG = Config(
    width=700,
    height=400,
    directed=True,
    physics=True,
    hierarchical=False,
)

_colors = THEME["node_colors"]


def build_project_graph(projects: list[dict]) -> tuple[list, list]:
    """Build agraph nodes/edges from search_projects results."""
    nodes = []
    edges = []
    seen = set()

    for p in projects:
        pid = p.get("id", "")
        if not pid or pid in seen:
            continue
        seen.add(pid)
        label = p.get("title", pid)[:30]
        nodes.append(Node(
            id=pid, label=label, size=30,
            color=_colors["Project"],
            title=p.get("summary", ""),
        ))
        cat = p.get("category", "")
        if cat and cat not in seen:
            seen.add(cat)
            nodes.append(Node(
                id=cat, label=cat, size=20,
                color=_colors["Skill"],
            ))
        if cat:
            edges.append(Edge(source=pid, target=cat, label="category"))

    return nodes, edges


def build_jd_match_graph(jd_results: list[dict], requirement_name: str = "JD") -> tuple[list, list]:
    """Star graph: JD requirement at center, matching projects around it."""
    nodes = [Node(
        id="jd_center", label=requirement_name, size=35,
        color=_colors["JDRequirement"],
    )]
    edges = []

    for item in jd_results:
        pid = item.get("project_id", item.get("id", ""))
        if not pid:
            continue
        title = item.get("title", pid)[:25]
        strength = item.get("strength", "")
        nodes.append(Node(
            id=pid, label=title, size=25,
            color=_colors["Project"],
            title=f"Strength: {strength}",
        ))
        edges.append(Edge(
            source="jd_center", target=pid,
            label=strength,
            width=item.get("weight", 1) * 2,
        ))

    return nodes, edges


def build_skill_chart(skills_data: list[dict]) -> go.Figure:
    """Horizontal bar chart of skill frequency across projects."""
    if not skills_data:
        return go.Figure()

    skills = [s.get("skill", "") for s in skills_data]
    counts = [s.get("project_count", 0) for s in skills_data]
    categories = [s.get("category", "") for s in skills_data]

    fig = go.Figure(go.Bar(
        x=counts,
        y=skills,
        orientation="h",
        marker_color=[_colors.get(c, _colors["Skill"]) for c in categories],
        text=categories,
        textposition="auto",
    ))
    fig.update_layout(
        title="Skill Distribution",
        xaxis_title="Projects Using Skill",
        yaxis=dict(autorange="reversed"),
        height=max(300, len(skills) * 30),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def build_achievement_chart(achievements: list[dict]) -> go.Figure:
    """Horizontal bar chart of numeric achievements."""
    if not achievements:
        return go.Figure()

    labels = []
    values = []
    for a in achievements[:15]:
        val = a.get("value")
        if val is None:
            continue
        text = a.get("achievement", "")[:40]
        unit = a.get("unit", "")
        labels.append(f"{text} ({unit})" if unit else text)
        values.append(float(val))

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker_color=_colors["Achievement"],
    ))
    fig.update_layout(
        title="Key Achievements",
        xaxis_title="Value",
        yaxis=dict(autorange="reversed"),
        height=max(300, len(labels) * 35),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def build_jd_fit_radar(jd_fit_data: list[dict]) -> go.Figure:
    """Radar chart showing match strength across all JD requirements."""
    if not jd_fit_data:
        return go.Figure()

    names = [d.get("name", d.get("requirement_id", "")) for d in jd_fit_data]
    weights = [d.get("total_weight", 0) for d in jd_fit_data]

    # Close the radar polygon
    names_closed = names + [names[0]]
    weights_closed = weights + [weights[0]]

    fig = go.Figure(go.Scatterpolar(
        r=weights_closed,
        theta=names_closed,
        fill="toself",
        marker_color=_colors["JDRequirement"],
        line_color=_colors["JDRequirement"],
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title="JD Requirements Fit",
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    return fig
