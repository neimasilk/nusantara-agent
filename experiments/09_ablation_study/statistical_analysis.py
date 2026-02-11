import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from scipy import stats

DEFAULT_RESULTS_DIR = Path("experiments/09_ablation_study/results")


def _load_run_files(results_dir: Path) -> List[Dict]:
    run_files = sorted((results_dir / "baseline_runs").glob("B*/run_seed_*.json"))
    if not run_files:
        raise FileNotFoundError(
            f"Tidak ada hasil baseline run di {(results_dir / 'baseline_runs').as_posix()}"
        )
    runs: List[Dict] = []
    for path in run_files:
        obj = json.loads(path.read_text(encoding="utf-8"))
        obj["_path"] = path.as_posix()
        runs.append(obj)
    return runs


def _group_by_baseline(runs: List[Dict]) -> Dict[str, List[Dict]]:
    grouped: Dict[str, List[Dict]] = {}
    for run in runs:
        baseline_id = run.get("baseline_id", "UNKNOWN")
        grouped.setdefault(baseline_id, []).append(run)
    for baseline_runs in grouped.values():
        baseline_runs.sort(key=lambda x: x.get("seed", 0))
    return grouped


def _mean_ci(values: List[float], confidence: float = 0.95) -> Tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    arr = np.array(values, dtype=float)
    if len(arr) == 1:
        return (float(arr[0]), float(arr[0]))
    mean = float(arr.mean())
    if float(np.std(arr, ddof=1)) == 0.0:
        return (mean, mean)
    sem = stats.sem(arr)
    interval = stats.t.interval(confidence, len(arr) - 1, loc=mean, scale=sem)
    low = float(interval[0]) if np.isfinite(interval[0]) else mean
    high = float(interval[1]) if np.isfinite(interval[1]) else mean
    return (low, high)


def _cohens_d_paired(x: List[float], y: List[float]) -> float:
    arr_x = np.array(x, dtype=float)
    arr_y = np.array(y, dtype=float)
    diff = arr_x - arr_y
    if len(diff) < 2:
        return 0.0
    sd = float(np.std(diff, ddof=1))
    if sd == 0:
        return 0.0
    return float(np.mean(diff) / sd)


def _paired_tests(x: List[float], y: List[float]) -> Dict:
    if len(x) != len(y):
        raise ValueError("Panjang array paired test harus sama.")
    if len(x) < 2:
        return {
            "n_pairs": len(x),
            "t_test_pvalue": None,
            "wilcoxon_pvalue": None,
            "cohens_d": 0.0,
        }

    diff = np.array(x, dtype=float) - np.array(y, dtype=float)
    if np.allclose(diff, 0.0):
        return {
            "n_pairs": len(x),
            "t_test_pvalue": 1.0,
            "wilcoxon_pvalue": 1.0,
            "cohens_d": 0.0,
        }
    if float(np.std(diff, ddof=1)) == 0.0:
        # Semua delta sama arah/magnitudo; paired t-test tidak stabil secara numerik.
        try:
            _w_stat, w_p = stats.wilcoxon(x, y)
            w_p_value = float(w_p) if np.isfinite(w_p) else None
        except Exception:
            w_p_value = None
        return {
            "n_pairs": len(x),
            "t_test_pvalue": 0.0,
            "wilcoxon_pvalue": w_p_value,
            "cohens_d": 0.0,
        }

    _t_stat, t_p = stats.ttest_rel(x, y)
    try:
        _w_stat, w_p = stats.wilcoxon(x, y)
        w_p_value = float(w_p) if np.isfinite(w_p) else None
    except Exception:
        w_p_value = None

    t_p_value = float(t_p) if np.isfinite(t_p) else None
    return {
        "n_pairs": len(x),
        "t_test_pvalue": t_p_value,
        "wilcoxon_pvalue": w_p_value,
        "cohens_d": _cohens_d_paired(x, y),
    }


def _align_by_seed(lhs_runs: List[Dict], rhs_runs: List[Dict]) -> Tuple[List[int], List[float], List[float]]:
    lhs_map = {int(r.get("seed", -1)): float(r.get("accuracy", 0.0)) for r in lhs_runs}
    rhs_map = {int(r.get("seed", -1)): float(r.get("accuracy", 0.0)) for r in rhs_runs}
    seeds = sorted(set(lhs_map.keys()) & set(rhs_map.keys()))
    lhs = [lhs_map[s] for s in seeds]
    rhs = [rhs_map[s] for s in seeds]
    return seeds, lhs, rhs


def run_statistical_analysis(results_dir: Path, reference_baseline: str) -> Dict:
    runs = _load_run_files(results_dir)
    grouped = _group_by_baseline(runs)

    baseline_stats: Dict[str, Dict] = {}
    for baseline_id, baseline_runs in grouped.items():
        accuracies = [float(r.get("accuracy", 0.0)) for r in baseline_runs]
        mean = float(np.mean(accuracies)) if accuracies else 0.0
        std = float(np.std(accuracies, ddof=1)) if len(accuracies) > 1 else 0.0
        ci_low, ci_high = _mean_ci(accuracies, confidence=0.95)
        baseline_stats[baseline_id] = {
            "baseline_id": baseline_id,
            "n_runs": len(accuracies),
            "seeds": [int(r.get("seed", -1)) for r in baseline_runs],
            "accuracies": accuracies,
            "mean_accuracy": mean,
            "std_accuracy": std,
            "ci95_accuracy": [ci_low, ci_high],
        }

    if reference_baseline not in grouped:
        raise RuntimeError(
            f"Reference baseline {reference_baseline} tidak ditemukan. Baseline tersedia: {sorted(grouped.keys())}"
        )

    pairwise_vs_reference: List[Dict] = []
    ref_runs = grouped[reference_baseline]
    for baseline_id, baseline_runs in grouped.items():
        if baseline_id == reference_baseline:
            continue
        seeds, lhs, rhs = _align_by_seed(baseline_runs, ref_runs)
        tests = _paired_tests(lhs, rhs)
        pairwise_vs_reference.append(
            {
                "baseline_id": baseline_id,
                "reference_baseline": reference_baseline,
                "paired_seeds": seeds,
                "baseline_accuracies": lhs,
                "reference_accuracies": rhs,
                "delta_mean_accuracy": float(np.mean(np.array(lhs) - np.array(rhs))) if seeds else 0.0,
                **tests,
            }
        )

    ranking = sorted(
        baseline_stats.values(),
        key=lambda x: x["mean_accuracy"],
        reverse=True,
    )

    report = {
        "results_dir": results_dir.as_posix(),
        "n_total_runs": len(runs),
        "reference_baseline": reference_baseline,
        "baseline_stats": baseline_stats,
        "pairwise_vs_reference": pairwise_vs_reference,
        "ranking_by_mean_accuracy": [
            {"baseline_id": item["baseline_id"], "mean_accuracy": item["mean_accuracy"]}
            for item in ranking
        ],
    }

    json_path = results_dir / "statistical_analysis.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Saved JSON report: {json_path.as_posix()}")

    md_path = results_dir / "statistical_analysis.md"
    md_path.write_text(_render_markdown_report(report), encoding="utf-8")
    print(f"[OK] Saved Markdown report: {md_path.as_posix()}")
    return report


def _render_markdown_report(report: Dict) -> str:
    lines: List[str] = []
    lines.append("# Statistical Analysis — ART-066")
    lines.append("")
    lines.append(f"- Results dir: `{report['results_dir']}`")
    lines.append(f"- Total runs: {report['n_total_runs']}")
    lines.append(f"- Reference baseline: `{report['reference_baseline']}`")
    lines.append("")
    lines.append("## Baseline Summary")
    lines.append("")
    lines.append("| Baseline | N Run | Mean Acc | Std | 95% CI |")
    lines.append("|---|---:|---:|---:|---|")
    for baseline_id in sorted(report["baseline_stats"].keys()):
        item = report["baseline_stats"][baseline_id]
        ci = item["ci95_accuracy"]
        lines.append(
            f"| {baseline_id} | {item['n_runs']} | {item['mean_accuracy']:.4f} | "
            f"{item['std_accuracy']:.4f} | [{ci[0]:.4f}, {ci[1]:.4f}] |"
        )
    lines.append("")
    lines.append("## Pairwise vs Reference")
    lines.append("")
    lines.append("| Baseline | Delta Mean Acc | n_pairs | t-test p | Wilcoxon p | Cohen's d |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for row in sorted(report["pairwise_vs_reference"], key=lambda x: x["baseline_id"]):
        t_p = "-" if row["t_test_pvalue"] is None else f"{row['t_test_pvalue']:.6f}"
        w_p = "-" if row["wilcoxon_pvalue"] is None else f"{row['wilcoxon_pvalue']:.6f}"
        lines.append(
            f"| {row['baseline_id']} | {row['delta_mean_accuracy']:.4f} | "
            f"{row['n_pairs']} | {t_p} | {w_p} | {row['cohens_d']:.4f} |"
        )
    lines.append("")
    lines.append("## Ranking by Mean Accuracy")
    lines.append("")
    for idx, row in enumerate(report["ranking_by_mean_accuracy"], start=1):
        lines.append(f"{idx}. `{row['baseline_id']}` — {row['mean_accuracy']:.4f}")
    lines.append("")
    lines.append(
        "Catatan: analisis ini menghitung statistik terhadap run yang tersedia pada folder hasil."
    )
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ART-066 statistical analysis untuk hasil ART-065.")
    parser.add_argument(
        "--results-dir",
        type=str,
        default=str(DEFAULT_RESULTS_DIR),
        help="Direktori hasil yang berisi baseline_runs.",
    )
    parser.add_argument(
        "--reference-baseline",
        type=str,
        default="B5",
        help="Baseline acuan untuk pairwise test (default B5).",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    run_statistical_analysis(Path(args.results_dir), args.reference_baseline)
