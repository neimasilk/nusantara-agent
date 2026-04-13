"""Shared dataset split contract for benchmark runners.

This module enforces a single source of truth for dev/locked split usage
across experiment runners.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Literal, Sequence, Tuple


EvaluationMode = Literal["scientific_claimable", "operational_offline"]
DatasetSplitMode = Literal["full", "dev", "locked_test"]

DEFAULT_SPLIT_POLICY_PATH = Path("experiments/09_ablation_study/dataset_split.json")

_SPLIT_KEYS = {
    "dev": "dev_set",
    "locked_test": "locked_test_set",
}
_VALID_SPLIT_MODES = {"full", "dev", "locked_test"}


def _ensure_string_list(values: object, field_name: str) -> List[str]:
    if not isinstance(values, list):
        raise RuntimeError(f"Split policy invalid: '{field_name}' harus berupa list.")
    out: List[str] = []
    seen = set()
    for item in values:
        if not isinstance(item, str):
            raise RuntimeError(f"Split policy invalid: '{field_name}' harus berisi string.")
        value = item.strip()
        if not value:
            raise RuntimeError(f"Split policy invalid: '{field_name}' berisi ID kosong.")
        if value in seen:
            raise RuntimeError(f"Split policy invalid: duplicate ID '{value}' di '{field_name}'.")
        seen.add(value)
        out.append(value)
    return out


def resolve_dataset_split_mode(mode: EvaluationMode, requested_split: str) -> DatasetSplitMode:
    requested = str(requested_split or "").strip().lower()
    if requested:
        if requested not in _VALID_SPLIT_MODES:
            raise RuntimeError(
                f"dataset_split tidak valid: '{requested}'. Pilihan valid: full, dev, locked_test."
            )
        return requested  # type: ignore[return-value]

    # Default operasional: aman, hanya dev set.
    if mode == "operational_offline":
        return "dev"
    # Default scientific_claimable: backward compatible dengan benchmark canonical penuh.
    return "full"


def load_split_policy(path: Path) -> Dict[str, List[str]]:
    if not path.exists():
        raise FileNotFoundError(f"Split policy tidak ditemukan: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Gagal membaca split policy {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError(f"Split policy invalid: expected object, got {type(payload).__name__}")

    dev_ids = _ensure_string_list(payload.get("dev_set"), "dev_set")
    locked_ids = _ensure_string_list(payload.get("locked_test_set"), "locked_test_set")

    overlap = sorted(set(dev_ids) & set(locked_ids))
    if overlap:
        preview = ", ".join(overlap[:5])
        suffix = "" if len(overlap) <= 5 else f", +{len(overlap) - 5} lagi"
        raise RuntimeError(f"Split policy invalid: overlap dev_set vs locked_test_set ({preview}{suffix})")

    return {
        "dev_set": dev_ids,
        "locked_test_set": locked_ids,
    }


def apply_dataset_split(
    cases: Sequence[Dict],
    split_mode: DatasetSplitMode,
    split_policy_path: Path,
    *,
    strict: bool = True,
) -> Tuple[List[Dict], Dict[str, object]]:
    if split_mode == "full":
        return list(cases), {
            "dataset_split_mode": "full",
            "split_policy_path": str(split_policy_path),
            "requested_case_ids": None,
            "selected_cases": len(cases),
            "missing_case_ids": [],
        }

    policy = load_split_policy(split_policy_path)
    policy_key = _SPLIT_KEYS[split_mode]
    requested_ids = policy[policy_key]
    requested_set = set(requested_ids)

    selected: List[Dict] = []
    dataset_ids = set()
    duplicate_dataset_ids = set()
    for entry in cases:
        case_id = str(entry.get("id", "")).strip()
        if not case_id:
            continue
        if case_id in dataset_ids:
            duplicate_dataset_ids.add(case_id)
        dataset_ids.add(case_id)
        if case_id in requested_set:
            selected.append(entry)

    if duplicate_dataset_ids and strict:
        dup = sorted(duplicate_dataset_ids)
        preview = ", ".join(dup[:5])
        suffix = "" if len(dup) <= 5 else f", +{len(dup) - 5} lagi"
        raise RuntimeError(f"Dataset invalid: duplicate case id terdeteksi ({preview}{suffix})")

    missing_ids = sorted(requested_set - dataset_ids)
    if missing_ids and strict:
        preview = ", ".join(missing_ids[:5])
        suffix = "" if len(missing_ids) <= 5 else f", +{len(missing_ids) - 5} lagi"
        raise RuntimeError(
            f"Split policy mismatch: {len(missing_ids)} ID pada '{policy_key}' tidak ditemukan di dataset "
            f"({preview}{suffix})"
        )

    return selected, {
        "dataset_split_mode": split_mode,
        "split_policy_path": str(split_policy_path),
        "split_policy_key": policy_key,
        "requested_case_ids": len(requested_ids),
        "selected_cases": len(selected),
        "missing_case_ids": missing_ids,
    }
