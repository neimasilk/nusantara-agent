import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIM_GATE_PATH = ROOT / "scripts" / "claim_gate.py"

spec = importlib.util.spec_from_file_location("claim_gate_module", CLAIM_GATE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Gagal memuat scripts/claim_gate.py")
claim_gate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = claim_gate
spec.loader.exec_module(claim_gate)


class ClaimGateKeyNumbersTests(unittest.TestCase):
    def _minimal_key_number_text(self, extra: str = "") -> str:
        return (
            "ASP-only 58.6% (41/70)\n"
            "ASP+Ollama 64.3% (45/70)\n"
            "ASP+DeepSeek 68.6% (48/70)\n"
            "on the 70 evaluable cases\n"
            "benchmark of 74\n"
            f"{extra}\n"
        )

    def test_check_key_numbers_passes_on_canonical_values(self) -> None:
        result = claim_gate.check_key_numbers(self._minimal_key_number_text())
        self.assertEqual(result.status, "pass")
        self.assertFalse(result.blocking)

    def test_check_key_numbers_warns_on_known_exploratory_ratio(self) -> None:
        text = self._minimal_key_number_text("exploratory run 38/70 and paired baseline 42/70")
        result = claim_gate.check_key_numbers(text)
        self.assertEqual(result.status, "warn")
        self.assertFalse(result.blocking)
        self.assertIn("exploratory /70 ratios", result.message)

    def test_check_key_numbers_fails_on_unknown_ratio(self) -> None:
        text = self._minimal_key_number_text("unexpected report 39/70")
        result = claim_gate.check_key_numbers(text)
        self.assertEqual(result.status, "fail")
        self.assertTrue(result.blocking)
        self.assertIn("unexpected benchmark ratio", result.message)


if __name__ == "__main__":
    unittest.main()
