import json
import os
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

try:
    from langchain_openai import ChatOpenAI
    _HAS_LANGCHAIN_OPENAI = True
except ImportError:
    ChatOpenAI = Any  # type: ignore[assignment]
    _HAS_LANGCHAIN_OPENAI = False

try:
    from langchain_core.messages import SystemMessage
except ImportError:
    class SystemMessage:  # type: ignore[no-redef]
        def __init__(self, content: str):
            self.content = content

from .self_correction import revise_answer
from ..utils.token_usage import extract_token_usage as _extract_token_usage, merge_usage as _merge_usage

load_dotenv()


def _get_llm() -> ChatOpenAI:
    if not _HAS_LANGCHAIN_OPENAI:
        raise ImportError(
            "Dependency 'langchain_openai' tidak tersedia. "
            "Mode debate membutuhkan dependency ini."
        )
    return ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
    )


def _json_or_raw(text: str) -> Dict:
    text = text.strip()
    if "```json" in text:
        start = text.index("```json") + len("```json")
        # Cek apakah ada closing fence
        if "```" in text[start:]:
            end = text.index("```", start)
            text = text[start:end].strip()
        else:
            # Unclosed fence, gunakan sisa text setelah opening
            text = text[start:].strip()
    elif "```" in text:
        start = text.index("```") + len("```")
        if "```" in text[start:]:
            end = text.index("```", start)
            text = text[start:end].strip()
        else:
            text = text[start:].strip()
    try:
        return json.loads(text)
    except Exception:
        return {"raw_output": text}


def _build_answer_prompt(
    agent_label: str,
    query: str,
    context: str,
    round_num: int,
) -> str:
    return (
        f"Kamu adalah {agent_label}. Jawab terstruktur, ringkas, dan evidence-grounded.\n"
        f"ROUND: {round_num}\n"
        f"QUERY: {query}\n"
        f"CONTEXT: {context}\n"
        "\n"
        "ATURAN KETAT:\n"
        "- HANYA buat klaim yang bisa didukung evidence dari CONTEXT.\n"
        "- Jika evidence tidak ada, masukkan ke uncertainties.\n"
        "- Maksimal 6 klaim, setiap klaim 1 kalimat singkat.\n"
        "- Jangan menambah informasi baru di luar CONTEXT.\n"
        "- Jawaban ringkas (<= 1200 karakter).\n"
        "\n"
        "OUTPUT WAJIB JSON dengan skema:\n"
        "{\n"
        '  "round": 1,\n'
        '  "agent": "NLA" | "ALA",\n'
        '  "answer": "...",\n'
        '  "claims": [\n'
        "    {\n"
        '      "id": "C1",\n'
        '      "statement": "Klaim utama",\n'
        '      "evidence": ["source_id_1"],\n'
        '      "confidence": 0.0,\n'
        '      "assumptions": ["A1"]\n'
        "    }\n"
        "  ],\n"
        '  "uncertainties": ["U1"],\n'
        '  "open_questions": ["Q1"]\n'
        "}\n"
    )


def _build_critique_prompt(
    agent_label: str,
    target_label: str,
    target_answer: Dict,
    round_num: int,
) -> str:
    return (
        f"Kamu adalah {agent_label}. Kritik jawaban agent {target_label}.\n"
        f"ROUND: {round_num}\n"
        f"TARGET ANSWER: {json.dumps(target_answer, ensure_ascii=False)}\n\n"
        "Buat minimal 3 kritik spesifik.\n"
        "Fokus pada: evidence_gap, logic_gap, overclaim, dan klaim tanpa dasar.\n"
        "Output WAJIB JSON dengan skema:\n"
        "{\n"
        '  "round": 1,\n'
        '  "agent": "NLA" | "ALA",\n'
        '  "target": "NLA" | "ALA",\n'
        '  "critiques": [\n'
        "    {\n"
        '      "id": "K1",\n'
        '      "target_claim_id": "C1",\n'
        '      "issue_type": "evidence_gap" | "logic_gap" | "conflict" | "domain_mismatch" | "overclaim",\n'
        '      "description": "Kritik spesifik",\n'
        '      "severity": "CRITICAL" | "MAJOR" | "MINOR",\n'
        '      "suggested_fix": "Perbaikan konkret"\n'
        "    }\n"
        "  ]\n"
        "}\n"
    )


def _invoke_json(llm: ChatOpenAI, prompt: str) -> Tuple[Dict, Dict[str, int]]:
    response = llm.invoke([SystemMessage(content=prompt)])
    return _json_or_raw(response.content), _extract_token_usage(response)


def run_debate(
    query: str,
    national_context: str,
    adat_context: str,
    max_rounds: int = 2,
    llm: Optional[ChatOpenAI] = None,
) -> Dict:
    if max_rounds < 2:
        max_rounds = 2

    llm = llm or _get_llm()

    logs: List[Dict] = []
    nla_answer: Optional[Dict] = None
    ala_answer: Optional[Dict] = None
    usage_totals: Dict[str, int] = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    llm_call_count = 0

    for round_num in range(1, max_rounds + 1):
        # Initial / revised answers
        nla_prompt = _build_answer_prompt(
            "National Law Agent (NLA)",
            query,
            national_context,
            round_num,
        )
        ala_prompt = _build_answer_prompt(
            "Adat Law Agent (ALA)",
            query,
            adat_context,
            round_num,
        )
        nla_answer, nla_usage = _invoke_json(llm, nla_prompt)
        _merge_usage(usage_totals, nla_usage)
        llm_call_count += 1

        ala_answer, ala_usage = _invoke_json(llm, ala_prompt)
        _merge_usage(usage_totals, ala_usage)
        llm_call_count += 1

        logs.append({"type": "answer", "round": round_num, "agent": "NLA", "data": nla_answer})
        logs.append({"type": "answer", "round": round_num, "agent": "ALA", "data": ala_answer})

        # Cross critiques
        nla_on_ala, nla_crit_usage = _invoke_json(
            llm, _build_critique_prompt("National Law Agent (NLA)", "ALA", ala_answer, round_num)
        )
        _merge_usage(usage_totals, nla_crit_usage)
        llm_call_count += 1

        ala_on_nla, ala_crit_usage = _invoke_json(
            llm, _build_critique_prompt("Adat Law Agent (ALA)", "NLA", nla_answer, round_num)
        )
        _merge_usage(usage_totals, ala_crit_usage)
        llm_call_count += 1

        logs.append({"type": "critique", "round": round_num, "agent": "NLA", "target": "ALA", "data": nla_on_ala})
        logs.append({"type": "critique", "round": round_num, "agent": "ALA", "target": "NLA", "data": ala_on_nla})

        # Revision step if not last round
        if round_num < max_rounds:
            nla_answer, nla_rev, nla_rev_usage = revise_answer(
                agent_label="National Law Agent (NLA)",
                query=query,
                context=national_context,
                round_num=round_num + 1,
                previous_answer=nla_answer,
                critiques_received=ala_on_nla,
                llm=llm,
            )
            _merge_usage(usage_totals, nla_rev_usage)
            llm_call_count += 1

            ala_answer, ala_rev, ala_rev_usage = revise_answer(
                agent_label="Adat Law Agent (ALA)",
                query=query,
                context=adat_context,
                round_num=round_num + 1,
                previous_answer=ala_answer,
                critiques_received=nla_on_ala,
                llm=llm,
            )
            _merge_usage(usage_totals, ala_rev_usage)
            llm_call_count += 1

            logs.append(
                {"type": "revision", "round": round_num + 1, "agent": "NLA", "data": nla_answer, "meta": nla_rev}
            )
            logs.append(
                {"type": "revision", "round": round_num + 1, "agent": "ALA", "data": ala_answer, "meta": ala_rev}
            )

    return {
        "query": query,
        "max_rounds": max_rounds,
        "final_nla": nla_answer,
        "final_ala": ala_answer,
        "logs": logs,
        "token_usage": usage_totals,
        "llm_call_count": llm_call_count,
    }


def save_debate_logs(output_dir: str, debate_result: Dict) -> None:
    os.makedirs(output_dir, exist_ok=True)
    logs_index: List[Dict] = []
    severity_counts = {"CRITICAL": 0, "MAJOR": 0, "MINOR": 0}
    needs_human_review = False

    for entry in debate_result.get("logs", []):
        entry_type = entry.get("type")
        round_num = entry.get("round")
        agent = (entry.get("agent") or "").lower()
        target = (entry.get("target") or "").lower()

        filename = None
        if entry_type == "answer":
            if agent:
                filename = f"debate_round{round_num}_{agent}.json"
        elif entry_type == "revision":
            if agent:
                filename = f"revision_round{round_num}_{agent}.json"
        elif entry_type == "critique":
            if agent and target:
                filename = f"critique_round{round_num}_{agent}_on_{target}.json"
                critiques = entry.get("data", {}).get("critiques", [])
                for critique in critiques:
                    severity = critique.get("severity")
                    if severity in severity_counts:
                        severity_counts[severity] += 1
                        if severity == "CRITICAL":
                            needs_human_review = True

        if filename:
            path = os.path.join(output_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(entry.get("data"), f, ensure_ascii=False, indent=2)
            logs_index.append(
                {
                    "type": entry_type,
                    "round": round_num,
                    "agent": entry.get("agent"),
                    "target": entry.get("target"),
                    "file": filename,
                }
            )

    summary = {
        "query": debate_result.get("query"),
        "max_rounds": debate_result.get("max_rounds"),
        "final_nla": debate_result.get("final_nla"),
        "final_ala": debate_result.get("final_ala"),
        "token_usage": debate_result.get("token_usage", {}),
        "llm_call_count": debate_result.get("llm_call_count", 0),
        "critique_counts": severity_counts,
        "needs_human_review": needs_human_review,
        "logs_index": logs_index,
    }
    with open(os.path.join(output_dir, "debate_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
