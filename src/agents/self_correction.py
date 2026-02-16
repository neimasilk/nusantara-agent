"""ARCHIVED: Self-correction loop showed no measurable improvement.
Not used in active pipeline. Kept for historical reference."""

import json
import os
from typing import Any, Dict, Optional, Tuple

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

from ..utils.token_usage import extract_token_usage as _extract_token_usage

load_dotenv()


def _get_llm() -> ChatOpenAI:
    from src.utils.llm import get_llm
    return get_llm()


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


def _build_revision_prompt(
    agent_label: str,
    query: str,
    context: str,
    round_num: int,
    previous_answer: Dict,
    critiques_received: Dict,
) -> str:
    return (
        f"Kamu adalah {agent_label}. Lakukan self-correction.\n"
        f"ROUND: {round_num}\n"
        f"QUERY: {query}\n"
        f"CONTEXT: {context}\n\n"
        "JAWABAN SEBELUMNYA:\n"
        f"{json.dumps(previous_answer, ensure_ascii=False)}\n\n"
        "KRITIK YANG DITERIMA:\n"
        f"{json.dumps(critiques_received, ensure_ascii=False)}\n\n"
        "INSTRUKSI:\n"
        "- Perbaiki klaim yang dikritik dengan evidence yang lebih kuat.\n"
        "- Jika kritik valid, ubah klaim / turunkan confidence.\n"
        "- Jika kritik tidak valid, jelaskan alasan singkat di assumptions.\n\n"
        "- HANYA gunakan evidence dari CONTEXT.\n"
        "- Maksimal 6 klaim, ringkas.\n"
        "- Jika evidence tidak ada, pindahkan ke uncertainties.\n"
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


def _summarize_revision(before: Dict, after: Dict) -> Dict:
    before_claims = {c.get("id"): c for c in before.get("claims", []) if isinstance(c, dict)}
    after_claims = {c.get("id"): c for c in after.get("claims", []) if isinstance(c, dict)}

    changed = 0
    for cid, after_claim in after_claims.items():
        before_claim = before_claims.get(cid)
        if not before_claim:
            changed += 1
            continue
        if after_claim.get("statement") != before_claim.get("statement"):
            changed += 1
            continue
        if after_claim.get("evidence") != before_claim.get("evidence"):
            changed += 1
            continue
        if after_claim.get("confidence") != before_claim.get("confidence"):
            changed += 1
            continue

    return {
        "before_claims": len(before_claims),
        "after_claims": len(after_claims),
        "changed_claims": changed,
    }


def revise_answer(
    agent_label: str,
    query: str,
    context: str,
    round_num: int,
    previous_answer: Dict,
    critiques_received: Dict,
    llm: Optional[ChatOpenAI] = None,
) -> Tuple[Dict, Dict, Dict[str, int]]:
    llm = llm or _get_llm()
    prompt = _build_revision_prompt(
        agent_label=agent_label,
        query=query,
        context=context,
        round_num=round_num,
        previous_answer=previous_answer,
        critiques_received=critiques_received,
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    revised = _json_or_raw(response.content)
    revision_summary = _summarize_revision(previous_answer, revised)
    return revised, revision_summary, _extract_token_usage(response)
