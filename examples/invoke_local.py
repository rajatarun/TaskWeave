#!/usr/bin/env python3
"""Run TaskWeave from a JSON config file without starting the HTTP server."""

import argparse
import json
import sys
from pathlib import Path

# Allow running from repo root
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.agent_initializer import create_agent_from_config  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Invoke TaskWeave locally from a config file.")
    parser.add_argument(
        "--config",
        default=str(ROOT / "config" / "tool_config.json"),
        help="Path to agent config JSON",
    )
    parser.add_argument(
        "--input",
        default="Compare Q1 and Q2 sales trends",
        help="User question / input string",
    )
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    agent, memory = create_agent_from_config(config)
    result = agent.invoke({"input": args.input})

    print(json.dumps({"result": result, "shared_memory": memory}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
