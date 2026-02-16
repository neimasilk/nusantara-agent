import json
import os
import re
from typing import Any, Dict, Optional

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

load_dotenv()


ROUTER_LABELS = ("pure_national", "pure_adat", "conflict", "consensus")


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


def _keyword_score(query: str) -> Dict[str, int]:
    q = query.lower()
    national_terms = [
        "kuhperdata",
        "perdata",
        "hukum nasional",
        "yurisprudensi",
        "mahkamah agung",
        "putusan",
        "perjanjian",
        "wanprestasi",
        "gono-gini",
        "harta bersama",
    ]
    adat_terms = [
        "adat",
        "minangkabau",
        "bali",
        "jawa",
        "pusako",
        "mamak",
        "kemenakan",
        "ulayat",
        "banjar",
        "sentana",
        "drue",
        "drue tengah",
    ]
    conflict_terms = [
        "konflik",
        "bertentangan",
        "vs",
        "versus",
        "bertabrakan",
        "pluralisme",
    ]
    national = sum(1 for t in national_terms if t in q)
    adat = sum(1 for t in adat_terms if t in q)
    conflict = sum(1 for t in conflict_terms if t in q)
    return {"national": national, "adat": adat, "conflict": conflict}


def _heuristic_route(query: str) -> Dict:
    scores = _keyword_score(query)
    national = scores["national"]
    adat = scores["adat"]
    conflict = scores["conflict"]

    # Logika klasifikasi lebih ketat
    if adat > 0 and national > 0:
        if conflict > 0 or adat >= 2:
            label = "conflict"
        else:
            label = "consensus"
    elif national > 1 and adat == 0:
        label = "pure_national"
    elif adat > 1 and national == 0:
        label = "pure_adat"
    elif national > adat:
        label = "pure_national"
    elif adat > national:
        label = "pure_adat"
    else:
        label = "consensus"

    return {
        "label": label,
        "scores": scores,
        "confidence": 0.65,
        "method": "heuristic",
    }


def _llm_route(query: str, llm: ChatOpenAI) -> Dict:
    prompt = (
        "Klasifikasikan query hukum ke salah satu label berikut:\n"
        "- pure_national\n"
        "- pure_adat\n"
        "- conflict\n"
        "- consensus\n\n"
        "Definisi singkat:\n"
        "- pure_national: hanya hukum nasional\n"
        "- pure_adat: hanya hukum adat\n"
        "- conflict: ada pertentangan eksplisit antara norma nasional dan adat\n"
        "- consensus: menyebut keduanya tapi tidak konflik eksplisit\n\n"
        f"QUERY: {query}\n\n"
        "Output WAJIB JSON:\n"
        "{\n"
        '  "label": "pure_national | pure_adat | conflict | consensus",\n'
        '  "confidence": 0.0,\n'
        '  "rationale": "ringkas"\n'
        "}\n"
    )
    response = llm.invoke([SystemMessage(content=prompt)])
    data = _json_or_raw(response.content)
    if data.get("label") not in ROUTER_LABELS:
        data["label"] = "consensus"
    data["method"] = "llm"
    return data


def route_query(query: str, use_llm: bool = False, llm: Optional[ChatOpenAI] = None) -> Dict:
    if use_llm:
        if not _HAS_LANGCHAIN_OPENAI:
            fallback = _heuristic_route(query)
            fallback["method"] = "heuristic_fallback"
            return fallback
        return _llm_route(query, llm or _get_llm())
    return _heuristic_route(query)


def classify_router_accuracy(test_cases: Dict[str, str]) -> float:
    """
    test_cases: dict {query: expected_label}
    """
    if not test_cases:
        return 0.0
    correct = 0
    for query, expected in test_cases.items():
        predicted = route_query(query, use_llm=False).get("label")
        if predicted == expected:
            correct += 1
    return correct / len(test_cases)
