import json
import csv
import os
from collections import Counter
from datetime import datetime

def load_cases(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_derived_label(votes):
    # Filter out empty votes
    valid_votes = [v for v in votes.values() if v and v != "N/A"]
    
    if not valid_votes:
        return "NO_VOTES", "NO_VOTES"
    
    counts = Counter(valid_votes)
    most_common = counts.most_common(2)
    
    top_label, top_count = most_common[0]
    total_votes = len(valid_votes)
    
    # Check for tie
    if len(most_common) > 1 and most_common[1][1] == top_count:
        return "SPLIT", "TIE"
    
    status = "MAJORITY"
    if top_count == total_votes:
        status = "UNANIMOUS"
        
    return top_label, status

def audit_cases(cases):
    results = []
    summary = {
        "total_cases": 0,
        "mismatches": 0,
        "ahli4_coverage": 0,
        "consensus_stats": {"UNANIMOUS": 0, "MAJORITY": 0, "TIE": 0}
    }
    
    for case in cases:
        summary["total_cases"] += 1
        
        votes = case.get("expert_votes", {})
        ahli4_vote = votes.get("ahli4")
        if ahli4_vote and ahli4_vote != "N/A":
            summary["ahli4_coverage"] += 1
            
        derived_label, consensus_status = calculate_derived_label(votes)
        
        # Update stats
        if consensus_status == "TIE":
            summary["consensus_stats"]["TIE"] += 1
        elif consensus_status == "UNANIMOUS":
            summary["consensus_stats"]["UNANIMOUS"] += 1
        elif consensus_status == "MAJORITY":
            summary["consensus_stats"]["MAJORITY"] += 1
            
        gold_label = case.get("gold_label")
        is_mismatch = (derived_label != "SPLIT" and derived_label != gold_label) or \
                      (derived_label == "SPLIT" and gold_label != "SPLIT")
        
        if is_mismatch:
            summary["mismatches"] += 1
            
        results.append({
            "id": case.get("id"),
            "gold_label": gold_label,
            "derived_label": derived_label,
            "consensus_type": consensus_status,
            "is_mismatch": is_mismatch,
            "ahli4_vote": ahli4_vote if ahli4_vote else "N/A",
            "votes": json.dumps(votes)
        })
        
    return results, summary

def main():
    input_file = "data/processed/gold_standard/gs_active_cases.json"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    cases = load_cases(input_file)
    results, summary = audit_cases(cases)
    
    # Print summary to stdout for capture
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
