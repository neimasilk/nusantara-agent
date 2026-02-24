"""Single mode benchmark runner for DeepSeek cross-validation.

Runs ONLY asp_llm mode with DeepSeek API backend.
Skips DISPUTED/SPLIT/AMBIGUOUS labels.
Error handling: logs error and continues to next case on failure.
Supports resume from checkpoint.
"""

import json
import os
import sys
import traceback
import signal
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
from concurrent.futures import TimeoutError as FutureTimeout


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.router import _json_or_raw
from src.pipeline.nusantara_agent import NusantaraAgentPipeline
from src.utils.benchmark_contract import (
    UNRESOLVED_GOLD_LABELS,
    count_evaluable_cases,
    is_evaluable_gold_label,
)
from src.utils.reasoning_contract import summarize_reasoning_contract


DEFAULT_DATASET_PATH = ROOT / "data" / "processed" / "gold_standard" / "gs_active_cases.json"
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "09_ablation_study"
VALID_LABELS = ("A", "B", "C", "D")
CHECKPOINT_EVERY = 5  # Save every N cases
CASE_TIMEOUT = 60  # Timeout per case in seconds


def _path_for_report(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except Exception:
        return str(path.resolve())


def _load_dataset(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset tidak ditemukan: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise RuntimeError(f"Dataset harus list, dapat: {type(data).__name__}")
    return data


def _detect_runtime_backend(pipeline: NusantaraAgentPipeline) -> str:
    if pipeline.orchestrator.__class__.__name__ == "_OfflineOrchestrator":
        return "offline_fallback"
    return "llm_langgraph"


def _extract_predicted_label(agent_analysis: Any) -> str:
    try:
        payload = _json_or_raw(str(agent_analysis or ""))
    except Exception:
        payload = {}

    label = str(payload.get("label", "")).upper().strip()
    if label in VALID_LABELS:
        return label
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


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Case processing timeout")


def process_single_case(pipeline, query: str, gold: str, case_id: str) -> Dict[str, Any]:
    """Process a single case with timeout handling."""
    try:
        output = pipeline.process_query(query)
        predicted = _extract_predicted_label(output.get("agent_analysis", ""))
        match = predicted == gold
        return {
            "id": case_id,
            "gold": gold,
            "predicted": predicted,
            "match": match,
            "reasoning": output.get("agent_analysis", ""),
            "error": None,
            "timed_out": False,
        }
    except TimeoutException:
        return {
            "id": case_id,
            "gold": gold,
            "predicted": "D",
            "match": False,
            "reasoning": "",
            "error": "TIMEOUT",
            "timed_out": True,
        }
    except Exception as exc:
        return {
            "id": case_id,
            "gold": gold,
            "predicted": "D",
            "match": False,
            "reasoning": "",
            "error": _format_exception(exc),
            "timed_out": False,
        }


def run_asp_llm_benchmark(
    dataset_path: Path = DEFAULT_DATASET_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    resume: bool = True,
) -> Dict[str, Any]:
    """Run asp_llm mode benchmark with DeepSeek API backend."""
    
    # Set backend to deepseek
    os.environ["NUSANTARA_LLM_BACKEND"] = "deepseek"
    os.environ.pop("NUSANTARA_FORCE_OFFLINE", None)
    
    from src.utils.llm import has_llm_credentials, get_active_backend
    if not has_llm_credentials():
        backend = get_active_backend()
        raise RuntimeError(f"Backend '{backend}' tidak punya kredensial.")
    
    print(f"[INFO] Using backend: {get_active_backend()}")
    
    dataset = _load_dataset(dataset_path)
    print(f"[INFO] Dataset loaded: {dataset_path}")
    print(f"[INFO] Total cases: {len(dataset)}, Evaluable: {count_evaluable_cases(dataset)}")
    
    print(f"[INFO] Initializing pipeline...")
    pipeline = NusantaraAgentPipeline()
    runtime_backend = _detect_runtime_backend(pipeline)
    print(f"[INFO] Runtime backend: {runtime_backend}")
    
    if runtime_backend != "llm_langgraph":
        raise RuntimeError("Expected llm_langgraph backend but got offline_fallback")
    
    skipped_labels = sorted(UNRESOLVED_GOLD_LABELS)
    
    # Filter to evaluable cases only
    evaluable_cases = []
    for entry in dataset:
        gold = str(entry.get("gold_label", "")).upper().strip()
        if is_evaluable_gold_label(gold):
            evaluable_cases.append(entry)
    
    total_to_eval = len(evaluable_cases)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"results_deepseek_asp_llm_{date.today().isoformat()}.json"
    
    # Check for existing checkpoint
    start_idx = 0
    existing_results = []
    existing_gold = []
    existing_pred = []
    existing_errors = []
    
    if resume and output_path.exists():
        try:
            checkpoint = json.loads(output_path.read_text(encoding="utf-8"))
            if checkpoint.get("results"):
                existing_results = checkpoint["results"]
                # Count completed cases
                completed_ids = {r["id"] for r in existing_results if r.get("predicted")}
                start_idx = len(completed_ids)
                # Restore metrics
                for r in existing_results:
                    if r.get("gold") and r.get("predicted"):
                        existing_gold.append(r["gold"])
                        existing_pred.append(r["predicted"])
                    if r.get("error"):
                        existing_errors.append({"case_id": r["id"], "error": r["error"]})
                print(f"[INFO] Resuming from checkpoint: {start_idx}/{total_to_eval} cases already processed")
        except Exception as e:
            print(f"[WARN] Could not load checkpoint: {e}")
            start_idx = 0
            existing_results = []
            existing_gold = []
            existing_pred = []
            existing_errors = []
    
    results = existing_results.copy()
    gold_labels = existing_gold.copy()
    pred_labels = existing_pred.copy()
    errors = existing_errors.copy()
    
    unresolved_skipped = len(dataset) - total_to_eval
    correct = sum(1 for r in results if r.get("match"))
    
    print(f"[INFO] Starting from case {start_idx + 1}/{total_to_eval}")
    print(f"[INFO] Skipping labels: {skipped_labels}")
    
    for idx in range(start_idx, total_to_eval):
        entry = evaluable_cases[idx]
        gold = str(entry.get("gold_label", "")).upper().strip()
        case_id = str(entry.get("id", f"case_{idx}"))
        query = str(entry.get("query", ""))
        
        print(f"[{idx+1:03d}/{total_to_eval:03d}] {case_id}: ", end="", flush=True)
        
        result = process_single_case(pipeline, query, gold, case_id)
        
        results.append(result)
        gold_labels.append(gold)
        pred_labels.append(result["predicted"])
        
        if result["match"]:
            correct += 1
            status = "OK"
        else:
            status = "FAIL"
        
        if result.get("error"):
            errors.append({"case_id": case_id, "error": result["error"]})
            if result.get("timed_out"):
                print(f"TIMEOUT (pred={result['predicted']})")
            else:
                print(f"ERROR (pred={result['predicted']})")
        else:
            print(f"gold={gold} pred={result['predicted']} {status}")
        
        # Save checkpoint every N cases
        if (idx + 1) % CHECKPOINT_EVERY == 0 or idx == total_to_eval - 1:
            evaluated = len(results)
            accuracy = correct / evaluated if evaluated > 0 else 0.0
            ci_low, ci_high = _wilson_interval(correct, evaluated)
            per_label = _compute_per_label_metrics(gold_labels, pred_labels)
            
            payload = {
                "date": date.today().isoformat(),
                "mode": "asp_llm",
                "backend": "deepseek",
                "runtime_backend": runtime_backend,
                "source_dataset": _path_for_report(dataset_path),
                "total_raw_cases": len(dataset),
                "unresolved_skipped": unresolved_skipped,
                "unresolved_labels": skipped_labels,
                "total_evaluated": evaluated,
                "progress_pct": round(100 * (idx + 1) / total_to_eval, 1),
                "correct": correct,
                "accuracy": accuracy,
                "accuracy_wilson_95ci": {"low": ci_low, "high": ci_high},
                "per_label_metrics": per_label,
                "errors": errors,
                "error_count": len(errors),
                "timeout_count": sum(1 for e in errors if e.get("error") == "TIMEOUT"),
                "reasoning_metadata_contract": summarize_reasoning_contract(results),
                "results": results,
            }
            output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"    [Checkpoint saved: {evaluated}/{total_to_eval}, acc={accuracy:.1%}]")
    
    print(f"\n[OK] Results saved: {output_path}")
    return payload


def print_summary(result: Dict[str, Any]) -> None:
    """Print benchmark summary."""
    print("\n" + "=" * 60)
    print("BENCHMARK SUMMARY - DeepSeek ASP+LLM")
    print("=" * 60)
    
    print(f"\nDate: {result['date']}")
    print(f"Backend: {result['backend']}")
    print(f"Runtime: {result['runtime_backend']}")
    print(f"Dataset: {result['source_dataset']}")
    
    print(f"\nCases:")
    print(f"  Total raw: {result['total_raw_cases']}")
    print(f"  Skipped (unresolved): {result['unresolved_skipped']}")
    print(f"  Evaluated: {result['total_evaluated']}")
    print(f"  Errors: {result.get('error_count', 0)}")
    print(f"  Timeouts: {result.get('timeout_count', 0)}")
    
    acc = result['accuracy']
    ci = result['accuracy_wilson_95ci']
    print(f"\nAccuracy: {acc:.1%} ({result['correct']}/{result['total_evaluated']})")
    print(f"Wilson 95% CI: [{ci['low']:.3f}, {ci['high']:.3f}]")
    
    print(f"\nPer-Label Metrics:")
    print(f"  Label | Support | Precision | Recall")
    print(f"  ------|---------|-----------|--------")
    for label in VALID_LABELS:
        m = result['per_label_metrics'][label]
        print(f"  {label}     | {m['support']:7d} | {m['precision']:.3f}     | {m['recall']:.3f}")
    
    OLLAMA_BASELINE = 0.70
    diff = acc - OLLAMA_BASELINE
    print(f"\nComparison with Ollama (70.0%):")
    if diff > 0:
        print(f"  DeepSeek: +{diff:.1%} better than Ollama")
    elif diff < 0:
        print(f"  DeepSeek: {diff:.1%} worse than Ollama")
    else:
        print(f"  DeepSeek: Same as Ollama")
    
    print("=" * 60)


def main() -> int:
    """Main entry point."""
    print("=" * 60)
    print("DeepSeek Cross-Validation Benchmark")
    print("=" * 60)
    
    try:
        result = run_asp_llm_benchmark(resume=True)
        print_summary(result)
        return 0
    except Exception as exc:
        print(f"\n[FATAL] Benchmark failed: {exc}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
