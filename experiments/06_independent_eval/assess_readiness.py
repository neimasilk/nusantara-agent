import json
from pathlib import Path
from typing import Dict, List

from run_precheck import (
    DIR_ANNOT,
    DIR_GOLD_TEXT,
    DIR_MA,
    MAX_DETAIL_ERROR,
    TARGET_ANNOTATOR,
    TARGET_PARAGRAF,
    TARGET_PUTUSAN_MA,
    baca_json,
    validasi_annotasi_minimal,
    validasi_putusan_minimal,
)

ROOT = Path(__file__).resolve().parents[2]
READINESS_PATH = ROOT / "experiments" / "06_independent_eval" / "readiness_status.json"
AGREEMENT_REPORT_PATH = ROOT / "data" / "processed" / "gold_standard" / "agreement_report.md"


def _scan_annotation_files() -> Dict:
    annot_files = [
        p
        for p in sorted(DIR_ANNOT.glob("*.json"))
        if p.name not in {"template_annotasi.json"}
    ]
    invalid = 0
    details: List[str] = []
    for path in annot_files:
        try:
            obj = baca_json(path)
            errs = validasi_annotasi_minimal(obj)
            if errs:
                invalid += 1
                if len(details) < MAX_DETAIL_ERROR:
                    details.append(f"{path.name}: {', '.join(errs)}")
        except Exception as exc:
            invalid += 1
            if len(details) < MAX_DETAIL_ERROR:
                details.append(f"{path.name}: {exc}")
    return {
        "count": len(annot_files),
        "invalid_count": invalid,
        "invalid_examples": details,
        "target_count": TARGET_PARAGRAF * TARGET_ANNOTATOR,
    }


def _scan_ma_files() -> Dict:
    ma_files = [
        p
        for p in sorted(DIR_MA.glob("*.json"))
        if p.name not in {"schema_putusan.json", "template_putusan_0001.json"}
    ]
    invalid = 0
    draft = 0
    details: List[str] = []
    for path in ma_files:
        try:
            obj = baca_json(path)
            errs = validasi_putusan_minimal(obj)
            if errs:
                invalid += 1
                if len(details) < MAX_DETAIL_ERROR:
                    details.append(f"{path.name}: {', '.join(errs)}")
            status_verifikasi = str(obj.get("metadata", {}).get("status_verifikasi", "")).strip().lower()
            if status_verifikasi == "draft":
                draft += 1
        except Exception as exc:
            invalid += 1
            if len(details) < MAX_DETAIL_ERROR:
                details.append(f"{path.name}: {exc}")
    return {
        "count": len(ma_files),
        "invalid_count": invalid,
        "draft_count": draft,
        "invalid_examples": details,
        "target_count": TARGET_PUTUSAN_MA,
    }


def build_readiness_status() -> Dict:
    text_files = sorted(DIR_GOLD_TEXT.glob("*.txt")) if DIR_GOLD_TEXT.exists() else []
    annotation = _scan_annotation_files()
    ma = _scan_ma_files()

    operational_ready_art028 = (
        len(text_files) >= TARGET_PARAGRAF
        and annotation["count"] >= annotation["target_count"]
        and annotation["invalid_count"] == 0
    )
    operational_ready_art030 = (
        ma["count"] >= ma["target_count"] and ma["invalid_count"] == 0
    )

    # Scientific gate lebih ketat: butuh bukti agreement report + putusan non-draft.
    scientific_ready_art028 = operational_ready_art028 and AGREEMENT_REPORT_PATH.exists()
    scientific_ready_art030 = (
        operational_ready_art030 and ma["draft_count"] == 0
    )

    operational_ready_art031 = operational_ready_art028 and operational_ready_art030
    scientific_ready_art031 = scientific_ready_art028 and scientific_ready_art030

    blockers = []
    if not scientific_ready_art028:
        blockers.append(
            "ART-028 belum scientific-ready: agreement report final belum tersedia atau coverage belum memenuhi syarat."
        )
    if not scientific_ready_art030:
        blockers.append(
            "ART-030 belum scientific-ready: putusan MA tervalidasi (50+ non-draft) belum terpenuhi."
        )

    return {
        "as_of": "2026-02-11",
        "targets": {
            "paragraf": TARGET_PARAGRAF,
            "annotator": TARGET_ANNOTATOR,
            "putusan_ma": TARGET_PUTUSAN_MA,
        },
        "counts": {
            "gold_text_files": len(text_files),
            "annotations": annotation,
            "ma_decisions": ma,
        },
        "art_status": {
            "ART-028_operational_ready": operational_ready_art028,
            "ART-030_operational_ready": operational_ready_art030,
            "ART-031_operational_ready": operational_ready_art031,
            "ART-028_scientific_ready": scientific_ready_art028,
            "ART-030_scientific_ready": scientific_ready_art030,
            "ART-031_scientific_ready": scientific_ready_art031,
        },
        "blockers_scientific": blockers,
        "notes": [
            "Operational-ready berarti artefak ada dan lolos validasi minimal.",
            "Scientific-ready berarti memenuhi syarat klaim paper (agreement report final + putusan MA non-draft tervalidasi).",
        ],
    }


def main() -> None:
    status = build_readiness_status()
    READINESS_PATH.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Readiness status saved: {READINESS_PATH.as_posix()}")
    print(f"- ART-031 operational_ready: {status['art_status']['ART-031_operational_ready']}")
    print(f"- ART-031 scientific_ready: {status['art_status']['ART-031_scientific_ready']}")
    if status["blockers_scientific"]:
        print("- Blockers:")
        for idx, blocker in enumerate(status["blockers_scientific"], start=1):
            print(f"  {idx}. {blocker}")


if __name__ == "__main__":
    main()
