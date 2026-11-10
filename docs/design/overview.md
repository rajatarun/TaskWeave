# Design overview

TaskWeave turns a JSON **agent config** into a runnable workflow at request time.

## Components

```
HTTP (main.py)
    → normalize_config (agents/agent_initializer.py)
    → create_agent_from_config
        → langgraph: StateGraph over tools in dependency order
        → langchain: create_agent with tool list (fallback to sequential runner on import errors)
    → tool_factory.build_tool (core/tool_factory.py)
        → llm_prompt | api_call | analysis
```

## Config shape

Top-level keys:

- `agent`: `framework` (`langgraph` | `langchain`), optional `model`, `system_prompt`
- `tools`: array of tool definitions with `name`, `type`, `description`, optional `input` (dependency names)

Execution order is a **topological sort** on `input` edges (`_compute_execution_order`).

## Shared memory

`build_tool` writes each tool's output to a module-level `shared_memory` dict keyed by tool name. Downstream tools read upstream outputs via `input` and `params_from_input`.

## Auto config generation

`POST /invoke/auto` calls `generate_config_from_question`, which prompts an LLM with the full `config/tool_schema.json` registry. On parse/validation failure, a **fallback** config is returned (`metadata.fallback_reason`).

## Extension point

New behavior is added by:

1. Defining tools in JSON (registry + request config)
2. Implementing types in `core/tool_factory.py` (see [EXTENDING.md](../EXTENDING.md))
