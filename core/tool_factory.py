import requests
from langchain.agents import Tool
from core.llm import call_llm

def build_tool(tool_def, shared_memory):
    tool_type = tool_def["type"]

    def run(input):
        inputs = {}
        if "input" in tool_def:
            for dep in tool_def["input"]:
                inputs[dep] = shared_memory.get(dep, {}).get("output", {})
        inputs.update(input)

        if tool_type == "llm_prompt":
            prompt = tool_def["prompt_template"].format(input=inputs.get("question", ""))
            response = call_llm(prompt)
            output = {"output": response}

        elif tool_type == "api_call":
            data = {param: inputs.get(param, "") for param in tool_def["params_from_input"]}
            res = requests.request(
                method=tool_def["method"],
                url=tool_def["endpoint"],
                json=data
            )
            output = {"output": res.json()}

        elif tool_type == "analysis":
            prompt = tool_def["prompt_template"].format(input=inputs.get("question", ""))
            response = call_llm(prompt)
            output = {"output": f"Correlation analysis done using inputs: {inputs}"}

        else:
            raise ValueError(f"Unsupported tool type: {tool_type}")

        shared_memory[tool_def["name"]] = output
        return output

    return Tool(
        name=tool_def["name"],
        description=tool_def["description"],
        func=run
    )
