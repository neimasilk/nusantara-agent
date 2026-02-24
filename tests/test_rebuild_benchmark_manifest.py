import importlib.util
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "rebuild_benchmark_manifest.py"

spec = importlib.util.spec_from_file_location("rebuild_manifest_module", SCRIPT_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Gagal memuat scripts/rebuild_benchmark_manifest.py")
rebuild_manifest_module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = rebuild_manifest_module
spec.loader.exec_module(rebuild_manifest_module)


class RebuildManifestPolicyTests(unittest.TestCase):
    def _run_rebuild(self, **kwargs: object) -> int:
        sink = StringIO()
        with redirect_stdout(sink):
            return rebuild_manifest_module.rebuild_manifest(**kwargs)

    def _write_dataset(self, path: Path, n: int) -> None:
        payload = [
            {
                "id": f"GS-{i:04d}",
                "query": f"case {i}",
                "gold_label": "A" if i % 2 else "B",
            }
            for i in range(1, n + 1)
        ]
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def test_default_declared_total_follows_dataset_not_legacy_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            dataset = root / "gs_active_cases.json"
            manifest = root / "benchmark_manifest.json"
            reference = root / "reference.md"

            self._write_dataset(dataset, 3)
            reference.write_text("reference claim", encoding="utf-8")
            manifest.write_text(
                json.dumps({"reference_claim": {"declared_total_cases": 82}}),
                encoding="utf-8",
            )

            code = self._run_rebuild(
                dataset_path=dataset,
                manifest_path=manifest,
                reference_path=reference,
                as_of_date="2026-02-24",
                owner="test-owner",
                declared_total_cases=None,
                inherit_declared_total_from_manifest=False,
            )
            self.assertEqual(code, 0)

            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["reference_claim"]["declared_total_cases"], 3)
            self.assertEqual(payload["reference_claim"]["declared_total_cases_source"], "dataset_actual")
            self.assertTrue(payload["integrity_checks"]["count_matches_reference_claim"])

    def test_cli_override_declared_total_cases_is_respected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            dataset = root / "gs_active_cases.json"
            manifest = root / "benchmark_manifest.json"
            reference = root / "reference.md"

            self._write_dataset(dataset, 4)
            reference.write_text("reference claim", encoding="utf-8")

            code = self._run_rebuild(
                dataset_path=dataset,
                manifest_path=manifest,
                reference_path=reference,
                as_of_date="2026-02-24",
                owner="test-owner",
                declared_total_cases=10,
                inherit_declared_total_from_manifest=False,
            )
            self.assertEqual(code, 0)

            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["reference_claim"]["declared_total_cases"], 10)
            self.assertEqual(payload["reference_claim"]["declared_total_cases_source"], "cli_override")
            self.assertFalse(payload["integrity_checks"]["count_matches_reference_claim"])

    def test_legacy_mode_can_inherit_previous_declared_total_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            dataset = root / "gs_active_cases.json"
            manifest = root / "benchmark_manifest.json"
            reference = root / "reference.md"

            self._write_dataset(dataset, 5)
            reference.write_text("reference claim", encoding="utf-8")
            manifest.write_text(
                json.dumps({"reference_claim": {"declared_total_cases": 82}}),
                encoding="utf-8",
            )

            code = self._run_rebuild(
                dataset_path=dataset,
                manifest_path=manifest,
                reference_path=reference,
                as_of_date="2026-02-24",
                owner="test-owner",
                declared_total_cases=None,
                inherit_declared_total_from_manifest=True,
            )
            self.assertEqual(code, 0)

            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["reference_claim"]["declared_total_cases"], 82)
            self.assertEqual(payload["reference_claim"]["declared_total_cases_source"], "manifest_legacy")
            self.assertFalse(payload["integrity_checks"]["count_matches_reference_claim"])


if __name__ == "__main__":
    unittest.main()
