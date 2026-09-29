import re
import requests
from core.tool_registry import tool


@tool
def convert_currency(query: str) -> str:
    """
    Convert an amount from one currency to another.
    The query should describe the conversion, e.g. '100 USD to INR'.
    Uses the free Frankfurter exchange rate API (no API key required).
    """
    try:
        match = re.search(
            r"([\d.,]+)\s*([A-Za-z]{3})\s*(?:to|->|in)\s*([A-Za-z]{3})",
            query,
            re.IGNORECASE,
        )
        if not match:
            return (
                "❌ Could not understand the conversion request. "
                "Please use a format like '100 USD to INR'."
            )

        amount = float(match.group(1).replace(",", ""))
        from_cur = match.group(2).upper()
        to_cur = match.group(3).upper()

        url = "https://api.frankfurter.app/latest"
        params = {"amount": amount, "from": from_cur, "to": to_cur}
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()

        if resp.status_code != 200 or to_cur not in data.get("rates", {}):
            return f"❌ Could not convert {from_cur} to {to_cur}. Please check the currency codes."

        converted = data["rates"][to_cur]
        rate = converted / amount
        return (
            f"{amount:,.2f} {from_cur} = {converted:,.2f} {to_cur} "
            f"(rate: 1 {from_cur} = {rate:.4f} {to_cur})"
        )
    except Exception as e:
        return f"❌ Error converting currency: {e}"
