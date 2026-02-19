import json
import os
import sys
from collections import defaultdict
from typing import Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Complete GS-* domain mapping based on query content analysis
_GS_DOMAIN_MAP = {
    # Minangkabau (pusako, mamak, matrilineal)
    1: "Minangkabau", 2: "Minangkabau", 3: "Minangkabau",
    4: "Minangkabau",  # pusako context (darurat adat)
    5: "Minangkabau", 6: "Minangkabau",
    25: "Minangkabau", 26: "Minangkabau",
    33: "Nasional",  # KUHPerdata bagian istri
    34: "Nasional",  # KUHPerdata pembagian harta
    35: "Minangkabau", 36: "Minangkabau", 37: "Minangkabau",
    38: "Minangkabau", 39: "Minangkabau", 40: "Minangkabau",
    41: "Minangkabau",
    # Bali (sentana, druwe, rajeg, nyentana, pakraman)
    7: "Bali", 8: "Bali",  # sanggah/pengabenan = Bali ritual
    9: "Bali", 10: "Bali",  # sentana rajeg context
    11: "Bali", 12: "Bali", 13: "Bali",  # yadnya = Bali
    14: "Bali",
    27: "Bali", 28: "Bali", 29: "Bali",
    45: "Bali", 46: "Bali",  # sentana/Bali inheritance context
    48: "Bali", 49: "Bali",
    102: "Bali", 103: "Bali",
    # Jawa (gono-gini, bilateral, sepikul segendongan)
    15: "Jawa", 16: "Jawa", 17: "Jawa", 18: "Jawa",
    19: "Jawa", 20: "Jawa", 21: "Jawa", 22: "Jawa",
    23: "Jawa", 24: "Jawa",
    30: "Jawa", 31: "Jawa", 32: "Jawa",
    # Nasional (KUHPerdata)
    42: "Nasional",
    # D-label cases (insufficient info, Jawa context)
    54: "Jawa", 55: "Jawa",
}


def get_domain(case_id):
    """Map case ID to domain."""
    if case_id.startswith("CS-MIN-"):
        return "Minangkabau"
    if case_id.startswith("CS-BAL-"):
        return "Bali"
    if case_id.startswith("CS-JAW-"):
        return "Jawa"
    if case_id.startswith("CS-NAS-"):
        return "Nasional"
    if case_id.startswith("CS-LIN-"):
        return "Lintas"

    if case_id.startswith("GS-"):
        try:
            num = int(case_id.split("-")[1])
            return _GS_DOMAIN_MAP.get(num, "Unknown")
        except (ValueError, IndexError):
            pass

    return "Unknown"


def _wilson_interval(successes: int, total: int, z: float = 1.96) -> Tuple[float, float]:
    if total <= 0:
        return 0.0, 0.0
    phat = successes / total
    z2 = z * z
    denom = 1.0 + (z2 / total)
    center = (phat + (z2 / (2.0 * total))) / denom
    margin = (z / denom) * ((phat * (1.0 - phat) / total + z2 / (4.0 * total * total)) ** 0.5)
    return max(0.0, center - margin), min(1.0, center + margin)

def analyze_file(file_path):
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = data.get("results", [])
    if not results:
        return None

    LABELS = ["A", "B", "C", "D"]
    domain_stats = defaultdict(lambda: {
        "correct": 0, "total": 0,
        "gold_list": [], "pred_list": [],
        "confusion": defaultdict(int),
    })

    for item in results:
        cid = item["id"]
        gold = item["gold"]
        pred = item["predicted"]
        domain = get_domain(cid)

        domain_stats[domain]["total"] += 1
        if item.get("match", pred == gold):
            domain_stats[domain]["correct"] += 1
        domain_stats[domain]["gold_list"].append(gold)
        domain_stats[domain]["pred_list"].append(pred)
        domain_stats[domain]["confusion"][(gold, pred)] += 1

    formatted = {}
    for domain, stats in domain_stats.items():
        total = stats["total"]
        correct = stats["correct"]
        acc = correct / total if total > 0 else 0
        ci_low, ci_high = _wilson_interval(correct, total)

        # Per-label metrics
        per_label = {}
        for label in LABELS:
            tp = sum(1 for g, p in zip(stats["gold_list"], stats["pred_list"]) if g == label and p == label)
            fp = sum(1 for g, p in zip(stats["gold_list"], stats["pred_list"]) if g != label and p == label)
            fn = sum(1 for g, p in zip(stats["gold_list"], stats["pred_list"]) if g == label and p != label)
            support = sum(1 for g in stats["gold_list"] if g == label)
            per_label[label] = {
                "support": support,
                "precision": tp / (tp + fp) if (tp + fp) > 0 else 0.0,
                "recall": tp / (tp + fn) if (tp + fn) > 0 else 0.0,
            }

        formatted[domain] = {
            "accuracy": acc,
            "correct": correct,
            "total": total,
            "wilson_95ci": [ci_low, ci_high],
            "per_label": per_label,
            "confusion_matrix": {f"{g}->{p}": count for (g, p), count in stats["confusion"].items()},
        }
    return formatted

def main():
    base_dir = os.path.join(ROOT, "experiments", "09_ablation_study")
    files = {
        "ASP-only": "results_dual_asp_only_2026-02-19.json",
        "ASP+Ollama": "results_dual_asp_llm_2026-02-19.json",
        "ASP+DeepSeek": "results_deepseek_asp_llm_2026-02-19.json",
    }

    all_analysis = {}

    for mode, filename in files.items():
        path = os.path.join(base_dir, filename)
        print(f"Analyzing {mode} ({filename})...")
        analysis = analyze_file(path)
        if analysis:
            all_analysis[mode] = analysis
        else:
            print(f"  Warning: not found or no results.")

    # Save results
    output_path = os.path.join(base_dir, "domain_analysis_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_analysis, f, indent=2, ensure_ascii=False)

    # Collect all domains
    all_domains = set()
    for mode_data in all_analysis.values():
        all_domains.update(mode_data.keys())

    preferred_order = ["Minangkabau", "Bali", "Jawa", "Nasional", "Lintas"]
    remaining = sorted(d for d in all_domains if d not in preferred_order)
    ordered_domains = [d for d in preferred_order if d in all_domains] + remaining

    mode_names = [m for m in files.keys() if m in all_analysis]

    # --- Table 1: Per-domain accuracy ---
    print("\n=== Per-Domain Accuracy ===")
    hdr = f"{'Domain':<15} | {'N':>3}"
    for m in mode_names:
        hdr += f" | {m:>16}"
    print(hdr)
    print("-" * len(hdr))

    totals = {m: {"correct": 0, "total": 0} for m in mode_names}
    for dom in ordered_domains:
        n = 0
        cells = []
        for m in mode_names:
            if m in all_analysis and dom in all_analysis[m]:
                s = all_analysis[m][dom]
                n = s["total"]
                cells.append(f"{s['accuracy']:5.1%} ({s['correct']:2d}/{s['total']:2d})")
                totals[m]["correct"] += s["correct"]
                totals[m]["total"] += s["total"]
            else:
                cells.append(f"{'N/A':>16}")
        row = f"{dom:<15} | {n:3d}"
        for c in cells:
            row += f" | {c:>16}"
        print(row)

    # Overall
    print("-" * len(hdr))
    row = f"{'OVERALL':<15} | {totals[mode_names[0]]['total']:3d}"
    for m in mode_names:
        t = totals[m]
        acc = t["correct"] / t["total"] if t["total"] > 0 else 0
        row += f" | {acc:5.1%} ({t['correct']:2d}/{t['total']:2d})"
    print(row)

    # --- Table 2: Per-domain gold label distribution ---
    print("\n=== Gold Label Distribution per Domain ===")
    # Use first available mode to get distribution
    first_mode = mode_names[0]
    hdr2 = f"{'Domain':<15} | {'A':>3} | {'B':>3} | {'C':>3} | {'D':>3} | {'Total':>5}"
    print(hdr2)
    print("-" * len(hdr2))
    for dom in ordered_domains:
        if dom in all_analysis[first_mode]:
            pl = all_analysis[first_mode][dom].get("per_label", {})
            a = pl.get("A", {}).get("support", 0)
            b = pl.get("B", {}).get("support", 0)
            c = pl.get("C", {}).get("support", 0)
            d = pl.get("D", {}).get("support", 0)
            print(f"{dom:<15} | {a:3d} | {b:3d} | {c:3d} | {d:3d} | {a+b+c+d:5d}")

    # --- Table 3: Per-domain confusion highlights ---
    print("\n=== Dominant Error Patterns per Domain ===")
    for dom in ordered_domains:
        for m in mode_names:
            if m in all_analysis and dom in all_analysis[m]:
                cm = all_analysis[m][dom].get("confusion_matrix", {})
                errors = {k: v for k, v in cm.items() if k.split("->")[0] != k.split("->")[1] and v > 0}
                if errors:
                    top = sorted(errors.items(), key=lambda x: -x[1])[:3]
                    err_str = ", ".join(f"{k}({v})" for k, v in top)
                    print(f"  {dom:<13} [{m:<12}]: {err_str}")

    print(f"\n[OK] Results saved to {output_path}")

if __name__ == "__main__":
    main()
