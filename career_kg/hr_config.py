"""
Career KG — HR Chatbot Configuration
Quick questions, candidate profile, theme, and JD labels for HR recruiters.
"""

QUICK_QUESTIONS = {
    "Experience": [
        {"label": "B2B Sales", "query": "B2B sales experience with specific examples and outcomes"},
        {"label": "Leadership", "query": "Team leadership and management experience with concrete examples"},
        {"label": "Career Timeline", "query": "Show the complete career timeline with companies and roles"},
    ],
    "Skills": [
        {"label": "Tech Stack", "query": "What is the candidate's full technical skill set?"},
        {"label": "AI Projects", "query": "Describe all AI-related projects in detail"},
        {"label": "Top Projects", "query": "What are the top 3 most impactful projects?"},
    ],
    "JD Fit": [
        {"label": "JD Match", "query": "How well does the candidate match the JD requirements overall?"},
        {"label": "Why Anthropic", "query": "Why is the candidate applying to Anthropic?"},
        {"label": "Strengths", "query": "What are the candidate's key strengths and differentiators?"},
    ],
    "Metrics": [
        {"label": "Key Metrics", "query": "Show all quantifiable achievements and performance metrics"},
        {"label": "Revenue Impact", "query": "What are the revenue-related achievements?"},
        {"label": "Cost Savings", "query": "Are there any cost reduction or efficiency improvement results?"},
    ],
}

CANDIDATE_PROFILE = {
    "name": "Hansol Cho",
    "name_kr": "조한솔",
    "title": "AI Transformation Lead",
    "company": "F&F Corporation",
    "years": "8+",
    "projects": "11",
    "skills": "42+",
    "achievements": "28",
    "education": "Kyung Hee University (Philosophy)",
    "target_role": "Account Executive (Startups), Anthropic Korea",
}

JD_REQUIREMENTS_DISPLAY = {
    "b2b-sales": "B2B Startup Sales",
    "tech-sales": "Technical Stakeholder Sales",
    "strategic-advisor": "Strategic Business Advisor",
    "ai-passion": "AI Passion & Safe AI",
    "analytical-execution": "Analytical + Creative Execution",
    "korean-market": "Korean Market Expansion",
}

THEME = {
    "primary": "#4A90D9",
    "secondary": "#6C63FF",
    "accent": "#FF6B6B",
    "bg_dark": "#1E1E2E",
    "bg_light": "#F8F9FA",
    "text": "#2D3436",
    "node_colors": {
        "Project": "#4A90D9",
        "Skill": "#27AE60",
        "Company": "#F39C12",
        "JDRequirement": "#E74C3C",
        "Achievement": "#9B59B6",
        "Person": "#1ABC9C",
        "Position": "#3498DB",
    },
}
