import os
from typing import Annotated, TypedDict, List, Dict
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from ..utils.token_usage import extract_token_usage as _extract_token_usage

load_dotenv()


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
    )


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    national_context: str
    adat_context: str
    rule_results: Dict
    retrieval_context: str
    final_synthesis: str
    usage: Dict[str, int]


def _national_agent(llm: ChatOpenAI, state: AgentState):
    query = state["messages"][0].content
    rules = state.get("rule_results", {}).get("nasional", [])
    prompt = (
        "Kamu adalah pakar hukum perdata nasional Indonesia. "
        f"Analisis pertanyaan ini berdasarkan KUHPerdata: '{query}'.\n"
        f"HASIL ANALISIS SIMBOLIK (FACTS): {rules}\n"
        "Gunakan hasil simbolik tersebut sebagai jangkar analisismu."
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    return {
        "national_context": response.content,
    }


def _adat_agent(llm: ChatOpenAI, state: AgentState):
    query = state["messages"][0].content
    rules = state.get("rule_results", {}).get("adat", {})
    retrieval = state.get("retrieval_context", "")
    prompt = (
        "Kamu adalah pakar hukum adat (Minangkabau, Bali, Jawa). "
        f"Analisis pertanyaan ini: '{query}'.\n"
        f"KONTEKS DOKUMEN: {retrieval}\n"
        f"HASIL ANALISIS SIMBOLIK (FACTS): {rules}\n"
        "Fokus pada hak komunal vs individu sesuai data tersebut."
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    return {
        "adat_context": response.content,
    }


def _supervisor_agent(llm: ChatOpenAI, state: AgentState, route_label: str = None):
    default_position = {
        "pure_national": "A (Nasional)",
        "pure_adat": "B (Adat)",
        "conflict": "C (Konflik)",
        "consensus": "A/B (Konsensus)"
    }.get(route_label, "Tidak ditentukan")

    national = state.get("national_context", "")
    adat = state.get("adat_context", "")
    rules = state.get("rule_results", {})
    query = state["messages"][0].content
    
    nasional_output = rules.get('nasional', [])
    adat_output = rules.get('adat', {})
    
    # Cek explicit conflict dari output rule engine
    has_nasional_conflict = any('conflict' in str(item).lower() for item in nasional_output)
    has_adat_conflict = any(
        any('conflict' in str(item).lower() for item in domain_rules)
        for domain_rules in adat_output.values()
        if isinstance(domain_rules, list)
    )
    
    # Cek domain triggers untuk konteks
    q_lower = query.lower()
    has_minang_keywords = any(k in q_lower for k in ['minang', 'pusako', 'kemenakan', 'mamak', 'kaum'])
    has_bali_keywords = any(k in q_lower for k in ['bali', 'purusa', 'sanggah', 'druwe', 'sentana'])
    has_jawa_keywords = any(k in q_lower for k in ['jawa', 'gono-gini', 'ragil', 'wekas', 'sigar'])
    has_national_keywords = any(k in q_lower for k in ['ham', 'uu ', 'undang', 'mahkamah konstitusi', 'mdp', 'putusan', 'sertifikat', 'shm', 'poligami', 'cerai', 'perceraian', 'kua', 'pengadilan'])
    has_ham_extreme = any(k in q_lower for k in ['dilarang bersekolah', 'tidak boleh sekolah', 'larangan sekolah', 'kesehatan', 'puskesmas'])
    has_mk_mdp = any(k in q_lower for k in ['mdp', 'mahkamah konstitusi', 'putusan mk'])
    
    # Logic adjustment for Router Mismatch
    router_warning = ""
    if route_label == "pure_adat" and has_national_keywords:
        router_warning = "WARNING: Router melabeli 'Adat', tapi terdeteksi kata kunci Hukum Nasional (SHM/UU/Pengadilan). PERTIMBANGKAN A atau C jika relevan."
        if "shm" in q_lower and "ulayat" in q_lower:
            router_warning += " (SHM di atas tanah ulayat adalah indikator kuat KONFLIK/C)."
    elif route_label == "pure_national" and (has_minang_keywords or has_bali_keywords or has_jawa_keywords):
        router_warning = "WARNING: Router melabeli 'Nasional', tapi terdeteksi istilah Adat. PERTIMBANGKAN B atau C jika relevan."

    prompt = (
        "Kamu adalah Hakim Adjudikator yang ahli dalam pluralisme hukum Indonesia.\n\n"
        f"PERTANYAAN: {query}\n\n"
        f"Router Classification: {route_label}\n"
        f"Default Position: {default_position}\n"
        f"System Warning: {router_warning}\n\n"
        "=== DATA SIMBOLIK DARI RULE ENGINE ===\n"
        f"Output Nasional: {nasional_output if nasional_output else '[TIDAK ADA OUTPUT]'}\n"
        f"Output Adat: {adat_output if adat_output else '[TIDAK ADA OUTPUT]'}\n"
        f"Explicit Conflict Detected: Nasional={has_nasional_conflict}, Adat={has_adat_conflict}\n\n"
        "=== HIERARKI KEPUTUSAN (Urutkan dari atas) ===\n\n"
        "INSTRUKSI UTAMA:\n"
        f"- Mulai analisis dengan Default Position: {default_position}\n"
        "- Hanya menyimpang dari default position jika ditemukan bukti KUAT di Data Simbolik atau Fakta Hukum.\n"
        "- Jika ragu, kembali ke Default Position.\n\n"
        "LANGKAH 1: Cek HAM FUNDAMENTAL\n"
        f"  - Pelanggaran HAM ekstrem terdeteksi: {has_ham_extreme}\n"
        "  - Jika ada: LANGSUNG PILIH A (Nasional)\n"
        "  - Contoh: Larangan sekolah, larangan kesehatan, diskriminasi gender sistemik\n\n"
        "LANGKAH 2: Cek Pure National Law\n"
        "  - Jika kasus bisa diselesaikan dengan UU yang jelas → A\n"
        "  - Contoh: Poligami, wasiat, perkawinan di bawah umur, formalitas admin\n\n"
        "LANGKAH 3: Cek Pure Internal Adat\n"
        f"  - Domain adat terdeteksi: Minang={has_minang_keywords}, Bali={has_bali_keywords}, Jawa={has_jawa_keywords}\n"
        "  - Jika kasus internal komunitas adat TANPA implikasi UU/HAM → B\n"
        "  - Contoh: Sengketa harta pusako antar-kaum, status kemenakan\n\n"
        "LANGKAH 4: Cek Konflik Nasional vs Adat (Label C)\n"
        f"  - Putusan MK/MDP terdeteksi: {has_mk_mdp}\n"
        "  - Catatan: MDP (Majelis Desa Pakraman) adalah lembaga adat Bali yang sering mereformasi adat konservatif.\n"
        "  - PILIH C HANYA JIKA:\n"
        "    a) Ada konflik NYATA antara aturan adat dan hukum nasional (atau putusan reformis), DAN\n"
        "    b) Konflik tersebut MATERIIL (mempengaruhi hasil akhir), DAN\n"
        "    c) Tidak bisa diselesaikan dengan A atau B saja\n"
        "  - Contoh C yang VALID:\n"
        "    * Larangan waris perempuan dalam adat vs Putusan MK tentang kesetaraan\n"
        "    * Pusako tinggi tidak boleh keluar kaum (Ulayat) vs SHM (Nasional)\n"
        "    * Aturan adat kuno vs Keputusan MDP modern\n"
        "  - Contoh BUKAN C (jangan pilih C):\n"
        "    * Konflik internal dalam satu sistem adat → pilih B\n"
        "    * Poligami yang sudah diatur UU → pilih A\n\n"
        "LANGKAH 5: Default\n"
        "  - Jika ragu antara C dan B → pilih B (Adat)\n"
        "  - Jika ragu antara C dan A → pilih A (Nasional)\n"
        "  - Jika informasi tidak cukup → pilih D\n\n"
        "=== OUTPUT FORMAT (WAJIB JSON) ===\n"
        "{\n"
        '  "label": "A|B|C|D",\n'
        '  "langkah_keputusan": "1|2|3|4|5",\n'
        '  "alasan_utama": "Jelaskan logika pemilihan",\n'
        '  "konflik_terdeteksi": "Ya/Tidak"\n'
        "}\n"
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    return {
        "final_synthesis": response.content,
    }


def build_parallel_orchestrator(graph_data_path: str = "experiments/01_triple_extraction/result.json", route_label: str = None):
    llm = _get_llm()

    workflow = StateGraph(AgentState)
    workflow.add_node("start", lambda state: {})
    workflow.add_node("national_law", lambda state: _national_agent(llm, state))
    workflow.add_node("adat_law", lambda state: _adat_agent(llm, state))
    workflow.add_node("adjudicator", lambda state: _supervisor_agent(llm, state, route_label))

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
