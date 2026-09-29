"""
══════════════════════════════════════════════
AGENT — the reusable Agent class, AgentResponse, and factory
══════════════════════════════════════════════
Framework-level code. No weather/news/stock-specific logic here.
"""

import json
from core.tool_registry import TOOL_REGISTRY


class AgentResponse:
    """Wraps the final text reply from any agent so every agent returns the same type."""
    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f"AgentResponse(text={self.text[:80]!r})"


class Agent:
    def __init__(self, name: str, instructions: str, tools: list,
                 middleware: list, llm_client, model: str):
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.middleware = middleware
        self._client = llm_client
        self._model = model

    async def run(self, user_message: str) -> AgentResponse:
        """Entry point. Chains middleware around _execute()."""
        inputs = {"agent": self.name, "message": user_message}

        async def core():
            return await self._execute(user_message)

        call = core
        for mw in reversed(self.middleware):
            outer_mw = mw
            inner_call = call

            async def chained(mw=outer_mw, nxt=inner_call):
                return await mw.process(inputs, nxt)

            call = chained

        return await call()

    async def _execute(self, user_message: str) -> AgentResponse:
        """The tool-calling loop: decide tool -> run tool -> summarize result."""
        tool_schemas = [t._schema for t in self.tools if hasattr(t, "_schema")]

        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": user_message},
        ]

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=tool_schemas if tool_schemas else None,
                tool_choice="required" if tool_schemas else None,
                temperature=0,
            )
        except Exception as e:
            print(f"  ❌ [{self.name}] LLM tool-call request failed: {e}")
            return AgentResponse(
                "Sorry, I had trouble finding that information just now. "
                "Could you please try rephrasing your request?"
            )

        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for tc in msg.tool_calls:
                fn_name = tc.function.name

                try:
                    fn_args = json.loads(tc.function.arguments)
                except json.JSONDecodeError as e:
                    print(f"  ❌ [{self.name}] Could not parse tool arguments: {e}")
                    return AgentResponse(
                        "Sorry, I had trouble understanding that request. "
                        "Could you please try rephrasing it?"
                    )

                fn = TOOL_REGISTRY[fn_name]["fn"]

                print(f"  🔧 [{self.name}] Calling {fn_name}({fn_args})")
                result = fn(**fn_args)
                print(f"  📦 [{self.name}] Result: {result[:80]}...")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

            try:
                final = await self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    temperature=0,
                )
            except Exception as e:
                print(f"  ❌ [{self.name}] LLM final-answer request failed: {e}")
                return AgentResponse(
                    "Sorry, I found some information but had trouble "
                    "summarizing it. Please try again."
                )
            return AgentResponse(final.choices[0].message.content or "")

        return AgentResponse(msg.content or "Sorry, I couldn't get an answer.")


def as_agent(llm_client, model: str, name: str, instructions: str,
             tools: list = None, middleware: list = None) -> Agent:
    """Factory to create an Agent cleanly."""
    return Agent(
        name=name,
        instructions=instructions,
        tools=tools or [],
        middleware=middleware or [],
        llm_client=llm_client,
        model=model,
    )
