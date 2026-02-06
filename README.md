🧠 TaskWeave

TaskWeave is a JSON-driven agent framework built with LangChain + LangGraph. A single config file controls which runtime is created and how tools are chained.

## Intent of the app

The app is designed to:
- create agents dynamically from JSON,
- parse user questions through that runtime,
- execute modular tasks (`llm_prompt`, `api_call`, `analysis`),
- and chain outputs across tasks.

## Runtime modes

`config/tool_config.json` drives agent creation via `agent.framework`:

- `langgraph` → deterministic dependency-ordered pipeline using `input` references.
- `langchain` → model-driven tool selection using LangChain's `create_agent` (falls back to deterministic sequential mode if LangChain provider extras are unavailable).

Both runtimes accept user payloads as:

```python
{"input": "your question"}
```

## Tool chaining model

Each tool can declare dependencies via:

```json
"input": ["UpstreamToolName"]
```

At runtime, upstream outputs are loaded from shared memory and passed into downstream tools.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_openai_key  # optional; mock response is used when missing
python main.py
```

## Notes

- If OpenAI credentials are missing, `call_llm` returns a mock response for local testing.
- In restricted environments, API tool calls may fall back to a structured warning payload.
