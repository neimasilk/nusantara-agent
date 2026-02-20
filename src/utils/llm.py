"""Shared LLM initialization for all agent modules.

Supports multiple backends via NUSANTARA_LLM_BACKEND env var:
  - "ollama"   : Local Ollama (OpenAI-compatible at localhost:11434/v1)
  - "deepseek" : DeepSeek API (default)
  - "kimi"     : Moonshot/Kimi API
"""

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

try:
    import httpx
    _HAS_HTTPX = True
except ImportError:
    httpx = Any  # type: ignore[assignment]
    _HAS_HTTPX = False

# Backend configuration table
_BACKEND_CONFIGS = {
    "deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url_default": "https://api.deepseek.com",
        "model_default": "deepseek-chat",
        "timeout_default": 120,
    },
    "ollama": {
        "api_key_env": None,  # Ollama tidak butuh API key
        "base_url_default": "http://localhost:11434/v1",
        "model_default": "qwen2.5:7b-instruct",
        "timeout_default": 300,  # Local inference bisa lambat
    },
    "kimi": {
        "api_key_env": "KIMI_API_KEY",
        "base_url_default": "https://api.moonshot.cn/v1",
        "model_default": "moonshot-v1-8k",
        "timeout_default": 120,
    },
}


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_active_backend() -> str:
    """Return the active LLM backend name."""
    backend = os.getenv("NUSANTARA_LLM_BACKEND", "deepseek").strip().lower()
    if backend not in _BACKEND_CONFIGS:
        raise ValueError(
            f"Backend '{backend}' tidak dikenal. "
            f"Pilihan: {', '.join(_BACKEND_CONFIGS.keys())}"
        )
    return backend


def has_llm_credentials() -> bool:
    """Check if the active backend has required credentials."""
    backend = get_active_backend()
    cfg = _BACKEND_CONFIGS[backend]
    if cfg["api_key_env"] is None:
        return True  # Ollama tidak butuh API key
    return bool(os.getenv(cfg["api_key_env"]))


def get_llm() -> ChatOpenAI:
    """Return a ChatOpenAI instance configured for the active backend."""
    if not _HAS_LANGCHAIN_OPENAI:
        raise ImportError(
            "Dependency 'langchain_openai' tidak tersedia. "
            "Install requirements atau gunakan mode offline fallback."
        )

    backend = get_active_backend()
    cfg = _BACKEND_CONFIGS[backend]

    # Resolve API key
    if cfg["api_key_env"] is None:
        api_key = "ollama"  # ChatOpenAI requires non-empty string
    else:
        api_key = os.getenv(cfg["api_key_env"])

    # Allow env overrides for base_url and model
    base_url = os.getenv("NUSANTARA_LLM_BASE_URL", cfg["base_url_default"])
    model = os.getenv("NUSANTARA_LLM_MODEL", cfg["model_default"])

    temperature = float(os.getenv("NUSANTARA_LLM_TEMPERATURE", "0"))

    llm_kwargs = {
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
        "temperature": temperature,
    }

    # Default: ignore system/user proxy env vars to avoid local dead-proxy issues.
    # Override with NUSANTARA_LLM_TRUST_ENV_PROXY=1 when a real proxy is required.
    trust_env_proxy = _env_bool("NUSANTARA_LLM_TRUST_ENV_PROXY", False)

    if _HAS_HTTPX:
        timeout_seconds = float(os.getenv("NUSANTARA_LLM_TIMEOUT_SEC",
                                          str(cfg["timeout_default"])))
        llm_kwargs["http_client"] = httpx.Client(
            trust_env=trust_env_proxy,
            timeout=timeout_seconds,
        )
        llm_kwargs["http_async_client"] = httpx.AsyncClient(
            trust_env=trust_env_proxy,
            timeout=timeout_seconds,
        )

    return ChatOpenAI(**llm_kwargs)
