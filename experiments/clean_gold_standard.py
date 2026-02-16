"""
Remove Ahli-3 from gold standard and recompute labels.
Ahli-3 confirmed as under-qualified rater (S1 level, not domain expert).

Input:  data/processed/gold_standard/gs_active_cases.json (24 cases, 3 raters)
Output: data/processed/gold_standard/gs_active_cases.json (updated, 2 raters)
        data/processed/gold_standard/gs_active_cases_backup_3raters.json (backup)
"""

import json
import shutil
from pathlib import Path

INPUT = Path("data/processed/gold_standard/gs_active_cases.json")
BACKUP = Path("data/processed/gold_standard/gs_active_cases_backup_3raters.json")


def main():
    # Backup original
    shutil.copy2(INPUT, BACKUP)
    print(f"Backup saved to {BACKUP}")

    with open(INPUT, "r", encoding="utf-8") as f:
        cases = json.load(f)

    agreed = []
    disputed = []

    for case in cases:
        votes = case["expert_votes"]
        v1 = votes["ahli1"]
        v2 = votes["ahli2"]

        # Remove ahli3
        case["expert_votes"] = {"ahli1": v1, "ahli2": v2}

        if v1 == v2:
            case["gold_label"] = v1
            case["consensus"] = "unanimous"
            agreed.append(case["id"])
        else:
            case["gold_label"] = "DISPUTED"
            case["consensus"] = "disputed"
            disputed.append(case["id"])

    with open(INPUT, "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)

    print(f"\nResults:")
    print(f"  Total cases: {len(cases)}")
    print(f"  Agreed (ahli1 == ahli2): {len(agreed)}")
    print(f"  Disputed (ahli1 != ahli2): {len(disputed)}")
    print(f"\nAgreed cases: {agreed}")
    print(f"Disputed cases: {disputed}")
    print(f"\nGold standard updated at {INPUT}")


if __name__ == "__main__":
    main()
