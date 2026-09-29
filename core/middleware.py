"""
══════════════════════════════════════════════
MIDDLEWARE — wraps behavior around agent execution
══════════════════════════════════════════════
"""

import time


class AgentMiddleware:
    """
    Base class for all middleware.
    Subclasses override process() to add behavior
    before and after the agent runs.
    """
    async def process(self, inputs: dict, next_call):
        return await next_call()


class LoggingMiddleware(AgentMiddleware):
    """Logs every agent request and how long it took."""
    async def process(self, inputs: dict, next_call):
        print(f"\n  📨 [{inputs['agent']}] Request: {inputs['message'][:60]}...")
        t0 = time.perf_counter()
        result = await next_call()
        elapsed = time.perf_counter() - t0
        print(f"  ✅ [{inputs['agent']}] Done in {elapsed:.1f}s: {result.text[:80]}...")
        return result
