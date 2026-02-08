import json

from _common import build_parser, compact_payload, fallback_answer, save_if_needed
from src.pipeline.nusantara_agent import JsonGraphRetriever


def run_baseline(query: str, graph_json_path: str = "experiments/01_triple_extraction/result.json") -> dict:
    retriever = JsonGraphRetriever(graph_json_path)
    graph_context = retriever.retrieve_context(query, limit=10)
    jawaban = fallback_answer(query, "B3_GRAPH", [graph_context])
    return compact_payload(
        baseline_id="B3",
        query=query,
        jawaban=jawaban,
        komponen_aktif=["graph_retrieval", "llm_or_template_synthesis"],
        komponen_nonaktif=["vector_retrieval", "rule_engine", "debate"],
        detail={"graph_context": graph_context, "graph_path": graph_json_path},
    )


def main() -> None:
    parser = build_parser("Apa konteks adat Minangkabau terkait pusako tinggi?")
    parser.add_argument(
        "--graph-json",
        type=str,
        default="experiments/01_triple_extraction/result.json",
        help="Path JSON knowledge graph.",
    )
    args = parser.parse_args()
    result = run_baseline(args.query, graph_json_path=args.graph_json)
    save_if_needed(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

