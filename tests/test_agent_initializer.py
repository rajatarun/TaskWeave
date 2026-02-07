import unittest

from agents.agent_initializer import create_agent_from_config, normalize_config


class TestAgentInitializer(unittest.TestCase):
    def test_normalize_config_from_list(self):
        config = normalize_config([
            {
                "name": "ProblemTranslator",
                "description": "Translates user queries",
                "type": "llm_prompt",
                "prompt_template": "Translate: {input}",
            }
        ])
        self.assertIn("agent", config)
        self.assertIn("tools", config)
        self.assertEqual(len(config["tools"]), 1)

    def test_create_agent_missing_tools_key_raises(self):
        with self.assertRaises(ValueError):
            create_agent_from_config({"agent": {"framework": "langgraph"}})

    def test_create_agent_unknown_dependency_raises(self):
        bad_config = {
            "agent": {"framework": "langgraph"},
            "tools": [
                {
                    "name": "Analyzer",
                    "description": "Analyze",
                    "type": "analysis",
                    "prompt_template": "Analyze: {input}",
                    "input": ["MissingTool"],
                }
            ],
        }
        with self.assertRaises(ValueError):
            create_agent_from_config(bad_config)

    def test_create_agent_langgraph_runs_minimal_tools(self):
        config = {
            "agent": {"framework": "langgraph"},
            "tools": [
                {
                    "name": "ProblemTranslator",
                    "description": "Translate",
                    "type": "llm_prompt",
                    "prompt_template": "Translate: {input}",
                },
                {
                    "name": "Analyzer",
                    "description": "Analyze",
                    "type": "analysis",
                    "prompt_template": "Analyze: {input}",
                    "input": ["ProblemTranslator"],
                },
            ],
        }
        agent, memory = create_agent_from_config(config)
        result = agent.invoke({"input": "Compare Q1 and Q2"})
        self.assertIn("outputs", result)
        self.assertIn("ProblemTranslator", result["outputs"])
        self.assertIn("Analyzer", result["outputs"])
        self.assertIn("ProblemTranslator", memory)


if __name__ == "__main__":
    unittest.main()
