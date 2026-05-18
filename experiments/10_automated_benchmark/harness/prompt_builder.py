"""Build minimal prompts for the multi-LLM benchmark.

Token economy: the system prompt is loaded once and reused, so providers
that support caching (DeepSeek, Kimi) get cache hits after call #1.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

PROMPTS = Path(__file__).resolve().parents[1] / "prompts"


@lru_cache(maxsize=4)
def system_prompt(condition: int) -> str:
    if condition == 1:
        path = PROMPTS / "system_prompt_cond1.txt"
    elif condition == 2:
        path = PROMPTS / "system_prompt_cond2.txt"
    elif condition == 3:
        path = PROMPTS / "system_prompt_cond3.txt"
    else:
        raise ValueError(f"unknown condition {condition}; expected 1, 2 or 3")
    return path.read_text(encoding="utf-8").strip()


def user_message(case_query: str) -> str:
    """Single-line user message — no extra framing, no instruction echo."""
    return f"Kasus: {case_query}"


def build_messages(case_query: str, condition: int) -> list[dict]:
    return [
        {"role": "system", "content": system_prompt(condition)},
        {"role": "user", "content": user_message(case_query)},
    ]
