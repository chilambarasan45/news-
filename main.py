"""
══════════════════════════════════════════════
MAIN — CLI entry point
══════════════════════════════════════════════
Run with: python main.py
"""

import asyncio
from supervisor import handle_user_message


async def main():
    print("\n🤖 Smart News Assistant  —  MAF Edition")
    print("=" * 55)
    print("Agents  : NewsAgent | WeatherAgent | StockAgent | CurrencyAgent | TranslateAgent")
    print("          | TimeAgent | FetchAgent | WikipediaAgent")
    print("          (Time, Fetch, Wikipedia agents are MCP-powered)")
    print("Pattern : Supervisor → Intent Classify → Specialist Agent")
    print("Type 'quit' to exit")
    print("=" * 55)

    while True:
        user_input = input("\n👤 You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("👋 Goodbye!")
            break

        response = await handle_user_message(user_input)
        print(f"\n🤖 Bot: {response}")


if __name__ == "__main__":
    asyncio.run(main())
