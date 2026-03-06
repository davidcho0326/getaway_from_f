"""
Career KG — Chat Interface
REPL loop for querying the career knowledge graph.
"""
import json
from orchestrator import RAGOrchestrator
from graph_rag import CareerGraphRAG

WELCOME = """
╔══════════════════════════════════════════════════════╗
║  Career Knowledge Graph — Interactive Chat           ║
║  Hansol Cho · Anthropic Startups AE Candidate        ║
╠══════════════════════════════════════════════════════╣
║  Ask questions about career, projects, skills, etc.  ║
║  Commands: !help  !graph  !jd  !quit                 ║
╚══════════════════════════════════════════════════════╝
"""

HELP_TEXT = """
Commands:
  !help   — Show this help message
  !graph  — Show Knowledge Graph statistics
  !jd     — List JD requirement IDs for match queries
  !quit   — Exit the chat

Example questions:
  • MCP 서버를 만든 프로젝트는?
  • B2B 영업 역량을 증명하는 프로젝트는?
  • 가장 많이 사용한 기술 TOP 5
  • 숫자로 된 성과 보여줘
  • 왜 Anthropic에 지원하나?
"""

JD_IDS = """
JD Requirement IDs (for match queries):
  b2b-sales           — B2B startup sales, consultative approach
  tech-sales          — Selling to technical stakeholders
  strategic-advisor   — Strategic business advisor to founders
  ai-passion          — Passion for AI, especially safe AI
  analytical-execution — Analytical + creative execution
  korean-market       — Korean market expansion
"""


def main():
    print(WELCOME)
    orch = RAGOrchestrator()

    try:
        while True:
            try:
                query = input("\n❓ You: ").strip()
            except EOFError:
                break

            if not query:
                continue

            if query == "!quit":
                print("👋 Goodbye!")
                break
            elif query == "!help":
                print(HELP_TEXT)
                continue
            elif query == "!graph":
                stats = orch.graph.get_stats()
                print("\n📊 Knowledge Graph Stats")
                print("─" * 35)
                for label, count in stats["nodes"].items():
                    print(f"  {label}: {count}")
                print(f"  Relationships: {stats['total_relationships']}")
                continue
            elif query == "!jd":
                print(JD_IDS)
                continue

            print("\n🤔 Thinking...\n")
            answer = orch.process_query(query)
            print(f"💡 {answer}")

    except KeyboardInterrupt:
        print("\n👋 Interrupted. Goodbye!")
    finally:
        orch.close()


if __name__ == "__main__":
    main()
