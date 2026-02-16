import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict

# Pastikan import `src.*` bisa dari project root.
sys.path.append(os.getcwd())

from src.utils.benchmark_contract import (
    UNRESOLVED_GOLD_LABELS,
    count_evaluable_cases,
    resolve_manifest_evaluable_count,
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _label_distribution(data: list) -> Dict[str, int]:
    dist: Dict[str, int] = {}
    for item in data:
        label = str(item.get("gold_label", "")).upper()
        dist[label] = dist.get(label, 0) + 1
    return dist


def validate_manifest(manifest_path: Path, require_reference_match: bool) -> int:
    if not manifest_path.exists():
        print(f"[ERROR] Manifest tidak ditemukan: {manifest_path}")
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[ERROR] Manifest tidak valid JSON: {exc}")
        return 1

    bench = manifest.get("benchmark_file", {})
    dataset_path = Path(bench.get("path", ""))
    if not dataset_path.exists():
        print(f"[ERROR] Dataset benchmark tidak ditemukan: {dataset_path}")
        return 1

    try:
        data = json.loads(dataset_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[ERROR] Dataset tidak valid JSON: {exc}")
        return 1

    if not isinstance(data, list):
        print(f"[ERROR] Dataset harus list, dapat: {type(data).__name__}")
        return 1

    errors = 0
    warns = 0

    file_hash = _sha256(dataset_path)
    expected_hash = str(bench.get("sha256", "")).upper()
    if expected_hash and file_hash != expected_hash:
        print(f"[ERROR] Hash mismatch: manifest={expected_hash} runtime={file_hash}")
        errors += 1
    else:
        print(f"[OK] Hash match: {file_hash}")

    runtime_count = len(data)
    expected_count = bench.get("total_cases_actual")
    if expected_count is not None and runtime_count != int(expected_count):
        print(f"[ERROR] total_cases_actual mismatch: manifest={expected_count} runtime={runtime_count}")
        errors += 1
    else:
        print(f"[OK] total_cases_actual: {runtime_count}")

    runtime_dist = _label_distribution(data)
    expected_dist = bench.get("label_distribution", {})
    if expected_dist:
        normalized_expected = {str(k).upper(): int(v) for k, v in expected_dist.items()}
        if runtime_dist != normalized_expected:
            print(f"[ERROR] label_distribution mismatch: manifest={normalized_expected} runtime={runtime_dist}")
            errors += 1
        else:
            print(f"[OK] label_distribution match")

    runtime_evaluable = count_evaluable_cases(data)
    expected_evaluable = resolve_manifest_evaluable_count(bench)
    if expected_evaluable is not None and runtime_evaluable != expected_evaluable:
        print(
            "[ERROR] evaluable_cases mismatch: "
            f"manifest={expected_evaluable} runtime={runtime_evaluable}"
        )
        errors += 1
    else:
        print(f"[OK] evaluable_cases: {runtime_evaluable}")
        print(f"[INFO] unresolved_labels_excluded={sorted(UNRESOLVED_GOLD_LABELS)}")

    integrity = manifest.get("integrity_checks", {})
    ref_match = integrity.get("count_matches_reference_claim")
    if ref_match is False:
        msg = "[WARN] Reference claim mismatch masih aktif (declared_total_cases != total_cases_actual)."
        if require_reference_match:
            print(msg.replace("[WARN]", "[ERROR]"))
            errors += 1
        else:
            print(msg)
            warns += 1

    print(f"[SUMMARY] errors={errors} warns={warns}")
    return 1 if errors else 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validasi integritas benchmark manifest.")
    parser.add_argument(
        "--manifest",
        type=str,
        default="data/benchmark_manifest.json",
        help="Path ke benchmark manifest JSON.",
    )
    parser.add_argument(
        "--require-reference-match",
        action="store_true",
        help="Fail jika count_matches_reference_claim = false.",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    raise SystemExit(validate_manifest(Path(args.manifest), args.require_reference_match))
