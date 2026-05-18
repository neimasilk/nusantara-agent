"""Provider configuration for multi-LLM benchmark.

All four providers expose an OpenAI-compatible REST API, so we use a single
client class (openai.OpenAI) with different (base_url, api_key, model)
triples.

Token economy: callers should reuse a single client per provider for the
duration of a sweep so connection / auth setup is amortised.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Hint: load .env then .env.txt (user keeps keys in .env.txt).
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_PROJECT_ROOT / ".env")
load_dotenv(_PROJECT_ROOT / ".env.txt", override=False)


@dataclass(frozen=True)
class ProviderSpec:
    name: str
    base_url: str
    api_key_env: str | None
    default_model: str
    supports_caching: bool
    pricing_input_per_m: float    # USD per 1M input tokens
    pricing_output_per_m: float   # USD per 1M output tokens
    pricing_cached_per_m: float | None = None

    def api_key(self) -> str:
        if self.api_key_env is None:
            return "ollama"
        key = os.getenv(self.api_key_env)
        if not key:
            raise RuntimeError(
                f"Missing env var '{self.api_key_env}' for provider "
                f"'{self.name}'. Add it to .env.txt or .env."
            )
        return key


# Public pricing reference (best-effort, updated 2026-05). Always re-verify
# from actual API responses (the runner logs the bill per call).
PROVIDERS: dict[str, ProviderSpec] = {
    "deepseek": ProviderSpec(
        name="deepseek",
        base_url="https://api.deepseek.com",
        api_key_env="DEEPSEEK_API_KEY",
        default_model="deepseek-chat",
        supports_caching=True,
        pricing_input_per_m=0.27,
        pricing_output_per_m=1.10,
        pricing_cached_per_m=0.07,
    ),
    "grok": ProviderSpec(
        name="grok",
        base_url="https://api.x.ai/v1",
        api_key_env="XAI_API_KEY",
        default_model="grok-4.20-0309-non-reasoning",
        supports_caching=False,
        pricing_input_per_m=3.00,
        pricing_output_per_m=15.00,
    ),
    "kimi": ProviderSpec(
        name="kimi",
        base_url="https://api.moonshot.ai/v1",
        api_key_env="KIMI_API_KEY",
        default_model="moonshot-v1-8k",
        supports_caching=True,
        pricing_input_per_m=1.00,
        pricing_output_per_m=1.00,
        pricing_cached_per_m=0.10,
    ),
    "ollama": ProviderSpec(
        name="ollama",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        api_key_env=None,
        default_model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct"),
        supports_caching=False,
        pricing_input_per_m=0.0,
        pricing_output_per_m=0.0,
    ),
}


def estimate_call_cost(spec: ProviderSpec,
                       input_tokens: int,
                       output_tokens: int,
                       cached_input_tokens: int = 0) -> float:
    """Estimate USD cost for one call given token counts."""
    cached_cost = 0.0
    if cached_input_tokens > 0 and spec.pricing_cached_per_m is not None:
        cached_cost = cached_input_tokens * spec.pricing_cached_per_m / 1_000_000
    fresh_input = max(0, input_tokens - cached_input_tokens)
    fresh_cost = fresh_input * spec.pricing_input_per_m / 1_000_000
    out_cost = output_tokens * spec.pricing_output_per_m / 1_000_000
    return cached_cost + fresh_cost + out_cost
