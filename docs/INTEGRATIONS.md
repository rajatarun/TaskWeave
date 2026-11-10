# Integration opportunities

TaskWeave is a small JSON-driven agent runner (LangGraph / LangChain) exposed over a local HTTP API. Below are ecosystems where adapters would add the most value. **Implemented today** means shipping code in this repo; most rows are research notes for contributors.

| Integration | Fit | Implemented today | Adapter sketch | Effort |
| ----------- | --- | ----------------- | -------------- | ------ |
| **LangGraph / LangChain** | High | Yes | Native: configs select `agent.framework` and tools become `langchain_core.tools.Tool` instances | — |
| **OpenAI Chat Completions** | High | Yes | `core/llm.py` calls `openai.chat.completions`; mock path when no API key | Small to extend models |
| **MCP (Model Context Protocol)** | High | No | Expose each JSON tool type as MCP tools; map `POST /invoke` to an MCP server resource or stdio bridge | Medium |
| **Anthropic Messages API** | Medium | No | Parallel `call_llm` backend selected by `agent.provider` | Small–medium |
| **AWS Bedrock / AgentCore** | Medium | No | Replace `call_llm` with Bedrock Converse; optional Step Functions wrapper (see successor [TeamWeave](https://github.com/rajatarun/TeamWeave)) | Medium–large |
| **OpenTelemetry** | Medium | No | Spans around `build_tool.run`, HTTP handlers, and LangGraph nodes | Small–medium |
| **FastAPI / Starlette** | Medium | No | Swap `http.server` for ASGI, async handlers, OpenAPI docs | Medium |
| **Pydantic validation** | Medium | Partial | Validate configs against JSON Schema derived from `tool_schema.json` | Small |
| **Docker / Compose** | Low–Med | No | Dockerfile + compose with optional `OPENAI_API_KEY` | Small |
| **LangSmith / Langfuse** | Low–Med | No | Trace callbacks on LangChain path only | Small |

## Recommended first adapters

1. **MCP server** — High fit: TaskWeave already treats tools as named, describable units with tags (`config/tool_schema.json`). An MCP adapter would let Claude Desktop, Cursor, and other MCP clients invoke the same tool graph without custom HTTP glue.

2. **OpenTelemetry** — Medium fit, high ops value: minimal code hooks in `main.py` and `tool_factory.py` would make chained `api_call` + LLM steps visible in standard backends.

3. **Config JSON Schema** — Medium fit, low effort: generate schema from the registry and reject bad `POST /invoke` payloads before graph construction.

## Out of scope for this repo

Hosted multi-tenant SaaS, built-in identity, and managed RAG are intentionally absent; [TeamWeave](https://github.com/rajatarun/TeamWeave) is the maintained path for AWS-scale orchestration.
