import unittest

from src.agents.router import classify_router_accuracy, route_query


class RouterTests(unittest.TestCase):
    def test_route_pure_national(self):
        result = route_query("Analisis KUHPerdata terkait wanprestasi perjanjian.", use_llm=False)
        self.assertEqual(result["label"], "pure_national")

    def test_route_pure_adat(self):
        result = route_query("Sengketa pusako dan hak kemenakan dalam adat Minangkabau.", use_llm=False)
        self.assertEqual(result["label"], "pure_adat")

    def test_route_conflict(self):
        result = route_query("Ada konflik antara KUHPerdata versus adat Minangkabau soal warisan.", use_llm=False)
        self.assertEqual(result["label"], "conflict")

    def test_route_consensus_fallback(self):
        result = route_query("Bagaimana penyelesaian sengketa keluarga yang adil?", use_llm=False)
        self.assertEqual(result["label"], "consensus")

    def test_classify_router_accuracy(self):
        cases = {
            "KUHPerdata tentang gono-gini": "pure_national",
            "Hak mamak atas pusako": "pure_adat",
            "Konflik hukum nasional dan adat": "conflict",
            "Pendapat umum tentang mediasi sengketa": "consensus",
        }
        score = classify_router_accuracy(cases)
        self.assertGreaterEqual(score, 0.75)

    def test_route_empty_string_fallback(self):
        """Edge case: empty string should not crash, fallback to consensus."""
        result = route_query("", use_llm=False)
        self.assertIn("label", result)
        self.assertIn("confidence", result)

    def test_route_whitespace_only_fallback(self):
        """Edge case: whitespace-only query should fallback gracefully."""
        result = route_query("   \n\t  ", use_llm=False)
        self.assertIn("label", result)
        self.assertIn("confidence", result)

    def test_route_mixed_conflict_keywords(self):
        """Edge case: multiple conflict keywords should still detect conflict."""
        result = route_query(
            "Konflik antara KUHPerdata dan adat Bali tentang warisan versus sentana",
            use_llm=False
        )
        self.assertEqual(result["label"], "conflict")

    def test_route_case_insensitive(self):
        """Edge case: uppercase keywords should still work."""
        result = route_query("KONFLIK HUKUM NASIONAL DAN ADAT", use_llm=False)
        self.assertEqual(result["label"], "conflict")


if __name__ == "__main__":
    unittest.main()
