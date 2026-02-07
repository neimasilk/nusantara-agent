import argparse
import json
import os
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


RUBRIC_TEXT = Path("experiments/07_advanced_orchestration/rubric.md").read_text(encoding="utf-8")


def _get_client(provider: str) -> OpenAI:
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY tidak ditemukan.")
        return OpenAI(api_key=api_key)
    if provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY tidak ditemukan.")
        return OpenAI(api_key=api_key, base_url="https://api.anthropic.com")
    if provider == "kimi":
        api_key = os.getenv("KIMI_API_KEY") or os.getenv("MOONSHOT_API_KEY")
        if not api_key:
            raise ValueError("KIMI_API_KEY/MOONSHOT_API_KEY tidak ditemukan.")
        return OpenAI(api_key=api_key, base_url="https://api.moonshot.ai/v1")
    raise ValueError("Provider tidak dikenal. Pilih: openai | anthropic")


def _load_run_index(path: Path) -> List[Dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("run_index harus list.")
    return data


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _score_one(client: OpenAI, model: str, query: str, answer: str) -> Dict:
    system_prompt = (
        "Kamu adalah evaluator independen. "
        "Tugasmu memberi skor berdasarkan rubric. "
        "JANGAN gunakan DeepSeek. Berikan skor 0-5 per dimensi."
    )
    user_prompt = (
        f"RUBRIC:\n{RUBRIC_TEXT}\n\n"
        f"QUERY:\n{query}\n\n"
        f"ANSWER:\n{answer}\n\n"
        "Output WAJIB JSON:\n"
        "{\n"
        '  "accuracy": 0,\n'
        '  "completeness": 0,\n'
        '  "cultural_sensitivity": 0,\n'
        '  "notes": "ringkas"\n'
        "}\n"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-score Exp07 outputs with independent LLM")
    parser.add_argument(
        "--run-index",
        default="experiments/07_advanced_orchestration/results/run_index.json",
        help="Path ke run_index.json",
    )
    parser.add_argument(
        "--provider",
        default="openai",
        help="LLM provider: openai | anthropic | kimi",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Model evaluator (bukan DeepSeek)",
    )
    parser.add_argument(
        "--out",
        default="experiments/07_advanced_orchestration/llm_scores.json",
        help="Path output skor JSON",
    )
    args = parser.parse_args()

    if args.provider == "kimi" and args.model == "gpt-4o-mini":
        args.model = "kimi-k2-turbo-preview"

    client = _get_client(args.provider)
    run_index = _load_run_index(Path(args.run_index))

    scores: List[Dict] = []
    for item in run_index:
        query_id = item.get("query_id")
        query = item.get("query", "")
        final_path = Path(item.get("artifacts", {}).get("final_synthesis", ""))
        answer = _read_text(final_path)
        if not answer:
            continue
        score = _score_one(client, args.model, query, answer)
        score["query_id"] = query_id
        scores.append(score)

    Path(args.out).write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"count": len(scores), "out": args.out}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
