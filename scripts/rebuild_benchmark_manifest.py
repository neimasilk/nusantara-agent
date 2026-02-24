import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Pastikan import `src.*` bisa dari project root.
sys.path.append(os.getcwd())

from src.utils.benchmark_contract import (
    UNRESOLVED_GOLD_LABELS,
    count_evaluable_cases,
)


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


def _resolve_declared_total_cases(
    *,
    total_cases_actual: int,
    manifest_path: Path,
    declared_total_cases: Optional[int],
    inherit_declared_total_from_manifest: bool,
) -> Tuple[int, str]:
    if declared_total_cases is not None:
        if int(declared_total_cases) <= 0:
            raise ValueError("--declared-total-cases harus > 0.")
        return int(declared_total_cases), "cli_override"

    if inherit_declared_total_from_manifest and manifest_path.exists():
        try:
            old_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            old_value = int(old_manifest.get("reference_claim", {}).get("declared_total_cases"))
            if old_value > 0:
                return old_value, "manifest_legacy"
        except Exception:
            pass

    return int(total_cases_actual), "dataset_actual"


def rebuild_manifest(
    dataset_path: Path,
    manifest_path: Path,
    reference_path: Path,
    as_of_date: str,
    owner: str,
    declared_total_cases: Optional[int],
    inherit_declared_total_from_manifest: bool,
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
    evaluable = count_evaluable_cases(data)

    try:
        resolved_declared_total_cases, declared_source = _resolve_declared_total_cases(
            total_cases_actual=total_cases_actual,
            manifest_path=manifest_path,
            declared_total_cases=declared_total_cases,
            inherit_declared_total_from_manifest=inherit_declared_total_from_manifest,
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 1

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
            "evaluable_cases_excluding_disputed": evaluable,
            # Backward compatibility untuk script lama
            "evaluable_cases_excluding_split": evaluable,
        },
        "reference_claim": {
            "path": str(reference_path).replace("\\", "/"),
            "sha256": _sha256(reference_path),
            "declared_total_cases": resolved_declared_total_cases,
            "declared_total_cases_source": declared_source,
        },
        "integrity_checks": {
            "count_matches_reference_claim": total_cases_actual == resolved_declared_total_cases,
            "notes": [
                "Manifest direbuild otomatis dari dataset aktif.",
                "Gunakan validate_benchmark_manifest.py untuk verifikasi sebelum benchmark formal.",
                "Default declared_total_cases mengikuti jumlah dataset aktif agar audit tidak mewarisi angka historis secara diam-diam.",
                f"Label unresolved yang dikecualikan dari evaluasi: {sorted(UNRESOLVED_GOLD_LABELS)}",
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
        f"declared_total_cases={resolved_declared_total_cases}, "
        f"declared_total_cases_source={declared_source}, "
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
        default="docs/human_only/artifacts/benchmark_scope_active_74_cases_2026-02-24.md",
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
    parser.add_argument(
        "--declared-total-cases",
        type=int,
        default=None,
        help=(
            "Override jumlah kasus referensi. "
            "Jika tidak diisi, default mengikuti jumlah kasus dataset aktif."
        ),
    )
    parser.add_argument(
        "--inherit-declared-total-from-manifest",
        action="store_true",
        help=(
            "Gunakan declared_total_cases dari manifest lama (legacy mode). "
            "Tidak disarankan untuk baseline scientific terbaru."
        ),
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
            declared_total_cases=args.declared_total_cases,
            inherit_declared_total_from_manifest=args.inherit_declared_total_from_manifest,
        )
    )
