import json
from typing import Any, Dict, List, TypedDict

from langchain.agents import create_agent as create_langchain_agent
from langgraph.graph import END, StateGraph

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
            "agent": {"framework": "langgraph", "model": "gpt-4o-mini", "verbose": True},
            "tools": raw,
        }

    if "tools" not in raw:
        raise ValueError("Invalid config: expected top-level 'tools' key")

    return raw


def _compute_execution_order(tool_defs: List[Dict[str, Any]]) -> List[str]:
    tool_map = {tool["name"]: tool for tool in tool_defs}
    indegree = {name: 0 for name in tool_map}
    graph = {name: [] for name in tool_map}

    for tool in tool_defs:
        for dep in tool.get("input", []):
            if dep not in tool_map:
                raise ValueError(f"Tool '{tool['name']}' depends on unknown tool '{dep}'.")
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


def _extract_question(payload: Dict[str, Any]) -> str:
    question = payload.get("input") or payload.get("question") or ""
    if not question:
        raise ValueError("Missing question. Provide payload with 'input' or 'question'.")
    return question


class SequentialDynamicAgent:
    def __init__(self, ordered_tools, metadata: Dict[str, Any] | None = None):
        self.ordered_tools = ordered_tools
        self.metadata = metadata or {}

    def invoke(self, payload: Dict[str, Any]):
        question = _extract_question(payload)
        outputs = {}
        for tool in self.ordered_tools:
            result = tool.invoke({"question": question})
            outputs[tool.name] = result
        response = {"question": question, "outputs": outputs}
        if self.metadata:
            response["metadata"] = self.metadata
        return response


class LangChainDynamicAgent:
    def __init__(self, compiled_agent):
        self.compiled_agent = compiled_agent

    def invoke(self, payload: Dict[str, Any]):
        question = _extract_question(payload)
        return self.compiled_agent.invoke({"messages": [{"role": "user", "content": question}]})


class LangGraphDynamicAgent:
    def __init__(self, graph):
        self.graph = graph

    def invoke(self, payload: Dict[str, Any]):
        question = _extract_question(payload)
        return self.graph.invoke({"question": question, "outputs": {}})


def _build_sequential_fallback(config: Dict[str, Any], reason: str):
    tool_defs = config["tools"]
    tool_map = {tool["name"]: build_tool(tool, shared_memory) for tool in tool_defs}
    execution_order = _compute_execution_order(tool_defs)
    ordered_tools = [tool_map[name] for name in execution_order]
    return SequentialDynamicAgent(ordered_tools, {"fallback_reason": reason})


def _build_langchain_agent(config: Dict[str, Any]):
    tools = [build_tool(tool_def, shared_memory) for tool_def in config["tools"]]
    model_name = config.get("agent", {}).get("model", "gpt-4o-mini")
    system_prompt = config.get("agent", {}).get(
        "system_prompt",
        "You are a dynamic orchestrator. Choose the right tools based on user intent and available tool descriptions.",
    )

    try:
        compiled_agent = create_langchain_agent(
            model=model_name,
            tools=tools,
            system_prompt=system_prompt,
        )
    except ImportError as exc:
        return _build_sequential_fallback(config, f"langchain runtime unavailable: {exc}")

    return LangChainDynamicAgent(compiled_agent)


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

    return LangGraphDynamicAgent(workflow.compile())


def create_agent(config_path: str = "config/tool_config.json"):
    shared_memory.clear()
    config = load_tool_config(config_path)
    framework = config.get("agent", {}).get("framework", "langgraph").lower()

    if framework == "langchain":
        return _build_langchain_agent(config), shared_memory
    if framework == "langgraph":
        return _build_langgraph_agent(config), shared_memory

    raise ValueError("Unsupported framework. Use 'langchain' or 'langgraph'.")
