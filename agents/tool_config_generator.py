import json
from typing import Any, Dict, List

from core.llm import call_llm


DEFAULT_AGENT_SETTINGS = {
    "framework": "langgraph",
    "model": "gpt-4o-mini",
    "system_prompt": "You are a task orchestrator that selects tools to solve the user request.",
}


def _load_schema(schema_path: str) -> Dict[str, Any]:
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _validate_tool_names(selected_tools: List[Dict[str, Any]], registry: Dict[str, Any]) -> None:
    registry_map = {tool["name"]: tool for tool in registry.get("tools", [])}
    for tool in selected_tools:
        if tool.get("name") not in registry_map:
            raise ValueError(f"Selected tool '{tool.get('name')}' not found in schema registry.")


def _normalize_generated_config(config: Dict[str, Any], registry: Dict[str, Any]) -> Dict[str, Any]:
    tools = config.get("tools", [])
    _validate_tool_names(tools, registry)
    return {
        "agent": {**DEFAULT_AGENT_SETTINGS, **config.get("agent", {})},
        "tools": tools,
    }


def _fallback_config(question: str, registry: Dict[str, Any]) -> Dict[str, Any]:
    tools = registry.get("tools", [])
    if not tools:
        raise ValueError("Tool schema registry is empty.")

    safe_order = [tool for tool in tools if tool.get("name") in {"ProblemTranslator", "DataFetcher", "Analyzer"}]
    if not safe_order:
        safe_order = tools[:3]

    return {
        "agent": DEFAULT_AGENT_SETTINGS,
        "tools": safe_order,
        "metadata": {"fallback_reason": "LLM config generation unavailable", "question": question},
    }


def generate_config_from_question(question: str, schema_path: str = "config/tool_schema.json") -> Dict[str, Any]:
    registry = _load_schema(schema_path)

    prompt = (
        "You are a configuration generator for TaskWeave. "
        "Given a user question and the tool registry JSON, select the minimal set of tools "
        "needed to solve the request, and output ONLY valid JSON matching this shape:\n"
        "{\n"
        "  \"agent\": {\"framework\": \"langgraph\", \"model\": \"gpt-4o-mini\", \"system_prompt\": \"...\"},\n"
        "  \"tools\": [<tool objects from registry>]\n"
        "}\n\n"
        "Rules:\n"
        "- Use exact tool objects from the registry (no edits).\n"
        "- Preserve dependency order (upstream before downstream).\n"
        "- Include only the tools needed.\n"
        "- Output JSON only, no extra text.\n\n"
        f"User question: {question}\n\n"
        "Tool registry JSON:\n"
        f"{json.dumps(registry)}"
    )

    response = call_llm(prompt)
    try:
        generated = json.loads(response)
    except json.JSONDecodeError:
        return _fallback_config(question, registry)

    try:
        return _normalize_generated_config(generated, registry)
    except Exception:
        return _fallback_config(question, registry)
