import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple

from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ASP_PATH = ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_only_2026-02-19.json"
DEFAULT_LLM_PATH = ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_llm_2026-02-19.json"
LABELS = ("A", "B", "C", "D")


def _load_mode_results(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Result file tidak ditemukan: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("skipped"):
        raise RuntimeError(
            f"Mode pada {path} berstatus skipped: {data.get('skip_reason', 'unknown reason')}"
        )
    results = data.get("results")
    if not isinstance(results, list):
        raise RuntimeError(f"Field 'results' tidak valid pada {path}")
    return data


def _to_case_map(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        case_id = str(item.get("id", "")).strip()
        if not case_id:
            continue
        out[case_id] = item
    return out


def _align_case_ids(
    asp_map: Dict[str, Dict[str, Any]],
    llm_map: Dict[str, Dict[str, Any]],
) -> Tuple[List[str], List[str], List[str]]:
    asp_ids = set(asp_map.keys())
    llm_ids = set(llm_map.keys())
    common = sorted(asp_ids & llm_ids)
    asp_only = sorted(asp_ids - llm_ids)
    llm_only = sorted(llm_ids - asp_ids)
    return common, asp_only, llm_only


def _build_confusion_matrix(
    case_ids: List[str],
    case_map: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, int]]:
    matrix = {g: {p: 0 for p in LABELS} for g in LABELS}
    for case_id in case_ids:
        row = case_map[case_id]
        gold = str(row.get("gold", "")).upper().strip()
        pred = str(row.get("predicted", "")).upper().strip()
        if gold in LABELS and pred in LABELS:
            matrix[gold][pred] += 1
    return matrix


def _cohens_kappa(matrix: Dict[str, Dict[str, int]]) -> float:
    n = sum(matrix[g][p] for g in LABELS for p in LABELS)
    if n == 0:
        return 0.0

    po = sum(matrix[l][l] for l in LABELS) / n

    row_totals = {g: sum(matrix[g][p] for p in LABELS) for g in LABELS}
    col_totals = {p: sum(matrix[g][p] for g in LABELS) for p in LABELS}

    pe = sum((row_totals[l] / n) * (col_totals[l] / n) for l in LABELS)
    if pe >= 1.0:
        return 0.0
    return (po - pe) / (1.0 - pe)


def _per_label_f1(matrix: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, float]]:
    metrics: Dict[str, Dict[str, float]] = {}
    for label in LABELS:
        tp = matrix[label][label]
        fp = sum(matrix[g][label] for g in LABELS if g != label)
        fn = sum(matrix[label][p] for p in LABELS if p != label)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        metrics[label] = {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": sum(matrix[label][p] for p in LABELS),
        }
    return metrics


def _accuracy_from_matrix(matrix: Dict[str, Dict[str, int]]) -> float:
    n = sum(matrix[g][p] for g in LABELS for p in LABELS)
    if n == 0:
        return 0.0
    correct = sum(matrix[l][l] for l in LABELS)
    return correct / n


def _mcnemar_stats(
    case_ids: List[str],
    asp_map: Dict[str, Dict[str, Any]],
    llm_map: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    both_correct = 0
    asp_only_correct = 0
    llm_only_correct = 0
    both_wrong = 0

    for case_id in case_ids:
        asp_ok = bool(asp_map[case_id].get("match"))
        llm_ok = bool(llm_map[case_id].get("match"))
        if asp_ok and llm_ok:
            both_correct += 1
        elif asp_ok and (not llm_ok):
            asp_only_correct += 1
        elif (not asp_ok) and llm_ok:
            llm_only_correct += 1
        else:
            both_wrong += 1

    b = asp_only_correct
    c = llm_only_correct
    discordant = b + c

    if discordant == 0:
        exact_p = 1.0
        chi2_value = 0.0
        chi2_cc_value = 0.0
        chi2_p = 1.0
        chi2_cc_p = 1.0
    else:
        exact_p = float(stats.binomtest(k=b, n=discordant, p=0.5, alternative="two-sided").pvalue)
        chi2_value = ((b - c) ** 2) / discordant
        chi2_cc_value = ((abs(b - c) - 1) ** 2) / discordant
        chi2_p = float(stats.chi2.sf(chi2_value, df=1))
        chi2_cc_p = float(stats.chi2.sf(chi2_cc_value, df=1))

    return {
        "table_2x2": {
            "asp_correct_llm_correct": both_correct,
            "asp_correct_llm_wrong": asp_only_correct,
            "asp_wrong_llm_correct": llm_only_correct,
            "asp_wrong_llm_wrong": both_wrong,
        },
        "discordant_pairs": discordant,
        "asp_only_better_count": asp_only_correct,
        "asp_llm_better_count": llm_only_correct,
        "exact_binomial_pvalue": exact_p,
        "chi_square": chi2_value,
        "chi_square_pvalue": chi2_p,
        "chi_square_continuity_corrected": chi2_cc_value,
        "chi_square_continuity_corrected_pvalue": chi2_cc_p,
    }


def _matrix_table(matrix: Dict[str, Dict[str, int]]) -> str:
    headers = ["Gold\\Pred", *LABELS]
    rows = [[g, *(str(matrix[g][p]) for p in LABELS)] for g in LABELS]

    all_rows = [headers] + rows
    widths = [max(len(row[i]) for row in all_rows) for i in range(len(headers))]

    def fmt(row: List[str]) -> str:
        return " | ".join(row[i].ljust(widths[i]) for i in range(len(row)))

    sep = "-+-".join("-" * w for w in widths)
    lines = [fmt(headers), sep]
    lines.extend(fmt(r) for r in rows)
    return "\n".join(lines)


def _f1_table(metrics: Dict[str, Dict[str, float]]) -> str:
    headers = ["Label", "Precision", "Recall", "F1", "Support"]
    rows: List[List[str]] = []
    for label in LABELS:
        item = metrics[label]
        rows.append(
            [
                label,
                f"{item['precision']:.3f}",
                f"{item['recall']:.3f}",
                f"{item['f1']:.3f}",
                str(int(item["support"])),
            ]
        )

    all_rows = [headers] + rows
    widths = [max(len(row[i]) for row in all_rows) for i in range(len(headers))]

    def fmt(row: List[str]) -> str:
        return " | ".join(row[i].ljust(widths[i]) for i in range(len(row)))

    sep = "-+-".join("-" * w for w in widths)
    lines = [fmt(headers), sep]
    lines.extend(fmt(r) for r in rows)
    return "\n".join(lines)


def _print_report(report: Dict[str, Any]) -> None:
    print("=== Statistical Comparison: ASP-only vs ASP+LLM ===")
    print(f"Common matched cases: {report['n_common_cases']}")
    print("")

    mc = report["mcnemar"]
    t = mc["table_2x2"]
    print("McNemar 2x2 (correctness):")
    print("ASP\\LLM | Correct | Wrong")
    print("--------+---------+------")
    print(f"Correct | {t['asp_correct_llm_correct']:<7} | {t['asp_correct_llm_wrong']}")
    print(f"Wrong   | {t['asp_wrong_llm_correct']:<7} | {t['asp_wrong_llm_wrong']}")
    print(
        "Exact binomial p-value: "
        f"{mc['exact_binomial_pvalue']:.6f} "
        f"(discordant={mc['discordant_pairs']}, asp_only_better={mc['asp_only_better_count']}, "
        f"asp_llm_better={mc['asp_llm_better_count']})"
    )
    print(
        "Chi-square p-value: "
        f"{mc['chi_square_pvalue']:.6f} "
        f"(cc p-value={mc['chi_square_continuity_corrected_pvalue']:.6f})"
    )
    print("")

    for mode_key in ("asp_only", "asp_llm"):
        mode = report["modes"][mode_key]
        print(f"[{mode_key}] accuracy={mode['accuracy']:.3f} kappa={mode['cohens_kappa']:.3f}")
        print("Confusion Matrix (rows=gold, cols=pred):")
        print(_matrix_table(mode["confusion_matrix"]))
        print("Per-label F1:")
        print(_f1_table(mode["per_label_metrics"]))
        print("")


def main() -> int:
    asp_data = _load_mode_results(DEFAULT_ASP_PATH)
    llm_data = _load_mode_results(DEFAULT_LLM_PATH)

    asp_map = _to_case_map(asp_data["results"])
    llm_map = _to_case_map(llm_data["results"])
    common_ids, asp_only_ids, llm_only_ids = _align_case_ids(asp_map, llm_map)

    if not common_ids:
        raise RuntimeError("Tidak ada case ID overlap antara hasil ASP-only dan ASP+LLM.")

    asp_matrix = _build_confusion_matrix(common_ids, asp_map)
    llm_matrix = _build_confusion_matrix(common_ids, llm_map)

    asp_per_label = _per_label_f1(asp_matrix)
    llm_per_label = _per_label_f1(llm_matrix)

    date_tag = str(llm_data.get("date") or asp_data.get("date") or date.today().isoformat())
    out_path = ROOT / "experiments" / "09_ablation_study" / f"statistical_comparison_{date_tag}.json"

    report: Dict[str, Any] = {
        "date": date_tag,
        "inputs": {
            "asp_only": str(DEFAULT_ASP_PATH.resolve()),
            "asp_llm": str(DEFAULT_LLM_PATH.resolve()),
        },
        "n_common_cases": len(common_ids),
        "case_id_alignment": {
            "asp_only_not_in_llm": asp_only_ids,
            "asp_llm_not_in_asp_only": llm_only_ids,
        },
        "mcnemar": _mcnemar_stats(common_ids, asp_map, llm_map),
        "modes": {
            "asp_only": {
                "accuracy": _accuracy_from_matrix(asp_matrix),
                "cohens_kappa": _cohens_kappa(asp_matrix),
                "confusion_matrix": asp_matrix,
                "per_label_metrics": asp_per_label,
            },
            "asp_llm": {
                "accuracy": _accuracy_from_matrix(llm_matrix),
                "cohens_kappa": _cohens_kappa(llm_matrix),
                "confusion_matrix": llm_matrix,
                "per_label_metrics": llm_per_label,
            },
        },
    }

    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    _print_report(report)
    print(f"[OK] Saved: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
