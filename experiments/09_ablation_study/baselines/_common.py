import argparse
import json
from typing import Dict, List


def build_parser(default_query: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query",
        type=str,
        default=default_query,
        help="Pertanyaan hukum yang akan dievaluasi.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Path output JSON (opsional).",
    )
    return parser


def save_if_needed(output_path: str, payload: Dict) -> None:
    if not output_path:
        return
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def fallback_answer(query: str, mode: str, contexts: List[str]) -> str:
    if not contexts:
        return f"[{mode}] Jawaban ringkas untuk query: {query}. Evidence eksplisit tidak tersedia."
    kalimat = " ".join(contexts[:2])
    return f"[{mode}] Query: {query}. Ringkasan evidence: {kalimat}"


def compact_payload(
    baseline_id: str,
    query: str,
    jawaban: str,
    komponen_aktif: List[str],
    komponen_nonaktif: List[str],
    detail: Dict,
) -> Dict:
    return {
        "baseline_id": baseline_id,
        "query": query,
        "jawaban": jawaban,
        "komponen_aktif": komponen_aktif,
        "komponen_nonaktif": komponen_nonaktif,
        "detail": detail,
    }

