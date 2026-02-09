import argparse
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


DEFAULT_PATCHES: Dict[str, str] = {
    "CS-MIN-004": "C",
    "CS-MIN-011": "B",
    "CS-LIN-052": "C",
    "CS-LIN-017": "A",
    "CS-BAL-014": "B",
    "CS-LIN-016": "A",
}


def _load_dataset(path: Path) -> List[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def _patch_dataset(data: List[dict], patches: Dict[str, str]) -> Tuple[List[Tuple[str, str, str]], List[str]]:
    updates: List[Tuple[str, str, str]] = []
    not_found: List[str] = []
    by_id = {str(item.get("id", "")).strip(): item for item in data}

    for case_id, new_label in patches.items():
        case = by_id.get(case_id)
        if case is None:
            not_found.append(case_id)
            continue
        old_label = str(case.get("gold_label", "")).upper()
        case["gold_label"] = new_label
        updates.append((case_id, old_label, new_label))

    return updates, not_found


def run(dataset: Path, commit: bool, backup: Path | None) -> int:
    if not dataset.exists():
        print(f"[ERROR] Dataset tidak ditemukan: {dataset}")
        return 1

    try:
        data = _load_dataset(dataset)
    except Exception as exc:
        print(f"[ERROR] Dataset JSON invalid: {exc}")
        return 1

    if not isinstance(data, list):
        print(f"[ERROR] Dataset harus list, dapat: {type(data).__name__}")
        return 1

    updates, not_found = _patch_dataset(data, DEFAULT_PATCHES)
    for case_id, old_label, new_label in updates:
        status = "UNCHANGED" if old_label == new_label else "UPDATED"
        print(f"[{status}] {case_id}: {old_label} -> {new_label}")

    if not_found:
        for case_id in not_found:
            print(f"[WARN] ID tidak ditemukan: {case_id}")

    if not commit:
        print(f"[SUMMARY] dry_run updates={len(updates)} not_found={len(not_found)}")
        return 0

    if backup is not None:
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dataset, backup)
        print(f"[OK] Backup dibuat: {backup}")

    dataset.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Dataset dipatch: {dataset}")
    print(f"[SUMMARY] commit updates={len(updates)} not_found={len(not_found)}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Patch gold_label untuk kasus mismatch yang sudah diputuskan.")
    parser.add_argument(
        "--dataset",
        type=str,
        default="data/processed/gold_standard/gs_active_cases.json",
        help="Path dataset JSON.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Terapkan patch ke file dataset. Tanpa flag ini hanya dry-run.",
    )
    parser.add_argument(
        "--backup",
        type=str,
        default="",
        help="Path backup file (hanya saat --commit).",
    )
    return parser


if __name__ == "__main__":
    args = _parser().parse_args()
    backup_path = Path(args.backup) if args.backup else None
    raise SystemExit(run(dataset=Path(args.dataset), commit=args.commit, backup=backup_path))
