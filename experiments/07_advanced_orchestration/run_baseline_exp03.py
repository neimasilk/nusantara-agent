import argparse
import json
import os
import time
from pathlib import Path
from typing import Dict, List, Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[List[HumanMessage], lambda x, y: x + y]
    national_context: str
    adat_context: str
    final_synthesis: str


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
    )


def _read_graph_data(graph_data_path: str) -> str:
    path = Path(graph_data_path)
    if not path.exists():
        return "[ERROR] Knowledge Graph data tidak ditemukan."
    return path.read_text(encoding="utf-8")


def _national_agent(llm: ChatOpenAI, state: AgentState):
    query = state["messages"][0].content
    prompt = (
        "Kamu adalah pakar hukum perdata nasional Indonesia. "
        f"Analisis pertanyaan ini berdasarkan KUHPerdata: '{query}'. "
        "Fokus pada hak anak kandung dan aturan harta pencaharian (gono-gini)."
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"national_context": response.content}


def _adat_agent(llm: ChatOpenAI, graph_data_path: str, state: AgentState):
    graph_data = _read_graph_data(graph_data_path)
    query = state["messages"][0].content
    prompt = (
        "Kamu adalah tetua adat Minangkabau. "
        "Analisis pertanyaan ini berdasarkan data Knowledge Graph adat berikut: "
        f"{graph_data}. Pertanyaan: '{query}'. "
        "Fokus pada hak kemenakan dan perbedaan Pusako Tinggi vs Pusako Rendah."
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"adat_context": response.content}


def _supervisor_agent(llm: ChatOpenAI, state: AgentState):
    national = state.get("national_context", "")
    adat = state.get("adat_context", "")
    query = state["messages"][0].content
    prompt = (
        "Kamu adalah Hakim Supervisor yang ahli dalam pluralisme hukum. "
        f"Tugasmu adalah mensintesis jawaban dari perspektif Nasional: {national} "
        f"dan perspektif Adat: {adat}. Pertanyaan User: {query}. "
        "Akui adanya konflik norma dan jelaskan solusi pluralistik."
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    return {"final_synthesis": response.content}


def build_baseline_orchestrator(graph_data_path: str):
    llm = _get_llm()
    workflow = StateGraph(AgentState)
    workflow.add_node("national_law", lambda state: _national_agent(llm, state))
    workflow.add_node("adat_law", lambda state: _adat_agent(llm, graph_data_path, state))
    workflow.add_node("adjudicator", lambda state: _supervisor_agent(llm, state))
    workflow.set_entry_point("national_law")
    workflow.add_edge("national_law", "adat_law")
    workflow.add_edge("adat_law", "adjudicator")
    workflow.add_edge("adjudicator", END)
    return workflow.compile()


def _load_queries(path: Path) -> List[Dict[str, str]]:
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


def run_baseline(query_file: Path, graph_data_path: str, output_dir: Path, limit: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    queries = _load_queries(query_file)
    if limit > 0:
        queries = queries[:limit]

    app = build_baseline_orchestrator(graph_data_path=graph_data_path)
    run_index = []

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
        state = app.invoke({"messages": [HumanMessage(content=query)]})
        t1 = time.perf_counter()

        final_answer = state.get("final_synthesis", "")
        (case_dir / "final_synthesis.txt").write_text(final_answer, encoding="utf-8")

        summary = {
            "query_id": query_id,
            "query": query,
            "graph_data_path": graph_data_path,
            "timing_seconds": {"total": round(t1 - t0, 4)},
            "artifacts": {"final_synthesis": str(case_dir / "final_synthesis.txt")},
        }
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        run_index.append(summary)

    (output_dir / "run_index.json").write_text(
        json.dumps(run_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run baseline Exp03 sequential pipeline on Exp07 queries")
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
        default="experiments/07_advanced_orchestration/baseline_results",
        help="Folder output baseline",
    )
    parser.add_argument("--limit", type=int, default=0, help="Batasi jumlah query (0 = semua)")

    args = parser.parse_args()
    run_baseline(
        query_file=Path(args.query_file),
        graph_data_path=args.graph_data,
        output_dir=Path(args.output_dir),
        limit=args.limit,
    )
