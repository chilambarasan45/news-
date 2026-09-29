"""
Loads prompt text files from the /prompts folder.
Keeps prompts out of Python code entirely.
"""

import os

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")


def load_prompt(name: str) -> str:
    """
    Load a prompt file by name (without .txt extension).
    Example: load_prompt("weather_agent") -> reads prompts/weather_agent.txt
    """
    path = os.path.join(PROMPTS_DIR, f"{name}.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
