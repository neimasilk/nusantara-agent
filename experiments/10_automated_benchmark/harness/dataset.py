"""Load the 70-case benchmark (49 dev + 21 test) for Phase 1."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEV_FILE = ROOT / "experiments" / "09_ablation_study" / "benchmark_dev_seed42.json"
TEST_FILE = ROOT / "experiments" / "10_automated_benchmark" / "data" / "benchmark_test_recovered.json"


def load_dev() -> list[dict]:
    return json.loads(DEV_FILE.read_text(encoding="utf-8"))


def load_test() -> list[dict]:
    return json.loads(TEST_FILE.read_text(encoding="utf-8"))


def load_all() -> list[dict]:
    """Combined 70-case set. Each case has id, query, gold_label."""
    dev = [_normalize(c) for c in load_dev()]
    test = [_normalize(c) for c in load_test()]
    return dev + test


def _normalize(case: dict) -> dict:
    return {
        "id": case["id"],
        "query": case.get("query", ""),
        "gold_label": case.get("gold_label", ""),
        "split": "dev" if "expert_votes" in case else "test",
    }
