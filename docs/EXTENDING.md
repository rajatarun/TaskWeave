# Extending TaskWeave

## Plugin model (JSON + one code hook)

TaskWeave does not load dynamic Python plugins at runtime. Extensions follow a fixed pattern:

1. **Registry entry** — Add a tool object to `config/tool_schema.json` (include `tags` for auto-config generation).
2. **Runtime handler** — Add a branch in `core/tool_factory.py` inside `build_tool` for your `type` string.
3. **Optional test** — Extend `tests/` with a minimal config exercising the new type.

### Tool definition fields

| Field | Required | Notes |
| ----- | -------- | ----- |
| `name` | Yes | Unique in config |
| `description` | Yes | Shown to LangChain agent path |
| `type` | Yes | `llm_prompt`, `api_call`, or `analysis` today |
| `prompt_template` | For LLM types | Python `str.format`; use `{input}` |
| `method`, `endpoint` | For `api_call` | Passed to `requests.request` |
| `params_from_input` | Optional | Keys pulled from shared memory |
| `input` | Optional | Upstream tool names (DAG edges) |
| `tags` | Recommended | Used by `generate_config_from_question` |

### Example: custom tool type (planned pattern)

To add `type: "transform"`:

```python
# In core/tool_factory.py, inside run():
elif tool_type == "transform":
    output = {"output": your_logic(inputs)}
```

Keep outputs as `{"output": ...}` so `shared_memory` stays consistent.

## Framework selection

Set `agent.framework`:

- `langgraph` — Deterministic DAG execution in registry order (default).
- `langchain` — Agent chooses tools via LangChain; falls back to sequential execution if imports fail.

## HTTP API

No code changes are required to add tools-only workflows: POST a full config to `/invoke`. For registry-backed generation, update `tool_schema.json` only.

## Dependency graph rules

- `input` must reference existing tool `name` values.
- Cycles are rejected at agent creation time.
- Missing upstream tools raise `ValueError` during `create_agent_from_config`.
