# Good first issues (draft for maintainers)

Concrete starter tasks derived from the current codebase. Owners can copy these into GitHub issues.

---

### 1. Add `requests` to documented dependencies

**Files:** `requirements.txt`, `README.md`

**Problem:** `core/tool_factory.py` imports `requests` but `requirements.txt` does not list it.

**Acceptance criteria:**

- `pip install -r requirements.txt` installs everything needed for `api_call` tools.
- CI (if present) passes.

---

### 2. Bind-address documentation and example

**Files:** `main.py`, `README.md`, `examples/`

**Problem:** Default `0.0.0.0` is convenient in containers but surprising on laptops.

**Acceptance criteria:**

- README documents `host`/`port` options.
- Example showing `127.0.0.1` binding (env var or small wrapper—implementation choice).

---

### 3. JSON Schema for agent configs

**Files:** `config/`, `agents/agent_initializer.py`, `tests/`

**Problem:** Invalid configs fail at runtime with assorted errors.

**Acceptance criteria:**

- `config/agent_config.schema.json` validates minimal happy-path config.
- Unit test rejects config missing `tools`.

---

### 4. `GET /health` extended metadata

**Files:** `main.py`, `tests/`

**Problem:** Health check returns only `{"status": "ok"}`.

**Acceptance criteria:**

- Response includes `schema_version` from `tool_schema.json` (no secrets).
- Test covers new fields.

---

### 5. Remove or justify unused `boto3` dependency

**Files:** `requirements.txt`, `README.md`

**Problem:** `boto3` is installed but unused in source.

**Acceptance criteria:**

- Either remove from `requirements.txt` or document planned Bedrock integration as **planned** in README.

---

### 6. LangChain path integration test

**Files:** `tests/test_agent_initializer.py`

**Problem:** Only `langgraph` path has an end-to-end invoke test.

**Acceptance criteria:**

- Test with `framework: langchain` runs without crash (mock LLM acceptable).

---

### 7. Request body size guard

**Files:** `main.py`

**Problem:** Large `Content-Length` bodies are read fully into memory.

**Acceptance criteria:**

- Configurable max body size; returns `413` when exceeded.
- Unit test with mocked handler.

---

### 8. Example: custom tool in registry

**Files:** `examples/custom_tool_config.json`, `docs/EXTENDING.md`

**Problem:** No sample showing a minimal two-tool DAG.

**Acceptance criteria:**

- `python examples/invoke_local.py --config examples/custom_tool_config.json` succeeds offline.

---

### 9. OpenAPI sketch for HTTP API

**Files:** `docs/openapi.yaml`

**Problem:** API is documented only in README prose.

**Acceptance criteria:**

- OpenAPI 3 document for `/health`, `/invoke`, `/invoke/auto` matching `main.py` behavior.

---

### 10. Topological sort performance micro-note

**Files:** `agents/agent_initializer.py`, `tests/`

**Problem:** Queue uses `list.pop(0)` (O(n²) for large graphs).

**Acceptance criteria:**

- Use `collections.deque` for order computation; existing tests still pass.
