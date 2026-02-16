import unittest

from src.utils.benchmark_contract import (
    count_evaluable_cases,
    is_evaluable_gold_label,
    normalize_gold_label,
    resolve_manifest_evaluable_count,
)


class BenchmarkContractTests(unittest.TestCase):
    def test_normalize_gold_label(self):
        self.assertEqual(normalize_gold_label(" a "), "A")
        self.assertEqual(normalize_gold_label(None), "")

    def test_is_evaluable_gold_label(self):
        self.assertTrue(is_evaluable_gold_label("A"))
        self.assertFalse(is_evaluable_gold_label("SPLIT"))
        self.assertFalse(is_evaluable_gold_label("DISPUTED"))
        self.assertFalse(is_evaluable_gold_label("ambiguous"))

    def test_count_evaluable_cases(self):
        cases = [
            {"gold_label": "A"},
            {"gold_label": "DISPUTED"},
            {"gold_label": "C"},
            {"gold_label": "SPLIT"},
            {"gold_label": "D"},
        ]
        self.assertEqual(count_evaluable_cases(cases), 3)

    def test_resolve_manifest_evaluable_count_prefers_disputed_key(self):
        benchmark_meta = {
            "evaluable_cases_excluding_disputed": 14,
            "evaluable_cases_excluding_split": 22,
        }
        self.assertEqual(resolve_manifest_evaluable_count(benchmark_meta), 14)

    def test_resolve_manifest_evaluable_count_fallback_split_key(self):
        benchmark_meta = {"evaluable_cases_excluding_split": 22}
        self.assertEqual(resolve_manifest_evaluable_count(benchmark_meta), 22)


if __name__ == "__main__":
    unittest.main()
