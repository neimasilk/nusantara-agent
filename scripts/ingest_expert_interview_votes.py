import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


VALID_LABELS = {"A", "B", "C", "D"}


def _normalize_label(value: str) -> str:
    return str(value).strip().upper()


def _find_label(row: Dict[str, str], expert_id: str) -> str:
    candidates = [
        row.get(f"label_{expert_id}", ""),
        row.get("label", ""),
    ]
    for candidate in candidates:
        label = _normalize_label(candidate)
        if label:
            return label
    return ""


def _build_case_index(data: List[Dict]) -> Dict[str, Dict]:
    index: Dict[str, Dict] = {}
    for case in data:
        case_id = str(case.get("id", "")).strip()
        if case_id:
            index[case_id] = case
    return index


def ingest_votes(
    dataset_path: Path,
    input_csv_path: Path,
    output_path: Path,
    expert_id: str,
    split_only: bool,
    allow_overwrite: bool,
) -> int:
    if not dataset_path.exists():
        print(f"[ERROR] Dataset tidak ditemukan: {dataset_path}")
        return 1
    if not input_csv_path.exists():
        print(f"[ERROR] CSV input tidak ditemukan: {input_csv_path}")
        return 1

    try:
        data = json.loads(dataset_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[ERROR] Dataset JSON invalid: {exc}")
        return 1

    if not isinstance(data, list):
        print(f"[ERROR] Dataset harus list, dapat: {type(data).__name__}")
        return 1

    try:
        with input_csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    except Exception as exc:
        print(f"[ERROR] CSV input invalid: {exc}")
        return 1

    case_index = _build_case_index(data)

    updated = 0
    adjudicated = 0
    skipped = 0
    errors: List[str] = []

    for i, row in enumerate(rows, start=2):
        case_id = str(row.get("id", "")).strip()
        if not case_id:
            skipped += 1
            continue

        case = case_index.get(case_id)
        if case is None:
            errors.append(f"Line {i}: id tidak ditemukan di dataset -> {case_id}")
            continue

        label = _find_label(row, expert_id)
        if not label:
            skipped += 1
            continue
        if label not in VALID_LABELS:
            errors.append(f"Line {i}: label tidak valid ({label}) untuk id {case_id}")
            continue

        gold_label_current = _normalize_label(case.get("gold_label", ""))
        if split_only and gold_label_current != "SPLIT":
            skipped += 1
            continue

        votes = case.get("expert_votes")
        if not isinstance(votes, dict):
            votes = {}
            case["expert_votes"] = votes

        if expert_id in votes and not allow_overwrite:
            errors.append(f"Line {i}: vote {expert_id} sudah ada untuk id {case_id} (pakai --allow-overwrite)")
            continue

        votes[expert_id] = label
        updated += 1

        if gold_label_current == "SPLIT":
            case["gold_label"] = label
            case["consensus"] = f"adjudicated_{expert_id}"
            adjudicated += 1

        # Simpan catatan interview (opsional tapi audit-friendly)
        notes = case.get("interview_notes")
        if not isinstance(notes, dict):
            notes = {}
            case["interview_notes"] = notes
        notes[expert_id] = {
            "confidence": str(
                row.get(f"confidence_{expert_id}", "") or row.get("confidence", "")
            ).strip(),
            "rationale": str(
                row.get(f"rationale_{expert_id}", "") or row.get("rationale", "")
            ).strip(),
            "reference_1": str(row.get("reference_1", "")).strip(),
            "reference_2": str(row.get("reference_2", "")).strip(),
            "session_date": str(row.get("session_date", "")).strip(),
            "interviewer_name": str(row.get("interviewer_name", "")).strip(),
            "mode": str(row.get("mode", "")).strip() or "online_interview",
            "ingested_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    if errors:
        print("[ERROR] Validasi gagal:")
        for err in errors:
            print(f" - {err}")
        print(f"[SUMMARY] updated={updated} adjudicated={adjudicated} skipped={skipped} errors={len(errors)}")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Hasil ingest disimpan: {output_path}")
    print(f"[SUMMARY] updated={updated} adjudicated={adjudicated} skipped={skipped} errors=0")
    return 0


def _default_output(dataset_path: str, expert_id: str) -> str:
    src = Path(dataset_path)
    suffix = f".post_{expert_id}.json"
    if src.suffix.lower() == ".json":
        return str(src.with_suffix(suffix))
    return str(src) + suffix


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest hasil interview online ahli ke dataset gold-standard."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="data/processed/gold_standard/gs_active_cases.json",
        help="Path dataset JSON sumber.",
    )
    parser.add_argument(
        "--input-csv",
        type=str,
        required=True,
        help="Path CSV hasil interview yang sudah diisi.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Path output dataset hasil ingest. Default: <dataset>.post_<expert_id>.json",
    )
    parser.add_argument(
        "--expert-id",
        type=str,
        default="ahli4",
        help="ID ahli yang sedang di-ingest (misal: ahli4).",
    )
    parser.add_argument(
        "--all-cases",
        action="store_true",
        help="Izinkan ingest ke semua kasus. Default hanya kasus SPLIT.",
    )
    parser.add_argument(
        "--allow-overwrite",
        action="store_true",
        help="Izinkan overwrite vote existing untuk expert_id yang sama.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Tulis hasil langsung ke file dataset sumber.",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    output = args.dataset if args.in_place else (args.output or _default_output(args.dataset, args.expert_id))
    raise SystemExit(
        ingest_votes(
            dataset_path=Path(args.dataset),
            input_csv_path=Path(args.input_csv),
            output_path=Path(output),
            expert_id=args.expert_id,
            split_only=not args.all_cases,
            allow_overwrite=args.allow_overwrite,
        )
    )
