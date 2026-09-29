"""
══════════════════════════════════════════════
CONFIG — central place for keys, model name, settings
══════════════════════════════════════════════
Real-world rule: NEVER hardcode API keys in code.
Load them from environment variables (or a .env file).

Setup:
  1. Copy .env.example to .env
  2. Fill in your real keys in .env
  3. Install python-dotenv: pip install python-dotenv
"""

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env file into environment variables, if present

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Create a .env file (see .env.example) "
        "or export GROQ_API_KEY in your shell."
    )

if not WEATHER_API_KEY:
    raise RuntimeError(
        "WEATHER_API_KEY is not set. Create a .env file (see .env.example) "
        "or export WEATHER_API_KEY in your shell."
    )

# Model used by every agent + the intent classifier.
# Change this in ONE place to swap models across the whole app.
MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
