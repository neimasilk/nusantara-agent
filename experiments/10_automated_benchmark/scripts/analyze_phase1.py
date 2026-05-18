"""Statistical analysis of Phase 1 multi-LLM benchmark runs.

Loads the most recent jsonl per (provider, condition) under runs/,
computes:
  - Per-(model, condition) accuracy + Wilson 95% CI
  - Per-label precision / recall / F1
  - Per-domain accuracy breakdown
  - McNemar test pairwise across all (model, condition) combinations
  - Fleiss kappa across the 6 LLM conditions (do LLMs agree with each other?)
  - Cohen kappa for each (model, condition) vs gold
  - Hard-case analysis: cases that fail across all 6 conditions

Pure-stdlib + numpy/scipy if available. Falls back to manual computations.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
ANALYSIS = ROOT / "analysis"
ANALYSIS.mkdir(exist_ok=True, parents=True)

CASE_DOMAIN_MAP = (ROOT.parents[1]
                   / "experiments" / "09_ablation_study"
                   / "case_id_domain_map.json")

LABELS = ["A", "B", "C", "D"]


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    spread = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - spread), min(1.0, centre + spread))


def load_run(jsonl_path: Path) -> list[dict]:
    out = []
    for line in jsonl_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        out.append(json.loads(line))
    return out


def find_latest_runs() -> dict[tuple[str, int], Path]:
    """For each (provider, condition) pair, find the most recent jsonl."""
    by_key: dict[tuple[str, int], Path] = {}
    for f in sorted(RUNS.glob("*/*.jsonl")):
        name = f.stem
        if "_all" not in name:
            continue
        parts = name.split("_")
        provider = parts[0]
        cond_str = parts[1]
        if not cond_str.startswith("cond"):
            continue
        cond = int(cond_str.replace("cond", ""))
        by_key[(provider, cond)] = f  # later iterations overwrite
    return by_key


def confusion(rows: list[dict]) -> dict:
    cm = {g: Counter() for g in LABELS}
    for r in rows:
        if r.get("error"):
            continue
        g = r.get("gold")
        p = r.get("predicted")
        if g in LABELS and p in LABELS:
            cm[g][p] += 1
    return cm


def per_label_prf(cm: dict) -> dict:
    out = {}
    for L in LABELS:
        tp = cm[L][L]
        fn = sum(cm[L][o] for o in LABELS if o != L)
        fp = sum(cm[g][L] for g in LABELS if g != L)
        support = tp + fn
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        out[L] = {"precision": round(prec, 3),
                  "recall": round(rec, 3),
                  "f1": round(f1, 3),
                  "support": support}
    return out


def mcnemar(rows_a: list[dict], rows_b: list[dict]) -> dict:
    """Exact binomial McNemar test for paired predictions vs gold."""
    by_id_a = {r["id"]: r for r in rows_a if not r.get("error")}
    by_id_b = {r["id"]: r for r in rows_b if not r.get("error")}
    common = set(by_id_a) & set(by_id_b)
    b = c = 0  # A right & B wrong / A wrong & B right
    for cid in common:
        a_ok = by_id_a[cid].get("match")
        b_ok = by_id_b[cid].get("match")
        if a_ok and not b_ok:
            b += 1
        elif b_ok and not a_ok:
            c += 1
    n = b + c
    if n == 0:
        return {"n_disagree": 0, "b": b, "c": c, "p_value": 1.0}

    # Two-sided exact binomial: 2 * P(X <= min(b,c) | n, 0.5)
    k = min(b, c)
    p = 0.0
    for i in range(k + 1):
        p += math.comb(n, i) * (0.5 ** n)
    p_two = min(1.0, 2 * p)
    return {"n_disagree": n, "b": b, "c": c, "p_value": round(p_two, 5)}


def fleiss_kappa(items_x_raters: list[list[str]]) -> float:
    """Compute Fleiss kappa given per-case rater labels.

    items_x_raters[i] = list of labels assigned to case i (one per rater).
    """
    n_cases = len(items_x_raters)
    if n_cases == 0:
        return float("nan")
    n_raters = len(items_x_raters[0])
    if n_raters < 2:
        return float("nan")

    # Build n_ij matrix: case i × category j -> count
    cats = sorted({lbl for row in items_x_raters for lbl in row})
    cat_index = {c: i for i, c in enumerate(cats)}
    K = len(cats)
    N = n_cases

    p_j = [0.0] * K
    P_i = [0.0] * N
    for i, row in enumerate(items_x_raters):
        counts = [0] * K
        for lbl in row:
            counts[cat_index[lbl]] += 1
        for j in range(K):
            p_j[j] += counts[j]
        P_i[i] = (sum(c * c for c in counts) - n_raters) / (n_raters * (n_raters - 1))

    total_assignments = n_raters * N
    p_j = [pj / total_assignments for pj in p_j]
    P_bar = sum(P_i) / N
    Pe_bar = sum(pj * pj for pj in p_j)

    if Pe_bar >= 1.0:
        return float("nan")
    return (P_bar - Pe_bar) / (1 - Pe_bar)


def cohen_kappa(rows: list[dict]) -> float:
    pairs = [(r["gold"], r["predicted"]) for r in rows
             if not r.get("error")
             and r.get("gold") in LABELS
             and r.get("predicted") in LABELS]
    if not pairs:
        return float("nan")
    cats = LABELS
    n = len(pairs)
    obs = sum(1 for g, p in pairs if g == p) / n
    g_counts = Counter(g for g, _ in pairs)
    p_counts = Counter(p for _, p in pairs)
    exp = sum((g_counts[c] / n) * (p_counts[c] / n) for c in cats)
    if exp >= 1.0:
        return float("nan")
    return (obs - exp) / (1 - exp)


def per_domain(rows: list[dict], domain_map: dict) -> dict:
    by_dom: dict[str, list[bool]] = defaultdict(list)
    for r in rows:
        if r.get("error"):
            continue
        d = domain_map.get(r["id"], "Unknown")
        ok = r.get("match", False)
        by_dom[d].append(ok)
    return {d: {"n": len(v),
                "accuracy": round(sum(v) / len(v), 3) if v else 0.0}
            for d, v in by_dom.items()}


def main() -> None:
    if not CASE_DOMAIN_MAP.exists():
        domain_map = {}
    else:
        domain_map = json.loads(CASE_DOMAIN_MAP.read_text(encoding="utf-8"))

    keys_and_files = find_latest_runs()
    print(f"[analyze] Found {len(keys_and_files)} (provider, cond) runs")
    for k, v in keys_and_files.items():
        print(f"   {k}: {v.relative_to(ROOT)}")

    all_rows: dict[tuple[str, int], list[dict]] = {
        k: load_run(v) for k, v in keys_and_files.items()
    }

    summary: dict = {}
    for (prov, cond), rows in all_rows.items():
        rows_ok = [r for r in rows if not r.get("error")]
        n = len(rows_ok)
        n_correct = sum(1 for r in rows_ok if r.get("match"))
        acc = n_correct / n if n > 0 else 0.0
        lo, hi = wilson_ci(n_correct, n)
        prf = per_label_prf(confusion(rows_ok))
        dom = per_domain(rows_ok, domain_map)
        ck = cohen_kappa(rows_ok)
        summary[f"{prov}_cond{cond}"] = {
            "n_evaluated": n,
            "n_correct": n_correct,
            "accuracy": round(acc, 3),
            "wilson_95ci": (round(lo, 3), round(hi, 3)),
            "cohen_kappa_vs_gold": round(ck, 3) if not math.isnan(ck) else None,
            "per_label": prf,
            "per_domain": dom,
        }

    # Pairwise McNemar across every (model, cond) pair
    mcnemar_table: dict = {}
    keys = list(all_rows.keys())
    for a, b in combinations(keys, 2):
        mc = mcnemar(all_rows[a], all_rows[b])
        label = f"{a[0]}_cond{a[1]} vs {b[0]}_cond{b[1]}"
        mcnemar_table[label] = mc

    # Fleiss kappa across all 6 (model, cond) raters
    # Need to align on common case set.
    all_ids = set.intersection(*({r["id"] for r in rs if not r.get("error")}
                                 for rs in all_rows.values()))
    aligned = []
    aligned_with_gold = []
    for cid in sorted(all_ids):
        per_case = []
        for k in keys:
            for r in all_rows[k]:
                if r["id"] == cid and not r.get("error"):
                    per_case.append(r.get("predicted") or "X")
                    break
        if len(per_case) == len(keys):
            aligned.append(per_case)
            # Also include gold among raters for "do LLMs agree with gold?"
            gold = next((r["gold"] for r in all_rows[keys[0]]
                         if r["id"] == cid and not r.get("error")), None)
            if gold:
                aligned_with_gold.append(per_case + [gold])

    kappa_models_only = fleiss_kappa(aligned)
    kappa_with_gold = fleiss_kappa(aligned_with_gold)

    # Hard cases: where ALL 6 (model, cond) fail
    hard_cases = []
    for cid in sorted(all_ids):
        all_fail = True
        gold = None
        preds = {}
        for k in keys:
            for r in all_rows[k]:
                if r["id"] == cid and not r.get("error"):
                    if r.get("match"):
                        all_fail = False
                    gold = r["gold"]
                    preds[f"{k[0]}_cond{k[1]}"] = r.get("predicted")
                    break
        if all_fail:
            hard_cases.append({"id": cid, "gold": gold, "predictions": preds,
                               "domain": domain_map.get(cid, "Unknown")})

    out = {
        "summary": summary,
        "pairwise_mcnemar": mcnemar_table,
        "n_llm_conditions": len(keys),
        "fleiss_kappa_across_llm_conditions": round(kappa_models_only, 3),
        "fleiss_kappa_models_plus_gold": round(kappa_with_gold, 3),
        "hard_cases_all_fail": hard_cases,
        "n_hard_cases": len(hard_cases),
    }
    (ANALYSIS / "phase1_summary.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print()
    print("=" * 60)
    print("PHASE 1 SUMMARY")
    print("=" * 60)
    print()
    print(f"{'Run':<22} {'Acc':>6} {'Wilson 95% CI':>20}  {'kappa-gold':>7}")
    for k, v in summary.items():
        ci = v["wilson_95ci"]
        ck = v["cohen_kappa_vs_gold"]
        ck_s = f"{ck:.3f}" if ck is not None else "n/a"
        print(f"{k:<22} {v['accuracy']:>6.3f} "
              f"[{ci[0]:.3f}, {ci[1]:.3f}]  {ck_s:>7}")
    print()
    print(f"Fleiss kappa across {out['n_llm_conditions']} LLM conditions: "
          f"{out['fleiss_kappa_across_llm_conditions']}")
    print(f"Fleiss kappa with gold as extra rater: "
          f"{out['fleiss_kappa_models_plus_gold']}")
    print(f"Hard cases (all 6 fail): {out['n_hard_cases']}")
    print()
    print("Pairwise McNemar p-values (smallest first):")
    sorted_mc = sorted(mcnemar_table.items(), key=lambda kv: kv[1]["p_value"])
    for k, v in sorted_mc[:10]:
        print(f"   {k:<46} n_disagree={v['n_disagree']:>3} "
              f"p={v['p_value']:.4f}")
    print()
    print(f"[analyze] Wrote {ANALYSIS/'phase1_summary.json'}")


if __name__ == "__main__":
    main()
