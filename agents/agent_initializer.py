import json
from core.tool_factory import build_tool
from langchain.agents import initialize_agent, AgentType
from core.llm import call_llm
from langchain_core.runnables import Runnable
from typing import Any
from langchain_core.prompts_values import StringPromptValue

shared_memory = {}

def load_tool_config():
    with open("config/tool_config.json", "r") as f:
        return json.load(f)



class CustomLLMWrapper(Runnable):
    def invoke(self, input: Any, config: dict = None, **kwargs) -> str:
        # Handle PromptValue input
        if isinstance(input, StringPromptValue):
            prompt = input.to_string()
        elif isinstance(input, dict) and "input" in input:
            prompt = input["input"]
        elif isinstance(input, str):
            prompt = input
        else:
            raise ValueError(f"Unsupported input type: {type(input)}")

        return call_llm(prompt)

def create_agent():
    tools = []
    config = load_tool_config()
    for tool_def in config:
        tools.append(build_tool(tool_def, shared_memory))

    llm = CustomLLMWrapper()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent, shared_memory
