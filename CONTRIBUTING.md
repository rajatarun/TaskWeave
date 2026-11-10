# Contributing to TaskWeave

Thank you for your interest. TaskWeave is **archived** as a reference implementation; maintainers accept small fixes and documentation improvements on a best-effort basis.

## Development setup

```bash
git clone https://github.com/rajatarun/TaskWeave.git
cd TaskWeave
python3 -m pip install -r requirements.txt
```

Use a virtual environment if your platform supports `python3 -m venv`.

## Running tests

```bash
python3 -m unittest discover -s tests -v
```

Optional offline eval (synthetic timing, mock LLM):

```bash
python3 examples/synthetic_eval.py
```

## Style

- Python 3.10+ compatible syntax
- Keep JSON configs valid and aligned with `config/tool_schema.json` conventions
- Prefer focused changes; match existing module layout (`agents/`, `core/`)

## Pull request process

1. Fork and create a branch from `main`.
2. Keep claims in docs aligned with code behavior.
3. Ensure unit tests pass.
4. Open a PR with a clear description and link any related discussion.
5. Do not include secrets, personal data, or unrelated refactors.

## Extension points

See [docs/EXTENDING.md](docs/EXTENDING.md) for adding tool types and registry entries.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Report unacceptable behavior to repository maintainers via GitHub.
