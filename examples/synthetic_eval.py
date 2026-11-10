#!/usr/bin/env python3
"""
Offline synthetic evaluation: runs the LangGraph path with mock LLM (no API key).
Results are timing-only and labeled synthetic — not production benchmarks.
"""

import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.agent_initializer import create_agent_from_config  # noqa: E402

CONFIG = json.loads((ROOT / "examples" / "custom_tool_config.json").read_text(encoding="utf-8"))
RUNS = 20
QUESTION = "Synthetic eval question"


def main() -> int:
    durations_ms = []
    tool_names = []

    for _ in range(RUNS):
        agent, _memory = create_agent_from_config(CONFIG)
        tool_names = [t["name"] for t in CONFIG["tools"]]
        start = time.perf_counter()
        agent.invoke({"input": QUESTION})
        durations_ms.append((time.perf_counter() - start) * 1000)

    total = sum(durations_ms)
    p50 = statistics.median(durations_ms)

    print(
        f"synthetic_eval: {RUNS} runs, framework=langgraph, tools={len(tool_names)}\n"
        f"total_wall_ms={total:.2f} p50_ms={p50:.2f}\n"
        f"tools_per_run={tool_names}\n"
        f"label=synthetic_no_openai_key"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
