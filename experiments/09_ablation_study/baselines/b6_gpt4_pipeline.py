import json
import os

from _common import build_parser, compact_payload, fallback_answer, save_if_needed
from src.pipeline.nusantara_agent import NusantaraAgentPipeline


def _gpt4_synthesis_or_fallback(query: str, contexts: list) -> tuple[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return fallback_answer(query, "B6_GPT4_FALLBACK", contexts), "fallback_no_api_key"

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        prompt = (
            "Ringkas jawaban hukum berikut secara hati-hati berdasarkan konteks yang ada.\n"
            f"Query: {query}\n"
            f"Konteks: {' '.join(contexts[:4])}\n"
            "Jawaban ringkas:"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return response.choices[0].message.content.strip(), "gpt4_live"
    except Exception:
        return fallback_answer(query, "B6_GPT4_FALLBACK", contexts), "fallback_runtime_error"


def run_baseline(query: str) -> dict:
    pipeline = NusantaraAgentPipeline()
    result = pipeline.process_query(query)
    contexts = [result.get("graph_context", "")] + result.get("vector_context", [])
    jawaban, mode = _gpt4_synthesis_or_fallback(query, contexts)
    return compact_payload(
        baseline_id="B6",
        query=query,
        jawaban=jawaban,
        komponen_aktif=["router", "graph_retrieval", "vector_retrieval", "rule_engine", "gpt4_synthesis"],
        komponen_nonaktif=["debate"],
        detail={"mode": mode, "route": result.get("route", {}), "rule_results": result.get("rule_results", {})},
    )


def main() -> None:
    parser = build_parser("Bagaimana relasi hukum nasional dan adat dalam sengketa waris?")
    args = parser.parse_args()
    result = run_baseline(args.query)
    save_if_needed(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

