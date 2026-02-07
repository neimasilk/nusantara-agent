from typing import Dict


def extract_token_usage(message) -> Dict[str, int]:
    """Extract token usage from a LangChain LLM response message.

    Supports both ``usage_metadata`` (LangChain >=0.1) and the older
    ``response_metadata.token_usage`` dict.
    """
    usage = getattr(message, "usage_metadata", None) or {}
    response_metadata = getattr(message, "response_metadata", None) or {}
    token_usage = response_metadata.get("token_usage", {}) if isinstance(response_metadata, dict) else {}

    prompt_tokens = usage.get("input_tokens", token_usage.get("prompt_tokens", 0))
    completion_tokens = usage.get("output_tokens", token_usage.get("completion_tokens", 0))
    total_tokens = usage.get("total_tokens", token_usage.get("total_tokens", 0))

    if not total_tokens:
        total_tokens = prompt_tokens + completion_tokens

    return {
        "prompt_tokens": int(prompt_tokens or 0),
        "completion_tokens": int(completion_tokens or 0),
        "total_tokens": int(total_tokens or 0),
    }


def merge_usage(acc: Dict[str, int], usage: Dict[str, int]) -> None:
    """Add token counts from *usage* into accumulator *acc* in-place."""
    acc["prompt_tokens"] += int(usage.get("prompt_tokens", 0))
    acc["completion_tokens"] += int(usage.get("completion_tokens", 0))
    acc["total_tokens"] += int(usage.get("total_tokens", 0))
