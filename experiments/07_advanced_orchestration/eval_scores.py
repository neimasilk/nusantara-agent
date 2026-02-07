import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List, Optional


def _load_scores(path: Path) -> List[Dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Format skor harus list of objects.")
    return data


def _load_run_index(path: Path) -> List[Dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Format run_index harus list of objects.")
    return data


def _avg(values: List[float]) -> float:
    return round(mean(values), 4) if values else 0.0


def _normalize_query_id(value: Any) -> str:
    return str(value).strip().upper()


def _filter_scores_by_query_ids(scores: List[Dict], query_ids: List[str]) -> List[Dict]:
    allowed = {_normalize_query_id(qid) for qid in query_ids if _normalize_query_id(qid)}
    if not allowed:
        return scores
    return [item for item in scores if _normalize_query_id(item.get("query_id", "")) in allowed]


def _to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _extract_total_tokens(item: Dict) -> Optional[Dict[str, float]]:
    token_usage = item.get("token_usage")
    if not isinstance(token_usage, dict):
        return None

    total = token_usage.get("total")
    if isinstance(total, dict):
        prompt_tokens = _to_float(total.get("prompt_tokens"))
        completion_tokens = _to_float(total.get("completion_tokens"))
        total_tokens = _to_float(total.get("total_tokens"))
    else:
        prompt_tokens = _to_float(token_usage.get("prompt_tokens"))
        completion_tokens = _to_float(token_usage.get("completion_tokens"))
        total_tokens = _to_float(token_usage.get("total_tokens"))

    if total_tokens <= 0 and (prompt_tokens > 0 or completion_tokens > 0):
        total_tokens = prompt_tokens + completion_tokens

    if total_tokens <= 0 and prompt_tokens <= 0 and completion_tokens <= 0:
        return None

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }


def _extract_stage_tokens(item: Dict, stage: str) -> Optional[float]:
    token_usage = item.get("token_usage")
    if not isinstance(token_usage, dict):
        return None
    stage_usage = token_usage.get(stage)
    if not isinstance(stage_usage, dict):
        return None
    total_tokens = _to_float(stage_usage.get("total_tokens"))
    if total_tokens <= 0:
        prompt = _to_float(stage_usage.get("prompt_tokens"))
        completion = _to_float(stage_usage.get("completion_tokens"))
        total_tokens = prompt + completion
    return total_tokens if total_tokens > 0 else None


def _estimate_cost(
    prompt_tokens: float,
    completion_tokens: float,
    price_input_per_1m: float,
    price_output_per_1m: float,
) -> float:
    if price_input_per_1m <= 0 and price_output_per_1m <= 0:
        return 0.0
    return (prompt_tokens / 1_000_000.0) * price_input_per_1m + (
        completion_tokens / 1_000_000.0
    ) * price_output_per_1m


def summarize_run_index(
    run_index: List[Dict],
    price_input_per_1m: float = 0.0,
    price_output_per_1m: float = 0.0,
) -> Dict:
    total_times = [_to_float(item.get("timing_seconds", {}).get("total")) for item in run_index]
    total_times = [x for x in total_times if x > 0]

    result: Dict[str, Any] = {
        "count": len(run_index),
        "timing": {
            "avg_total_seconds": _avg(total_times),
            "min_total_seconds": round(min(total_times), 4) if total_times else 0.0,
            "max_total_seconds": round(max(total_times), 4) if total_times else 0.0,
        },
    }

    # Stage timing only when available (advanced run usually has these)
    stage_keys = ["retrieval_parallel", "debate", "supervisor"]
    stage_avgs: Dict[str, float] = {}
    for stage in stage_keys:
        values = [_to_float(item.get("timing_seconds", {}).get(stage)) for item in run_index]
        values = [x for x in values if x > 0]
        if values:
            stage_avgs[stage] = _avg(values)
    if stage_avgs:
        result["timing"]["avg_stage_seconds"] = stage_avgs

    token_rows = [_extract_total_tokens(item) for item in run_index]
    token_rows = [row for row in token_rows if row is not None]
    if token_rows:
        prompt_values = [row["prompt_tokens"] for row in token_rows]
        completion_values = [row["completion_tokens"] for row in token_rows]
        total_values = [row["total_tokens"] for row in token_rows]

        prompt_sum = sum(prompt_values)
        completion_sum = sum(completion_values)
        total_sum = sum(total_values)

        tokens_summary: Dict[str, Any] = {
            "available_count": len(token_rows),
            "avg_prompt_tokens": _avg(prompt_values),
            "avg_completion_tokens": _avg(completion_values),
            "avg_total_tokens": _avg(total_values),
            "sum_prompt_tokens": round(prompt_sum, 2),
            "sum_completion_tokens": round(completion_sum, 2),
            "sum_total_tokens": round(total_sum, 2),
        }

        stage_token_avgs: Dict[str, float] = {}
        for stage in stage_keys:
            stage_values = [_extract_stage_tokens(item, stage) for item in run_index]
            stage_values = [x for x in stage_values if x is not None and x > 0]
            if stage_values:
                stage_token_avgs[stage] = _avg(stage_values)
        if stage_token_avgs:
            tokens_summary["avg_stage_total_tokens"] = stage_token_avgs

        estimated_cost_total = _estimate_cost(
            prompt_tokens=prompt_sum,
            completion_tokens=completion_sum,
            price_input_per_1m=price_input_per_1m,
            price_output_per_1m=price_output_per_1m,
        )
        if estimated_cost_total > 0:
            estimated_cost_avg = estimated_cost_total / len(token_rows)
            tokens_summary["cost_estimate"] = {
                "price_input_per_1m": price_input_per_1m,
                "price_output_per_1m": price_output_per_1m,
                "estimated_total": round(estimated_cost_total, 6),
                "estimated_avg_per_query": round(estimated_cost_avg, 6),
            }

        result["tokens"] = tokens_summary

    call_values = []
    for item in run_index:
        calls = item.get("llm_call_count")
        if isinstance(calls, dict):
            call_values.append(_to_float(calls.get("total")))
        elif calls is not None:
            call_values.append(_to_float(calls))
    call_values = [x for x in call_values if x > 0]
    if call_values:
        result["llm_calls"] = {
            "avg_total_calls": _avg(call_values),
        }

    return result


def compare_run_summaries(advanced: Dict, baseline: Dict) -> Dict:
    comparison: Dict[str, Any] = {}

    adv_timing = advanced.get("timing", {}).get("avg_total_seconds", 0.0)
    base_timing = baseline.get("timing", {}).get("avg_total_seconds", 0.0)
    if adv_timing > 0 and base_timing > 0:
        ratio = adv_timing / base_timing
        comparison["timing"] = {
            "advanced_vs_baseline_ratio": round(ratio, 4),
            "overhead_pct": round((ratio - 1.0) * 100.0, 2),
            "delta_seconds": round(adv_timing - base_timing, 4),
        }

    adv_tokens = advanced.get("tokens", {}).get("avg_total_tokens", 0.0)
    base_tokens = baseline.get("tokens", {}).get("avg_total_tokens", 0.0)
    if adv_tokens > 0 and base_tokens > 0:
        ratio = adv_tokens / base_tokens
        comparison["tokens"] = {
            "advanced_vs_baseline_ratio": round(ratio, 4),
            "overhead_pct": round((ratio - 1.0) * 100.0, 2),
            "delta_tokens": round(adv_tokens - base_tokens, 4),
        }

    adv_calls = advanced.get("llm_calls", {}).get("avg_total_calls", 0.0)
    base_calls = baseline.get("llm_calls", {}).get("avg_total_calls", 0.0)
    if adv_calls > 0 and base_calls > 0:
        ratio = adv_calls / base_calls
        comparison["llm_calls"] = {
            "advanced_vs_baseline_ratio": round(ratio, 4),
            "delta_calls": round(adv_calls - base_calls, 4),
        }

    return comparison


def summarize(scores: List[Dict]) -> Dict:
    acc = [item.get("accuracy", 0) for item in scores]
    comp = [item.get("completeness", 0) for item in scores]
    cult = [item.get("cultural_sensitivity", 0) for item in scores]
    total = [a + c + s for a, c, s in zip(acc, comp, cult)]

    return {
        "count": len(scores),
        "avg_accuracy": _avg(acc),
        "avg_completeness": _avg(comp),
        "avg_cultural_sensitivity": _avg(cult),
        "avg_total": _avg(total),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize Exp07 scores")
    parser.add_argument(
        "--scores",
        default="experiments/07_advanced_orchestration/scoring_template.json",
        help="Path ke file skor JSON",
    )
    parser.add_argument(
        "--run-index",
        default="",
        help="(Opsional) Path run_index advanced untuk ringkasan timing/token",
    )
    parser.add_argument(
        "--baseline-run-index",
        default="",
        help="(Opsional) Path run_index baseline untuk komparasi efisiensi",
    )
    parser.add_argument(
        "--align-scores-with-run",
        action="store_true",
        help="Filter skor agar hanya query_id yang ada di run_index advanced",
    )
    parser.add_argument(
        "--price-input-per-1m",
        type=float,
        default=0.0,
        help="(Opsional) Harga input token per 1M token untuk estimasi cost",
    )
    parser.add_argument(
        "--price-output-per-1m",
        type=float,
        default=0.0,
        help="(Opsional) Harga output token per 1M token untuk estimasi cost",
    )
    parser.add_argument(
        "--baseline-price-input-per-1m",
        type=float,
        default=None,
        help="(Opsional) Override harga input baseline per 1M token",
    )
    parser.add_argument(
        "--baseline-price-output-per-1m",
        type=float,
        default=None,
        help="(Opsional) Override harga output baseline per 1M token",
    )
    parser.add_argument(
        "--out",
        default="experiments/07_advanced_orchestration/score_summary.json",
        help="Path output ringkasan JSON",
    )
    args = parser.parse_args()

    scores = _load_scores(Path(args.scores))
    run_index: Optional[List[Dict]] = None
    run_index_path: Optional[Path] = None

    if args.run_index:
        run_index_path = Path(args.run_index)
        run_index = _load_run_index(run_index_path)
        if args.align_scores_with_run:
            run_query_ids = [item.get("query_id", "") for item in run_index]
            scores = _filter_scores_by_query_ids(scores, run_query_ids)

    summary = summarize(scores)

    if run_index is not None and run_index_path is not None:
        summary["run_summary"] = summarize_run_index(
            run_index,
            price_input_per_1m=args.price_input_per_1m,
            price_output_per_1m=args.price_output_per_1m,
        )
        summary["run_summary"]["source"] = str(run_index_path)

    if args.baseline_run_index:
        baseline_path = Path(args.baseline_run_index)
        baseline_run_index = _load_run_index(baseline_path)
        baseline_input_price = (
            args.baseline_price_input_per_1m
            if args.baseline_price_input_per_1m is not None
            else args.price_input_per_1m
        )
        baseline_output_price = (
            args.baseline_price_output_per_1m
            if args.baseline_price_output_per_1m is not None
            else args.price_output_per_1m
        )
        summary["baseline_run_summary"] = summarize_run_index(
            baseline_run_index,
            price_input_per_1m=baseline_input_price,
            price_output_per_1m=baseline_output_price,
        )
        summary["baseline_run_summary"]["source"] = str(baseline_path)

        if "run_summary" in summary:
            summary["efficiency_comparison"] = compare_run_summaries(
                advanced=summary["run_summary"],
                baseline=summary["baseline_run_summary"],
            )

    consistency_checks: Dict[str, Any] = {}
    if "run_summary" in summary:
        run_count = summary["run_summary"].get("count", 0)
        consistency_checks["score_vs_run_count_match"] = {
            "score_count": summary.get("count", 0),
            "run_count": run_count,
            "match": summary.get("count", 0) == run_count,
        }
    if "baseline_run_summary" in summary and "run_summary" in summary:
        adv_count = summary["run_summary"].get("count", 0)
        base_count = summary["baseline_run_summary"].get("count", 0)
        consistency_checks["advanced_vs_baseline_run_count_match"] = {
            "advanced_run_count": adv_count,
            "baseline_run_count": base_count,
            "match": adv_count == base_count,
        }
    if consistency_checks:
        summary["consistency_checks"] = consistency_checks

    Path(args.out).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
