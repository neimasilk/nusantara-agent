import json

from _common import build_parser, compact_payload, fallback_answer, save_if_needed


def run_baseline(query: str) -> dict:
    jawaban = fallback_answer(query, "B1_DIRECT", [])
    return compact_payload(
        baseline_id="B1",
        query=query,
        jawaban=jawaban,
        komponen_aktif=["llm_direct_prompting"],
        komponen_nonaktif=["graph_retrieval", "vector_retrieval", "rule_engine", "debate"],
        detail={"provider": "deepseek_chat_or_fallback", "retrieval": False, "rules": False},
    )


def main() -> None:
    parser = build_parser("Apakah anak perempuan berhak waris menurut hukum nasional?")
    args = parser.parse_args()
    result = run_baseline(args.query)
    save_if_needed(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

