# Launch draft (not published)

Use this as a starting point for a blog post, README pin, or community announcement. **Do not** treat TaskWeave as actively developed; it remains a reference implementation superseded by [TeamWeave](https://github.com/rajatarun/TeamWeave) for production AWS workflows.

## Draft post

### Title idea

**TaskWeave: define agent workflows in JSON, run them locally in minutes**

### Problem

Teams experimenting with LangGraph and LangChain often hard-code tool chains in Python. That makes it harder to swap tools, audit configs, or let non-developers sketch workflows.

### Why it matters

A small, API-first runner lets you treat an agent workflow as data: version the JSON, test tool graphs, and iterate without redeploying application code.

### What TaskWeave does

- Accepts a JSON config describing tools (`llm_prompt`, `api_call`, `analysis`) and dependencies.
- Builds a LangGraph DAG (or LangChain agent) per request.
- Exposes `POST /invoke`, auto-config via `POST /invoke/auto`, and `GET /health`.
- Runs fully offline for structure tests; real LLM calls only when `OPENAI_API_KEY` is set.

### Honest limits

- Archived reference repo; no tagged releases or SLA.
- No auth on HTTP endpoints.
- No built-in observability or RAG.
- `boto3` in requirements is unused in current source.

### Synthetic check (local, mock LLM)

From repo root after `pip install -r requirements.txt`:

```bash
python3 examples/synthetic_eval.py
```

Example output (recorded on synthetic run without `OPENAI_API_KEY`; your numbers will vary):

```
synthetic_eval: 20 runs, framework=langgraph, tools=2
total_wall_ms=28.28 p50_ms=1.33
tools_per_run=['ProblemTranslator', 'Analyzer']
label=synthetic_no_openai_key
```

## Communities where this fits

- LangChain / LangGraph Discord and GitHub discussions (JSON workflows, small graphs)
- Local-first / self-hosted AI tooling threads
- MCP adapter builders (tool registry → MCP tools)
- Educators teaching agent DAGs before cloud orchestration

## Channels (draft only)

- Personal blog or dev.to technical post
- Show HN / relevant subreddits (r/LangChain) with clear **archived** disclaimer
- Link from TeamWeave README as historical predecessor
