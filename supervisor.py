"""
══════════════════════════════════════════════
SUPERVISOR / ORCHESTRATOR
──────────────────────────────────────────────
Classifies intent(s) in the user's message, routes each part to the
right specialist agent, and combines their answers into one reply.
══════════════════════════════════════════════
"""

import json

from openai import AsyncOpenAI

from config import GROQ_API_KEY, GROQ_BASE_URL, MODEL
from core.agent import AgentResponse
from core.prompt_loader import load_prompt
from agents.registry import AGENT_MAP

client = AsyncOpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

CLASSIFIER_PROMPT_TEMPLATE = load_prompt("intent_classifier")


async def classify_intent(user_message: str) -> list[dict]:
    """
    Classifies user message into ONE OR MORE intents.
    Returns a list, e.g.:
    [{"intent": "stock", "topic": "Jio", "reason": "..."}]
    """
    prompt = CLASSIFIER_PROMPT_TEMPLATE.format(user_message=user_message)

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(text)

    if isinstance(parsed, dict):
        parsed = [parsed]
    return parsed


def unknown_reply(topic: str) -> str:
    """Single source of truth for the 'out of scope' reply."""
    return (
        f"Sorry, I can't help with '{topic}'. 😊\n\n"
        "I'm a Smart News Assistant. Here's what I can do:\n\n"
        "  📰 News     — 'Give me cricket news'\n"
        "  📈 Stocks   — 'What is Tesla stock price?'\n"
        "  🌤️  Weather  — 'Weather in Chennai'\n"
        "  🕐 Time     — 'What time is it in Tokyo?'\n"
        "  🔗 Webpage  — 'Summarize this article: <link>'\n"
        "  📖 Knowledge — 'Who is Sundar Pichai?'\n"
        "  💱 Currency — 'Convert 100 USD to INR'\n"
        "  🌐 Translate — 'Translate hello to French'\n\n"
        "Please try one of those!"
    )


REFUSAL_PHRASES = [
    "i can't help",
    "i cannot help",
    "i'm not able to help",
    "i am not able to help",
    "sorry, i can't",
    "sorry, i cannot",
    "i don't have information",
    "i do not have information",
    "no information found",
    "no news found",
    "no results found",
]


def looks_like_refusal(text: str) -> bool:
    """Checks if the agent's own reply sounds like a refusal/empty result."""
    lowered = text.lower()
    return any(phrase in lowered for phrase in REFUSAL_PHRASES)


async def handle_user_message(user_message: str) -> str:
    """
    1. Classify intent(s) — may return more than one
    2. For each supported intent -> run that agent
    3. For each unknown part -> note it for the polite decline message
    4. Combine all agent answers + ONE polite decline section at the end
    """
    print(f"\n{'='*55}")
    print(f"👤 User: {user_message}")
    print("=" * 55)

    print("🧠 Supervisor: Classifying intent(s)...")
    classifications = await classify_intent(user_message)

    for c in classifications:
        print(f"   Intent : {c['intent']}  |  Topic: {c['topic']}  |  Reason: {c['reason']}")

    answer_sections = []
    unsupported_topics = []

    for c in classifications:
        intent = c["intent"]
        topic = c["topic"]

        if intent == "unknown":
            unsupported_topics.append(topic)
            continue

        print(f"\n🤖 Supervisor → routing '{topic}' to {AGENT_MAP[intent].name}...")
        response: AgentResponse = await AGENT_MAP[intent].run(
            f"{user_message}\n\n(Focus only on this part: {topic})"
        )

        if looks_like_refusal(response.text):
            unsupported_topics.append(topic)
        else:
            answer_sections.append(response.text)

    final_parts = []

    if answer_sections:
        final_parts.append("\n\n".join(answer_sections))

    if unsupported_topics:
        topics_str = "', '".join(unsupported_topics)
        decline = (
            f"Also, I'm a Smart News Assistant and can't help with '{topics_str}'. 😊\n"
            "I can only help with: 📰 News | 📈 Stocks | 🌤️ Weather | 🕐 Time | "
            "🔗 Webpage | 📖 Knowledge | 💱 Currency | 🌐 Translate"
        )
        final_parts.append(decline)

    if not answer_sections and unsupported_topics:
        return unknown_reply(unsupported_topics[0])

    return "\n\n".join(final_parts)
