import argparse
import json
import os
import time
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

import sys

sys.path.append(os.getcwd())

from src.agents import run_debate, save_debate_logs, route_query
from src.agents.orchestrator import build_parallel_orchestrator

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


def _supervisor_synthesis(llm: ChatOpenAI, query: str, nla: Dict, ala: Dict) -> str:
    prompt = (
        "Kamu adalah Hakim Supervisor yang ahli dalam pluralisme hukum. "
        "Sintesis jawaban berdasarkan dua agent berikut:\n\n"
        f"NLA: {json.dumps(nla, ensure_ascii=False)}\n"
        f"ALA: {json.dumps(ala, ensure_ascii=False)}\n\n"
        f"QUERY: {query}\n\n"
        "Tulis jawaban final yang mengakui konflik norma, jelaskan trade-off, "
        "dan beri keputusan pluralistik. Ringkas, faktual, dan tidak overclaim."
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    return response.content


def run_experiment(
    query_file: Path,
    graph_data_path: str,
    output_dir: Path,
    max_rounds: int,
    limit: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    queries = _load_queries(query_file)

    app = build_parallel_orchestrator(graph_data_path=graph_data_path)
    llm = _get_llm()

    run_index = []

    if limit > 0:
        queries = queries[:limit]

    for item in queries:
        query_id = item.get("id", "Q")
        query = item.get("query", "").strip()
        if not query:
            continue

        case_dir = output_dir / query_id
        case_dir.mkdir(parents=True, exist_ok=True)
        summary_path = case_dir / "summary.json"
        if summary_path.exists():
            run_index.append(json.loads(summary_path.read_text(encoding="utf-8")))
            continue

        t0 = time.perf_counter()
        routing = route_query(query, use_llm=False)

        inputs = {"messages": [HumanMessage(content=query)]}
        state = app.invoke(inputs)
        t1 = time.perf_counter()

        national_context = state.get("national_context", "")
        adat_context = state.get("adat_context", "")

        debate_result = run_debate(
            query=query,
            national_context=national_context,
            adat_context=adat_context,
            max_rounds=max_rounds,
        )
        save_debate_logs(str(case_dir), debate_result)
        t2 = time.perf_counter()

        final_answer = _supervisor_synthesis(
            llm,
            query=query,
            nla=debate_result.get("final_nla", {}),
            ala=debate_result.get("final_ala", {}),
        )
        t3 = time.perf_counter()

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

    args = parser.parse_args()

    run_experiment(
        query_file=Path(args.query_file),
        graph_data_path=args.graph_data,
        output_dir=Path(args.output_dir),
        max_rounds=args.rounds,
        limit=args.limit,
    )
