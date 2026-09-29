"""
══════════════════════════════════════════════
AGENT REGISTRY
──────────────────────────────────────────────
This is where prompts (from /prompts) + tools (from /tools)
get wired together into actual Agent objects.

App-specific code — this file KNOWS about weather, news, stocks etc.
The core/ framework code does not.
══════════════════════════════════════════════
"""

from openai import AsyncOpenAI

from config import GROQ_API_KEY, GROQ_BASE_URL, MODEL
from core.agent import as_agent
from core.middleware import LoggingMiddleware
from core.prompt_loader import load_prompt

from tools.news_tool import search_news
from tools.weather_tool import get_weather
from tools.stock_tool import get_stock_info
from tools.currency_tool import convert_currency
from tools.translate_tool import translate_text
from tools.mcp_tools import get_current_time, fetch_webpage, search_wikipedia

client = AsyncOpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

news_agent = as_agent(
    client, MODEL,
    name="NewsAgent",
    instructions=load_prompt("news_agent"),
    tools=[search_news],
    middleware=[LoggingMiddleware()],
)

weather_agent = as_agent(
    client, MODEL,
    name="WeatherAgent",
    instructions=load_prompt("weather_agent"),
    tools=[get_weather],
    middleware=[LoggingMiddleware()],
)

stock_agent = as_agent(
    client, MODEL,
    name="StockAgent",
    instructions=load_prompt("stock_agent"),
    tools=[get_stock_info],
    middleware=[LoggingMiddleware()],
)

time_agent = as_agent(
    client, MODEL,
    name="TimeAgent",
    instructions=load_prompt("time_agent"),
    tools=[get_current_time],
    middleware=[LoggingMiddleware()],
)

fetch_agent = as_agent(
    client, MODEL,
    name="FetchAgent",
    instructions=load_prompt("fetch_agent"),
    tools=[fetch_webpage],
    middleware=[LoggingMiddleware()],
)

wiki_agent = as_agent(
    client, MODEL,
    name="WikipediaAgent",
    instructions=load_prompt("wikipedia_agent"),
    tools=[search_wikipedia],
    middleware=[LoggingMiddleware()],
)

currency_agent = as_agent(
    client, MODEL,
    name="CurrencyAgent",
    instructions=load_prompt("currency_agent"),
    tools=[convert_currency],
    middleware=[LoggingMiddleware()],
)

translate_agent = as_agent(
    client, MODEL,
    name="TranslateAgent",
    instructions=load_prompt("translate_agent"),
    tools=[translate_text],
    middleware=[LoggingMiddleware()],
)

AGENT_MAP = {
    "news": news_agent,
    "stock": stock_agent,
    "weather": weather_agent,
    "time": time_agent,
    "fetch": fetch_agent,
    "wikipedia": wiki_agent,
    "currency": currency_agent,
    "translate": translate_agent,
}
