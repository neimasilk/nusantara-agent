"""Test deterministik untuk unified pipeline Nusantara-Agent."""

import unittest


class NusantaraPipelineTests(unittest.TestCase):
    def _build_pipeline(self):
        try:
            from src.pipeline.nusantara_agent import NusantaraAgentPipeline
        except ImportError as exc:
            self.skipTest(f"Dependency tidak tersedia: {exc}")
        return NusantaraAgentPipeline()

    def test_pipeline_pure_national(self):
        """Query nasional harus memicu rule nasional."""
        pipeline = self._build_pipeline()
        result = pipeline.process_query(
            "Menurut KUHPerdata, jika pewaris meninggalkan istri dan anak, siapa ahli warisnya?"
        )
        self.assertEqual(result["route"]["label"], "pure_national")
        nasional_atoms = result["rule_results"]["nasional"]
        self.assertTrue(any(atom.startswith("berhak_waris(") for atom in nasional_atoms))

    def test_pipeline_pure_adat_bali(self):
        """Query adat Bali harus memicu rule Bali."""
        pipeline = self._build_pipeline()
        result = pipeline.process_query(
            "Dalam adat Bali, apakah anak perempuan yang kawin keluar tetap mendapat waris?"
        )
        self.assertEqual(result["route"]["label"], "pure_adat")
        adat_bali = result["rule_results"]["adat"].get("bali", [])
        self.assertTrue(any("ahli_waris_terbatas" in atom for atom in adat_bali))
        self.assertEqual(result["rule_results"]["nasional"], [])

    def test_pipeline_conflict(self):
        """Query konflik harus memicu rule nasional dan adat."""
        pipeline = self._build_pipeline()
        result = pipeline.process_query(
            "Konflik antara KUHPerdata dan adat Bali terkait hak anak perempuan dalam waris bagaimana?"
        )
        self.assertEqual(result["route"]["label"], "conflict")
        self.assertGreater(len(result["rule_results"]["nasional"]), 0)
        self.assertIn("bali", result["rule_results"]["adat"])

    def test_pipeline_consensus(self):
        """Query consensus harus memproses nasional + adat tanpa kata konflik."""
        pipeline = self._build_pipeline()
        result = pipeline.process_query(
            "Bandingkan KUHPerdata dan adat Jawa tentang pembagian gono-gini secara rukun keluarga."
        )
        self.assertEqual(result["route"]["label"], "consensus")
        self.assertGreater(len(result["rule_results"]["nasional"]), 0)
        self.assertIn("jawa", result["rule_results"]["adat"])

    def test_pipeline_vector_and_graph_context_available(self):
        """Pipeline selalu mengembalikan konteks graph dan vector."""
        pipeline = self._build_pipeline()
        result = pipeline.process_query("Contoh query hukum adat")
        self.assertIn("graph_context", result)
        self.assertIn("vector_context", result)
        self.assertIsInstance(result["vector_context"], list)


if __name__ == "__main__":
    unittest.main()

