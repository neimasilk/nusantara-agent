import json
import os
from collections import Counter
import glob

def load_cases(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def calculate_derived_label(votes):
    valid_votes = [v for v in votes.values() if v and v != "N/A"]
    if not valid_votes:
        return "NO_VOTES", "NO_VOTES"
    counts = Counter(valid_votes)
    most_common = counts.most_common(2)
    top_label, top_count = most_common[0]
    total_votes = len(valid_votes)
    if len(most_common) > 1 and most_common[1][1] == top_count:
        return "SPLIT", "TIE"
    status = "MAJORITY"
    if top_count == total_votes:
        status = "UNANIMOUS"
    return top_label, status

def main():
    # 1. Audit Active Cases
    active_file = "data/processed/gold_standard/gs_active_cases.json"
    print(f"--- Auditing {active_file} ---")
    cases = load_cases(active_file)
    summary = {
        "total_cases": 0,
        "mismatches": 0,
        "ahli4_coverage": 0,
        "consensus_stats": {"UNANIMOUS": 0, "MAJORITY": 0, "TIE": 0},
        "split_resolved": []
    }
    
    # Check specific split cases
    target_splits = ["CS-MIN-005", "CS-MIN-015"]
    
    for case in cases:
        summary["total_cases"] += 1
        votes = case.get("expert_votes", {})
        ahli4 = votes.get("ahli4")
        
        if ahli4 and ahli4 != "N/A":
            summary["ahli4_coverage"] += 1
            
        derived, status = calculate_derived_label(votes)
        gold = case.get("gold_label")
        
        if status == "TIE": summary["consensus_stats"]["TIE"] += 1
        elif status == "UNANIMOUS": summary["consensus_stats"]["UNANIMOUS"] += 1
        elif status == "MAJORITY": summary["consensus_stats"]["MAJORITY"] += 1
            
        is_mismatch = (derived != "SPLIT" and derived != gold) or (derived == "SPLIT" and gold != "SPLIT")
        if is_mismatch:
            summary["mismatches"] += 1
            print(f"Mismatch: {case['id']} Gold:{gold} Derived:{derived} Votes:{votes}")

        if case['id'] in target_splits:
            summary["split_resolved"].append({
                "id": case['id'],
                "resolved": status != "TIE",
                "current_status": status,
                "votes": votes
            })

    print(json.dumps(summary, indent=2))

    # 2. Trace 82 Claims
    print("\n--- Tracing 82 Claims ---")
    annotation_files = glob.glob("data/processed/gold_standard/annotations/*.json")
    # Group by case ID (assuming format GS-XXXX__annYY.json)
    case_ids = set()
    for f in annotation_files:
        basename = os.path.basename(f)
        # Assuming filename GS-0001__ann01.json -> GS-0001 is not the ID format in active cases (CS-XXX-YYY)
        # Wait, let's check the format.
        # The active cases have IDs like CS-MIN-011.
        # The annotation files are GS-0001...
        # We need to map them or count them.
        case_id = basename.split('__')[0]
        case_ids.add(case_id)
    
    print(f"Total unique case IDs in annotations folder: {len(case_ids)}")
    print(f"First 5 case IDs: {sorted(list(case_ids))[:5]}")
    print(f"Last 5 case IDs: {sorted(list(case_ids))[-5:]}")

if __name__ == "__main__":
    main()
