"""
Compute Inter-Rater Agreement (IRA) for gold standard cases.
Task P-001 from simplified registry.

Input: data/processed/gold_standard/gs_active_cases.json
Output: Inter-rater agreement metrics (Fleiss' Kappa, Krippendorff's Alpha, % agreement)
"""

import json
import sys
from collections import Counter
from itertools import combinations

def load_cases(path="data/processed/gold_standard/gs_active_cases.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def pairwise_agreement(ratings_matrix):
    """Compute pairwise agreement (% of items where rater pair agrees)."""
    n_items = len(ratings_matrix)
    n_raters = len(ratings_matrix[0])
    pairs = list(combinations(range(n_raters), 2))

    results = {}
    for i, j in pairs:
        agree = sum(1 for item in ratings_matrix if item[i] == item[j])
        results[f"rater_{i+1}_vs_{j+1}"] = agree / n_items

    overall = sum(results.values()) / len(results)
    return results, overall

def fleiss_kappa(ratings_matrix, categories):
    """
    Compute Fleiss' Kappa for multiple raters.
    ratings_matrix: list of lists, each inner list = ratings from all raters for one item
    categories: list of possible categories
    """
    N = len(ratings_matrix)  # number of items
    n = len(ratings_matrix[0])  # number of raters
    k = len(categories)  # number of categories

    cat_to_idx = {c: i for i, c in enumerate(categories)}

    # Build count matrix: N x k
    # n_ij = number of raters who assigned category j to item i
    count_matrix = []
    for item_ratings in ratings_matrix:
        counts = [0] * k
        for rating in item_ratings:
            if rating in cat_to_idx:
                counts[cat_to_idx[rating]] += 1
        count_matrix.append(counts)

    # P_i = (1 / (n*(n-1))) * (sum(n_ij^2) - n) for each item
    P_i_list = []
    for counts in count_matrix:
        sum_sq = sum(c * c for c in counts)
        P_i = (sum_sq - n) / (n * (n - 1))
        P_i_list.append(P_i)

    # P_bar = mean of P_i
    P_bar = sum(P_i_list) / N

    # p_j = proportion of all assignments to category j
    p_j = []
    total_assignments = N * n
    for j in range(k):
        col_sum = sum(count_matrix[i][j] for i in range(N))
        p_j.append(col_sum / total_assignments)

    # P_e_bar = sum(p_j^2)
    P_e_bar = sum(p * p for p in p_j)

    # Kappa = (P_bar - P_e_bar) / (1 - P_e_bar)
    if P_e_bar == 1.0:
        return 1.0  # perfect agreement

    kappa = (P_bar - P_e_bar) / (1 - P_e_bar)
    return kappa

def krippendorff_alpha_nominal(ratings_matrix, categories):
    """
    Compute Krippendorff's Alpha for nominal data.
    """
    N = len(ratings_matrix)  # items
    n = len(ratings_matrix[0])  # raters

    # Total number of pairable values
    total_pairs = 0

    # Observed disagreement
    D_o = 0
    for item_ratings in ratings_matrix:
        # Count valid ratings per item
        valid = [r for r in item_ratings if r is not None]
        m = len(valid)
        if m < 2:
            continue
        total_pairs += m

        # Within-item disagreement
        for a, b in combinations(valid, 2):
            if a != b:
                D_o += 1

    # Normalize observed disagreement
    # D_o = (1/(n_total * (n_per_item - 1))) * sum of disagreements
    n_total = sum(len([r for r in item in ratings_matrix if r is not None])
                  for item in ratings_matrix) if False else 0

    # Simpler approach: compute using coincidence matrix
    # Build frequency of each category across all ratings
    all_ratings = []
    for item_ratings in ratings_matrix:
        all_ratings.extend([r for r in item_ratings if r is not None])

    n_total_ratings = len(all_ratings)
    freq = Counter(all_ratings)

    # Expected disagreement (chance)
    D_e = 0
    cat_list = list(freq.keys())
    for c1 in cat_list:
        for c2 in cat_list:
            if c1 != c2:
                D_e += freq[c1] * freq[c2]
    D_e /= (n_total_ratings * (n_total_ratings - 1))

    # Observed disagreement
    D_o_norm = 0
    n_items_used = 0
    for item_ratings in ratings_matrix:
        valid = [r for r in item_ratings if r is not None]
        m = len(valid)
        if m < 2:
            continue
        n_items_used += 1
        disagreements = sum(1 for a, b in combinations(valid, 2) if a != b)
        n_pairs = m * (m - 1) / 2
        D_o_norm += disagreements / n_pairs

    D_o_final = D_o_norm / n_items_used if n_items_used > 0 else 0

    if D_e == 0:
        return 1.0

    alpha = 1 - (D_o_final / D_e)
    return alpha

def cohens_kappa_pairwise(ratings1, ratings2, categories):
    """Compute Cohen's Kappa between two raters."""
    n = len(ratings1)

    # Observed agreement
    agree = sum(1 for a, b in zip(ratings1, ratings2) if a == b)
    p_o = agree / n

    # Expected agreement
    cat_to_idx = {c: i for i, c in enumerate(categories)}
    k = len(categories)

    freq1 = Counter(ratings1)
    freq2 = Counter(ratings2)

    p_e = sum((freq1.get(c, 0) / n) * (freq2.get(c, 0) / n) for c in categories)

    if p_e == 1.0:
        return 1.0

    kappa = (p_o - p_e) / (1 - p_e)
    return kappa

def main():
    cases = load_cases()

    # Extract ratings matrix (excluding SPLIT cases for clean analysis)
    categories = ["A", "B", "C", "D"]

    all_ratings = []
    non_split_ratings = []
    case_ids = []
    case_ids_non_split = []

    for case in cases:
        votes = case["expert_votes"]
        ratings = [votes.get("ahli1"), votes.get("ahli2"), votes.get("ahli3")]
        all_ratings.append(ratings)
        case_ids.append(case["id"])

        if case.get("gold_label") != "SPLIT":
            non_split_ratings.append(ratings)
            case_ids_non_split.append(case["id"])

    print("=" * 70)
    print("INTER-RATER AGREEMENT ANALYSIS")
    print("=" * 70)
    print(f"\nTotal cases: {len(all_ratings)}")
    print(f"Non-SPLIT cases: {len(non_split_ratings)}")
    print(f"SPLIT cases: {len(all_ratings) - len(non_split_ratings)}")
    print(f"Categories: {categories}")
    print(f"Raters: 3 (ahli1, ahli2, ahli3)")

    # 1. Consensus distribution
    print("\n" + "-" * 50)
    print("1. CONSENSUS DISTRIBUTION")
    print("-" * 50)

    unanimous = sum(1 for r in all_ratings if len(set(r)) == 1)
    majority = sum(1 for r in all_ratings if len(set(r)) == 2)
    no_consensus = sum(1 for r in all_ratings if len(set(r)) == 3)

    print(f"Unanimous (3/3): {unanimous} ({unanimous/len(all_ratings)*100:.1f}%)")
    print(f"Majority  (2/3): {majority} ({majority/len(all_ratings)*100:.1f}%)")
    print(f"No consensus:    {no_consensus} ({no_consensus/len(all_ratings)*100:.1f}%)")

    # 2. Pairwise agreement
    print("\n" + "-" * 50)
    print("2. PAIRWISE AGREEMENT (% items where pair agrees)")
    print("-" * 50)

    pairwise, overall_pairwise = pairwise_agreement(all_ratings)
    for pair, agreement in pairwise.items():
        print(f"  {pair}: {agreement:.3f} ({agreement*100:.1f}%)")
    print(f"  Average pairwise: {overall_pairwise:.3f} ({overall_pairwise*100:.1f}%)")

    # 3. Cohen's Kappa (pairwise)
    print("\n" + "-" * 50)
    print("3. COHEN'S KAPPA (pairwise, all 24 cases)")
    print("-" * 50)

    rater_cols = list(zip(*all_ratings))  # transpose
    for (i, j) in combinations(range(3), 2):
        kappa = cohens_kappa_pairwise(rater_cols[i], rater_cols[j], categories)
        print(f"  Ahli-{i+1} vs Ahli-{j+1}: {kappa:.3f}")

    # 4. Fleiss' Kappa (all raters)
    print("\n" + "-" * 50)
    print("4. FLEISS' KAPPA (multi-rater)")
    print("-" * 50)

    fk_all = fleiss_kappa(all_ratings, categories)
    print(f"  All 24 cases: {fk_all:.3f}")

    fk_non_split = fleiss_kappa(non_split_ratings, categories)
    print(f"  Non-SPLIT only (22 cases): {fk_non_split:.3f}")

    # Interpretation
    if fk_all < 0:
        interp = "Less than chance agreement"
    elif fk_all < 0.20:
        interp = "Slight agreement"
    elif fk_all < 0.40:
        interp = "Fair agreement"
    elif fk_all < 0.60:
        interp = "Moderate agreement"
    elif fk_all < 0.80:
        interp = "Substantial agreement"
    else:
        interp = "Almost perfect agreement"

    print(f"\n  Interpretation (Landis & Koch): {interp}")

    # 5. Krippendorff's Alpha
    print("\n" + "-" * 50)
    print("5. KRIPPENDORFF'S ALPHA (nominal)")
    print("-" * 50)

    alpha_all = krippendorff_alpha_nominal(all_ratings, categories)
    print(f"  All 24 cases: {alpha_all:.3f}")

    alpha_non_split = krippendorff_alpha_nominal(non_split_ratings, categories)
    print(f"  Non-SPLIT only (22 cases): {alpha_non_split:.3f}")

    threshold = 0.667
    print(f"\n  Target threshold: {threshold}")
    print(f"  {'PASS' if alpha_all >= threshold else 'BELOW THRESHOLD'}: alpha = {alpha_all:.3f} {'>='>= ''} {threshold}")

    # 6. Per-category analysis
    print("\n" + "-" * 50)
    print("6. PER-CATEGORY AGREEMENT")
    print("-" * 50)

    for cat in categories:
        cat_cases = [(i, r) for i, r in enumerate(all_ratings)
                     if any(vote == cat for vote in r)]
        if not cat_cases:
            print(f"  Category {cat}: No cases")
            continue

        agree_count = sum(1 for _, r in cat_cases if all(v == cat for v in r))
        majority_count = sum(1 for _, r in cat_cases if sum(1 for v in r if v == cat) >= 2)

        print(f"  Category {cat}: {len(cat_cases)} cases involved")
        print(f"    Unanimous: {agree_count} ({agree_count/len(cat_cases)*100:.0f}%)")
        print(f"    Majority:  {majority_count} ({majority_count/len(cat_cases)*100:.0f}%)")

    # 7. Confusion patterns (who disagrees with whom?)
    print("\n" + "-" * 50)
    print("7. DISAGREEMENT PATTERNS")
    print("-" * 50)

    disagreement_pairs = Counter()
    for ratings in all_ratings:
        for a, b in combinations(ratings, 2):
            if a != b:
                pair = tuple(sorted([a, b]))
                disagreement_pairs[pair] += 1

    print("  Most common disagreement pairs:")
    for pair, count in disagreement_pairs.most_common():
        print(f"    {pair[0]} vs {pair[1]}: {count} times")

    # 8. Ahli-3 deviation analysis
    print("\n" + "-" * 50)
    print("8. RATER DEVIATION ANALYSIS")
    print("-" * 50)

    for rater_idx in range(3):
        deviations = 0
        for ratings in all_ratings:
            others = [ratings[j] for j in range(3) if j != rater_idx]
            if ratings[rater_idx] not in others:
                deviations += 1
        print(f"  Ahli-{rater_idx+1} deviates from both others: {deviations}/{len(all_ratings)} ({deviations/len(all_ratings)*100:.1f}%)")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Fleiss' Kappa:        {fk_all:.3f} ({interp})")
    print(f"Krippendorff's Alpha: {alpha_all:.3f}")
    print(f"Average Pairwise:     {overall_pairwise:.3f}")
    print(f"Unanimous cases:      {unanimous}/{len(all_ratings)} ({unanimous/len(all_ratings)*100:.1f}%)")

    if alpha_all < 0.667:
        print(f"\nWARNING: Alpha ({alpha_all:.3f}) is below the 0.667 threshold.")
        print("This should be reported honestly as a limitation in the paper.")
        print("Consider: (a) focus analysis on unanimous/majority cases only,")
        print("          (b) discuss disagreement as evidence of task difficulty,")
        print("          (c) use majority voting with documented limitations.")

    return {
        "fleiss_kappa": fk_all,
        "krippendorff_alpha": alpha_all,
        "pairwise_agreement": overall_pairwise,
        "unanimous_rate": unanimous / len(all_ratings),
        "n_cases": len(all_ratings),
        "n_raters": 3,
    }

if __name__ == "__main__":
    results = main()
