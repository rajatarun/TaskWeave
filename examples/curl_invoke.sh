#!/usr/bin/env bash
# Requires: curl, TaskWeave running on localhost:8000 (python3 main.py)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== GET /health =="
curl -sS "http://127.0.0.1:8000/health" | python3 -m json.tool

echo "== POST /invoke (minimal config) =="
curl -sS -X POST "http://127.0.0.1:8000/invoke" \
  -H "Content-Type: application/json" \
  -d @"${ROOT}/examples/post_invoke_body.json" | python3 -m json.tool

echo "== POST /invoke/auto =="
curl -sS -X POST "http://127.0.0.1:8000/invoke/auto" \
  -H "Content-Type: application/json" \
  -d '{"input": "Compare Q1 and Q2 sales trends"}' | python3 -m json.tool
