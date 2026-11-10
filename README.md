# TaskWeave

> **Archived (September 2026).** TaskWeave is a reference JSON-driven agent framework in this portfolio. Active development continues in [TeamWeave](https://github.com/rajatarun/TeamWeave) (AWS Step Functions, Bedrock, validation, RAG, observability). This repo remains useful as a minimal, local, API-first pattern.

**TaskWeave lets you define multi-step LLM and API workflows as JSON and run them over a small HTTP API—no cloud account required for local development.**

## Who this is for

- Developers learning **LangGraph / LangChain** tool chaining without boilerplate
- Teams prototyping **config-as-data** agent graphs before moving to hosted orchestration
- Contributors exploring **registry-based auto-config** from `config/tool_schema.json`

<!-- Demo GIF: add a short screen recording of `examples/invoke_local.py` output here -->

## 5-minute quickstart

**Requirements:** Python 3.10+, network optional (mock LLM without `OPENAI_API_KEY`).

```bash
git clone https://github.com/rajatarun/TaskWeave.git
cd TaskWeave
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 examples/invoke_local.py
```

Start the HTTP API (second terminal):

```bash
python3 main.py
```

Verify health:

```bash
curl -sS http://127.0.0.1:8000/health
```

Optional: real OpenAI responses:

```bash
export OPENAI_API_KEY=your-key-here
python3 examples/invoke_local.py --input "Summarize our Q1 pipeline risks"
```

## Three copy-paste examples

### 1. Local invoke (no server)

```bash
python3 examples/invoke_local.py --config examples/custom_tool_config.json --input "Draft a launch checklist"
```

### 2. HTTP invoke with explicit config

```bash
curl -sS -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d @examples/post_invoke_body.json
```

### 3. Auto-generated config from a question

```bash
curl -sS -X POST http://127.0.0.1:8000/invoke/auto \
  -H "Content-Type: application/json" \
  -d '{"input": "Compare Q1 and Q2 sales trends"}'
```

Full HTTP script: `bash examples/curl_invoke.sh` (server must be running).

## API overview

| Method | Path | Purpose |
| ------ | ---- | ------- |
| `GET` | `/health` | Liveness |
| `POST` | `/invoke` | Run agent from request JSON (`config` + `input`) |
| `POST` | `/invoke/auto` | Build config from registry + question, then run |

Response fields include `result`, `shared_memory` (tool outputs), and for `/invoke/auto` also `config`.

### Tool types

| `type` | Behavior |
| ------ | -------- |
| `llm_prompt` | `prompt_template.format(input=...)` → `call_llm` |
| `api_call` | HTTP request; fallback JSON if request fails |
| `analysis` | LLM over collected `input` dependencies |

Frameworks: `agent.framework` = `langgraph` (default DAG) or `langchain` (agent with tools).

## Project layout

| Path | Role |
| ---- | ---- |
| `main.py` | HTTP server |
| `agents/agent_initializer.py` | Graph / agent construction |
| `agents/tool_config_generator.py` | `/invoke/auto` config generation |
| `core/tool_factory.py` | Tool type implementations |
| `config/tool_schema.json` | Tool registry (tags for LLM selection) |
| `examples/` | Runnable scripts |
| `docs/` | Integrations, security, extending, launch draft |

## Local-first usage

- Runs on your machine; **no AWS or cloud setup** is required.
- Without `OPENAI_API_KEY`, LLM steps return **mock** text (see `core/llm.py`).
- `api_call` tools use endpoints you configure; the default registry uses `postman-echo.com`.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md). Design notes: [docs/design/overview.md](docs/design/overview.md).

## License

Apache-2.0 — see [LICENSE](LICENSE).

## Security

Report issues privately: [SECURITY.md](SECURITY.md). Threat model sketch: [docs/security-notes.md](docs/security-notes.md).
