"""Main runner for the multi-LLM benchmark sweep.

Usage:
  python -m experiments.10_automated_benchmark.harness.runner \
      --provider deepseek --condition 1 --split dev --limit 5

CLI defaults are conservative: --limit 5 (smoke), --split dev.
Producing a full sweep requires explicit --limit 0 (meaning unlimited).
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

# Path bootstrap: when invoked as a script via `python harness/runner.py`,
# the `harness` package directory is not on sys.path. Add the experiment
# root so siblings (dataset, prompt_builder, etc.) resolve.
_THIS_FILE = Path(__file__).resolve()
_EXP_ROOT = _THIS_FILE.parents[1]
if str(_EXP_ROOT) not in sys.path:
    sys.path.insert(0, str(_EXP_ROOT))

from harness import dataset, prompt_builder, label_parser  # noqa: E402
from harness.providers import PROVIDERS, estimate_call_cost  # noqa: E402

RUNS_DIR = _EXP_ROOT / "runs"


def _load_client(provider_name: str):
    """Late import to avoid forcing the openai dep when not needed."""
    try:
        from openai import OpenAI
    except ImportError as e:
        raise SystemExit(
            "openai package not installed. Run: pip install openai"
        ) from e

    spec = PROVIDERS[provider_name]
    return OpenAI(api_key=spec.api_key(), base_url=spec.base_url), spec


def _now_tag() -> str:
    return datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def run(provider_name: str, condition: int, split: str, limit: int,
        model_override: str | None, dry_run: bool, sleep_sec: float) -> None:
    if split == "dev":
        cases = dataset.load_dev()
        cases = [{"id": c["id"], "query": c.get("query", ""),
                  "gold_label": c.get("gold_label", ""), "split": "dev"}
                 for c in cases]
    elif split == "test":
        cases = dataset.load_test()
        cases = [{"id": c["id"], "query": c.get("query", ""),
                  "gold_label": c.get("gold_label", ""), "split": "test"}
                 for c in cases]
    elif split == "all":
        cases = dataset.load_all()
    else:
        raise SystemExit(f"unknown split: {split}")

    if limit > 0:
        cases = cases[:limit]
    print(f"[runner] {provider_name} cond={condition} split={split} "
          f"n={len(cases)} dry_run={dry_run}")

    spec = PROVIDERS[provider_name]
    model = model_override or spec.default_model
    print(f"[runner] model={model}")

    if dry_run:
        # Estimate token usage without calling.
        sys_p = prompt_builder.system_prompt(condition)
        # Approximate: 1 token ≈ 4 chars for ID prompts.
        sys_tok = len(sys_p) // 4
        total_in = 0
        for c in cases:
            user_tok = len(c["query"]) // 4 + 5
            total_in += sys_tok + user_tok
        total_out = len(cases) * 80
        est = estimate_call_cost(spec, total_in, total_out)
        print(f"[runner][dry] approx input_tokens={total_in}, "
              f"output_tokens={total_out}, est_cost_usd={est:.4f}")
        return

    client, _ = _load_client(provider_name)
    run_dir = RUNS_DIR / _now_tag()
    run_dir.mkdir(parents=True, exist_ok=True)
    out_path = run_dir / f"{provider_name}_cond{condition}_{split}.jsonl"

    total_input_tokens = 0
    total_output_tokens = 0
    total_cached_tokens = 0
    total_cost = 0.0
    n_ok = 0
    n_fail = 0

    with out_path.open("w", encoding="utf-8") as f:
        for i, case in enumerate(cases, 1):
            messages = prompt_builder.build_messages(case["query"], condition)
            t0 = time.time()
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.0,
                    max_tokens=120,
                )
            except Exception as e:  # noqa: BLE001
                n_fail += 1
                f.write(json.dumps({
                    "id": case["id"], "gold": case["gold_label"],
                    "error": str(e), "split": case["split"],
                }, ensure_ascii=False) + "\n")
                print(f"  [{i}/{len(cases)}] {case['id']} ERROR: {e}")
                continue
            dt = time.time() - t0
            raw = resp.choices[0].message.content or ""
            parsed = label_parser.parse(raw)

            usage = getattr(resp, "usage", None)
            in_tok = getattr(usage, "prompt_tokens", 0) if usage else 0
            out_tok = getattr(usage, "completion_tokens", 0) if usage else 0
            # DeepSeek + Kimi expose cached count in `prompt_cache_hit_tokens`
            # or similar fields on the raw response — we try a few names.
            cached_tok = 0
            if usage:
                for attr in ("prompt_cache_hit_tokens",
                             "cached_tokens",
                             "prompt_tokens_cached"):
                    v = getattr(usage, attr, None)
                    if v:
                        cached_tok = v
                        break

            cost = estimate_call_cost(spec, in_tok, out_tok, cached_tok)
            total_input_tokens += in_tok
            total_output_tokens += out_tok
            total_cached_tokens += cached_tok
            total_cost += cost

            ok = parsed["label"] == case["gold_label"]
            n_ok += int(ok)
            row = {
                "id": case["id"],
                "split": case["split"],
                "gold": case["gold_label"],
                "predicted": parsed["label"],
                "alasan": parsed["alasan"],
                "parse_status": parsed["parse_status"],
                "match": ok,
                "input_tokens": in_tok,
                "output_tokens": out_tok,
                "cached_tokens": cached_tok,
                "cost_usd": round(cost, 6),
                "latency_sec": round(dt, 3),
                "raw": raw[:400],
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            print(f"  [{i}/{len(cases)}] {case['id']} "
                  f"gold={case['gold_label']} pred={parsed['label']} "
                  f"{'OK' if ok else 'MISS'} "
                  f"in={in_tok} out={out_tok} "
                  f"cost=${cost:.5f}")

            if sleep_sec > 0:
                time.sleep(sleep_sec)

    summary = {
        "provider": provider_name,
        "model": model,
        "condition": condition,
        "split": split,
        "n_cases": len(cases),
        "n_ok": n_ok,
        "n_fail": n_fail,
        "accuracy": (n_ok / max(1, len(cases) - n_fail)),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_cached_tokens": total_cached_tokens,
        "total_cost_usd": round(total_cost, 6),
        "output_file": str(out_path.relative_to(_EXP_ROOT.parents[1])),
    }
    summary_path = out_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    print()
    print(f"[runner] DONE. accuracy={summary['accuracy']:.3f} "
          f"cost=${summary['total_cost_usd']:.4f} "
          f"({summary['total_input_tokens']} in / "
          f"{summary['total_output_tokens']} out tokens)")
    print(f"[runner] {out_path}")
    print(f"[runner] {summary_path}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--provider", required=True, choices=list(PROVIDERS))
    p.add_argument("--condition", type=int, default=1, choices=[1, 2, 3])
    p.add_argument("--split", default="dev", choices=["dev", "test", "all"])
    p.add_argument("--limit", type=int, default=5,
                   help="Cap number of cases (0 = unlimited).")
    p.add_argument("--model", default=None, help="Override default model.")
    p.add_argument("--dry-run", action="store_true",
                   help="Estimate token / cost without calling API.")
    p.add_argument("--sleep", type=float, default=0.0,
                   help="Seconds to sleep between calls (rate limit safety).")
    args = p.parse_args()

    run(args.provider, args.condition, args.split, args.limit,
        args.model, args.dry_run, args.sleep)


if __name__ == "__main__":
    main()
