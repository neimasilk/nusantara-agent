"""Robust parser for the LLM JSON output: {"label": "...", "alasan": "..."}.

We expect a single-line JSON object, but real LLMs sometimes pad with
prose, markdown fences, or trailing notes. The parser strips known noise
and falls back to a regex sweep for "label" before giving up.
"""
from __future__ import annotations

import json
import re

VALID_LABELS = {"A", "B", "C", "D"}

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)
_LABEL_RE = re.compile(r'"label"\s*:\s*"([ABCD])"', re.IGNORECASE)
_LOOSE_LABEL_RE = re.compile(r"\b([ABCD])\b")


def parse(raw: str) -> dict:
    """Return {'label': X, 'alasan': str, 'parse_status': str}.

    parse_status is one of:
      - "json_ok"     : clean JSON parse
      - "regex_label" : fell back to regex extraction of label
      - "failed"      : could not extract a valid label
    """
    if not raw:
        return {"label": None, "alasan": "", "parse_status": "failed"}

    text = _FENCE_RE.sub("", raw).strip()

    # First, try strict JSON.
    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and "label" in obj:
            label = str(obj["label"]).strip().upper()
            if label in VALID_LABELS:
                return {
                    "label": label,
                    "alasan": str(obj.get("alasan", "")).strip(),
                    "parse_status": "json_ok",
                }
    except json.JSONDecodeError:
        pass

    # Fallback: grab "label": "X" via regex
    m = _LABEL_RE.search(text)
    if m:
        label = m.group(1).upper()
        if label in VALID_LABELS:
            # Try to also grab alasan if present.
            alasan_m = re.search(r'"alasan"\s*:\s*"([^"]*)"', text)
            alasan = alasan_m.group(1) if alasan_m else ""
            return {"label": label, "alasan": alasan,
                    "parse_status": "regex_label"}

    # Last resort: a single letter A/B/C/D anywhere
    m = _LOOSE_LABEL_RE.search(text)
    if m:
        return {"label": m.group(1).upper(), "alasan": "",
                "parse_status": "regex_label"}

    return {"label": None, "alasan": "", "parse_status": "failed"}
