from ddgs import DDGS
from core.tool_registry import tool


@tool
def search_news(topic: str) -> str:
    """Search latest news about any topic."""
    try:
        with DDGS() as ddgs:
            results = ddgs.text(f"{topic} news 2026", max_results=3)
            if not results:
                return f"No news found for {topic}"
            return "\n\n".join(
                f"• {r['title']}: {r['body'][:200]}" for r in results
            )
    except Exception as e:
        return f"❌ Error: {e}"
