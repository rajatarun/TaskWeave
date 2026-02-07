🧠 TaskWeave API

TaskWeave is now an API-first, JSON-driven agent framework built with LangChain + LangGraph.

## Intent of the app

The API is designed to:
- create a dynamic agent from request JSON,
- parse the user question,
- execute modular tasks (`llm_prompt`, `api_call`, `analysis`),
- and chain tool outputs across tasks.

## API contract

### `POST /invoke` (HTTP JSON)

Request body:

```json
{
  "config": {
    "agent": {
      "framework": "langgraph",
      "model": "gpt-4o-mini",
      "system_prompt": "You are a task orchestrator."
    },
    "tools": [
      {
        "name": "ProblemTranslator",
        "description": "Translates user query into a business problem",
        "type": "llm_prompt",
        "prompt_template": "Translate this question into a business problem: {input}"
      },
      {
        "name": "DataFetcher",
        "description": "Fetches data from API",
        "type": "api_call",
        "method": "POST",
        "endpoint": "https://postman-echo.com/post",
        "params_from_input": ["ProblemTranslator"],
        "input": ["ProblemTranslator"]
      },
      {
        "name": "Analyzer",
        "description": "Analyzes fetched data",
        "type": "analysis",
        "prompt_template": "Analyze this: {input}",
        "input": ["DataFetcher"]
      }
    ]
  },
  "input": "Compare Q1 and Q2 sales trends"
}
```

Response includes:
- `result`: runtime output
- `shared_memory`: all tool outputs for chained tasks

### `GET /health`
Returns service health.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Notes

- `agent.framework` supports `langgraph` and `langchain`.
- If OpenAI credentials are missing, mock LLM responses are returned.
- If API calls fail (e.g., restricted network), `api_call` tools return fallback payloads.
