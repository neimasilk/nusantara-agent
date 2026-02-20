import json
import re
import argparse
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
OLD_RESULTS_PATH = ROOT / "experiments" / "09_ablation_study" / "results_deepseek_asp_llm_2026-02-19.json"
NEW_RESULTS_PATH = ROOT / "experiments" / "09_ablation_study" / "results_dual_asp_llm_2026-02-19.json"
DATASET_PATH = ROOT / "data" / "processed" / "gold_standard" / "gs_active_cases.json"
DOMAIN_MAP_SOURCE = ROOT / "docs" / "human_only" / "AHLI 2 - LABELING.md"


def _load_json(path: Path) -> Dict:
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _to_case_map(results_payload: Dict) -> Dict[str, Dict]:
    rows = results_payload.get("results")
    if not isinstance(rows, list):
        raise RuntimeError(f"Field 'results' tidak valid pada file: {results_payload}")
    mapping: Dict[str, Dict] = {}
    for row in rows:
        case_id = str(row.get("id", "")).strip()
        if case_id:
            mapping[case_id] = row
    return mapping


def _domain_from_case_id(case_id: str) -> str:
    cid = case_id.upper()
    if "-MIN-" in cid:
        return "Minangkabau"
    if "-BAL-" in cid:
        return "Bali"
    if "-JAW-" in cid:
        return "Jawa"
    if "-NAS-" in cid:
        return "Nasional"
    if "-LIN-" in cid:
        return "Lintas"
    return "Unknown"


def _load_domain_map_from_labeling_doc() -> Dict[str, str]:
    if not DOMAIN_MAP_SOURCE.exists():
        return {}
    text = DOMAIN_MAP_SOURCE.read_text(encoding="utf-8")
    pattern = re.compile(
        r"Case ID:\s*(GS-\d{4}).*?\*\*Domain:\*\*\s*([A-Za-z]+)",
        re.S,
    )
    out: Dict[str, str] = {}
    for case_id, domain in pattern.findall(text):
        out[case_id.strip()] = domain.strip()
    return out


def _infer_domain(case_id: str, query_text: str, domain_map: Dict[str, str]) -> str:
    if case_id in domain_map:
        return domain_map[case_id]

    by_id = _domain_from_case_id(case_id)
    if by_id != "Unknown":
        return by_id

    q = (query_text or "").lower()
    if "minangkabau" in q or "nagari" in q:
        return "Minangkabau"
    if "bali" in q or "desa adat" in q:
        return "Bali"
    if "jawa" in q:
        return "Jawa"
    if "kuhperdata" in q or "uu " in q or "uupa" in q:
        return "Nasional"
    return "Unknown"


def _dataset_query_index() -> Dict[str, str]:
    data = _load_json(DATASET_PATH)
    if not isinstance(data, list):
        raise RuntimeError(f"Dataset tidak valid: {DATASET_PATH}")
    out: Dict[str, str] = {}
    for row in data:
        cid = str(row.get("id", "")).strip()
        out[cid] = str(row.get("query", "")).strip()
    return out


def _render_cases(title: str, rows: List[Dict]) -> None:
    print(title)
    if not rows:
        print("  (none)")
        return
    for r in rows:
        print(
            "  - "
            f"{r['id']} | domain={r['domain']} | gold={r['gold']} | "
            f"old_pred={r['old_pred']} -> new_pred={r['new_pred']} | "
            f"old_match={r['old_match']} new_match={r['new_match']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Regression Analysis for Ablation Study")
    parser.add_argument("--old", type=str, default=str(OLD_RESULTS_PATH), help="Path to old result JSON")
    parser.add_argument("--new", type=str, default=str(NEW_RESULTS_PATH), help="Path to new result JSON")
    args = parser.parse_args()

    old_path = Path(args.old)
    new_path = Path(args.new)

    old_payload = _load_json(old_path)
    new_payload = _load_json(new_path)

    old_map = _to_case_map(old_payload)
    new_map = _to_case_map(new_payload)

    case_ids = sorted(set(old_map.keys()) & set(new_map.keys()))
    if not case_ids:
        raise RuntimeError("Tidak ada overlap case ID antara hasil lama dan hasil baru.")

    old_only = sorted(set(old_map.keys()) - set(new_map.keys()))
    new_only = sorted(set(new_map.keys()) - set(old_map.keys()))
    if old_only:
        print(f"[WARN] Case hanya di old: {len(old_only)}")
    if new_only:
        print(f"[WARN] Case hanya di new: {len(new_only)}")

    query_index = _dataset_query_index()
    domain_map = _load_domain_map_from_labeling_doc()

    regressions: List[Dict] = []
    improvements: List[Dict] = []
    unchanged_correct = 0
    unchanged_wrong = 0

    reg_domain_counter: Counter = Counter()
    imp_domain_counter: Counter = Counter()
    reg_gold_counter: Counter = Counter()
    imp_gold_counter: Counter = Counter()
    reg_shift_counter: Counter = Counter()
    imp_shift_counter: Counter = Counter()

    for case_id in case_ids:
        old_row = old_map[case_id]
        new_row = new_map[case_id]

        old_match = bool(old_row.get("match"))
        new_match = bool(new_row.get("match"))
        gold = str(new_row.get("gold", old_row.get("gold", ""))).strip().upper()
        old_pred = str(old_row.get("predicted", "")).strip().upper()
        new_pred = str(new_row.get("predicted", "")).strip().upper()

        domain = _infer_domain(case_id, query_index.get(case_id, ""), domain_map)
        item = {
            "id": case_id,
            "domain": domain,
            "gold": gold,
            "old_pred": old_pred,
            "new_pred": new_pred,
            "old_match": old_match,
            "new_match": new_match,
        }

        if old_match and (not new_match):
            regressions.append(item)
            reg_domain_counter[domain] += 1
            reg_gold_counter[gold] += 1
            reg_shift_counter[f"{old_pred}->{new_pred}"] += 1
        elif (not old_match) and new_match:
            improvements.append(item)
            imp_domain_counter[domain] += 1
            imp_gold_counter[gold] += 1
            imp_shift_counter[f"{old_pred}->{new_pred}"] += 1
        elif old_match and new_match:
            unchanged_correct += 1
        else:
            unchanged_wrong += 1

    total = len(case_ids)
    print("=== Regression Analysis: ASP+LLM Old vs New ===")
    print(f"old_file: {old_path}")
    print(f"new_file: {new_path}")
    print(f"cases_compared: {total}")
    print(
        "status_counts: "
        f"regression={len(regressions)}, "
        f"improvement={len(improvements)}, "
        f"unchanged_correct={unchanged_correct}, "
        f"unchanged_wrong={unchanged_wrong}"
    )
    print("")

    _render_cases("Regressions (correct -> wrong):", regressions)
    print("")
    _render_cases("Improvements (wrong -> correct):", improvements)
    print("")

    print("Domain impact:")
    print(f"  regression_by_domain: {dict(reg_domain_counter)}")
    print(f"  improvement_by_domain: {dict(imp_domain_counter)}")
    print("")

    print("Label patterns:")
    print(f"  regression_by_gold_label: {dict(reg_gold_counter)}")
    print(f"  improvement_by_gold_label: {dict(imp_gold_counter)}")
    print(f"  regression_pred_shift: {dict(reg_shift_counter)}")
    print(f"  improvement_pred_shift: {dict(imp_shift_counter)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
