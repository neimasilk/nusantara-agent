import os
from typing import Annotated, TypedDict, List, Dict
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    national_context: str
    adat_context: str
    final_synthesis: str
    national_usage: Dict[str, int]
    adat_usage: Dict[str, int]
    supervisor_usage: Dict[str, int]


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


def _extract_token_usage(message: BaseMessage) -> Dict[str, int]:
    usage = getattr(message, "usage_metadata", None) or {}
    response_metadata = getattr(message, "response_metadata", None) or {}
    token_usage = response_metadata.get("token_usage", {}) if isinstance(response_metadata, dict) else {}

    prompt_tokens = usage.get("input_tokens", token_usage.get("prompt_tokens", 0))
    completion_tokens = usage.get("output_tokens", token_usage.get("completion_tokens", 0))
    total_tokens = usage.get("total_tokens", token_usage.get("total_tokens", 0))

    if not total_tokens:
        total_tokens = prompt_tokens + completion_tokens

    return {
        "prompt_tokens": int(prompt_tokens or 0),
        "completion_tokens": int(completion_tokens or 0),
        "total_tokens": int(total_tokens or 0),
    }


def _national_agent(llm: ChatOpenAI, state: AgentState):
    query = state["messages"][0].content
    prompt = (
        "Kamu adalah pakar hukum perdata nasional Indonesia. "
        f"Analisis pertanyaan ini berdasarkan KUHPerdata: '{query}'. "
        "Fokus pada hak anak kandung dan aturan harta pencaharian (gono-gini)."
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    return {
        "national_context": response.content,
        "national_usage": _extract_token_usage(response),
    }


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
    return {
        "adat_context": response.content,
        "adat_usage": _extract_token_usage(response),
    }


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
    return {
        "final_synthesis": response.content,
        "supervisor_usage": _extract_token_usage(response),
    }


def build_parallel_orchestrator(graph_data_path: str = "experiments/01_triple_extraction/result.json"):
    llm = _get_llm()

    workflow = StateGraph(AgentState)
    workflow.add_node("start", lambda state: {})
    workflow.add_node("national_law", lambda state: _national_agent(llm, state))
    workflow.add_node("adat_law", lambda state: _adat_agent(llm, graph_data_path, state))
    workflow.add_node("adjudicator", lambda state: _supervisor_agent(llm, state))

    workflow.set_entry_point("start")
    workflow.add_edge("start", "national_law")
    workflow.add_edge("start", "adat_law")
    workflow.add_edge("national_law", "adjudicator")
    workflow.add_edge("adat_law", "adjudicator")
    workflow.add_edge("adjudicator", END)

    return workflow.compile()


def run_parallel_query(query: str, graph_data_path: str = "experiments/01_triple_extraction/result.json"):
    app = build_parallel_orchestrator(graph_data_path=graph_data_path)
    inputs = {"messages": [HumanMessage(content=query)]}
    return app.invoke(inputs)


if __name__ == "__main__":
    q = (
        "Seorang ayah Minangkabau meninggal. "
        "Dia meninggalkan rumah yang dibeli dari hasil kerjanya sendiri. "
        "Siapa yang lebih berhak: anak kandungnya atau kemenakannya?"
    )
    state = run_parallel_query(q)
    print("\n--- FINAL SYNTHESIS ---\n")
    print(state.get("final_synthesis", "N/A"))
