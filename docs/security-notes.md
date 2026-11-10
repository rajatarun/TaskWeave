# Security notes (threat model sketch)

TaskWeave is a **local-first** HTTP service: you run `python main.py` on your machine or container. It does **not** require AWS or other cloud accounts. Optional OpenAI calls only occur when `OPENAI_API_KEY` (or `OPENAI_KEY`) is set.

## Assets

- User questions and tool outputs held in process memory (`shared_memory` in `agents/agent_initializer.py`)
- Arbitrary HTTP endpoints configured in `api_call` tools
- LLM prompts built from JSON templates and user input

## Trust boundaries

| Boundary | Risk | Mitigation |
| -------- | ---- | ---------- |
| `POST /invoke` body | Untrusted JSON defines tools and endpoints | Run behind a reverse proxy with auth in production; restrict who can reach port 8000 |
| `api_call` tools | SSRF-style requests to internal URLs | Review configs; do not expose the API publicly without endpoint allowlists (not built in today) |
| LLM calls | Prompt injection via `input` | Treat LLM output as untrusted; validate before downstream actions |
| Mock mode | No external LLM when key missing | Safe for local dev; responses are deterministic stubs |

## Default exposure

The server binds to `0.0.0.0:8000` by default (`main.run`), which listens on all interfaces. For laptop development, consider `host=127.0.0.1` when wrapping `run()` or placing the process behind local-only networking.

## Secrets

- Store `OPENAI_API_KEY` in environment variables, not in JSON configs committed to git.
- `boto3` is listed in `requirements.txt` but is **not** used by the current codebase; it can be removed locally if you want a slimmer install.

## Not implemented (honest limits)

- Authentication or authorization on HTTP routes
- Rate limiting, request size caps beyond default `http.server` behavior
- Tool endpoint allowlists or egress filtering

See [SECURITY.md](../SECURITY.md) for coordinated disclosure.
