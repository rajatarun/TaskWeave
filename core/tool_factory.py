from typing import Any, Dict

import requests
from langchain_core.tools import Tool

from core.llm import call_llm


def _normalize_input(raw_input: Any) -> Dict[str, Any]:
    if isinstance(raw_input, dict):
        return raw_input
    if isinstance(raw_input, str):
        return {"question": raw_input}
    return {"question": str(raw_input)}


def build_tool(tool_def, shared_memory):
    tool_type = tool_def["type"]

    def run(raw_input):
        runtime_input = _normalize_input(raw_input)
        inputs = {"question": runtime_input.get("question", "")}

        for dep in tool_def.get("input", []):
            inputs[dep] = shared_memory.get(dep, {}).get("output")

        inputs.update(runtime_input)

        if tool_type == "llm_prompt":
            prompt = tool_def["prompt_template"].format(input=inputs.get("question", ""))
            response = call_llm(prompt)
            output = {"output": response}

        elif tool_type == "api_call":
            data = {param: inputs.get(param, "") for param in tool_def.get("params_from_input", [])}
            try:
                res = requests.request(
                    method=tool_def["method"],
                    url=tool_def["endpoint"],
                    json=data,
                    timeout=20,
                )
                res.raise_for_status()
                output = {"output": res.json()}
            except requests.RequestException as exc:
                output = {
                    "output": {
                        "warning": f"API call failed, using fallback payload: {exc}",
                        "mock_data": data,
                    }
                }

        elif tool_type == "analysis":
            prompt = tool_def["prompt_template"].format(input=inputs)
            response = call_llm(prompt)
            output = {"output": response}

        else:
            raise ValueError(f"Unsupported tool type: {tool_type}")

        shared_memory[tool_def["name"]] = output
        return output

    return Tool(name=tool_def["name"], description=tool_def["description"], func=run)
