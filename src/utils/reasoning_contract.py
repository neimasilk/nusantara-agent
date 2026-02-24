"""Utilities to validate reasoning metadata contract in benchmark outputs."""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Mapping, Sequence


REQUIRED_REASONING_FIELDS = (
    "label",
    "langkah_keputusan",
    "alasan_utama",
    "konflik_terdeteksi",
)


def parse_reasoning_payload(raw_reasoning: Any) -> Dict[str, Any]:
    """Parse reasoning payload expected to be JSON-like text."""
    if isinstance(raw_reasoning, dict):
        return raw_reasoning
    if not isinstance(raw_reasoning, str):
        return {}

    text = raw_reasoning.strip()
    if not text:
        return {}

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            parsed = json.loads(text[start : end + 1])
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return {}
    return {}


def _is_present(value: Any) -> bool:
    if value is None:
        return False
    return bool(str(value).strip())


def summarize_reasoning_contract(
    results: Sequence[Mapping[str, Any]],
    required_fields: Iterable[str] = REQUIRED_REASONING_FIELDS,
) -> Dict[str, Any]:
    """Return quality summary for reasoning metadata fields."""
    required = tuple(required_fields)
    total = len(results)
    parseable_count = 0
    complete_count = 0
    per_field_present = {field: 0 for field in required}
    missing_field_counts = {field: 0 for field in required}
    incomplete_case_ids: List[str] = []

    for row in results:
        payload = parse_reasoning_payload(row.get("reasoning", ""))
        if payload:
            parseable_count += 1

        missing = []
        for field in required:
            if _is_present(payload.get(field)):
                per_field_present[field] += 1
            else:
                missing.append(field)
                missing_field_counts[field] += 1

        if not missing:
            complete_count += 1
        else:
            case_id = str(row.get("id", "")).strip()
            if case_id:
                incomplete_case_ids.append(case_id)

    complete_ratio = (complete_count / total) if total else 0.0
    parseable_ratio = (parseable_count / total) if total else 0.0
    all_required_present = total > 0 and complete_count == total

    return {
        "required_fields": list(required),
        "total_results": total,
        "parseable_count": parseable_count,
        "parseable_ratio": parseable_ratio,
        "complete_count": complete_count,
        "complete_ratio": complete_ratio,
        "per_field_present_count": per_field_present,
        "missing_field_counts": missing_field_counts,
        "all_required_present": all_required_present,
        "claimable_for_layer_diagnosis": all_required_present,
        "incomplete_case_ids": sorted(incomplete_case_ids),
    }

