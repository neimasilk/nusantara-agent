"""Hard Cases Analysis: Deep dive into 12 cases where all 3 systems fail.

Output untuk section Error Analysis di paper.
"""

import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple, Counter
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]

# Input paths
COMP_PATH = ROOT / "experiments" / "09_ablation_study" / "statistical_comparison_3way_2026-02-19.json"
DATASET_PATH = ROOT / "data" / "processed" / "gold_standard" / "gs_active_cases.json"

RESULT_PATHS = {
    "asp_only": ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_only_2026-02-19.json",
    "ollama": ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_llm_2026-02-19.json",
    "deepseek": ROOT / "experiments" / "09_ablation_study" / "results_deepseek_asp_llm_2026-02-19.json",
}

LABELS = ("A", "B", "C", "D")


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _to_case_map(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        case_id = str(item.get("id", "")).strip()
        if not case_id:
            continue
        out[case_id] = item
    return out


def _detect_domain(query: str, case_id: str) -> str:
    """Detect domain from query text or case ID."""
    query_lower = query.lower()
    
    # Check case ID prefix
    if case_id.startswith("CS-MIN"):
        return "Minangkabau"
    elif case_id.startswith("CS-JAW"):
        return "Jawa"
    elif case_id.startswith("CS-BAL"):
        return "Bali"
    elif case_id.startswith("CS-LIN"):
        return "Lintas-Daerah"
    
    # Check keywords in query
    minang_keywords = ["minang", "minangkabau", "nagari", "mamak", "kaum", "ulayat", "pusako"]
    jawa_keywords = ["jawa", "adat jawa", "javanese", "gotong royong", "musyawarah", "pengajian"]
    bali_keywords = ["bali", "balinese", "adat bali", "druwe", "krama", "desa pakraman"]
    
    if any(kw in query_lower for kw in minang_keywords):
        return "Minangkabau"
    elif any(kw in query_lower for kw in jawa_keywords):
        return "Jawa"
    elif any(kw in query_lower for kw in bali_keywords):
        return "Bali"
    
    return "General/Unknown"


def _categorize_failure_pattern(gold: str, preds: Dict[str, str]) -> str:
    """Categorize the failure pattern."""
    pred_set = set(preds.values())
    
    # All three predict the same wrong label
    if len(pred_set) == 1:
        wrong_pred = list(pred_set)[0]
        if gold == "C" and wrong_pred == "B":
            return "Conflict_misclassified_as_Adat"
        elif gold == "C" and wrong_pred == "A":
            return "Conflict_misclassified_as_National"
        elif gold == "A" and wrong_pred == "B":
            return "National_misclassified_as_Adat"
        elif gold == "A" and wrong_pred == "C":
            return "National_misclassified_as_Conflict"
        elif gold == "B" and wrong_pred == "A":
            return "Adat_misclassified_as_National"
        elif gold == "B" and wrong_pred == "C":
            return "Adat_misclassified_as_Conflict"
        elif gold == "D":
            return "LabelD_always_fails"
        else:
            return f"All_same_wrong_{gold}_as_{wrong_pred}"
    
    # Two agree, one different
    elif len(pred_set) == 2:
        from collections import Counter
        pred_counts = Counter(preds.values())
        majority = pred_counts.most_common(1)[0][0]
        minority = [k for k in pred_set if k != majority][0]
        return f"Split_{gold}_majority_{majority}_minority_{minority}"
    
    # All three different
    else:
        return f"Complete_split_{gold}"


def _extract_key_issue(query: str) -> str:
    """Extract key issue from query text."""
    # Truncate to first 100 chars and look for key conflict keywords
    query_lower = query.lower()
    
    conflict_indicators = [
        "konflik", "bertentangan", "mendahului", "melanggar", "tidak sah",
        "dibatalkan", "perselisihan", "sengketa", "klaim", "gugatan"
    ]
    
    adat_indicators = [
        "adat", "kebiasaan", "tradisi", "istiadat", "hukum adat",
        "adat istiadat", "musyawarah", "mufakat"
    ]
    
    national_indicators = [
        "undang-undang", "peraturan", "perundang-undangan", "hukum nasional",
        "catatan sipil", "sertifikat", "hak milik", "bpn"
    ]
    
    signals = []
    if any(kw in query_lower for kw in conflict_indicators):
        signals.append("conflict")
    if any(kw in query_lower for kw in adat_indicators):
        signals.append("adat")
    if any(kw in query_lower for kw in national_indicators):
        signals.append("national")
    
    return "+".join(signals) if signals else "unclear"


def _get_first_n_words(text: str, n: int = 50) -> str:
    """Get first n words from text."""
    words = text.split()
    if len(words) <= n:
        return text
    return " ".join(words[:n]) + "..."


def analyze_hard_cases() -> Dict[str, Any]:
    """Analyze the 12 hard cases where all 3 systems fail."""
    
    # Load data
    comp_data = _load_json(COMP_PATH)
    dataset = _load_json(DATASET_PATH)
    
    # Load results from all 3 modes
    results = {}
    for name, path in RESULT_PATHS.items():
        data = _load_json(path)
        results[name] = _to_case_map(data.get("results", []))
    
    # Get the 12 hard case IDs
    cross_agreement = comp_data.get("cross_model_agreement", {})
    hard_case_ids = cross_agreement.get("all_agree", {}).get("wrong_cases", [])
    
    if len(hard_case_ids) != 12:
        print(f"[WARN] Expected 12 hard cases, found {len(hard_case_ids)}")
    
    # Build dataset lookup
    dataset_map = {str(d.get("id", "")): d for d in dataset if d.get("id")}
    
    # Analyze each hard case
    hard_cases = []
    gold_distribution = Counter()
    failure_patterns = Counter()
    domains = Counter()
    key_issues = Counter()
    
    for case_id in hard_case_ids:
        # Get predictions from each mode
        preds = {
            "asp_only": results["asp_only"].get(case_id, {}).get("predicted", "?"),
            "ollama": results["ollama"].get(case_id, {}).get("predicted", "?"),
            "deepseek": results["deepseek"].get(case_id, {}).get("predicted", "?"),
        }
        
        # Get gold label (should be same across all)
        gold = results["asp_only"].get(case_id, {}).get("gold", "?")
        
        # Get query from dataset
        case_data = dataset_map.get(case_id, {})
        query = case_data.get("query", "")
        query_snippet = _get_first_n_words(query, 50)
        
        # Detect domain
        domain = _detect_domain(query, case_id)
        
        # Categorize failure
        failure_pattern = _categorize_failure_pattern(gold, preds)
        
        # Extract key issue
        key_issue = _extract_key_issue(query)
        
        # Get reasoning snippets from each mode
        reasonings = {
            name: results[name].get(case_id, {}).get("reasoning", "")[:200]
            for name in RESULT_PATHS.keys()
        }
        
        case_analysis = {
            "case_id": case_id,
            "gold_label": gold,
            "predictions": preds,
            "domain": domain,
            "query_snippet": query_snippet,
            "key_issue_signals": key_issue,
            "failure_pattern": failure_pattern,
            "reasoning_snippets": reasonings,
        }
        hard_cases.append(case_analysis)
        
        # Update counters
        gold_distribution[gold] += 1
        failure_patterns[failure_pattern] += 1
        domains[domain] += 1
        key_issues[key_issue] += 1
    
    # Generate summary
    summary = {
        "total_hard_cases": len(hard_cases),
        "gold_distribution": dict(gold_distribution),
        "failure_patterns": dict(failure_patterns),
        "domain_distribution": dict(domains),
        "key_issue_signals": dict(key_issues),
    }
    
    # Generate recommendations
    recommendations = _generate_recommendations(summary, hard_cases)
    
    report = {
        "date": date.today().isoformat(),
        "summary": summary,
        "hard_cases": hard_cases,
        "recommendations": recommendations,
    }
    
    return report


def _generate_recommendations(summary: Dict[str, Any], hard_cases: List[Dict[str, Any]]) -> List[str]:
    """Generate recommendations based on analysis."""
    recommendations = []
    
    gold_dist = summary.get("gold_distribution", {})
    patterns = summary.get("failure_patterns", {})
    domains = summary.get("domain_distribution", {})
    
    # Check gold label distribution
    if gold_dist.get("C", 0) >= 5:
        recommendations.append(
            f"CONFLICT (C) cases are over-represented in failures ({gold_dist.get('C', 0)}/12). "
            "Need better conflict detection rules or improved prompt engineering for ambiguous cases."
        )
    
    if gold_dist.get("D", 0) > 0:
        recommendations.append(
            f"Label D (Error/Unclear) always fails ({gold_dist.get('D', 0)} cases). "
            "Need explicit training examples for edge cases and clearer criteria for D classification."
        )
    
    # Check failure patterns
    if patterns.get("Conflict_misclassified_as_Adat", 0) > 0:
        recommendations.append(
            f"{patterns.get('Conflict_misclassified_as_Adat', 0)} cases: Gold=C predicted as B. "
            "Systems struggle to detect conflicts when adat elements are prominent. "
            "Consider stronger conflict keyword detection."
        )
    
    if patterns.get("National_misclassified_as_Adat", 0) > 0:
        recommendations.append(
            f"{patterns.get('National_misclassified_as_Adat', 0)} cases: Gold=A predicted as B. "
            "Systems over-prioritize adat when both national and adat elements present."
        )
    
    # Check domain distribution
    if domains.get("Minangkabau", 0) >= 5:
        recommendations.append(
            f"Minangkabau cases over-represented ({domains.get('Minangkabau', 0)}/12). "
            "Consider domain-specific rule refinement for Minangkabau land/inheritance cases."
        )
    
    # General recommendations
    recommendations.append(
        "All 3 systems fail together on these cases, indicating fundamental limitations "
        "in current rule set and/or prompt design."
    )
    
    recommendations.append(
        "Recommendation: Add these 12 cases to training/validation set for prompt engineering "
        "and evaluate impact of additional symbolic rules."
    )
    
    return recommendations


def _print_report(report: Dict[str, Any]) -> None:
    """Print formatted report."""
    print("=" * 80)
    print("HARD CASES ANALYSIS: 12 Cases Where All 3 Systems Fail")
    print("=" * 80)
    print()
    
    summary = report["summary"]
    print("SUMMARY")
    print("-" * 80)
    print(f"Total hard cases analyzed: {summary['total_hard_cases']}")
    print()
    
    print("Gold Label Distribution in Hard Cases:")
    for label, count in sorted(summary["gold_distribution"].items()):
        pct = 100 * count / summary['total_hard_cases']
        print(f"  {label}: {count} cases ({pct:.1f}%)")
    print()
    
    print("Failure Patterns:")
    for pattern, count in sorted(summary["failure_patterns"].items(), key=lambda x: -x[1]):
        print(f"  {pattern}: {count} cases")
    print()
    
    print("Domain Distribution:")
    for domain, count in sorted(summary["domain_distribution"].items(), key=lambda x: -x[1]):
        pct = 100 * count / summary['total_hard_cases']
        print(f"  {domain}: {count} cases ({pct:.1f}%)")
    print()
    
    print("Key Issue Signals:")
    for issue, count in sorted(summary["key_issue_signals"].items(), key=lambda x: -x[1]):
        print(f"  {issue}: {count} cases")
    print()
    
    print("-" * 80)
    print("DETAILED CASE ANALYSIS")
    print("-" * 80)
    
    for i, case in enumerate(report["hard_cases"], 1):
        print(f"\n[{i:2d}] {case['case_id']}")
        print(f"     Domain: {case['domain']}")
        print(f"     Gold: {case['gold_label']} | "
              f"ASP-only: {case['predictions']['asp_only']} | "
              f"Ollama: {case['predictions']['ollama']} | "
              f"DeepSeek: {case['predictions']['deepseek']}")
        print(f"     Pattern: {case['failure_pattern']}")
        print(f"     Signals: {case['key_issue_signals']}")
        print(f"     Query: {case['query_snippet'][:80]}...")
    
    print()
    print("-" * 80)
    print("RECOMMENDATIONS")
    print("-" * 80)
    for i, rec in enumerate(report["recommendations"], 1):
        print(f"{i}. {rec}")
    print()


def main() -> int:
    """Main entry point."""
    print("Analyzing hard cases where all 3 systems fail...")
    print()
    
    report = analyze_hard_cases()
    _print_report(report)
    
    # Save output
    out_path = ROOT / "experiments" / "09_ablation_study" / f"hard_cases_analysis_{report['date']}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Saved: {out_path}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
