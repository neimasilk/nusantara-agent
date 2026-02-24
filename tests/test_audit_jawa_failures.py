import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "audit_jawa_failures.py"

spec = importlib.util.spec_from_file_location("audit_jawa_failures_module", SCRIPT_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Failed to load scripts/audit_jawa_failures.py")
audit = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = audit
spec.loader.exec_module(audit)


class AuditJawaFailuresTests(unittest.TestCase):
    def test_parse_reasoning_payload_plain_json(self) -> None:
        payload = audit.parse_reasoning_payload(
            '{"label":"A","langkah_keputusan":"1","konflik_terdeteksi":"Tidak"}'
        )
        self.assertEqual(payload.get("label"), "A")
        self.assertEqual(payload.get("langkah_keputusan"), "1")

    def test_parse_reasoning_payload_extracts_embedded_json(self) -> None:
        payload = audit.parse_reasoning_payload(
            "raw text prefix {\"label\":\"C\",\"konflik_terdeteksi\":\"Ya\"} suffix"
        )
        self.assertEqual(payload.get("label"), "C")
        self.assertEqual(payload.get("konflik_terdeteksi"), "Ya")

    def test_classify_layer_router_vs_adjudication_split(self) -> None:
        self.assertEqual(
            audit.classify_layer("C", "B", "no", "3"),
            "router_or_fact_extraction",
        )
        self.assertEqual(
            audit.classify_layer("C", "B", "yes", "4"),
            "adjudication_collapse_after_conflict",
        )

    def test_classify_layer_b_to_a_and_d_label(self) -> None:
        self.assertEqual(
            audit.classify_layer("B", "A", "no", "1"),
            "national_dominance_bias",
        )
        self.assertEqual(
            audit.classify_layer("D", "C", "unknown", ""),
            "no_abstention_path",
        )


if __name__ == "__main__":
    unittest.main()
