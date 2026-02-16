import argparse
import importlib
import json
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Literal, Tuple, Union

# Jalankan dari project root
sys.path.append(os.getcwd())

from src.agents.router import route_query
from src.utils.benchmark_contract import (
    UNRESOLVED_GOLD_LABELS,
    count_evaluable_cases,
    is_evaluable_gold_label,
    resolve_manifest_evaluable_count,
)

EvaluationMode = Literal["scientific_claimable", "operational_offline"]

MANIFEST_PATH = Path("data/benchmark_manifest.json")
LEGACY_GS_PATH = Path("data/processed/gold_standard/gs_active_cases.json")
DEFAULT_OUTPUT_DIR = Path("experiments/09_ablation_study/results")
BASELINES_DIR = Path("experiments/09_ablation_study/baselines")

BASELINE_MODULES = {
    "B1": "b1_direct_prompting",
    "B2": "b2_vector_rag",
    "B3": "b3_graph_only",
    "B4": "b4_no_rules",
    "B5": "b5_no_debate",
    "B6": "b6_gpt4_pipeline",
    "B7": "b7_claude_pipeline",
}

ROUTE_TO_LABEL = {
    "pure_national": "A",
    "pure_adat": "B",
    "conflict": "C",
    "consensus": "C",
}

VALID_LABELS = {"A", "B", "C", "D"}


def _load_manifest() -> Dict:
    if not MANIFEST_PATH.exists():
        return {}
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[WARN] Manifest invalid ({MANIFEST_PATH}): {exc}")
        return {}


def _resolve_dataset_path(gs_path: str, manifest: Dict) -> Path:
    if gs_path:
        return Path(gs_path)
    manifest_path = manifest.get("benchmark_file", {}).get("path", "")
    if manifest_path:
        return Path(manifest_path)
    return LEGACY_GS_PATH


def _resolve_strict_manifest(mode: EvaluationMode, strict_manifest: bool) -> bool:
    if mode == "scientific_claimable":
        return True
    return strict_manifest


def _enforce_mode_gate(manifest: Dict, mode: EvaluationMode) -> None:
    if mode != "scientific_claimable":
        return
    if not manifest:
        raise RuntimeError("Mode scientific_claimable membutuhkan benchmark manifest valid.")
    if manifest.get("integrity_checks", {}).get("count_matches_reference_claim") is False:
        raise RuntimeError(
            "Mode scientific_claimable ditolak karena manifest mismatch "
            "(count_matches_reference_claim=false)."
        )


def _validate_manifest_count(gs_data: List[Dict], manifest: Dict, strict_manifest: bool) -> None:
    if not manifest:
        return
    expected = manifest.get("benchmark_file", {}).get("total_cases_actual")
    if expected is None:
        return
    runtime_count = len(gs_data)
    if runtime_count != int(expected):
        msg = f"Manifest mismatch: runtime_count={runtime_count} vs manifest.total_cases_actual={expected}"
        if strict_manifest:
            raise RuntimeError(msg)
        print(f"[WARN] {msg}")

    expected_evaluable = resolve_manifest_evaluable_count(manifest.get("benchmark_file", {}))
    if expected_evaluable is None:
        return
    runtime_evaluable = count_evaluable_cases(gs_data)
    if runtime_evaluable != expected_evaluable:
        msg = (
            "Manifest mismatch: "
            f"runtime_evaluable={runtime_evaluable} "
            f"vs manifest_evaluable={expected_evaluable}"
        )
        if strict_manifest:
            raise RuntimeError(msg)
        print(f"[WARN] {msg}")


def _load_dataset(path: Path) -> List[Dict]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset tidak ditemukan: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise RuntimeError(f"Dataset harus list, dapat: {type(data).__name__}")
    return data


def _load_baseline_module(module_name: str):
    if str(BASELINES_DIR.resolve()) not in sys.path:
        sys.path.insert(0, str(BASELINES_DIR.resolve()))
    return importlib.import_module(module_name)


def _extract_label_from_text(text: str) -> str:
    if not text:
        return ""
    text = str(text).strip()

    # JSON-like label, contoh {"label":"C"}
    json_like = re.search(r'"label"\s*:\s*"([ABCDabcd])"', text)
    if json_like:
        return json_like.group(1).upper()

    # Plain label marker, contoh "Label: B"
    plain_like = re.search(r"\blabel\s*[:=]\s*([ABCDabcd])\b", text, flags=re.IGNORECASE)
    if plain_like:
        return plain_like.group(1).upper()
    return ""


def _infer_predicted_label(payload: Dict, query: str) -> Tuple[str, str]:
    direct = str(payload.get("label", "")).upper().strip()
    if direct in {"A", "B", "C", "D"}:
        return direct, "payload.label"

    detail = payload.get("detail", {}) if isinstance(payload, dict) else {}
    if isinstance(detail, dict):
        rule_results = detail.get("rule_results", {})
        if isinstance(rule_results, dict):
            nasional_atoms = rule_results.get("nasional", [])
            adat_obj = rule_results.get("adat", {})

            has_nasional = isinstance(nasional_atoms, list) and len(nasional_atoms) > 0
            has_adat = isinstance(adat_obj, dict) and any(
                isinstance(v, list) and len(v) > 0 for v in adat_obj.values()
            )
            has_conflict = False
            if has_nasional:
                has_conflict = any("conflict" in str(atom).lower() for atom in nasional_atoms)
            if not has_conflict and isinstance(adat_obj, dict):
                for atoms in adat_obj.values():
                    if isinstance(atoms, list) and any("conflict" in str(atom).lower() for atom in atoms):
                        has_conflict = True
                        break

            if has_conflict:
                return "C", "detail.rule_results.conflict"
            if has_nasional and not has_adat:
                return "A", "detail.rule_results.nasional_only"
            if has_adat and not has_nasional:
                return "B", "detail.rule_results.adat_only"
            if has_nasional and has_adat:
                return "C", "detail.rule_results.mixed"

        route = detail.get("route", {})
        if isinstance(route, dict):
            route_label = str(route.get("label", "")).strip().lower()
            if route_label in ROUTE_TO_LABEL:
                return ROUTE_TO_LABEL[route_label], "detail.route.label"

    jawaban = payload.get("jawaban", "") if isinstance(payload, dict) else ""
    text_label = _extract_label_from_text(jawaban)
    if text_label in {"A", "B", "C", "D"}:
        return text_label, "jawaban.text"

    route_fallback = route_query(query, use_llm=False).get("label", "")
    route_fallback = str(route_fallback).strip().lower()
    if route_fallback in ROUTE_TO_LABEL:
        return ROUTE_TO_LABEL[route_fallback], "query.route_fallback"

    return "D", "default.D"


def _derive_majority_vote(votes: Dict[str, str]) -> Tuple[str, str]:
    valid_votes = [
        str(v).upper().strip()
        for v in votes.values()
        if str(v).upper().strip() in VALID_LABELS
    ]
    if not valid_votes:
        return "D", "NO_VOTES"

    counts = Counter(valid_votes).most_common()
    if len(counts) > 1 and counts[0][1] == counts[1][1]:
        return "D", "TIE"

    label = counts[0][0]
    consensus = "UNANIMOUS" if counts[0][1] == len(valid_votes) else "MAJORITY"
    return label, consensus


def _run_single_baseline(
    baseline_id: str,
    module_name: str,
    cases: List[Dict],
    seed: int,
    output_dir: Path,
    mode: EvaluationMode,
    source_dataset: str,
) -> Dict:
    module = _load_baseline_module(module_name)
    if not hasattr(module, "run_baseline"):
        raise RuntimeError(f"Module {module_name} tidak punya fungsi run_baseline(query).")

    working_cases = [dict(item) for item in cases]
    random.Random(seed).shuffle(working_cases)

    predictions: List[Dict] = []
    total = 0
    correct = 0
    unresolved_skipped = 0

    for case in working_cases:
        gold = str(case.get("gold_label", "")).upper()
        if not is_evaluable_gold_label(gold):
            unresolved_skipped += 1
            continue

        total += 1
        query = str(case.get("query", ""))
        payload = module.run_baseline(query)
        predicted, label_source = _infer_predicted_label(payload, query)
        match = predicted == gold
        if match:
            correct += 1

        predictions.append(
            {
                "id": case.get("id", ""),
                "gold": gold,
                "predicted": predicted,
                "match": match,
                "label_source": label_source,
                "baseline_payload": payload,
            }
        )

    accuracy = correct / total if total else 0.0

    run_result = {
        "baseline_id": baseline_id,
        "module_name": module_name,
        "seed": seed,
        "evaluation_mode": mode,
        "source_dataset": source_dataset,
        "total_raw_cases": len(cases),
        "split_skipped": unresolved_skipped,  # Backward compatibility
        "unresolved_skipped": unresolved_skipped,
        "unresolved_labels": sorted(UNRESOLVED_GOLD_LABELS),
        "total_evaluated": total,
        "correct": correct,
        "accuracy": accuracy,
        "predictions": predictions,
    }

    baseline_dir = output_dir / "baseline_runs" / baseline_id
    baseline_dir.mkdir(parents=True, exist_ok=True)
    run_path = baseline_dir / f"run_seed_{seed}.json"
    run_path.write_text(json.dumps(run_result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"[OK] {baseline_id} seed={seed} "
        f"accuracy={accuracy:.2%} saved={run_path.as_posix()}"
    )
    return run_result


def _run_human_baseline(
    cases: List[Dict],
    output_dir: Path,
    mode: EvaluationMode,
    source_dataset: str,
) -> Dict:
    predictions: List[Dict] = []
    total = 0
    correct = 0
    unresolved_skipped = 0
    per_expert_stats: Dict[str, Dict[str, Union[int, float]]] = {}

    for case in cases:
        gold = str(case.get("gold_label", "")).upper()
        votes = case.get("expert_votes", {}) if isinstance(case, dict) else {}
        if not isinstance(votes, dict):
            votes = {}

        expert_labels = {
            str(k): str(v).upper().strip()
            for k, v in votes.items()
            if str(v).upper().strip() in VALID_LABELS
        }
        for expert_id, expert_label in expert_labels.items():
            stat = per_expert_stats.setdefault(
                expert_id,
                {"n": 0, "correct": 0, "accuracy": 0.0},
            )
            if is_evaluable_gold_label(gold):
                stat["n"] = int(stat["n"]) + 1
                if expert_label == gold:
                    stat["correct"] = int(stat["correct"]) + 1

        if not is_evaluable_gold_label(gold):
            unresolved_skipped += 1
            continue

        total += 1
        predicted, consensus_type = _derive_majority_vote(expert_labels)
        match = predicted == gold
        if match:
            correct += 1

        predictions.append(
            {
                "id": case.get("id", ""),
                "gold": gold,
                "predicted": predicted,
                "match": match,
                "label_source": "expert_votes.majority",
                "consensus_type": consensus_type,
                "expert_votes": expert_labels,
            }
        )

    for stat in per_expert_stats.values():
        n = int(stat["n"])
        c = int(stat["correct"])
        stat["accuracy"] = (c / n) if n else 0.0

    accuracy = correct / total if total else 0.0
    run_result = {
        "baseline_id": "B8",
        "module_name": "human_expert_panel",
        "seed": "human_panel",
        "evaluation_mode": mode,
        "source_dataset": source_dataset,
        "total_raw_cases": len(cases),
        "split_skipped": unresolved_skipped,  # Backward compatibility
        "unresolved_skipped": unresolved_skipped,
        "unresolved_labels": sorted(UNRESOLVED_GOLD_LABELS),
        "total_evaluated": total,
        "correct": correct,
        "accuracy": accuracy,
        "per_expert_stats": per_expert_stats,
        "predictions": predictions,
    }

    baseline_dir = output_dir / "baseline_runs" / "B8"
    baseline_dir.mkdir(parents=True, exist_ok=True)
    run_path = baseline_dir / "run_seed_human_panel.json"
    run_path.write_text(json.dumps(run_result, ensure_ascii=False, indent=2), encoding="utf-8")

    human_artifact_dir = BASELINES_DIR / "b8_human_expert"
    human_artifact_dir.mkdir(parents=True, exist_ok=True)
    human_summary_path = human_artifact_dir / "active_set_human_baseline_summary.json"
    human_summary = {
        "source_dataset": source_dataset,
        "evaluation_mode": mode,
        "total_evaluated": total,
        "accuracy_majority_vote": accuracy,
        "split_skipped": unresolved_skipped,
        "unresolved_skipped": unresolved_skipped,
        "unresolved_labels": sorted(UNRESOLVED_GOLD_LABELS),
        "per_expert_stats": per_expert_stats,
        "generated_from": run_path.as_posix(),
        "notes": [
            "Artifact ini berasal dari expert_votes yang tersedia di dataset aktif.",
            "Bukan pengganti target ART-064 full 200-case human baseline.",
        ],
    }
    human_summary_path.write_text(json.dumps(human_summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        f"[OK] B8 human_panel accuracy={accuracy:.2%} "
        f"saved={run_path.as_posix()}"
    )
    return run_result


def _summarize_runs(runs: List[Dict]) -> Dict:
    per_baseline: Dict[str, Dict] = {}
    for run in runs:
        baseline_id = run["baseline_id"]
        info = per_baseline.setdefault(
            baseline_id,
            {
                "baseline_id": baseline_id,
                "n_runs": 0,
                "seeds": [],
                "accuracies": [],
                "total_evaluated_per_run": [],
            },
        )
        info["n_runs"] += 1
        info["seeds"].append(run["seed"])
        info["accuracies"].append(run["accuracy"])
        info["total_evaluated_per_run"].append(run["total_evaluated"])

    for info in per_baseline.values():
        acc = info["accuracies"]
        info["mean_accuracy"] = sum(acc) / len(acc) if acc else 0.0
        if len(acc) > 1:
            mean = info["mean_accuracy"]
            var = sum((x - mean) ** 2 for x in acc) / (len(acc) - 1)
            info["std_accuracy"] = var ** 0.5
        else:
            info["std_accuracy"] = 0.0
    return {"per_baseline": per_baseline}


def run_all_baselines(
    gs_path: str,
    output_dir: Path,
    seeds: List[int],
    strict_manifest: bool,
    mode: EvaluationMode,
    force_offline: bool,
    disable_external_llm: bool,
    include_human_b8: bool,
) -> Dict:
    strict_manifest = _resolve_strict_manifest(mode, strict_manifest)
    manifest = _load_manifest()
    _enforce_mode_gate(manifest, mode)

    dataset_path = _resolve_dataset_path(gs_path, manifest)
    cases = _load_dataset(dataset_path)
    _validate_manifest_count(cases, manifest, strict_manifest)

    old_force_offline = os.getenv("NUSANTARA_FORCE_OFFLINE")
    old_openai = os.getenv("OPENAI_API_KEY")
    old_anthropic = os.getenv("ANTHROPIC_API_KEY")

    try:
        if force_offline:
            os.environ["NUSANTARA_FORCE_OFFLINE"] = "1"
        if disable_external_llm:
            os.environ.pop("OPENAI_API_KEY", None)
            os.environ.pop("ANTHROPIC_API_KEY", None)

        runs: List[Dict] = []
        for baseline_id, module_name in BASELINE_MODULES.items():
            for seed in seeds:
                runs.append(
                    _run_single_baseline(
                        baseline_id=baseline_id,
                        module_name=module_name,
                        cases=cases,
                        seed=seed,
                        output_dir=output_dir,
                        mode=mode,
                        source_dataset=dataset_path.as_posix(),
                    )
                )

        if include_human_b8:
            runs.append(
                _run_human_baseline(
                    cases=cases,
                    output_dir=output_dir,
                    mode=mode,
                    source_dataset=dataset_path.as_posix(),
                )
            )

        summary = {
            "evaluation_mode": mode,
            "strict_manifest": strict_manifest,
            "force_offline": force_offline,
            "disable_external_llm": disable_external_llm,
            "source_dataset": dataset_path.as_posix(),
            "n_baselines": len(BASELINE_MODULES),
            "human_baseline_included": include_human_b8,
            "n_seeds": len(seeds),
            "total_runs": len(runs),
            "seeds": seeds,
            "runs": [
                {
                    "baseline_id": r["baseline_id"],
                    "seed": r["seed"],
                    "accuracy": r["accuracy"],
                    "total_evaluated": r["total_evaluated"],
                }
                for r in runs
            ],
            "aggregate": _summarize_runs(runs),
        }
        output_dir.mkdir(parents=True, exist_ok=True)
        summary_path = output_dir / "run_all_baselines_summary.json"
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] Summary saved: {summary_path.as_posix()}")
        return summary
    finally:
        if old_force_offline is None:
            os.environ.pop("NUSANTARA_FORCE_OFFLINE", None)
        else:
            os.environ["NUSANTARA_FORCE_OFFLINE"] = old_force_offline

        if old_openai is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old_openai

        if old_anthropic is None:
            os.environ.pop("ANTHROPIC_API_KEY", None)
        else:
            os.environ["ANTHROPIC_API_KEY"] = old_anthropic


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Runner ART-065: semua baseline Exp09 (7 baseline x N seed).")
    parser.add_argument(
        "--mode",
        choices=["scientific_claimable", "operational_offline"],
        default="operational_offline",
        help="Mode evaluasi. scientific_claimable fail-hard bila manifest mismatch.",
    )
    parser.add_argument(
        "--gs-path",
        type=str,
        default="",
        help="Path dataset benchmark. Jika kosong pakai manifest -> fallback legacy.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help="Direktori output hasil baseline runs.",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[11, 22, 33],
        help="Daftar seed run. Default sesuai ART-065 = 3 seed.",
    )
    parser.add_argument(
        "--strict-manifest",
        action="store_true",
        dest="strict_manifest",
        help="Hard-fail jika runtime count tidak cocok manifest.",
    )
    parser.add_argument(
        "--no-strict-manifest",
        action="store_false",
        dest="strict_manifest",
        help="Izinkan mismatch (disarankan hanya untuk mode operational_offline).",
    )
    parser.set_defaults(strict_manifest=True)
    parser.add_argument(
        "--force-offline",
        action="store_true",
        default=True,
        help="Paksa mode offline (default true).",
    )
    parser.add_argument(
        "--allow-online",
        action="store_false",
        dest="force_offline",
        help="Izinkan mode online jika env/API tersedia.",
    )
    parser.add_argument(
        "--disable-external-llm",
        action="store_true",
        default=True,
        help="Hapus sementara OPENAI/ANTHROPIC key agar B6/B7 tidak hit API (default true).",
    )
    parser.add_argument(
        "--allow-external-llm",
        action="store_false",
        dest="disable_external_llm",
        help="Izinkan B6/B7 memakai API key bila tersedia.",
    )
    parser.add_argument(
        "--include-human-b8",
        action="store_true",
        default=True,
        help="Sertakan baseline B8 (human panel) dari expert_votes dataset aktif.",
    )
    parser.add_argument(
        "--skip-human-b8",
        action="store_false",
        dest="include_human_b8",
        help="Jalankan hanya baseline otomatis B1..B7.",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    run_all_baselines(
        gs_path=args.gs_path,
        output_dir=Path(args.output_dir),
        seeds=args.seeds,
        strict_manifest=args.strict_manifest,
        mode=args.mode,
        force_offline=args.force_offline,
        disable_external_llm=args.disable_external_llm,
        include_human_b8=args.include_human_b8,
    )
