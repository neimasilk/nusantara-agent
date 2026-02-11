import argparse
import json
import os
import sys
from typing import Dict, Literal

# Tambahkan root ke sys.path untuk import src
sys.path.append(os.getcwd())

from src.pipeline.nusantara_agent import NusantaraAgentPipeline
from src.agents.router import _json_or_raw

MANIFEST_PATH = "data/benchmark_manifest.json"
LEGACY_GS_PATH = "data/processed/gold_standard/gs_active_cases.json"
DEFAULT_OUTPUT_PATH = "experiments/09_ablation_study/results_phase1.json"
EvaluationMode = Literal["scientific_claimable", "operational_offline"]


def _load_manifest() -> Dict:
    if not os.path.exists(MANIFEST_PATH):
        return {}
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        print(f"[WARN] Gagal membaca manifest ({MANIFEST_PATH}): {exc}")
        return {}


def _resolve_gs_path(gs_path: str, manifest: Dict) -> str:
    if gs_path:
        return gs_path
    manifest_path = manifest.get("benchmark_file", {}).get("path", "")
    if manifest_path:
        return manifest_path
    return LEGACY_GS_PATH


def _log_manifest_status(gs_path: str, manifest: Dict) -> None:
    """Log status integritas dataset dari benchmark manifest bila tersedia."""
    if not manifest:
        print(f"[INFO] Manifest tidak ditemukan/invalid: {MANIFEST_PATH}")
        return

    benchmark = manifest.get("benchmark_file", {})
    reference_claim = manifest.get("reference_claim", {})
    integrity = manifest.get("integrity_checks", {})

    benchmark_path = benchmark.get("path", "")
    actual_count = benchmark.get("total_cases_actual")
    declared_count = reference_claim.get("declared_total_cases")
    count_match = integrity.get("count_matches_reference_claim")

    print(f"[INFO] Manifest loaded: {MANIFEST_PATH}")
    if benchmark_path and benchmark_path != gs_path:
        print(f"[WARN] gs_path runner ({gs_path}) != benchmark_file.path manifest ({benchmark_path})")
    if actual_count is not None:
        print(f"[INFO] Manifest total_cases_actual: {actual_count}")
    if declared_count is not None:
        print(f"[INFO] Reference declared_total_cases: {declared_count}")
    if count_match is False:
        print("[WARN] Dataset count mismatch terdeteksi antara dataset aktif dan reference claim.")


def _validate_manifest_integrity(gs_data: list, manifest: Dict, strict_manifest: bool) -> None:
    if not manifest:
        return

    benchmark = manifest.get("benchmark_file", {})
    manifest_actual = benchmark.get("total_cases_actual")
    if manifest_actual is None:
        return

    runtime_count = len(gs_data)
    if runtime_count == manifest_actual:
        pass
    else:
        msg = (
            f"Manifest mismatch: runtime_count={runtime_count} "
            f"vs manifest.total_cases_actual={manifest_actual}"
        )
        if strict_manifest:
            raise RuntimeError(msg)
        print(f"[WARN] {msg}")

    manifest_evaluable = benchmark.get("evaluable_cases_excluding_split")
    if manifest_evaluable is not None:
        runtime_evaluable = sum(
            1 for item in gs_data if str(item.get("gold_label", "")).upper() != "SPLIT"
        )
        if runtime_evaluable != int(manifest_evaluable):
            msg = (
                f"Manifest mismatch: runtime_evaluable={runtime_evaluable} "
                f"vs manifest.evaluable_cases_excluding_split={manifest_evaluable}"
            )
            if strict_manifest:
                raise RuntimeError(msg)
            print(f"[WARN] {msg}")


def _resolve_strict_manifest(mode: EvaluationMode, strict_manifest: bool) -> bool:
    if mode == "scientific_claimable":
        return True
    return strict_manifest


def _enforce_mode_gate(manifest: Dict, mode: EvaluationMode) -> None:
    if mode != "scientific_claimable":
        return

    if not manifest:
        raise RuntimeError(
            "Mode scientific_claimable membutuhkan benchmark manifest yang valid."
        )

    integrity = manifest.get("integrity_checks", {})
    if integrity.get("count_matches_reference_claim") is False:
        raise RuntimeError(
            "Mode scientific_claimable ditolak: count_matches_reference_claim=false. "
            "Promosikan dataset referensi atau gunakan mode operational_offline."
        )


def extract_label_from_agent(agent_analysis: str) -> str:
    """Mengekstrak label A/B/C/D dari output JSON supervisor agent."""
    try:
        data = _json_or_raw(agent_analysis)
        label = str(data.get("label", "D")).upper().strip()
        return label if label in ["A", "B", "C", "D"] else "D"
    except Exception:
        return "D"


def run_benchmark(
    gs_path: str,
    output_path: str,
    strict_manifest: bool,
    mode: EvaluationMode,
) -> None:
    strict_manifest = _resolve_strict_manifest(mode, strict_manifest)
    manifest = _load_manifest()
    gs_path = _resolve_gs_path(gs_path, manifest)

    _enforce_mode_gate(manifest, mode)

    if not os.path.exists(gs_path):
        print(f"Error: {gs_path} not found.")
        return

    _log_manifest_status(gs_path, manifest)

    with open(gs_path, "r", encoding="utf-8") as f:
        gs_data = json.load(f)

    if not isinstance(gs_data, list):
        raise RuntimeError(f"Dataset format invalid: expected list, got {type(gs_data).__name__}")

    _validate_manifest_integrity(gs_data, manifest, strict_manifest)

    pipeline = NusantaraAgentPipeline()
    results = []
    correct = 0
    total = 0
    split_count = 0

    print(f"Starting Benchmark on {len(gs_data)} cases (AGENT INTEGRATED)...")

    for entry in gs_data:
        if entry.get("gold_label") == "SPLIT":
            split_count += 1
            continue
        
        total += 1
        query = entry.get("query", "")
        gold = entry.get("gold_label", "D")
        
        print(f"[{total}] Processing {entry.get('id', f'IDX-{total:04d}')}...", end=" ", flush=True)
        
        # 1. Jalankan Pipeline (dengan Orchestrator)
        ai_output = pipeline.process_query(query)
        
        # 2. Extract Label langsung dari Agent Synthesis
        predicted = extract_label_from_agent(ai_output.get("agent_analysis", ""))
        
        match = (predicted == gold)
        if match:
            correct += 1
        
        results.append({
            "id": entry.get("id", ""),
            "gold": gold,
            "predicted": predicted,
            "match": match,
            "reasoning": ai_output.get("agent_analysis", "")
        })
        print(f"Gold: {gold} | Pred: {predicted} | {'OK' if match else 'FAIL'}")

    accuracy = correct / total if total > 0 else 0
    
    summary = {
        "evaluation_mode": mode,
        "strict_manifest": strict_manifest,
        "source_dataset": gs_path,
        "total_raw_cases": len(gs_data),
        "split_skipped": split_count,
        "total_evaluated": total,
        "correct": correct,
        "accuracy": accuracy,
        "results": results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*30)
    print(f"BENCHMARK COMPLETE")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Results saved to: {output_path}")
    print("="*30)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Benchmark runner untuk Experiment 09.")
    parser.add_argument(
        "--mode",
        choices=["scientific_claimable", "operational_offline"],
        default="scientific_claimable",
        help=(
            "Mode evaluasi. scientific_claimable akan fail-hard jika manifest tidak koheren; "
            "operational_offline untuk tracking operasional."
        ),
    )
    parser.add_argument(
        "--gs-path",
        type=str,
        default="",
        help="Path dataset benchmark. Jika kosong, akan pakai manifest lalu fallback legacy path.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_PATH,
        help="Path output hasil benchmark JSON.",
    )
    parser.add_argument(
        "--strict-manifest",
        action="store_true",
        dest="strict_manifest",
        help=(
            "Hard-fail jika jumlah kasus runtime tidak cocok manifest. "
            "Dalam mode scientific_claimable, flag ini selalu diperlakukan true."
        ),
    )
    parser.add_argument(
        "--no-strict-manifest",
        action="store_false",
        dest="strict_manifest",
        help="Izinkan mismatch runtime_count vs manifest (hanya disarankan untuk mode operational_offline).",
    )
    parser.set_defaults(strict_manifest=True)
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    run_benchmark(
        gs_path=args.gs_path,
        output_path=args.output,
        strict_manifest=args.strict_manifest,
        mode=args.mode,
    )
