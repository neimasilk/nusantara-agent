import argparse
import json
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

import sys

sys.path.append(os.getcwd())

from src.agents import run_debate, save_debate_logs, route_query
from src.agents.orchestrator import build_parallel_orchestrator
from src.utils.token_usage import extract_token_usage as _extract_token_usage, merge_usage as _add_usage
from src.kg_engine.search import SimpleKGSearch

load_dotenv()


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
    )


def _load_queries(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return [
            {
                "id": "Q1",
                "query": (
                    "Seorang ayah Minangkabau meninggal. "
                    "Dia meninggalkan rumah yang dibeli dari hasil kerjanya sendiri. "
                    "Siapa yang lebih berhak: anak kandungnya atau kemenakannya?"
                ),
            }
        ]

    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        if data and isinstance(data[0], str):
            return [{"id": f"Q{i+1}", "query": q} for i, q in enumerate(data)]
        return [
            {"id": item.get("id", f"Q{i+1}"), "query": item.get("query", "")}
            for i, item in enumerate(data)
            if isinstance(item, dict)
        ]
    raise ValueError("Format file query tidak dikenal. Gunakan list string atau list objek {id, query}.")


def _supervisor_synthesis(llm: ChatOpenAI, query: str, nla: Dict, ala: Dict) -> Tuple[str, Dict[str, int]]:
    prompt = (
        "Kamu adalah Hakim Supervisor yang ahli dalam pluralisme hukum. "
        "Sintesis jawaban berdasarkan dua agent berikut:\n\n"
        f"NLA: {json.dumps(nla, ensure_ascii=False)}\n"
        f"ALA: {json.dumps(ala, ensure_ascii=False)}\n\n"
        f"QUERY: {query}\n\n"
        "Tulis jawaban final yang mengakui konflik norma, jelaskan trade-off, "
        "dan beri keputusan pluralistik.\n"
        "ATURAN: ringkas (<= 1200 karakter), faktual, tidak overclaim, "
        "jangan menambah klaim di luar dua agent."
    )
    # Gunakan ChatOpenAI secara langsung untuk synthesis
    response = llm.invoke([SystemMessage(content=prompt)])
    return response.content, _extract_token_usage(response)


def run_experiment(
    query_file: Path,
    graph_data_path: str,
    output_dir: Path,
    max_rounds: int,
    limit: int,
    force: bool,
    start: int,
    count: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    queries = _load_queries(query_file)

    app = build_parallel_orchestrator(graph_data_path=graph_data_path)
    llm = _get_llm()
    searcher = SimpleKGSearch(graph_data_path)

    run_index = []

    if start < 0:
        start = 0
    if count > 0:
        queries = queries[start : start + count]
    elif limit > 0:
        queries = queries[:limit]

    for item in queries:
        query_id = item.get("id", "Q")
        query = item.get("query", "").strip()
        if not query:
            continue

        case_dir = output_dir / query_id
        case_dir.mkdir(parents=True, exist_ok=True)
        summary_path = case_dir / "summary.json"
        if summary_path.exists() and not force:
            run_index.append(json.loads(summary_path.read_text(encoding="utf-8")))
            continue

        print(f"Running Query {query_id}: {query[:50]}...")
        t0 = time.perf_counter()
        routing = route_query(query, use_llm=False)

        inputs = {"messages": [HumanMessage(content=query)]}
        state = app.invoke(inputs)
        t1 = time.perf_counter()

        national_context = state.get("national_context", "")
        adat_context = state.get("adat_context", "")

        retrieval_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        _add_usage(retrieval_usage, state.get("national_usage", {}))
        _add_usage(retrieval_usage, state.get("adat_usage", {}))
        _add_usage(retrieval_usage, state.get("supervisor_usage", {}))

        debate_result = run_debate(
            query=query,
            national_context=national_context,
            adat_context=adat_context,
            max_rounds=max_rounds,
            search_func=searcher.get_context_for_query
        )
        save_debate_logs(str(case_dir), debate_result)
        t2 = time.perf_counter()

        final_answer, supervisor_usage = _supervisor_synthesis(
            llm,
            query=query,
            nla=debate_result.get("final_nla", {}),
            ala=debate_result.get("final_ala", {}),
        )
        t3 = time.perf_counter()


        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        _add_usage(total_usage, retrieval_usage)
        _add_usage(total_usage, debate_result.get("token_usage", {}))
        _add_usage(total_usage, supervisor_usage)

        (case_dir / "final_synthesis.txt").write_text(final_answer, encoding="utf-8")

        summary = {
            "query_id": query_id,
            "query": query,
            "routing": routing,
            "graph_data_path": graph_data_path,
            "timing_seconds": {
                "retrieval_parallel": round(t1 - t0, 4),
                "debate": round(t2 - t1, 4),
                "supervisor": round(t3 - t2, 4),
                "total": round(t3 - t0, 4),
            },
            "token_usage": {
                "retrieval_parallel": retrieval_usage,
                "debate": debate_result.get("token_usage", {}),
                "supervisor": supervisor_usage,
                "total": total_usage,
            },
            "llm_call_count": {
                "retrieval_parallel": 3,
                "debate": debate_result.get("llm_call_count", 0),
                "supervisor": 1,
                "total": 4 + int(debate_result.get("llm_call_count", 0)),
            },
            "artifacts": {
                "debate_summary": str(case_dir / "debate_summary.json"),
                "final_synthesis": str(case_dir / "final_synthesis.txt"),
            },
        }

        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        run_index.append(summary)

    (output_dir / "run_index.json").write_text(
        json.dumps(run_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Experiment 07 - Advanced Orchestration")
    parser.add_argument(
        "--query-file",
        default="experiments/07_advanced_orchestration/test_queries.json",
        help="Path ke file query JSON",
    )
    parser.add_argument(
        "--graph-data",
        default="experiments/01_triple_extraction/result.json",
        help="Path ke knowledge graph data",
    )
    parser.add_argument(
        "--output-dir",
        default="experiments/07_advanced_orchestration/results",
        help="Folder output hasil eksperimen",
    )
    parser.add_argument("--rounds", type=int, default=2, help="Jumlah round debate")
    parser.add_argument("--limit", type=int, default=0, help="Batasi jumlah query (0 = semua)")
    parser.add_argument("--force", action="store_true", help="Tulis ulang output meski sudah ada")
    parser.add_argument("--start", type=int, default=0, help="Index mulai (0-based)")
    parser.add_argument("--count", type=int, default=0, help="Jumlah query dari index start (0 = semua)")

    args = parser.parse_args()

    run_experiment(
        query_file=Path(args.query_file),
        graph_data_path=args.graph_data,
        output_dir=Path(args.output_dir),
        max_rounds=args.rounds,
        limit=args.limit,
        force=args.force,
        start=args.start,
        count=args.count,
    )
