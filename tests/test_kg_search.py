import json
import tempfile
import unittest
from pathlib import Path

from src.kg_engine.search import SimpleKGSearch


class KGSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "kg.json"
        payload = {
            "triples": [
                {"head": "Pusako Tinggi", "relation": "dikelola_oleh", "tail": "Mamak", "category": "Otoritas"},
                {"head": "Pusako Rendah", "relation": "diwariskan_ke", "tail": "Anak Kandung", "category": "Warisan"},
                {"head": "Pusako Tinggi", "relation": "dikelola_oleh", "tail": "Mamak", "category": "Otoritas"},
            ]
        }
        self.path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        self.searcher = SimpleKGSearch(str(self.path))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_search_deduplicates(self):
        results = self.searcher.search("pusako, mamak", limit=10)
        self.assertEqual(len(results), 2)

    def test_search_not_found(self):
        results = self.searcher.search("nonexistent keyword", limit=5)
        self.assertEqual(results, [])

    def test_context_output(self):
        ctx = self.searcher.get_context_for_query("pusako")
        self.assertIn("Hasil pencarian Knowledge Graph tambahan", ctx)

    def test_context_not_found_output(self):
        ctx = self.searcher.get_context_for_query("xyz")
        self.assertIn("Tidak ditemukan informasi tambahan", ctx)


if __name__ == "__main__":
    unittest.main()
