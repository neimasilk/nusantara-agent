import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List


def _votes_to_text(votes: Dict[str, str]) -> str:
    if not isinstance(votes, dict):
        return ""
    parts = [f"{k}={v}" for k, v in sorted(votes.items())]
    return "; ".join(parts)


def export_cases(dataset_path: Path, output_path: Path, expert_id: str, split_only: bool) -> int:
    if not dataset_path.exists():
        print(f"[ERROR] Dataset tidak ditemukan: {dataset_path}")
        return 1

    try:
        data = json.loads(dataset_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[ERROR] Dataset JSON invalid: {exc}")
        return 1

    if not isinstance(data, list):
        print(f"[ERROR] Dataset harus list, dapat: {type(data).__name__}")
        return 1

    label_col = f"label_{expert_id}"
    confidence_col = f"confidence_{expert_id}"
    rationale_col = f"rationale_{expert_id}"

    rows: List[Dict[str, str]] = []
    for case in data:
        gold_label = str(case.get("gold_label", "")).upper()
        if split_only and gold_label != "SPLIT":
            continue

        rows.append(
            {
                "id": str(case.get("id", "")),
                "query": str(case.get("query", "")),
                "gold_label_current": gold_label,
                "consensus_current": str(case.get("consensus", "")),
                "expert_votes_current": _votes_to_text(case.get("expert_votes", {})),
                label_col: "",
                confidence_col: "",
                rationale_col: "",
                "reference_1": "",
                "reference_2": "",
                "session_date": "",
                "interviewer_name": "",
                "mode": "online_interview",
            }
        )

    if not rows:
        print("[WARN] Tidak ada kasus yang cocok untuk diexport.")
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Exported {len(rows)} kasus -> {output_path}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export kasus gold-standard ke template CSV untuk interview online ahli."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="data/processed/gold_standard/gs_active_cases.json",
        help="Path dataset JSON aktif.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/gold_standard/interview_online/interview_template_ahli4.csv",
        help="Path output CSV template interview.",
    )
    parser.add_argument(
        "--expert-id",
        type=str,
        default="ahli4",
        help="ID ahli yang akan mengisi template (misal: ahli4).",
    )
    parser.add_argument(
        "--all-cases",
        action="store_true",
        help="Export semua kasus, bukan hanya yang gold_label = SPLIT.",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    raise SystemExit(
        export_cases(
            dataset_path=Path(args.dataset),
            output_path=Path(args.output),
            expert_id=args.expert_id,
            split_only=not args.all_cases,
        )
    )
