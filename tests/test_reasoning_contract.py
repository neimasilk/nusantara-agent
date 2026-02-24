import unittest

from src.utils.reasoning_contract import parse_reasoning_payload, summarize_reasoning_contract


class ReasoningContractTests(unittest.TestCase):
    def test_parse_reasoning_payload_plain_json(self):
        payload = parse_reasoning_payload(
            '{"label":"B","langkah_keputusan":"3","alasan_utama":"adat","konflik_terdeteksi":"Tidak"}'
        )
        self.assertEqual(payload.get("label"), "B")
        self.assertEqual(payload.get("langkah_keputusan"), "3")

    def test_parse_reasoning_payload_embedded_json(self):
        payload = parse_reasoning_payload(
            'prefix text {"label":"C","langkah_keputusan":"4","alasan_utama":"x","konflik_terdeteksi":"Ya"} suffix'
        )
        self.assertEqual(payload.get("label"), "C")
        self.assertEqual(payload.get("konflik_terdeteksi"), "Ya")

    def test_summarize_reasoning_contract_complete(self):
        results = [
            {
                "id": "CASE-1",
                "reasoning": '{"label":"A","langkah_keputusan":"2","alasan_utama":"x","konflik_terdeteksi":"Tidak"}',
            },
            {
                "id": "CASE-2",
                "reasoning": '{"label":"C","langkah_keputusan":"4","alasan_utama":"y","konflik_terdeteksi":"Ya"}',
            },
        ]
        summary = summarize_reasoning_contract(results)
        self.assertTrue(summary["all_required_present"])
        self.assertTrue(summary["claimable_for_layer_diagnosis"])
        self.assertEqual(summary["complete_count"], 2)

    def test_summarize_reasoning_contract_incomplete(self):
        results = [
            {
                "id": "CASE-1",
                "reasoning": '{"label":"A","alasan_utama":"x"}',
            },
            {
                "id": "CASE-2",
                "reasoning": "not-json",
            },
        ]
        summary = summarize_reasoning_contract(results)
        self.assertFalse(summary["all_required_present"])
        self.assertFalse(summary["claimable_for_layer_diagnosis"])
        self.assertEqual(summary["complete_count"], 0)
        self.assertIn("CASE-1", summary["incomplete_case_ids"])
        self.assertIn("CASE-2", summary["incomplete_case_ids"])


if __name__ == "__main__":
    unittest.main()
