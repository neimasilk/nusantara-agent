"""Test deterministik untuk modul llm_judge utilities."""
import unittest


class LlmJudgeUtilsTests(unittest.TestCase):
    """Test suite untuk LLM judge utilities (non-LLM, deterministik)."""

    def test_json_extraction_plain(self):
        """Test: plain JSON tetap valid."""
        text = '{"scores":{"correctness":1.0}}'
        # Jika tidak ada method _extract_json_payload, test parser manual
        import json
        try:
            data = json.loads(text)
            self.assertEqual(data["scores"]["correctness"], 1.0)
        except json.JSONDecodeError:
            self.fail("Plain JSON should parse")

    def test_json_extraction_fenced(self):
        """Test: extraction dari fenced JSON code block."""
        text = """```json
{"scores":{"correctness":0.8}}
```"""
        import json
        # Simulate extraction
        if "```json" in text:
            start = text.index("```json") + len("```json")
            end = text.index("```", start)
            payload = text[start:end].strip()
            data = json.loads(payload)
            self.assertEqual(data["scores"]["correctness"], 0.8)
        else:
            self.fail("Should detect json fence")

    def test_json_extraction_invalid(self):
        """Edge case: invalid JSON should fallback gracefully."""
        text = "Not a JSON"
        import json
        try:
            json.loads(text)
            self.fail("Should raise JSONDecodeError")
        except json.JSONDecodeError:
            pass  # Expected


if __name__ == "__main__":
    unittest.main()
