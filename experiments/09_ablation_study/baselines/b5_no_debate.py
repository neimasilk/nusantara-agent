import json

from _common import build_parser, compact_payload, fallback_answer, save_if_needed
from src.pipeline.nusantara_agent import NusantaraAgentPipeline


def run_baseline(query: str) -> dict:
    pipeline = NusantaraAgentPipeline()
    result = pipeline.process_query(query)
    graph_context = result.get("graph_context", "")
    vector_context = result.get("vector_context", [])
    jawaban = fallback_answer(query, "B5_NO_DEBATE", [graph_context] + vector_context)

    return compact_payload(
        baseline_id="B5",
        query=query,
        jawaban=jawaban,
        komponen_aktif=["router", "graph_retrieval", "vector_retrieval", "rule_engine"],
        komponen_nonaktif=["debate"],
        detail={
            "route": result.get("route", {}),
            "graph_context": graph_context,
            "vector_context": vector_context,
            "rule_results": result.get("rule_results", {}),
            "debate_enabled": False,
        },
    )


def main() -> None:
    parser = build_parser("Bandingkan hukum nasional dan adat Jawa untuk waris anak perempuan.")
    args = parser.parse_args()
    result = run_baseline(args.query)
    save_if_needed(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

