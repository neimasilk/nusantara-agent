import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _label_distribution(data: List[Dict]) -> Dict[str, int]:
    dist: Dict[str, int] = {}
    for item in data:
        label = str(item.get("gold_label", "")).upper()
        dist[label] = dist.get(label, 0) + 1
    return dist


def rebuild_manifest(
    dataset_path: Path,
    manifest_path: Path,
    reference_path: Path,
    as_of_date: str,
    owner: str,
) -> int:
    if not dataset_path.exists():
        print(f"[ERROR] Dataset tidak ditemukan: {dataset_path}")
        return 1
    if not reference_path.exists():
        print(f"[ERROR] Reference claim file tidak ditemukan: {reference_path}")
        return 1

    try:
        data = json.loads(dataset_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[ERROR] Dataset JSON invalid: {exc}")
        return 1

    if not isinstance(data, list):
        print(f"[ERROR] Dataset harus list, dapat: {type(data).__name__}")
        return 1

    total_cases_actual = len(data)
    label_distribution = _label_distribution(data)
    evaluable = sum(1 for item in data if str(item.get("gold_label", "")).upper() != "SPLIT")

    # declared_total_cases dipertahankan dari manifest lama jika ada; fallback 82
    declared_total_cases = 82
    if manifest_path.exists():
        try:
            old_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            declared_total_cases = int(
                old_manifest.get("reference_claim", {}).get("declared_total_cases", declared_total_cases)
            )
        except Exception:
            pass

    manifest = {
        "manifest_version": "1.0",
        "dataset_id": f"gs_active_{as_of_date}",
        "as_of_date": as_of_date,
        "owner": owner,
        "benchmark_file": {
            "path": str(dataset_path).replace("\\", "/"),
            "sha256": _sha256(dataset_path),
            "last_write_time_utc": datetime.fromtimestamp(
                dataset_path.stat().st_mtime, timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_cases_actual": total_cases_actual,
            "label_distribution": label_distribution,
            "evaluable_cases_excluding_split": evaluable,
        },
        "reference_claim": {
            "path": str(reference_path).replace("\\", "/"),
            "sha256": _sha256(reference_path),
            "declared_total_cases": declared_total_cases,
        },
        "integrity_checks": {
            "count_matches_reference_claim": total_cases_actual == declared_total_cases,
            "notes": [
                "Manifest direbuild otomatis dari dataset aktif.",
                "Gunakan validate_benchmark_manifest.py untuk verifikasi sebelum benchmark formal.",
            ],
        },
        "provenance": {
            "source_summary": "Rebuilt from local repository artifacts without external API calls.",
            "generated_by": "scripts/rebuild_benchmark_manifest.py",
            "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    }

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Manifest rebuilt: {manifest_path}")
    print(
        "[SUMMARY] "
        f"total_cases_actual={total_cases_actual}, evaluable={evaluable}, "
        f"declared_total_cases={declared_total_cases}, "
        f"count_matches_reference_claim={manifest['integrity_checks']['count_matches_reference_claim']}"
    )
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rebuild benchmark manifest dari dataset aktif.")
    parser.add_argument(
        "--dataset",
        type=str,
        default="data/processed/gold_standard/gs_active_cases.json",
        help="Path dataset aktif.",
    )
    parser.add_argument(
        "--manifest",
        type=str,
        default="data/benchmark_manifest.json",
        help="Path output manifest.",
    )
    parser.add_argument(
        "--reference-claim",
        type=str,
        default="docs/gold_standard_consensus_report_complete_82_cases_2026-02-08.md",
        help="Path dokumen klaim referensi total kasus.",
    )
    parser.add_argument(
        "--as-of-date",
        type=str,
        default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        help="Tanggal as-of (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--owner",
        type=str,
        default="nusantara-agent",
        help="Owner manifest.",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    raise SystemExit(
        rebuild_manifest(
            dataset_path=Path(args.dataset),
            manifest_path=Path(args.manifest),
            reference_path=Path(args.reference_claim),
            as_of_date=args.as_of_date,
            owner=args.owner,
        )
    )
