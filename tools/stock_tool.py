from ddgs import DDGS
from core.tool_registry import tool


@tool
def get_stock_info(company: str) -> str:
    """Get latest stock info for a company."""
    try:
        with DDGS() as ddgs:
            results = ddgs.text(f"{company} stock price 2026", max_results=2)
            if not results:
                return f"No stock info for {company}"
            return "\n".join(
                f"• {r['title']}: {r['body'][:200]}" for r in results
            )
    except Exception as e:
        return f"❌ Error: {e}"
