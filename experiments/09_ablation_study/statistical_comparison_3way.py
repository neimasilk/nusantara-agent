"""3-Way Statistical Comparison: ASP-only vs ASP+Ollama vs ASP+DeepSeek

Output untuk paper: McNemar, Cohen's Kappa, Confusion Matrix, Fleiss' Kappa,
Cross-model agreement, Majority Vote analysis.
"""

import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple, Set
from collections import Counter

from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATHS = {
    "asp_only": ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_only_2026-02-19.json",
    "ollama": ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_llm_2026-02-19.json",
    "deepseek": ROOT / "experiments" / "09_ablation_study" / "results_deepseek_asp_llm_2026-02-19.json",
}
LABELS = ("A", "B", "C", "D")


def _load_mode_results(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Result file tidak ditemukan: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("skipped"):
        raise RuntimeError(f"Mode pada {path} berstatus skipped: {data.get('skip_reason', 'unknown')}")
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


def _align_case_ids(*maps: Dict[str, Dict[str, Any]]) -> List[str]:
    """Find common case IDs across all maps."""
    if not maps:
        return []
    sets = [set(m.keys()) for m in maps]
    common = sets[0]
    for s in sets[1:]:
        common &= s
    return sorted(common)


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
    """Cohen's Kappa: agreement between system and gold standard."""
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


def _fleiss_kappa(predictions: List[List[str]]) -> float:
    """
    Fleiss' Kappa for agreement among N raters (here 3 systems).
    predictions: list of N lists, each containing predictions for M items.
    """
    if not predictions or len(predictions) < 2:
        return 0.0

    n_items = len(predictions[0])
    n_raters = len(predictions)

    if n_items == 0:
        return 0.0

    # For each item, count how many raters chose each category
    P_hat = 0.0
    for i in range(n_items):
        counts = Counter(p[i] for p in predictions if i < len(p))
        # Proportion of agreeing pairs for this item
        n_ij_sum = sum(c ** 2 for c in counts.values())
        P_i = (n_ij_sum - n_raters) / (n_raters * (n_raters - 1)) if n_raters > 1 else 0
        P_hat += P_i
    P_hat /= n_items

    # Expected agreement by chance
    p_j = {}
    for label in LABELS:
        total = sum(1 for p in predictions for pred in p if pred == label)
        p_j[label] = total / (n_items * n_raters)

    Pe = sum(pj ** 2 for pj in p_j.values())

    if Pe >= 1.0:
        return 0.0
    return (P_hat - Pe) / (1.0 - Pe)


def _mcnemar_stats(
    case_ids: List[str],
    map1: Dict[str, Dict[str, Any]],
    map2: Dict[str, Dict[str, Any]],
    name1: str = "System1",
    name2: str = "System2",
) -> Dict[str, Any]:
    """McNemar test between two systems."""
    both_correct = 0
    s1_only_correct = 0
    s2_only_correct = 0
    both_wrong = 0

    for case_id in case_ids:
        s1_ok = bool(map1[case_id].get("match"))
        s2_ok = bool(map2[case_id].get("match"))
        if s1_ok and s2_ok:
            both_correct += 1
        elif s1_ok and (not s2_ok):
            s1_only_correct += 1
        elif (not s1_ok) and s2_ok:
            s2_only_correct += 1
        else:
            both_wrong += 1

    b = s1_only_correct
    c = s2_only_correct
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
        "comparison": f"{name1}_vs_{name2}",
        "table_2x2": {
            f"{name1}_correct_{name2}_correct": both_correct,
            f"{name1}_correct_{name2}_wrong": s1_only_correct,
            f"{name1}_wrong_{name2}_correct": s2_only_correct,
            f"{name1}_wrong_{name2}_wrong": both_wrong,
        },
        "discordant_pairs": discordant,
        f"{name1}_only_better_count": s1_only_correct,
        f"{name2}_only_better_count": s2_only_correct,
        "exact_binomial_pvalue": exact_p,
        "chi_square": chi2_value,
        "chi_square_pvalue": chi2_p,
        "chi_square_continuity_corrected": chi2_cc_value,
        "chi_square_continuity_corrected_pvalue": chi2_cc_p,
    }


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


def _cross_model_agreement(
    case_ids: List[str],
    maps: Dict[str, Dict[str, Dict[str, Any]]],
) -> Dict[str, Any]:
    """
    Analyze agreement patterns among 3 systems.
    Returns: all_agree, two_agree, all_disagree counts and case lists.
    """
    all_agree_correct = 0
    all_agree_wrong = 0
    two_agree_correct = 0  # 2 agree and match gold
    two_agree_wrong = 0    # 2 agree but wrong
    all_disagree = 0

    all_agree_correct_cases = []
    all_agree_wrong_cases = []
    two_agree_cases = []
    all_disagree_cases = []

    majority_correct = 0
    majority_total = 0

    for case_id in case_ids:
        preds = {name: str(m[case_id].get("predicted", "")).upper() for name, m in maps.items()}
        gold = str(list(maps.values())[0][case_id].get("gold", "")).upper()

        pred_values = list(preds.values())
        pred_counts = Counter(pred_values)
        most_common = pred_counts.most_common()

        # Check agreement pattern
        if len(pred_counts) == 1:
            # All 3 agree
            if preds[list(preds.keys())[0]] == gold:
                all_agree_correct += 1
                all_agree_correct_cases.append(case_id)
            else:
                all_agree_wrong += 1
                all_agree_wrong_cases.append(case_id)
        elif len(pred_counts) == 2 and most_common[0][1] == 2:
            # Exactly 2 agree, 1 different
            majority_pred = most_common[0][0]
            minority_pred = most_common[1][0]
            minority_system = [k for k, v in preds.items() if v == minority_pred][0]

            if majority_pred == gold:
                two_agree_correct += 1
            else:
                two_agree_wrong += 1

            two_agree_cases.append({
                "case_id": case_id,
                "gold": gold,
                "predictions": preds,
                "majority": majority_pred,
                "minority_system": minority_system,
                "minority_pred": minority_pred,
                "majority_correct": majority_pred == gold,
            })

            # Majority vote accuracy calculation
            majority_total += 1
            if majority_pred == gold:
                majority_correct += 1
        else:
            # All 3 different or other pattern
            all_disagree += 1
            all_disagree_cases.append({
                "case_id": case_id,
                "gold": gold,
                "predictions": preds,
            })

    return {
        "all_agree": {
            "correct": all_agree_correct,
            "wrong": all_agree_wrong,
            "total": all_agree_correct + all_agree_wrong,
            "correct_cases": all_agree_correct_cases,
            "wrong_cases": all_agree_wrong_cases,
        },
        "two_agree": {
            "correct": two_agree_correct,
            "wrong": two_agree_wrong,
            "total": two_agree_correct + two_agree_wrong,
            "cases": two_agree_cases,
        },
        "all_disagree": {
            "total": all_disagree,
            "cases": all_disagree_cases,
        },
        "majority_vote": {
            "applicable": majority_total,
            "correct": majority_correct,
            "accuracy": majority_correct / majority_total if majority_total > 0 else 0.0,
        },
    }


def _matrix_table(matrix: Dict[str, Dict[str, int]]) -> str:
    headers = ["G\\P", *LABELS]
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
        rows.append([
            label,
            f"{item['precision']:.3f}",
            f"{item['recall']:.3f}",
            f"{item['f1']:.3f}",
            str(int(item["support"])),
        ])

    all_rows = [headers] + rows
    widths = [max(len(row[i]) for row in all_rows) for i in range(len(headers))]

    def fmt(row: List[str]) -> str:
        return " | ".join(row[i].ljust(widths[i]) for i in range(len(row)))

    sep = "-+-".join("-" * w for w in widths)
    lines = [fmt(headers), sep]
    lines.extend(fmt(r) for r in rows)
    return "\n".join(lines)


def _print_report(report: Dict[str, Any]) -> None:
    print("=" * 70)
    print("3-WAY STATISTICAL COMPARISON: ASP-only vs Ollama vs DeepSeek")
    print("=" * 70)
    print(f"Common matched cases: {report['n_common_cases']}")
    print(f"Date: {report['date']}")
    print()

    # McNemar tests
    print("-" * 70)
    print("McNEMAR TESTS (Pairwise)")
    print("-" * 70)
    print(f"{'Comparison':<25} {'p-value':<12} {'Discordant':<12} {'Winner':<15}")
    print("-" * 70)
    for mc in report["mcnemar_tests"]:
        name = mc["comparison"]
        pval = mc["exact_binomial_pvalue"]
        disc = mc["discordant_pairs"]
        # Determine winner
        parts = name.split("_vs_")
        if len(parts) == 2:
            s1, s2 = parts
            s1_better = mc.get(f"{s1}_only_better_count", 0)
            s2_better = mc.get(f"{s2}_only_better_count", 0)
            if s1_better > s2_better:
                winner = f"{s1} (+{s1_better - s2_better})"
            elif s2_better > s1_better:
                winner = f"{s2} (+{s2_better - s1_better})"
            else:
                winner = "Tie"
        else:
            winner = "-"
        sig = "*" if pval < 0.05 else ""
        print(f"{name:<25} {pval:.6f}{sig:<5} {disc:<12} {winner}")
    print()

    # Cohen's Kappa
    print("-" * 70)
    print("COHEN'S KAPPA (System vs Gold)")
    print("-" * 70)
    print(f"{'Mode':<20} {'Accuracy':<12} {'Kappa':<12} {'Agreement'}")
    print("-" * 70)
    for mode_key, mode_data in report["modes"].items():
        acc = mode_data["accuracy"]
        kappa = mode_data["cohens_kappa"]
        # Interpretation
        if kappa >= 0.8:
            level = "Almost perfect"
        elif kappa >= 0.6:
            level = "Substantial"
        elif kappa >= 0.4:
            level = "Moderate"
        elif kappa >= 0.2:
            level = "Fair"
        else:
            level = "Slight"
        print(f"{mode_key:<20} {acc:.3f}       {kappa:.3f}       {level}")
    print()

    # Fleiss' Kappa
    print("-" * 70)
    print("FLEISS' KAPPA (Inter-rater agreement among 3 systems)")
    print("-" * 70)
    fk = report["fleiss_kappa"]
    print(f"Fleiss' Kappa: {fk:.3f}")
    if fk >= 0.8:
        interp = "Almost perfect agreement"
    elif fk >= 0.6:
        interp = "Substantial agreement"
    elif fk >= 0.4:
        interp = "Moderate agreement"
    elif fk >= 0.2:
        interp = "Fair agreement"
    else:
        interp = "Slight agreement"
    print(f"Interpretation: {interp}")
    print()

    # Cross-model agreement
    print("-" * 70)
    print("CROSS-MODEL AGREEMENT")
    print("-" * 70)
    cm = report["cross_model_agreement"]
    all_agree = cm["all_agree"]
    two_agree = cm["two_agree"]
    all_disagree = cm["all_disagree"]
    mv = cm["majority_vote"]

    print(f"All 3 agree (correct):     {all_agree['correct']:3d} cases")
    print(f"All 3 agree (wrong):       {all_agree['wrong']:3d} cases")
    print(f"All 3 agree (total):       {all_agree['total']:3d} cases ({100*all_agree['total']/report['n_common_cases']:.1f}%)")
    print()
    print(f"2 agree, 1 different:      {two_agree['total']:3d} cases ({100*two_agree['total']/report['n_common_cases']:.1f}%)")
    print(f"  - Majority correct:      {two_agree['correct']:3d}")
    print(f"  - Majority wrong:        {two_agree['wrong']:3d}")
    print()
    print(f"All 3 different:           {all_disagree['total']:3d} cases ({100*all_disagree['total']/report['n_common_cases']:.1f}%)")
    print()
    print(f"MAJORITY VOTE ACCURACY:    {mv['accuracy']:.1%} ({mv['correct']}/{mv['applicable']} cases where 2 agree)")
    print()

    # Confusion matrices
    print("-" * 70)
    print("CONFUSION MATRICES (rows=gold, cols=pred)")
    print("-" * 70)
    for mode_key, mode_data in report["modes"].items():
        print(f"\n[{mode_key}] Accuracy: {mode_data['accuracy']:.3f}")
        print(_matrix_table(mode_data["confusion_matrix"]))
        print("Per-label F1:")
        print(_f1_table(mode_data["per_label_metrics"]))


def main() -> int:
    # Load all three results
    data = {}
    maps = {}
    for name, path in DEFAULT_PATHS.items():
        data[name] = _load_mode_results(path)
        maps[name] = _to_case_map(data[name]["results"])

    # Find common case IDs
    common_ids = _align_case_ids(*maps.values())
    if not common_ids:
        raise RuntimeError("Tidak ada case ID overlap antara ketiga mode.")

    print(f"[INFO] Common cases across all 3 modes: {len(common_ids)}")

    # Build confusion matrices and metrics for each mode
    matrices = {}
    per_label_metrics = {}
    accuracies = {}
    kappas = {}

    for name, case_map in maps.items():
        matrices[name] = _build_confusion_matrix(common_ids, case_map)
        per_label_metrics[name] = _per_label_f1(matrices[name])
        accuracies[name] = _accuracy_from_matrix(matrices[name])
        kappas[name] = _cohens_kappa(matrices[name])

    # McNemar tests for all 3 pairs
    mcnemar_tests = [
        _mcnemar_stats(common_ids, maps["asp_only"], maps["ollama"], "asp_only", "ollama"),
        _mcnemar_stats(common_ids, maps["asp_only"], maps["deepseek"], "asp_only", "deepseek"),
        _mcnemar_stats(common_ids, maps["ollama"], maps["deepseek"], "ollama", "deepseek"),
    ]

    # Fleiss' Kappa (inter-rater agreement)
    predictions = [
        [str(maps[name][cid].get("predicted", "")).upper() for cid in common_ids]
        for name in ["asp_only", "ollama", "deepseek"]
    ]
    fleiss_k = _fleiss_kappa(predictions)

    # Cross-model agreement analysis
    cross_agreement = _cross_model_agreement(common_ids, maps)

    # Build report
    date_tag = date.today().isoformat()
    out_path = ROOT / "experiments" / "09_ablation_study" / f"statistical_comparison_3way_{date_tag}.json"

    report: Dict[str, Any] = {
        "date": date_tag,
        "n_common_cases": len(common_ids),
        "inputs": {name: str(path.resolve()) for name, path in DEFAULT_PATHS.items()},
        "mcnemar_tests": mcnemar_tests,
        "fleiss_kappa": fleiss_k,
        "cross_model_agreement": cross_agreement,
        "modes": {},
    }

    for name in DEFAULT_PATHS.keys():
        report["modes"][name] = {
            "accuracy": accuracies[name],
            "cohens_kappa": kappas[name],
            "confusion_matrix": matrices[name],
            "per_label_metrics": per_label_metrics[name],
        }

    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    _print_report(report)
    print()
    print(f"[OK] Saved: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
