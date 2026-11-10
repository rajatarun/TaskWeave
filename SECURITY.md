# Security Policy

## Supported versions

TaskWeave is archived as a reference implementation. Security fixes are accepted on a best-effort basis via pull request; there is no formal release cadence.

| Version | Supported |
| ------- | --------- |
| `main` (no tagged releases) | Best effort |

## Reporting a vulnerability

**Please do not open a public GitHub issue for security problems.**

1. Use [GitHub Security Advisories](https://github.com/rajatarun/TaskWeave/security/advisories/new) on this repository (preferred), or contact the repository owner through GitHub.
2. Include a description, steps to reproduce, and impact assessment.
3. Allow reasonable time for a fix before public disclosure.

We will acknowledge reports within a reasonable timeframe and coordinate on disclosure.

## Scope

In scope:

- The TaskWeave HTTP API (`main.py`) and agent runtime
- Dependency-induced risks in documented install paths (`requirements.txt`)
- Misuse of `api_call` tools pointing at unintended endpoints (configuration review)

Out of scope:

- Vulnerabilities in third-party APIs you configure in tool definitions (for example `postman-echo.com`)
- Issues that require a valid `OPENAI_API_KEY` to exploit on a deployment you control
