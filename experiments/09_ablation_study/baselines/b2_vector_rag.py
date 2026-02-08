import json

from _common import build_parser, compact_payload, fallback_answer, save_if_needed
from src.pipeline.nusantara_agent import InMemoryVectorRetriever


def run_baseline(query: str) -> dict:
    retriever = InMemoryVectorRetriever(
        [
            "KUHPerdata menekankan prioritas ahli waris dan perlindungan legitime portie.",
            "Dalam adat Jawa modern, gono-gini sering diselesaikan melalui musyawarah.",
            "Dalam adat Bali, hak waris perempuan berkembang pasca MDP 2010.",
        ]
    )
    contexts = retriever.retrieve(query, top_k=3)
    jawaban = fallback_answer(query, "B2_VECTOR", contexts)
    return compact_payload(
        baseline_id="B2",
        query=query,
        jawaban=jawaban,
        komponen_aktif=["vector_retrieval", "llm_or_template_synthesis"],
        komponen_nonaktif=["graph_retrieval", "rule_engine", "debate"],
        detail={"vector_context": contexts},
    )


def main() -> None:
    parser = build_parser("Bagaimana pembagian gono-gini dalam praktik hukum Indonesia?")
    args = parser.parse_args()
    result = run_baseline(args.query)
    save_if_needed(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

