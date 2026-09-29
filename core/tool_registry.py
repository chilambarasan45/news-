"""
══════════════════════════════════════════════
TOOL REGISTRY + @tool DECORATOR
──────────────────────────────────────────────
Framework-level code — knows nothing about weather, news, or
stocks specifically. Any project can reuse this file unchanged.
══════════════════════════════════════════════
"""

import inspect

TOOL_REGISTRY: dict[str, dict] = {}


def tool(fn):
    """
    Decorator that:
    - Reads the function's name, docstring, and type hints
    - Auto-builds an OpenAI-style tool schema
    - Registers the function in TOOL_REGISTRY
    - Attaches fn._schema to the function itself
    """
    sig = inspect.signature(fn)
    params = {}
    for name, param in sig.parameters.items():
        annotation = param.annotation
        if annotation == str or annotation == inspect.Parameter.empty:
            params[name] = {"type": "string"}
        elif annotation == int:
            params[name] = {"type": "integer"}
        elif annotation == float:
            params[name] = {"type": "number"}
        else:
            params[name] = {"type": "string"}

    schema = {
        "type": "function",
        "function": {
            "name": fn.__name__,
            "description": fn.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": params,
                "required": list(params.keys()),
            },
        },
    }

    TOOL_REGISTRY[fn.__name__] = {"fn": fn, "schema": schema}
    fn._is_tool = True
    fn._schema = schema
    return fn
