# Smart News Assistant — Restructured

Same logic as the original single-file `chatbot.py`, split into a
production-style folder layout.

## Folder structure

```
smart_news_assistant/
├── config.py              # loads API keys + model name from .env
├── main.py                 # CLI entry point
├── ui.py                    # Streamlit web UI (same logic, different front door)
├── supervisor.py            # intent classification + routing + reply combining
├── core/                    # reusable framework code (knows nothing about weather/news/etc.)
│   ├── tool_registry.py     # @tool decorator + TOOL_REGISTRY
│   ├── agent.py              # Agent class, AgentResponse, as_agent factory
│   ├── middleware.py          # AgentMiddleware base + LoggingMiddleware
│   └── prompt_loader.py        # loads .txt prompt files
├── tools/                    # app-specific tool functions
│   ├── news_tool.py
│   ├── weather_tool.py
│   ├── stock_tool.py
│   ├── currency_tool.py
│   ├── translate_tool.py
│   └── mcp_tools.py           # time / fetch / wikipedia (MCP-powered)
├── agents/
│   └── registry.py             # wires prompts + tools into Agent objects, builds AGENT_MAP
├── prompts/                     # every system prompt as its own .txt file
│   ├── news_agent.txt
│   ├── weather_agent.txt
│   ├── stock_agent.txt
│   ├── time_agent.txt
│   ├── fetch_agent.txt
│   ├── wikipedia_agent.txt
│   ├── currency_agent.txt
│   ├── translate_agent.txt
│   └── intent_classifier.txt
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# then edit .env and paste your real GROQ_API_KEY and WEATHER_API_KEY
```

## Run (terminal)

```bash
python main.py
```

## Run (web UI)

```bash
streamlit run ui.py
```

## Why this structure

- **Prompts live in `/prompts` as plain text** — editable by anyone
  without touching Python, easy to diff/review, easy to version separately.
- **`core/` vs `tools/` vs `agents/` separation** — `core/` is reusable
  framework code you could drop into a totally different project.
  `tools/` and `agents/` are the app-specific pieces.
- **Secrets in `.env`, never hardcoded** — `config.py` loads them and
  fails loudly if they're missing, instead of silently using a bad key.
- **`main.py` and `ui.py` share the same `supervisor.py`** — the "brain"
  doesn't care which interface is calling it.
