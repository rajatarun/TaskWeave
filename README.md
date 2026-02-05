🧠 TaskWeave

TaskWeave is a dynamic, JSON-driven agent framework built with LangChain and LangGraph. It creates an execution pipeline from configuration so questions can be parsed and processed by dynamically created agents.

## What this app does

1. Loads `config/tool_config.json`.
2. Reads `agent.framework` to decide runtime:
   - `langchain`: ReAct-style tool-using agent.
   - `langgraph`: Deterministic chained workflow built from tool dependencies.
3. Builds tools from JSON (`llm_prompt`, `api_call`, `analysis`).
4. Executes tasks with dependency-aware chaining and shared memory.

## JSON-driven agent behavior

- Agent type is controlled by JSON (`agent.framework` + `agent.agent_type`).
- Questions are passed as `{"input": "..."}`.
- Input is normalized and parsed by the dynamic agent runtime.
- Tool outputs are persisted and can be consumed by downstream tasks.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_openai_key  # optional; mock response is used if missing
python main.py
```

## Config example

See `config/tool_config.json` for a complete example including:
- dynamic framework selection,
- dependency chaining (`input` field),
- per-tool behavior definitions.

## Notes

- If no OpenAI key is provided, TaskWeave uses a mock LLM response for local testing.
- `api_call` tools should target reachable APIs.
