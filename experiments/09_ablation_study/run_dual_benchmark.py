import argparse
import json
import os
import re
import sys
import traceback
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.router import _json_or_raw
from src.pipeline.nusantara_agent import NusantaraAgentPipeline
from src.utils.benchmark_contract import (
    UNRESOLVED_GOLD_LABELS,
    count_evaluable_cases,
    is_evaluable_gold_label,
    resolve_manifest_evaluable_count,
)


DEFAULT_MANIFEST_PATH = ROOT / "data" / "benchmark_manifest.json"
DEFAULT_DATASET_PATH = ROOT / "data" / "processed" / "gold_standard" / "gs_active_cases.json"
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "09_ablation_study"
VALID_LABELS = ("A", "B", "C", "D")


def _path_for_report(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except Exception:
        return str(path.resolve())


def _load_manifest(path: Path) -> Dict[str, Any]:
    if not path.exists():
        print(f"[WARN] Manifest tidak ditemukan: {path}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[WARN] Gagal membaca manifest {path}: {exc}")
        return {}


def _resolve_dataset_path(dataset_arg: str, manifest: Dict[str, Any]) -> Path:
    if dataset_arg:
        return (ROOT / dataset_arg).resolve() if not Path(dataset_arg).is_absolute() else Path(dataset_arg)

    manifest_path = str(manifest.get("benchmark_file", {}).get("path", "")).strip()
    if manifest_path:
        p = Path(manifest_path)
        return (ROOT / p).resolve() if not p.is_absolute() else p

    return DEFAULT_DATASET_PATH


def _load_dataset(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset tidak ditemukan: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise RuntimeError(f"Dataset harus list, dapat: {type(data).__name__}")
    return data


def _validate_manifest_counts(
    dataset: List[Dict[str, Any]],
    manifest: Dict[str, Any],
    strict_manifest: bool,
) -> None:
    if not manifest:
        return

    benchmark = manifest.get("benchmark_file", {})
    expected_total = benchmark.get("total_cases_actual")
    if expected_total is not None:
        actual_total = len(dataset)
        if actual_total != int(expected_total):
            msg = (
                f"Manifest mismatch total_cases_actual: runtime={actual_total} "
                f"vs manifest={expected_total}"
            )
            if strict_manifest:
                raise RuntimeError(msg)
            print(f"[WARN] {msg}")

    expected_evaluable = resolve_manifest_evaluable_count(benchmark)
    if expected_evaluable is not None:
        actual_evaluable = count_evaluable_cases(dataset)
        if actual_evaluable != expected_evaluable:
            msg = (
                f"Manifest mismatch evaluable_cases: runtime={actual_evaluable} "
                f"vs manifest={expected_evaluable}"
            )
            if strict_manifest:
                raise RuntimeError(msg)
            print(f"[WARN] {msg}")


def _detect_runtime_backend(pipeline: NusantaraAgentPipeline) -> str:
    if pipeline.orchestrator.__class__.__name__ == "_OfflineOrchestrator":
        return "offline_fallback"
    return "llm_langgraph"


def _extract_predicted_label(agent_analysis: Any) -> str:
    text = str(agent_analysis or "")
    try:
        payload = _json_or_raw(text)
    except Exception:
        payload = {}

    label = str(payload.get("label", "")).upper().strip()
    if label in VALID_LABELS:
        return label

    # Fallback: regex extraction when JSON parsing fails due to trailing text
    m = re.search(r'"label"\s*:\s*"([A-Da-d])"', text)
    if m:
        return m.group(1).upper()

    # Last resort defensif agar benchmark tetap jalan.
    return "D"


def _format_exception(exc: Exception) -> str:
    root = f"{exc.__class__.__name__}: {exc}"
    cause = getattr(exc, "__cause__", None)
    if cause is None:
        return root
    return f"{root} | cause={cause.__class__.__name__}: {cause}"


def _wilson_interval(successes: int, total: int, z: float = 1.96) -> Tuple[float, float]:
    if total <= 0:
        return 0.0, 0.0

    phat = successes / total
    z2 = z * z
    denom = 1.0 + (z2 / total)
    center = (phat + (z2 / (2.0 * total))) / denom
    margin = (z / denom) * ((phat * (1.0 - phat) / total + z2 / (4.0 * total * total)) ** 0.5)
    low = max(0.0, center - margin)
    high = min(1.0, center + margin)
    return low, high


def _compute_per_label_metrics(gold: List[str], pred: List[str]) -> Dict[str, Dict[str, float]]:
    metrics: Dict[str, Dict[str, float]] = {}
    for label in VALID_LABELS:
        tp = sum(1 for g, p in zip(gold, pred) if g == label and p == label)
        fp = sum(1 for g, p in zip(gold, pred) if g != label and p == label)
        fn = sum(1 for g, p in zip(gold, pred) if g == label and p != label)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        metrics[label] = {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "support": sum(1 for g in gold if g == label),
            "precision": precision,
            "recall": recall,
        }
    return metrics


def _run_mode(
    mode: str,
    dataset: List[Dict[str, Any]],
    output_dir: Path,
    dataset_path: Path,
    skipped_labels: List[str],
) -> Dict[str, Any]:
    if mode not in {"asp_only", "asp_llm"}:
        raise ValueError(f"Mode tidak didukung: {mode}")

    old_force_offline = os.getenv("NUSANTARA_FORCE_OFFLINE")
    mode_skipped = False
    skip_reason = ""
    output_path = output_dir / f"results_dual_{mode}_{date.today().isoformat()}.json"

    try:
        if mode == "asp_only":
            os.environ["NUSANTARA_FORCE_OFFLINE"] = "1"
        else:
            os.environ.pop("NUSANTARA_FORCE_OFFLINE", None)
            from src.utils.llm import has_llm_credentials, get_active_backend
            if not has_llm_credentials():
                backend = get_active_backend()
                mode_skipped = True
                skip_reason = f"Backend '{backend}' tidak punya kredensial, mode ASP+LLM di-skip."

        if mode_skipped:
            payload = {
                "date": date.today().isoformat(),
                "mode": mode,
                "skipped": True,
                "skip_reason": skip_reason,
                "source_dataset": _path_for_report(dataset_path),
            }
            output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[WARN] {skip_reason}")
            print(f"[OK] Saved: {output_path}")
            return payload

        pipeline = NusantaraAgentPipeline()
        runtime_backend = _detect_runtime_backend(pipeline)

        if mode == "asp_llm" and runtime_backend != "llm_langgraph":
            skip_reason = (
                "Mode ASP+LLM diminta, tetapi runtime backend offline_fallback "
                "(cek dependency/langgraph/langchain_openai atau env API)."
            )
            payload = {
                "date": date.today().isoformat(),
                "mode": mode,
                "skipped": True,
                "skip_reason": skip_reason,
                "runtime_backend": runtime_backend,
                "source_dataset": _path_for_report(dataset_path),
            }
            output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[WARN] {skip_reason}")
            print(f"[OK] Saved: {output_path}")
            return payload

        results: List[Dict[str, Any]] = []
        gold_labels: List[str] = []
        pred_labels: List[str] = []
        unresolved_skipped = 0
        evaluated = 0
        correct = 0

        for entry in dataset:
            gold = str(entry.get("gold_label", "")).upper().strip()
            if not is_evaluable_gold_label(gold):
                unresolved_skipped += 1
                continue

            case_id = str(entry.get("id", ""))
            query = str(entry.get("query", ""))
            evaluated += 1

            try:
                output = pipeline.process_query(query)
            except Exception as exc:
                if mode == "asp_llm":
                    skip_reason = (
                        "Mode ASP+LLM gagal saat pemanggilan model: "
                        f"{_format_exception(exc)}"
                    )
                    payload = {
                        "date": date.today().isoformat(),
                        "mode": mode,
                        "skipped": True,
                        "skip_reason": skip_reason,
                        "runtime_backend": runtime_backend,
                        "source_dataset": _path_for_report(dataset_path),
                        "failed_case_id": case_id,
                        "failed_case_index_1based": evaluated,
                        "error_traceback_last_20_lines": traceback.format_exc().splitlines()[-20:],
                    }
                    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
                    print(f"[WARN] {skip_reason}")
                    print(f"[OK] Saved: {output_path}")
                    return payload
                raise

            predicted = _extract_predicted_label(output.get("agent_analysis", ""))
            match = predicted == gold
            if match:
                correct += 1

            gold_labels.append(gold)
            pred_labels.append(predicted)

            results.append(
                {
                    "id": case_id,
                    "gold": gold,
                    "predicted": predicted,
                    "match": match,
                    "reasoning": output.get("agent_analysis", ""),
                }
            )

        accuracy = correct / evaluated if evaluated > 0 else 0.0
        ci_low, ci_high = _wilson_interval(correct, evaluated)
        per_label = _compute_per_label_metrics(gold_labels, pred_labels)

        payload = {
            "date": date.today().isoformat(),
            "mode": mode,
            "skipped": False,
            "runtime_backend": runtime_backend,
            "source_dataset": _path_for_report(dataset_path),
            "total_raw_cases": len(dataset),
            "unresolved_skipped": unresolved_skipped,
            "unresolved_labels": skipped_labels,
            "total_evaluated": evaluated,
            "correct": correct,
            "accuracy": accuracy,
            "accuracy_wilson_95ci": {
                "low": ci_low,
                "high": ci_high,
            },
            "per_label_metrics": per_label,
            "results": results,
        }
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] Saved: {output_path}")
        return payload
    finally:
        if old_force_offline is None:
            os.environ.pop("NUSANTARA_FORCE_OFFLINE", None)
        else:
            os.environ["NUSANTARA_FORCE_OFFLINE"] = old_force_offline


def _render_comparison_table(mode_results: List[Dict[str, Any]]) -> str:
    headers = ["Mode", "Status", "Backend", "Evaluated", "Accuracy", "Wilson95% CI", "Notes"]
    rows: List[List[str]] = []

    for item in mode_results:
        mode = str(item.get("mode", ""))
        skipped = bool(item.get("skipped", False))
        if skipped:
            rows.append(
                [
                    mode,
                    "SKIPPED",
                    str(item.get("runtime_backend", "-")),
                    "-",
                    "-",
                    "-",
                    str(item.get("skip_reason", "")),
                ]
            )
            continue

        ci = item.get("accuracy_wilson_95ci", {})
        ci_text = f"[{float(ci.get('low', 0.0)):.3f}, {float(ci.get('high', 0.0)):.3f}]"
        rows.append(
            [
                mode,
                "DONE",
                str(item.get("runtime_backend", "")),
                str(item.get("total_evaluated", 0)),
                f"{float(item.get('accuracy', 0.0)):.3f}",
                ci_text,
                "",
            ]
        )

    all_rows = [headers] + rows
    widths = [max(len(str(r[i])) for r in all_rows) for i in range(len(headers))]

    def _fmt(row: List[str]) -> str:
        return " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))

    sep = "-+-".join("-" * w for w in widths)
    lines = [_fmt(headers), sep]
    lines.extend(_fmt(r) for r in rows)
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Dual benchmark runner: ASP-only (offline) vs ASP+LLM."
    )
    parser.add_argument(
        "--gs-path",
        type=str,
        default="",
        help="Path dataset benchmark. Jika kosong pakai manifest lalu fallback default.",
    )
    parser.add_argument(
        "--manifest-path",
        type=str,
        default=str(DEFAULT_MANIFEST_PATH),
        help="Path benchmark manifest JSON.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help="Direktori output file hasil benchmark dual mode.",
    )
    parser.add_argument(
        "--strict-manifest",
        action="store_true",
        help="Hard-fail jika total/evaluable runtime tidak cocok benchmark manifest.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()

    manifest_path = Path(args.manifest_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = _load_manifest(manifest_path)
    dataset_path = _resolve_dataset_path(args.gs_path, manifest)
    dataset = _load_dataset(dataset_path)
    _validate_manifest_counts(dataset, manifest, strict_manifest=args.strict_manifest)

    skipped_labels = sorted(UNRESOLVED_GOLD_LABELS)
    print(
        "[INFO] Dataset loaded:",
        f"path={dataset_path}",
        f"total={len(dataset)}",
        f"evaluable={count_evaluable_cases(dataset)}",
        f"skipped_labels={skipped_labels}",
    )

    asp_only_result = _run_mode(
        mode="asp_only",
        dataset=dataset,
        output_dir=output_dir,
        dataset_path=dataset_path,
        skipped_labels=skipped_labels,
    )
    asp_llm_result = _run_mode(
        mode="asp_llm",
        dataset=dataset,
        output_dir=output_dir,
        dataset_path=dataset_path,
        skipped_labels=skipped_labels,
    )

    table = _render_comparison_table([asp_only_result, asp_llm_result])
    print("\n=== Dual Benchmark Comparison ===")
    print(table)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
