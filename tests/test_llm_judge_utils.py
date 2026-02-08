import unittest

from src.evaluation.llm_judge import TripleEvaluator


class LlmJudgeUtilsTests(unittest.TestCase):
    def test_extract_json_payload_plain(self):
        text = '{"scores":{"correctness":1.0}}'
        self.assertEqual(TripleEvaluator._extract_json_payload(text), text)

    def test_extract_json_payload_fenced(self):
        text = """```json
{"scores":{"correctness":0.8}}
```"""
        payload = TripleEvaluator._extract_json_payload(text)
        self.assertIn('"correctness":0.8', payload)


if __name__ == "__main__":
    unittest.main()
