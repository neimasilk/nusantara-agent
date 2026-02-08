import json
import os

from _common import build_parser, compact_payload, fallback_answer, save_if_needed
from src.pipeline.nusantara_agent import NusantaraAgentPipeline


def _claude_synthesis_or_fallback(query: str, contexts: list) -> tuple[str, str]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return fallback_answer(query, "B7_CLAUDE_FALLBACK", contexts), "fallback_no_api_key"

    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=api_key)
        prompt = (
            "Ringkas jawaban hukum berikut secara netral berdasarkan konteks.\n"
            f"Query: {query}\n"
            f"Konteks: {' '.join(contexts[:4])}\n"
            "Jawaban ringkas:"
        )
        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=300,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}],
        )
        teks = ""
        for part in response.content:
            if getattr(part, "type", "") == "text":
                teks += part.text
        return teks.strip(), "claude_live"
    except Exception:
        return fallback_answer(query, "B7_CLAUDE_FALLBACK", contexts), "fallback_runtime_error"


def run_baseline(query: str) -> dict:
    pipeline = NusantaraAgentPipeline()
    result = pipeline.process_query(query)
    contexts = [result.get("graph_context", "")] + result.get("vector_context", [])
    jawaban, mode = _claude_synthesis_or_fallback(query, contexts)
    return compact_payload(
        baseline_id="B7",
        query=query,
        jawaban=jawaban,
        komponen_aktif=["router", "graph_retrieval", "vector_retrieval", "rule_engine", "claude_synthesis"],
        komponen_nonaktif=["debate"],
        detail={"mode": mode, "route": result.get("route", {}), "rule_results": result.get("rule_results", {})},
    )


def main() -> None:
    parser = build_parser("Apa pendekatan pluralistik terbaik untuk sengketa waris adat vs nasional?")
    args = parser.parse_args()
    result = run_baseline(args.query)
    save_if_needed(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

