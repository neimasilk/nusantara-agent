"""Test deterministik untuk unified pipeline Nusantara-Agent."""

import unittest
import json
from unittest.mock import patch


class _FakeOrchestrator:
    """Stub orchestrator untuk memastikan test pipeline tetap offline."""

    def __init__(self, route_label=None):
        self.route_label = route_label or "unknown"

    def invoke(self, _inputs):
        return {
            "final_synthesis": f"MOCK_SYNTHESIS[{self.route_label}]",
            "national_context": f"MOCK_NATIONAL[{self.route_label}]",
            "adat_context": f"MOCK_ADAT[{self.route_label}]",
        }


class NusantaraPipelineTests(unittest.TestCase):
    def setUp(self):
        self._builder_patcher = patch(
            "src.pipeline.nusantara_agent.build_parallel_orchestrator",
            side_effect=self._fake_build_parallel_orchestrator,
        )
        self._builder_patcher.start()
        self.addCleanup(self._builder_patcher.stop)

    @staticmethod
    def _fake_build_parallel_orchestrator(*_args, **kwargs):
        return _FakeOrchestrator(route_label=kwargs.get("route_label"))

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
            "Bandingkan KUHPerdata dan adat setempat tentang pembagian waris secara rukun keluarga."
        )
        self.assertEqual(result["route"]["label"], "consensus")
        self.assertIsInstance(result["rule_results"]["nasional"], list)
        self.assertGreater(len(result["rule_results"]["adat"]), 0)

    def test_pipeline_vector_and_graph_context_available(self):
        """Pipeline selalu mengembalikan konteks graph dan vector."""
        pipeline = self._build_pipeline()
        result = pipeline.process_query("Contoh query hukum adat")
        self.assertIn("graph_context", result)
        self.assertIn("vector_context", result)
        self.assertIsInstance(result["vector_context"], list)

    def test_jawa_guard_overrides_a_to_b_without_national_hard_constraints(self):
        pipeline = self._build_pipeline()
        synthesis = json.dumps(
            {
                "label": "A",
                "langkah_keputusan": "2",
                "alasan_utama": "Dummy",
                "konflik_terdeteksi": "Tidak",
            },
            ensure_ascii=False,
        )
        guarded = pipeline._apply_jawa_guard_v1(
            synthesis,
            query="Sengketa gono-gini adat Jawa tanpa kata nasional keras",
            rule_results={"nasional": [], "adat": {"jawa": ["can_inherit(anak,harta_gono_gini)"]}},
        )
        payload = json.loads(guarded)
        self.assertEqual(payload["label"], "B")
        self.assertEqual(payload["langkah_keputusan"], "3")
        self.assertEqual(payload.get("jawa_guard_v1"), "applied")

    def test_jawa_guard_does_not_override_when_national_hard_constraint_exists(self):
        pipeline = self._build_pipeline()
        synthesis = json.dumps(
            {
                "label": "A",
                "langkah_keputusan": "2",
                "alasan_utama": "Dummy",
                "konflik_terdeteksi": "Tidak",
            },
            ensure_ascii=False,
        )
        guarded = pipeline._apply_jawa_guard_v1(
            synthesis,
            query="Sengketa gono-gini adat Jawa terkait penetapan pengadilan",
            rule_results={"nasional": [], "adat": {"jawa": []}},
        )
        payload = json.loads(guarded)
        self.assertEqual(payload["label"], "A")
        self.assertNotIn("jawa_guard_v1", payload)

    def test_jawa_guard_still_overrides_for_generic_perceraian_context(self):
        pipeline = self._build_pipeline()
        synthesis = json.dumps(
            {
                "label": "A",
                "langkah_keputusan": "2",
                "alasan_utama": "Dummy",
                "konflik_terdeteksi": "Tidak",
            },
            ensure_ascii=False,
        )
        guarded = pipeline._apply_jawa_guard_v1(
            synthesis,
            query="Jika terjadi perceraian, pembagian harta gono-gini adat Jawa bagaimana?",
            rule_results={"nasional": [], "adat": {"jawa": []}},
        )
        payload = json.loads(guarded)
        self.assertEqual(payload["label"], "B")
        self.assertEqual(payload.get("jawa_guard_v1"), "applied")


if __name__ == "__main__":
    unittest.main()
