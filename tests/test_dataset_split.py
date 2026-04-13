import json
import tempfile
import unittest
from pathlib import Path

from src.utils.dataset_split import (
    apply_dataset_split,
    load_split_policy,
    resolve_dataset_split_mode,
)


class DatasetSplitTests(unittest.TestCase):
    def test_resolve_split_default_operational(self) -> None:
        self.assertEqual(resolve_dataset_split_mode("operational_offline", ""), "dev")

    def test_resolve_split_default_scientific(self) -> None:
        self.assertEqual(resolve_dataset_split_mode("scientific_claimable", ""), "full")

    def test_resolve_split_explicit_override(self) -> None:
        self.assertEqual(resolve_dataset_split_mode("operational_offline", "locked_test"), "locked_test")

    def test_load_policy_rejects_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "dataset_split.json"
            path.write_text(
                json.dumps(
                    {
                        "dev_set": ["GS-0001", "GS-0002"],
                        "locked_test_set": ["GS-0002"],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(RuntimeError):
                load_split_policy(path)

    def test_apply_split_dev_filters_cases(self) -> None:
        cases = [
            {"id": "GS-0001", "gold_label": "A"},
            {"id": "GS-0002", "gold_label": "B"},
            {"id": "GS-0003", "gold_label": "C"},
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "dataset_split.json"
            path.write_text(
                json.dumps(
                    {
                        "dev_set": ["GS-0001", "GS-0003"],
                        "locked_test_set": ["GS-0002"],
                    }
                ),
                encoding="utf-8",
            )
            selected, meta = apply_dataset_split(cases, "dev", path, strict=True)

        self.assertEqual([item["id"] for item in selected], ["GS-0001", "GS-0003"])
        self.assertEqual(meta["dataset_split_mode"], "dev")
        self.assertEqual(meta["requested_case_ids"], 2)
        self.assertEqual(meta["selected_cases"], 2)
        self.assertEqual(meta["missing_case_ids"], [])

    def test_apply_split_raises_when_policy_id_missing(self) -> None:
        cases = [{"id": "GS-0001", "gold_label": "A"}]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "dataset_split.json"
            path.write_text(
                json.dumps(
                    {
                        "dev_set": ["GS-0001", "GS-0999"],
                        "locked_test_set": [],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(RuntimeError):
                apply_dataset_split(cases, "dev", path, strict=True)


if __name__ == "__main__":
    unittest.main()
