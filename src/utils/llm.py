"""Shared LLM initialization for all agent modules."""

import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_openai import ChatOpenAI
    _HAS_LANGCHAIN_OPENAI = True
except ImportError:
    ChatOpenAI = Any  # type: ignore[assignment]
    _HAS_LANGCHAIN_OPENAI = False


def get_llm() -> ChatOpenAI:
    """Return a ChatOpenAI instance configured for the DeepSeek API."""
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
