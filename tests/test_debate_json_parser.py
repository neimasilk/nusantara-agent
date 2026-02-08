import unittest

from src.agents.debate import _json_or_raw


class DebateJsonParserTests(unittest.TestCase):
    def test_plain_json(self):
        data = _json_or_raw('{"a": 1, "b": "ok"}')
        self.assertEqual(data["a"], 1)
        self.assertEqual(data["b"], "ok")

    def test_fenced_json(self):
        text = """```json
{"answer":"ringkas","claims":[]}
```"""
        data = _json_or_raw(text)
        self.assertEqual(data["answer"], "ringkas")

    def test_non_json_fallback(self):
        text = "Output model tidak valid"
        data = _json_or_raw(text)
        self.assertIn("raw_output", data)

    def test_unclosed_fence_fallback(self):
        text = "```json\n{not-json}"
        data = _json_or_raw(text)
        self.assertIn("raw_output", data)

    def test_empty_string_fallback(self):
        """Edge case: empty string should return raw_output."""
        data = _json_or_raw("")
        self.assertIn("raw_output", data)
        self.assertEqual(data["raw_output"], "")

    def test_json_with_unicode(self):
        """Edge case: JSON with Indonesian unicode characters."""
        text = '{"answer": "hak waris dalam adat Minangkabau", "claims": ["mamak", "kemenakan"]}'
        data = _json_or_raw(text)
        self.assertEqual(data["answer"], "hak waris dalam adat Minangkabau")
        self.assertEqual(data["claims"], ["mamak", "kemenakan"])

    def test_partial_json_fallback(self):
        """Edge case: malformed/partial JSON should fallback."""
        text = '{"key": "value", "broken"}'
        data = _json_or_raw(text)
        self.assertIn("raw_output", data)

    def test_whitespace_only_fallback(self):
        """Edge case: whitespace-only string should fallback gracefully."""
        data = _json_or_raw("   \n\t  ")
        self.assertIn("raw_output", data)


if __name__ == "__main__":
    unittest.main()
