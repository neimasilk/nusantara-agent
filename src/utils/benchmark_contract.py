from typing import Dict, Iterable, Optional, Set


# Label yang tidak boleh dipakai untuk evaluasi akurasi final.
UNRESOLVED_GOLD_LABELS: Set[str] = {
    "SPLIT",
    "DISPUTED",
    "AMBIGUOUS",
}


def normalize_gold_label(label: object) -> str:
    return str(label or "").upper().strip()


def is_evaluable_gold_label(label: object) -> bool:
    return normalize_gold_label(label) not in UNRESOLVED_GOLD_LABELS


def count_evaluable_cases(cases: Iterable[Dict]) -> int:
    return sum(1 for item in cases if is_evaluable_gold_label(item.get("gold_label", "")))


def resolve_manifest_evaluable_count(benchmark_meta: Dict) -> Optional[int]:
    """Ambil jumlah evaluable dari manifest dengan backward compatibility."""
    if not isinstance(benchmark_meta, dict):
        return None

    for key in ("evaluable_cases_excluding_disputed", "evaluable_cases_excluding_split"):
        value = benchmark_meta.get(key)
        if value is not None:
            try:
                return int(value)
            except (TypeError, ValueError):
                return None
    return None
