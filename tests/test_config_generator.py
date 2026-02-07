import json
import unittest

from agents.tool_config_generator import generate_config_from_question


class TestConfigGenerator(unittest.TestCase):
    def test_generate_config_falls_back_with_mock_llm(self):
        config = generate_config_from_question("Compare Q1 and Q2 sales")
        self.assertIn("agent", config)
        self.assertIn("tools", config)
        self.assertIn("metadata", config)
        self.assertIn("fallback_reason", config["metadata"])
        self.assertGreater(len(config["tools"]), 0)

    def test_tool_schema_contains_tags(self):
        with open("config/tool_schema.json", "r", encoding="utf-8") as f:
            schema = json.load(f)
        self.assertIn("tools", schema)
        self.assertGreater(len(schema["tools"]), 0)
        for tool in schema["tools"]:
            self.assertIn("tags", tool)
            self.assertGreater(len(tool["tags"]), 0)


if __name__ == "__main__":
    unittest.main()
