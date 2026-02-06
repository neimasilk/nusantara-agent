import json
import os
from typing import Dict, List, Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

from .self_correction import revise_answer

load_dotenv()


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
    )


def _json_or_raw(text: str) -> Dict:
    text = text.strip()
    if "```json" in text:
        start = text.index("```json") + len("```json")
        end = text.index("```", start)
        text = text[start:end].strip()
    elif "```" in text:
        start = text.index("```") + len("```")
        end = text.index("```", start)
        text = text[start:end].strip()
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
        f"Kamu adalah {agent_label}. Jawab secara terstruktur dan ringkas.\n"
        f"ROUND: {round_num}\n"
        f"QUERY: {query}\n"
        f"CONTEXT: {context}\n"
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
        "Buat minimal 3 kritik spesifik. Output WAJIB JSON dengan skema:\n"
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


def _invoke_json(llm: ChatOpenAI, prompt: str) -> Dict:
    response = llm.invoke([SystemMessage(content=prompt)])
    return _json_or_raw(response.content)


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
        nla_answer = _invoke_json(llm, nla_prompt)
        ala_answer = _invoke_json(llm, ala_prompt)
        logs.append({"type": "answer", "round": round_num, "agent": "NLA", "data": nla_answer})
        logs.append({"type": "answer", "round": round_num, "agent": "ALA", "data": ala_answer})

        # Cross critiques
        nla_on_ala = _invoke_json(
            llm, _build_critique_prompt("National Law Agent (NLA)", "ALA", ala_answer, round_num)
        )
        ala_on_nla = _invoke_json(
            llm, _build_critique_prompt("Adat Law Agent (ALA)", "NLA", nla_answer, round_num)
        )
        logs.append({"type": "critique", "round": round_num, "agent": "NLA", "target": "ALA", "data": nla_on_ala})
        logs.append({"type": "critique", "round": round_num, "agent": "ALA", "target": "NLA", "data": ala_on_nla})

        # Revision step if not last round
        if round_num < max_rounds:
            nla_answer, nla_rev = revise_answer(
                agent_label="National Law Agent (NLA)",
                query=query,
                context=national_context,
                round_num=round_num + 1,
                previous_answer=nla_answer,
                critiques_received=ala_on_nla,
                llm=llm,
            )
            ala_answer, ala_rev = revise_answer(
                agent_label="Adat Law Agent (ALA)",
                query=query,
                context=adat_context,
                round_num=round_num + 1,
                previous_answer=ala_answer,
                critiques_received=nla_on_ala,
                llm=llm,
            )
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
    }


def save_debate_logs(output_dir: str, debate_result: Dict) -> None:
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "debate_summary.json"), "w", encoding="utf-8") as f:
        json.dump(debate_result, f, ensure_ascii=False, indent=2)
