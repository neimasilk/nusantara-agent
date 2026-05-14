import json
import os
from typing import Annotated, Any, Dict, List, Sequence, TypedDict

from dotenv import load_dotenv
from src.config.domain_keywords import (
    HAM_EXTREME_KEYWORDS,
    NATIONAL_DOMINANT_KEYWORDS,
    OFFLINE_ADAT_KEYWORDS,
    OFFLINE_ADMIN_CASE_KEYWORDS,
    OFFLINE_CONFLICT_KEYWORDS,
    OFFLINE_NATIONAL_KEYWORDS,
    SUPERVISOR_BALI_KEYWORDS,
    SUPERVISOR_HAM_EXTREME_KEYWORDS,
    SUPERVISOR_JAWA_KEYWORDS,
    SUPERVISOR_JAWA_BILATERAL_KEYWORDS,
    SUPERVISOR_MINANG_KEYWORDS,
    SUPERVISOR_MK_MDP_KEYWORDS,
    SUPERVISOR_NATIONAL_HARD_KEYWORDS,
    SUPERVISOR_NATIONAL_KEYWORDS,
)

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


def _contains_any(text: str, keywords: Sequence[str]) -> bool:
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
    has_ham_extreme = _contains_any(q, HAM_EXTREME_KEYWORDS)
    # National law clearly dominant: administrative or clear statutory cases
    has_national_dominant = _contains_any(q, NATIONAL_DOMINANT_KEYWORDS)
    has_national_keywords = _contains_any(q, OFFLINE_NATIONAL_KEYWORDS)
    has_adat_keywords = _contains_any(q, OFFLINE_ADAT_KEYWORDS)
    has_conflict_keywords = _contains_any(q, OFFLINE_CONFLICT_KEYWORDS)
    has_admin_case = _contains_any(q, OFFLINE_ADMIN_CASE_KEYWORDS)

    label = "D"
    langkah = "5"
    alasan = "Insufficient information to determine national/adat dominance."

    if has_ham_extreme:
        label = "A"
        langkah = "1"
        alasan = "Fundamental human rights violation or statutory age limit — deferred to national law."
    elif has_national_dominant and not has_symbolic_conflict:
        label = "A"
        langkah = "2"
        alasan = "Clear national administrative/procedural case with no symbolic conflict."
    elif has_symbolic_conflict:
        label = "C"
        langkah = "4"
        alasan = "Rule engine detected an explicit conflict between legal norms."
    elif route_label == "pure_national":
        label = "A"
        langkah = "2"
        alasan = "Router indicates a purely national domain with no symbolic conflict."
    elif route_label == "pure_adat":
        if has_national_keywords and has_conflict_keywords:
            label = "C"
            langkah = "4"
            alasan = "Strong national keywords detected within an adat context — treated as conflict."
        else:
            label = "B"
            langkah = "3"
            alasan = "Case is adat-dominant with no explicit conflict."
    elif route_label == "conflict":
        if has_admin_case and not has_symbolic_conflict:
            label = "A"
            langkah = "2"
            alasan = "National administrative dispute with no material symbolic conflict."
        else:
            label = "C"
            langkah = "4"
            alasan = "Router flagged a national–adat conflict."
    elif route_label == "consensus":
        if has_national_keywords and not has_adat_keywords:
            label = "A"
            langkah = "2"
            alasan = "National indicators dominant in a consensus query."
        elif has_adat_keywords and not has_national_keywords:
            label = "B"
            langkah = "3"
            alasan = "Adat indicators dominant in a consensus query."
        elif nasional_output and not adat_atoms:
            label = "A"
            langkah = "2"
            alasan = "National symbolic output available with no adat signal."
        elif adat_atoms and not nasional_output:
            label = "B"
            langkah = "3"
            alasan = "Adat symbolic output available with no national signal."
        elif nasional_output and adat_atoms:
            label = "C"
            langkah = "4"
            alasan = "Symbolic output from both legal systems present simultaneously."

    return {
        "label": label,
        "langkah_keputusan": langkah,
        "alasan_utama": alasan,
        "konflik_terdeteksi": "Ya" if label == "C" or has_symbolic_conflict else "Tidak",
    }


class _OfflineOrchestrator:
    """Fallback orchestrator for operation without LLM/LangGraph dependencies."""

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
    from src.utils.llm import get_llm
    return get_llm()


def _should_use_offline_fallback() -> bool:
    force_offline = os.getenv("NUSANTARA_FORCE_OFFLINE", "").strip().lower() in {"1", "true", "yes"}
    if force_offline:
        return True

    from src.utils.llm import has_llm_credentials
    has_creds = has_llm_credentials()
    deps_ready = _HAS_LANGCHAIN_OPENAI and _HAS_LANGCHAIN_CORE and _HAS_LANGGRAPH
    return not (has_creds and deps_ready)


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
        "You are an expert in Indonesian national civil law. "
        f"Analyse this question based on KUHPerdata: '{query}'.\n"
        f"SYMBOLIC ANALYSIS RESULTS (FACTS): {rules}\n"
        "Use these symbolic results as the anchor for your analysis."
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
        "You are an expert in adat law (Minangkabau, Bali, Jawa). "
        f"Analyse this question: '{query}'.\n"
        f"DOCUMENT CONTEXT: {retrieval}\n"
        f"SYMBOLIC ANALYSIS RESULTS (FACTS): {rules}\n"
        "Focus on communal versus individual rights in accordance with the provided data."
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

    # Check for explicit conflict in rule engine output
    has_nasional_conflict = any('conflict' in str(item).lower() for item in nasional_output)
    has_adat_conflict = any(
        any('conflict' in str(item).lower() for item in domain_rules)
        for domain_rules in adat_output.values()
        if isinstance(domain_rules, list)
    )

    # Check domain triggers for contextual signals
    q_lower = query.lower()
    has_minang_keywords = any(k in q_lower for k in SUPERVISOR_MINANG_KEYWORDS)
    has_bali_keywords = any(k in q_lower for k in SUPERVISOR_BALI_KEYWORDS)
    has_jawa_keywords = any(k in q_lower for k in SUPERVISOR_JAWA_KEYWORDS)
    has_jawa_bilateral_keywords = any(k in q_lower for k in SUPERVISOR_JAWA_BILATERAL_KEYWORDS)
    has_national_keywords = any(k in q_lower for k in SUPERVISOR_NATIONAL_KEYWORDS)
    has_national_hard_constraints = any(k in q_lower for k in SUPERVISOR_NATIONAL_HARD_KEYWORDS)
    has_ham_extreme = any(k in q_lower for k in SUPERVISOR_HAM_EXTREME_KEYWORDS)
    has_mk_mdp = any(k in q_lower for k in SUPERVISOR_MK_MDP_KEYWORDS)

    # Logic adjustment for Router Mismatch
    router_warning = ""
    if route_label == "pure_adat" and has_national_keywords:
        router_warning = "WARNING: Router labelled 'Adat', but National Law keywords detected (SHM/UU/Pengadilan). CONSIDER A or C if relevant."
        if "shm" in q_lower and "ulayat" in q_lower:
            router_warning += " (SHM on ulayat land is a strong indicator of CONFLICT/C)."
    elif route_label == "pure_national" and (has_minang_keywords or has_bali_keywords or has_jawa_keywords):
        router_warning = "WARNING: Router labelled 'National', but adat terminology detected. CONSIDER B or C if relevant."
    if has_jawa_bilateral_keywords and not has_national_hard_constraints:
        if router_warning:
            router_warning += " "
        router_warning += (
            "JAWA_GUARD_V1: If strong Jawa bilateral context is present (gono-gini/sigar semangka/wekas) "
            "without hard national constraints, DO NOT select A unless there is an explicit conflict."
        )

    prompt = (
        "You are an Adjudicator Judge specialising in Indonesian legal pluralism.\n\n"
        f"QUESTION: {query}\n\n"
        f"Router Classification: {route_label}\n"
        f"Default Position: {default_position}\n"
        f"System Warning: {router_warning}\n\n"
        "=== SYMBOLIC DATA FROM RULE ENGINE ===\n"
        f"National Output: {nasional_output if nasional_output else '[NO OUTPUT]'}\n"
        f"Adat Output: {adat_output if adat_output else '[NO OUTPUT]'}\n"
        f"Explicit Conflict Detected: Nasional={has_nasional_conflict}, Adat={has_adat_conflict}\n\n"
        "=== DECISION HIERARCHY (apply in order from top) ===\n\n"
        "MAIN INSTRUCTION:\n"
        f"- Begin analysis from the Default Position: {default_position}\n"
        "- Deviate from the default position only when STRONG evidence is found in Symbolic Data or Legal Facts.\n"
        "- When in doubt, return to the Default Position.\n\n"
        "STEP 1: Check FUNDAMENTAL HUMAN RIGHTS\n"
        f"  - Extreme human rights violation detected: {has_ham_extreme}\n"
        "  - If present: IMMEDIATELY SELECT A (National)\n"
        "  - Examples: prohibition on schooling, denial of healthcare, systemic gender discrimination\n\n"
        "STEP 2: Check Pure National Law\n"
        "  - If national law provides a CLEAR AND FINAL rule → A\n"
        "  - Select A if: legislation sets a firm limit or condition that CANNOT be overridden by adat\n"
        "  - Mandatory A examples:\n"
        "    * Minimum marriage age (Marriage Act) → A\n"
        "    * Court order requirement for child adoption → A\n"
        "    * Passport/immigration/civil registry formalities → A\n"
        "    * Polygamy regulated by statute → A\n"
        "  - Escalate to C ONLY if there is an ACTIVE CLAIM by one party under national law AGAINST a claim by another party under adat.\n"
        "  - Adat as narrative background is NOT a reason to select C.\n\n"
        "STEP 3: Check Pure Internal Adat\n"
        f"  - Adat domain detected: Minang={has_minang_keywords}, Bali={has_bali_keywords}, Jawa={has_jawa_keywords}\n"
        f"  - Strong Jawa bilateral signal: {has_jawa_bilateral_keywords}\n"
        f"  - Hard national constraint detected: {has_national_hard_constraints}\n"
        "  - If the case is internal to an adat community WITHOUT statutory/human rights implications → B\n"
        "  - Examples: harta pusako disputes between kaum members, kemenakan status\n\n"
        "JAWA GUARD V1 (Anti B→A)\n"
        "  - If strong Jawa bilateral signals are present (e.g. gono-gini/sigar semangka/wekas) and "
        "hard national constraints are NOT detected, default to B.\n"
        "  - Under these conditions, label A may only be selected when an explicit hard national basis "
        "or an explicit normative conflict validated by symbolic data is present.\n\n"
        "STEP 4: Check National vs Adat Conflict (Label C)\n"
        f"  - MK/MDP ruling detected: {has_mk_mdp}\n"
        "  - Note: MDP (Majelis Desa Pakraman) is a Balinese adat institution that frequently reforms conservative adat practice.\n"
        "  - SELECT C IF A CONFLICT (PERTENTANGAN) IS PRESENT:\n"
        "    a) National rule states X, but adat rule states Y\n"
        "    b) One party claims rights under national law, the other under adat\n"
        "    c) Case involves different ethnic groups or a community versus the State (SHM/Hutan Adat)\n"
        "  - Important principle: The existence of a KUHPerdata article or statute does NOT automatically override adat. If there is a norm dispute, that is C.\n"
        "  - VALID C examples:\n"
        "    * Prohibition on female inheritance in adat vs MK ruling on equality\n"
        "    * Pusako tinggi may not leave the kaum (Ulayat) vs SHM (National)\n"
        "    * Wekas/Oral Adat Testament vs Legitime Portie KUHPerdata\n"
        "  - NOT C examples (do not select C):\n"
        "    * Internal conflict within a single adat system → select B\n"
        "    * Polygamy already regulated by statute → select A\n\n"
        "STEP 5: Default\n"
        "  - If uncertain between C and B → select B (Adat)\n"
        "  - If uncertain between C and A → select A (National)\n"
        "  - If information is insufficient → select D\n\n"
        "=== OUTPUT FORMAT (MUST BE JSON) ===\n"
        "{\n"
        '  "label": "A|B|C|D",\n'
        '  "langkah_keputusan": "1|2|3|4|5",\n'
        '  "alasan_utama": "Explain the selection logic",\n'
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
            "Dependency 'langgraph' is not available. "
            "Install requirements or enable the fallback with NUSANTARA_FORCE_OFFLINE=1."
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
