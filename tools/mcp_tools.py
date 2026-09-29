"""
══════════════════════════════════════════════
MCP-POWERED TOOLS
──────────────────────────────────────────────
Unlike the other tool files, these don't contain the actual logic.
They connect to separate MCP SERVER programs (run as subprocesses)
and ask those servers to do the work.
══════════════════════════════════════════════
"""

import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from core.tool_registry import tool


async def call_mcp_tool(module_name: str, tool_name: str, arguments: dict) -> str:
    """
    Generic helper: starts ANY MCP server (given its Python module name)
    as a subprocess, connects to it, calls the requested tool, and
    returns the result as plain text.
    """
    server_params = StdioServerParameters(
        command="python3",
        args=["-m", module_name],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            return result.content[0].text


@tool
def get_current_time(timezone: str) -> str:
    """
    Get the current date and time in a given IANA timezone
    (e.g. 'Asia/Kolkata', 'America/New_York', 'Europe/London').
    Powered by the 'mcp-server-time' MCP server.
    """
    try:
        return asyncio.run(
            call_mcp_tool("mcp_server_time", "get_current_time", {"timezone": timezone})
        )
    except Exception as e:
        return f"❌ Error calling time MCP server: {e}"


@tool
def fetch_webpage(url: str) -> str:
    """
    Fetch the content of a webpage/article URL and return it as readable text.
    Powered by the 'mcp-server-fetch' MCP server.
    """
    try:
        return asyncio.run(
            call_mcp_tool("mcp_server_fetch", "fetch", {"url": url})
        )
    except Exception as e:
        return f"❌ Error calling fetch MCP server: {e}"


@tool
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for a topic and return a short factual summary.
    Powered by the 'wikipedia-mcp' MCP server.
    """
    try:
        search_result = asyncio.run(
            call_mcp_tool("wikipedia_mcp", "search_wikipedia", {"query": query, "limit": 1})
        )
        data = json.loads(search_result)
        results = data.get("results", [])
        if not results:
            return f"No Wikipedia article found for '{query}'."

        title = results[0]["title"]

        summary_result = asyncio.run(
            call_mcp_tool("wikipedia_mcp", "get_summary", {"title": title})
        )
        summary_data = json.loads(summary_result)
        summary = summary_data.get("summary")
        if not summary:
            return f"Found article '{title}' but could not retrieve a summary."
        return f"{title}: {summary}"
    except Exception as e:
        return f"❌ Error calling Wikipedia MCP server: {e}"
