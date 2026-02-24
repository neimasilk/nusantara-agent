"""Domain-specific failure audit for Jawa cases.

This script produces a reproducible JSON artifact for strategic review:
- Per-backend Jawa accuracy and confusion
- Layer-oriented failure diagnosis using reasoning metadata
- Cross-backend overlap for recurrent transitions (especially B->A)
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Sequence

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_DOMAIN_MAP = ROOT / "experiments" / "09_ablation_study" / "case_id_domain_map.json"

DEFAULT_BACKENDS = {
    "canonical_asp_only": ROOT / "experiments" / "09_ablation_study" / "results_fixed_asp_only_2026-02-20.json",
    "canonical_ollama_deepseek_r1": ROOT / "experiments" / "09_ablation_study" / "results_wordboundary_ollama_2026-02-20.json",
    "canonical_deepseek_api": ROOT / "experiments" / "09_ablation_study" / "results_deepseek_rollback_2026-02-20.json",
    "exploratory_asp_only": ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_only_2026-02-23.json",
    "exploratory_gpt_oss_20b": ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_llm_gpt_oss_20b_2026-02-23.json",
    "exploratory_qwen3_14b": ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_llm_qwen3_14b_2026-02-23.json",
}

OPEN_SOURCE_LOCAL_GROUP = [
    "canonical_ollama_deepseek_r1",
    "exploratory_gpt_oss_20b",
    "exploratory_qwen3_14b",
]


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _normalize_conflict_signal(value) -> str:
    text = str(value or "").strip().lower()
    if text in {"ya", "yes", "true", "1"}:
        return "yes"
    if text in {"tidak", "no", "false", "0"}:
        return "no"
    return "unknown"


def parse_reasoning_payload(raw_reasoning) -> Mapping[str, str]:
    """Parse reasoning field that is expected to contain a JSON object."""
    if isinstance(raw_reasoning, dict):
        return raw_reasoning
    if not isinstance(raw_reasoning, str):
        return {}

    raw_reasoning = raw_reasoning.strip()
    if not raw_reasoning:
        return {}

    try:
        data = json.loads(raw_reasoning)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        pass

    start = raw_reasoning.find("{")
    end = raw_reasoning.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            data = json.loads(raw_reasoning[start : end + 1])
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def classify_layer(gold: str, predicted: str, conflict_signal: str, decision_step: str) -> str:
    """Heuristic classification for root-cause layer."""
    if gold == predicted:
        return "correct"

    if gold == "C":
        if conflict_signal == "no":
            return "router_or_fact_extraction"
        if conflict_signal == "yes":
            return "adjudication_collapse_after_conflict"
        return "c_error_unknown_signal"

    if gold == "B" and predicted == "A":
        if decision_step in {"1", "2"}:
            return "national_dominance_bias"
        if conflict_signal == "yes":
            return "overconflict_then_national"
        return "national_dominance_bias"

    if gold == "B" and predicted == "C":
        return "over_conflict_trigger"

    if gold == "D":
        return "no_abstention_path"

    return "other"


def _extract_jawa_case_ids(domain_map: Mapping[str, str]) -> List[str]:
    jawa_ids = [case_id for case_id, domain in domain_map.items() if str(domain).strip().lower() == "jawa"]
    return sorted(jawa_ids)


def _build_transition(case: Mapping[str, str]) -> str:
    return f"{case.get('gold', '?')}->{case.get('predicted', '?')}"


def analyze_backend(result_path: Path, jawa_case_ids: Sequence[str]) -> Mapping[str, object]:
    if not result_path.exists():
        raise FileNotFoundError(f"Result file not found: {result_path}")

    payload = _load_json(result_path)
    results = payload.get("results", [])
    if not isinstance(results, list):
        raise ValueError(f"Invalid results format in {result_path}")

    jawa_set = set(jawa_case_ids)
    selected = [item for item in results if item.get("id") in jawa_set]
    found_ids = {item.get("id") for item in selected}
    missing_ids = sorted(jawa_set - found_ids)

    correct = 0
    confusion_counts: MutableMapping[str, int] = Counter()
    support_counts: MutableMapping[str, int] = Counter()
    transition_case_ids: MutableMapping[str, List[str]] = defaultdict(list)
    error_layer_counts: MutableMapping[str, int] = Counter()
    error_cases: List[Mapping[str, str]] = []

    for item in selected:
        case_id = str(item.get("id", ""))
        gold = str(item.get("gold", "")).strip()
        pred = str(item.get("predicted", "")).strip()
        match = bool(item.get("match", pred == gold))
        if match:
            correct += 1

        support_counts[gold] += 1
        transition = f"{gold}->{pred}"
        confusion_counts[transition] += 1
        transition_case_ids[transition].append(case_id)

        reasoning_payload = parse_reasoning_payload(item.get("reasoning"))
        conflict_signal = _normalize_conflict_signal(reasoning_payload.get("konflik_terdeteksi"))
        decision_step = str(reasoning_payload.get("langkah_keputusan", "")).strip()
        diagnosis = classify_layer(gold, pred, conflict_signal, decision_step)
        error_layer_counts[diagnosis] += 1

        if not match:
            error_cases.append(
                {
                    "id": case_id,
                    "gold": gold,
                    "predicted": pred,
                    "transition": transition,
                    "conflict_signal": conflict_signal,
                    "decision_step": decision_step or "unknown",
                    "diagnosis": diagnosis,
                }
            )

    total = len(selected)
    accuracy = (correct / total) if total else 0.0
    error_cases.sort(key=lambda item: (item["transition"], item["id"]))
    sorted_transitions = {key: sorted(value) for key, value in sorted(transition_case_ids.items())}

    return {
        "file": str(result_path),
        "total_jawa_cases_in_run": total,
        "missing_jawa_case_ids": missing_ids,
        "correct": correct,
        "accuracy": round(accuracy, 4),
        "label_support": dict(sorted(support_counts.items())),
        "confusion_counts": dict(sorted(confusion_counts.items())),
        "transition_case_ids": sorted_transitions,
        "error_layer_counts": dict(sorted(error_layer_counts.items())),
        "error_cases": error_cases,
    }


def _intersection_from_transitions(
    backend_metrics: Mapping[str, Mapping[str, object]], backend_names: Iterable[str], transition: str
) -> List[str]:
    sets = []
    for backend_name in backend_names:
        data = backend_metrics.get(backend_name)
        if not data:
            continue
        case_ids = set(data.get("transition_case_ids", {}).get(transition, []))
        sets.append(case_ids)
    if not sets:
        return []
    return sorted(set.intersection(*sets))


def _build_recommendations(backend_metrics: Mapping[str, Mapping[str, object]]) -> List[str]:
    recommendations: List[str] = []

    qwen = backend_metrics.get("exploratory_qwen3_14b", {})
    qwen_b_to_a = int(qwen.get("confusion_counts", {}).get("B->A", 0))
    if qwen_b_to_a >= 4:
        recommendations.append(
            "Tambahkan guard prompt anti B->A untuk domain Jawa: jika konteks adat bilateral kuat dan tidak ada conflict signal eksplisit, larang label A."
        )

    deepseek_r1 = backend_metrics.get("canonical_ollama_deepseek_r1", {})
    deepseek_api = backend_metrics.get("canonical_deepseek_api", {})
    if float(deepseek_api.get("accuracy", 0.0)) - float(deepseek_r1.get("accuracy", 0.0)) >= 0.2:
        recommendations.append(
            "Prioritaskan kalibrasi backend lokal (deepseek-r1/Qwen3) sebelum menambah aturan ASP baru; gap besar terhadap API menunjukkan isu kalibrasi adjudikator."
        )

    router_signals = 0
    adjudication_signals = 0
    for stats in backend_metrics.values():
        layers = stats.get("error_layer_counts", {})
        router_signals += int(layers.get("router_or_fact_extraction", 0))
        adjudication_signals += int(layers.get("adjudication_collapse_after_conflict", 0))
    if router_signals >= adjudication_signals:
        recommendations.append(
            "Untuk error C-domain Jawa, uji dulu perbaikan router/fact extraction (keyword-to-fact mapping) sebelum eksperimen prompt kompleks."
        )
    else:
        recommendations.append(
            "Untuk error C-domain Jawa, fokuskan iterasi pertama pada prompt adjudikator yang menjaga label C saat conflict signal sudah ada."
        )

    recommendations.append(
        "Bekukan tiga test regresi wajib Jawa: (1) B->A shared failures, (2) C dengan conflict signal harus tetap C, (3) kasus D tidak boleh dipaksa jadi A/B/C."
    )
    return recommendations


def build_audit_report(
    domain_map_path: Path, backend_paths: Mapping[str, Path], output_json: Path
) -> Mapping[str, object]:
    domain_map = _load_json(domain_map_path)
    if not isinstance(domain_map, dict):
        raise ValueError("case_id_domain_map.json must contain a JSON object")

    jawa_case_ids = _extract_jawa_case_ids(domain_map)
    if not jawa_case_ids:
        raise ValueError("No Jawa cases detected in domain map")

    backend_metrics = {}
    for backend_name, path in backend_paths.items():
        backend_metrics[backend_name] = analyze_backend(path, jawa_case_ids)

    overlap = {
        "b_to_a_all_local_open_source": _intersection_from_transitions(
            backend_metrics, OPEN_SOURCE_LOCAL_GROUP, "B->A"
        ),
        "b_to_a_all_canonical": _intersection_from_transitions(
            backend_metrics,
            ["canonical_asp_only", "canonical_ollama_deepseek_r1", "canonical_deepseek_api"],
            "B->A",
        ),
    }

    accuracy_board = {
        name: metrics.get("accuracy", 0.0) for name, metrics in backend_metrics.items()
    }
    best_backend = max(accuracy_board, key=accuracy_board.get)
    worst_backend = min(accuracy_board, key=accuracy_board.get)

    report = {
        "date": date.today().isoformat(),
        "domain": "Jawa",
        "jawa_case_ids": jawa_case_ids,
        "jawa_case_count": len(jawa_case_ids),
        "backend_files": {name: str(path) for name, path in backend_paths.items()},
        "backend_metrics": backend_metrics,
        "cross_backend_overlap": overlap,
        "summary": {
            "best_backend": best_backend,
            "best_accuracy": accuracy_board[best_backend],
            "worst_backend": worst_backend,
            "worst_accuracy": accuracy_board[worst_backend],
        },
        "recommendations": _build_recommendations(backend_metrics),
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit domain Jawa failures across benchmark backends.")
    parser.add_argument(
        "--domain-map",
        type=Path,
        default=DEFAULT_DOMAIN_MAP,
        help="Path to case_id_domain_map.json",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=ROOT / "experiments" / "09_ablation_study" / "jawa_failure_audit_2026-02-24.json",
        help="Output JSON path",
    )
    args = parser.parse_args()

    report = build_audit_report(args.domain_map, DEFAULT_BACKENDS, args.output_json)
    summary = report["summary"]
    print("[OK] Jawa failure audit generated")
    print(f"  Output: {args.output_json}")
    print(
        "  Best/Worst accuracy: "
        f"{summary['best_backend']}={summary['best_accuracy']:.3f}, "
        f"{summary['worst_backend']}={summary['worst_accuracy']:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
