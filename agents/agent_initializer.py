import json
from typing import Any, Dict, List, TypedDict

from langchain_core.prompt_values import StringPromptValue
from langchain_core.runnables import Runnable
from langgraph.graph import END, StateGraph

from core.llm import call_llm
from core.tool_factory import build_tool

shared_memory: Dict[str, Dict[str, Any]] = {}


class WorkflowState(TypedDict, total=False):
    question: str
    outputs: Dict[str, Dict[str, Any]]


def load_tool_config(path: str = "config/tool_config.json") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, list):
        return {
            "agent": {"framework": "langchain", "agent_type": "SEQUENTIAL", "verbose": True},
            "tools": raw,
        }

    if "tools" not in raw:
        raise ValueError("Invalid config: expected top-level 'tools' key")

    return raw


class CustomLLMWrapper(Runnable):
    def invoke(self, input: Any, config: dict = None, **kwargs) -> str:
        if isinstance(input, StringPromptValue):
            prompt = input.to_string()
        elif isinstance(input, dict):
            prompt = input.get("input") or input.get("question") or str(input)
        elif isinstance(input, str):
            prompt = input
        else:
            raise ValueError(f"Unsupported input type: {type(input)}")

        return call_llm(prompt)


def _compute_execution_order(tool_defs: List[Dict[str, Any]]) -> List[str]:
    tool_map = {tool["name"]: tool for tool in tool_defs}
    indegree = {name: 0 for name in tool_map}
    graph = {name: [] for name in tool_map}

    for tool in tool_defs:
        for dep in tool.get("input", []):
            if dep in tool_map:
                graph[dep].append(tool["name"])
                indegree[tool["name"]] += 1

    queue = [name for name, degree in indegree.items() if degree == 0]
    order = []

    while queue:
        node = queue.pop(0)
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(order) != len(tool_defs):
        raise ValueError("Cycle detected in tool dependency graph. Check `input` references.")

    return order


class SequentialDynamicAgent:
    def __init__(self, ordered_tools):
        self.ordered_tools = ordered_tools

    def invoke(self, payload: Dict[str, Any]):
        question = payload.get("input") or payload.get("question") or ""
        outputs = {}
        for tool in self.ordered_tools:
            result = tool.invoke({"question": question})
            outputs[tool.name] = result
        return {"question": question, "outputs": outputs}


def _build_langchain_agent(config: Dict[str, Any]):
    tool_defs = config["tools"]
    tool_map = {tool["name"]: build_tool(tool, shared_memory) for tool in tool_defs}
    execution_order = _compute_execution_order(tool_defs)
    ordered_tools = [tool_map[name] for name in execution_order]
    return SequentialDynamicAgent(ordered_tools)


def _build_langgraph_agent(config: Dict[str, Any]):
    tool_defs = config["tools"]
    tool_map = {tool["name"]: build_tool(tool, shared_memory) for tool in tool_defs}
    execution_order = _compute_execution_order(tool_defs)

    workflow = StateGraph(WorkflowState)

    for tool_name in execution_order:
        tool = tool_map[tool_name]

        def make_node(current_tool):
            def node(state: WorkflowState):
                question = state.get("question", "")
                result = current_tool.invoke({"question": question})
                outputs = dict(state.get("outputs", {}))
                outputs[current_tool.name] = result
                return {"question": question, "outputs": outputs}

            return node

        workflow.add_node(tool_name, make_node(tool))

    workflow.set_entry_point(execution_order[0])
    for idx in range(len(execution_order) - 1):
        workflow.add_edge(execution_order[idx], execution_order[idx + 1])
    workflow.add_edge(execution_order[-1], END)

    graph = workflow.compile()

    class LangGraphDynamicAgent:
        def invoke(self, payload: Dict[str, Any]):
            question = payload.get("input") or payload.get("question") or ""
            return graph.invoke({"question": question, "outputs": {}})

    return LangGraphDynamicAgent()


def create_agent(config_path: str = "config/tool_config.json"):
    shared_memory.clear()
    config = load_tool_config(config_path)
    framework = config.get("agent", {}).get("framework", "langchain").lower()

    if framework == "langchain":
        return _build_langchain_agent(config), shared_memory
    if framework == "langgraph":
        return _build_langgraph_agent(config), shared_memory

    raise ValueError("Unsupported framework. Use 'langchain' or 'langgraph'.")
