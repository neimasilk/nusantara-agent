import json
import os
from typing import Annotated, Any, Dict, List, TypedDict

from dotenv import load_dotenv

try:
    from langchain_openai import ChatOpenAI
    _HAS_LANGCHAIN_OPENAI = True
except ImportError:
    ChatOpenAI = Any  # type: ignore[assignment]
    _HAS_LANGCHAIN_OPENAI = False

try:
    from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
    _HAS_LANGCHAIN_CORE = True
except ImportError:
    _HAS_LANGCHAIN_CORE = False

    class _FallbackMessage:
        def __init__(self, content: str):
            self.content = content

    BaseMessage = _FallbackMessage  # type: ignore[assignment]
    HumanMessage = _FallbackMessage  # type: ignore[assignment]
    SystemMessage = _FallbackMessage  # type: ignore[assignment]

try:
    from langgraph.graph import END, StateGraph
    _HAS_LANGGRAPH = True
except ImportError:
    END = "__END__"
    StateGraph = None  # type: ignore[assignment]
    _HAS_LANGGRAPH = False

load_dotenv()


def _contains_any(text: str, keywords: List[str]) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in keywords)


def _extract_query_from_state(state: Dict[str, Any]) -> str:
    messages = state.get("messages", [])
    if not messages:
        return ""
    first = messages[0]
    if hasattr(first, "content"):
        return str(first.content)
    if isinstance(first, dict):
        return str(first.get("content", ""))
    return str(first)


def _flatten_adat_atoms(adat_output: Dict[str, Any]) -> List[str]:
    atoms: List[str] = []
    if not isinstance(adat_output, dict):
        return atoms
    for domain_atoms in adat_output.values():
        if isinstance(domain_atoms, list):
            atoms.extend(str(atom) for atom in domain_atoms)
    return atoms


def _offline_supervisor_decision(query: str, rules: Dict[str, Any], route_label: str) -> Dict[str, str]:
    q = query.lower()
    nasional_output = [str(atom) for atom in rules.get("nasional", [])]
    adat_output = rules.get("adat", {})
    adat_atoms = _flatten_adat_atoms(adat_output)
    all_atoms = nasional_output + adat_atoms

    has_symbolic_conflict = any("conflict" in atom.lower() for atom in all_atoms)
    has_ham_extreme = _contains_any(
        q,
        [
            "dilarang bersekolah",
            "tidak boleh sekolah",
            "larangan sekolah",
            "kesehatan",
            "puskesmas",
        ],
    )
    has_national_keywords = _contains_any(
        q,
        [
            "kuhperdata",
            "uu ",
            "undang",
            "pengadilan",
            "putusan",
            "shm",
            "poligami",
            "cerai",
            "paspor",
            "administrasi",
            "akta",
        ],
    )
    has_adat_keywords = _contains_any(
        q,
        [
            "adat",
            "minang",
            "pusako",
            "kemenakan",
            "mamak",
            "ulayat",
            "bali",
            "mdp",
            "jawa",
            "wekas",
            "ragil",
            "nyentana",
        ],
    )
    has_conflict_keywords = _contains_any(
        q,
        [
            "konflik",
            "vs",
            "versus",
            "bertentangan",
            "sengketa",
            "ulayat",
            "shm",
            "wekas",
            "nyentana",
            "legitime",
            "mdp",
        ],
    )
    has_admin_case = _contains_any(
        q,
        [
            "paspor",
            "akta",
            "catatan sipil",
            "administrasi",
            "dokumen",
        ],
    )

    label = "D"
    langkah = "5"
    alasan = "Informasi tidak cukup untuk menentukan dominansi nasional/adat."

    if has_ham_extreme:
        label = "A"
        langkah = "1"
        alasan = "Pelanggaran HAM fundamental diprioritaskan ke hukum nasional."
    elif has_symbolic_conflict:
        label = "C"
        langkah = "4"
        alasan = "Rule engine mendeteksi konflik eksplisit antar norma."
    elif route_label == "pure_national":
        label = "A"
        langkah = "2"
        alasan = "Router mengindikasikan domain nasional murni tanpa konflik simbolik."
    elif route_label == "pure_adat":
        if has_national_keywords and has_conflict_keywords:
            label = "C"
            langkah = "4"
            alasan = "Ada kata kunci nasional kuat dalam konteks adat, diperlakukan sebagai konflik."
        else:
            label = "B"
            langkah = "3"
            alasan = "Kasus dominan adat dan tidak ada konflik eksplisit."
    elif route_label == "conflict":
        if has_admin_case and not has_symbolic_conflict:
            label = "A"
            langkah = "2"
            alasan = "Sengketa administratif nasional tanpa konflik simbolik yang material."
        else:
            label = "C"
            langkah = "4"
            alasan = "Router menandai konflik nasional-adat."
    elif route_label == "consensus":
        if has_national_keywords and not has_adat_keywords:
            label = "A"
            langkah = "2"
            alasan = "Indikator nasional dominan pada query konsensus."
        elif has_adat_keywords and not has_national_keywords:
            label = "B"
            langkah = "3"
            alasan = "Indikator adat dominan pada query konsensus."
        elif nasional_output and not adat_atoms:
            label = "A"
            langkah = "2"
            alasan = "Output simbolik nasional tersedia tanpa sinyal adat."
        elif adat_atoms and not nasional_output:
            label = "B"
            langkah = "3"
            alasan = "Output simbolik adat tersedia tanpa sinyal nasional."
        elif nasional_output and adat_atoms:
            label = "C"
            langkah = "4"
            alasan = "Output simbolik dua sistem muncul bersamaan."

    return {
        "label": label,
        "langkah_keputusan": langkah,
        "alasan_utama": alasan,
        "konflik_terdeteksi": "Ya" if label == "C" or has_symbolic_conflict else "Tidak",
    }


class _OfflineOrchestrator:
    """Fallback orchestrator untuk mode tanpa dependency LLM/LangGraph."""

    def __init__(self, route_label: str = None):
        self.route_label = route_label or "consensus"

    def invoke(self, state: Dict[str, Any]) -> Dict[str, str]:
        query = _extract_query_from_state(state)
        rules = state.get("rule_results", {}) if isinstance(state, dict) else {}
        synthesis = _offline_supervisor_decision(query, rules, self.route_label)
        return {
            "national_context": "OFFLINE_FALLBACK_NATIONAL",
            "adat_context": "OFFLINE_FALLBACK_ADAT",
            "final_synthesis": json.dumps(synthesis, ensure_ascii=False),
        }


def _get_llm() -> ChatOpenAI:
    if not _HAS_LANGCHAIN_OPENAI:
        raise ImportError(
            "Dependency 'langchain_openai' tidak tersedia. "
            "Install requirements atau gunakan mode offline fallback."
        )
    return ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
    )


def _should_use_offline_fallback() -> bool:
    force_offline = os.getenv("NUSANTARA_FORCE_OFFLINE", "").strip().lower() in {"1", "true", "yes"}
    if force_offline:
        return True

    has_api_key = bool(os.getenv("DEEPSEEK_API_KEY"))
    deps_ready = _HAS_LANGCHAIN_OPENAI and _HAS_LANGCHAIN_CORE and _HAS_LANGGRAPH
    return not (has_api_key and deps_ready)


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
        "  - Jika kasus bisa diselesaikan dengan UU yang jelas DAN tidak ada sanggahan Adat yang kuat → A\n"
        "  - Contoh: Poligami, wasiat, perkawinan di bawah umur, formalitas admin\n"
        "  - PERINGATAN: Jika UU bertentangan dengan praktik adat yang masih hidup (Living Law), JANGAN langsung pilih A. Pertimbangkan C.\n\n"
        "LANGKAH 3: Cek Pure Internal Adat\n"
        f"  - Domain adat terdeteksi: Minang={has_minang_keywords}, Bali={has_bali_keywords}, Jawa={has_jawa_keywords}\n"
        "  - Jika kasus internal komunitas adat TANPA implikasi UU/HAM → B\n"
        "  - Contoh: Sengketa harta pusako antar-kaum, status kemenakan\n\n"
        "LANGKAH 4: Cek Konflik Nasional vs Adat (Label C)\n"
        f"  - Putusan MK/MDP terdeteksi: {has_mk_mdp}\n"
        "  - Catatan: MDP (Majelis Desa Pakraman) adalah lembaga adat Bali yang sering mereformasi adat konservatif.\n"
        "  - PILIH C JIKA TERJADI PERTENTANGAN (CONFLICT):\n"
        "    a) Aturan Nasional mengatakan X, tapi Aturan Adat mengatakan Y\n"
        "    b) Salah satu pihak menuntut hak berdasarkan Nasional, pihak lain berdasarkan Adat\n"
        "    c) Kasus melibatkan Suku yang berbeda atau Suku vs Negara (SHM/Hutan Adat)\n"
        "  - Prinsip Penting: Keberadaan pasal KUHPerdata/UU TIDAK otomatis mengalahkan Adat. Jika ada sengketa norma, itu adalah C.\n"
        "  - Contoh C yang VALID:\n"
        "    * Larangan waris perempuan dalam adat vs Putusan MK tentang kesetaraan\n"
        "    * Pusako tinggi tidak boleh keluar kaum (Ulayat) vs SHM (Nasional)\n"
        "    * Wekas/Wasiat Lisan Adat vs Legitime Portie KUHPerdata\n"
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
    if _should_use_offline_fallback():
        return _OfflineOrchestrator(route_label=route_label)

    if not _HAS_LANGGRAPH:
        raise ImportError(
            "Dependency 'langgraph' tidak tersedia. "
            "Install requirements atau aktifkan fallback dengan NUSANTARA_FORCE_OFFLINE=1."
        )

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
