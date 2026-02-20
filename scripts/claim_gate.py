"""Claim gate for paper readiness checks.

Run before committing paper changes or milestone reviews.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PAPER_PATH = ROOT / "paper" / "main.tex"
DEFAULT_BIB_PATH = ROOT / "paper" / "references.bib"


@dataclass
class CheckResult:
    status: str  # pass | fail | warn
    message: str
    blocking: bool = False


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_percentages(text: str) -> List[float]:
    values: List[float] = []
    for match in re.finditer(r"(\d+(?:\.\d+)?)\s*\\?%", text):
        before = text[max(0, match.start() - 10) : match.start()].lower()
        after = text[match.end() : match.end() + 10].lower()
        # Ignore confidence-level decorations such as "95% CI".
        if "ci" in before or "ci" in after:
            continue
        values.append(float(match.group(1)))
    return values


def _extract_ratios(text: str) -> List[Tuple[int, int]]:
    pairs: List[Tuple[int, int]] = []
    for match in re.finditer(r"(\d+)\s*/\s*(\d+)", text):
        pairs.append((int(match.group(1)), int(match.group(2))))
    return pairs


def _approx_equal(a: float, b: float, eps: float = 1e-6) -> bool:
    return abs(a - b) <= eps


def check_pending(paper_text: str) -> CheckResult:
    count = paper_text.count("[PENDING]")
    if count == 0:
        return CheckResult("pass", "No [PENDING] found")
    return CheckResult("fail", f"{count} [PENDING] marker(s) found", blocking=True)


def check_todo(paper_text: str) -> CheckResult:
    matches = re.findall(r"(?im)^\s*%+\s*TODO\b.*$", paper_text)
    if not matches:
        return CheckResult("pass", "No TODO comments found")
    return CheckResult("warn", f"{len(matches)} TODO comment(s) found (non-blocking)")


def check_key_numbers(paper_text: str) -> CheckResult:
    metric_specs = [
        ("ASP-only", 58.6, (41, 70)),
        ("ASP+Ollama", 64.3, (45, 70)),
        ("ASP+DeepSeek", 68.6, (48, 70)),
    ]

    errors: List[str] = []
    summary_parts = [f"{label}={pct:.1f}%" for label, pct, _ in metric_specs]

    all_pcts = _extract_percentages(paper_text)
    ratio70_all = [pair for pair in _extract_ratios(paper_text) if pair[1] == 70]

    for label, expected_pct, expected_ratio in metric_specs:
        has_expected_pct = any(_approx_equal(v, expected_pct) for v in all_pcts)
        has_expected_ratio = expected_ratio in ratio70_all
        if not (has_expected_pct or has_expected_ratio):
            errors.append(
                f"{label}: expected {expected_pct:.1f}% or {expected_ratio[0]}/{expected_ratio[1]} not found"
            )

    # Global /70 consistency: only canonical benchmark numerators are allowed.
    allowed_ratio70 = {(41, 70), (45, 70), (48, 70)}
    unexpected_ratio70 = sorted({pair for pair in ratio70_all if pair not in allowed_ratio70})
    if unexpected_ratio70:
        errors.append(f"unexpected benchmark ratio(s) /70 found: {unexpected_ratio70}")

    # Explicit percent-ratio pair consistency, e.g. "64.3% (45/70)".
    expected_pct_by_num70 = {41: 58.6, 45: 64.3, 48: 68.6}
    for match in re.finditer(r"(\d+(?:\.\d+)?)\s*\\?%\s*\((\d+)\s*/\s*70\)", paper_text):
        pct = float(match.group(1))
        num = int(match.group(2))
        expected_pct = expected_pct_by_num70.get(num)
        if expected_pct is None:
            continue
        if not _approx_equal(pct, expected_pct):
            errors.append(
                f"inconsistent percent/ratio pair: found {pct:.1f}% ({num}/70), expected {expected_pct:.1f}%"
            )

    evaluable_values = set()
    for pattern in (
        r"\(\s*(\d+)\s+evaluable\s*,\s*\d+\s+disputed",
        r"evaluable\s+agreed\s+cases\s*&\s*(\d+)",
        r"\bN\s*=\s*(\d+)\s+evaluable\s+cases\b",
        r"\bon\s+the\s+(\d+)\s+evaluable\s+cases\b",
    ):
        for m in re.finditer(pattern, paper_text, flags=re.IGNORECASE):
            evaluable_values.add(int(m.group(1)))
    if not evaluable_values:
        errors.append("total evaluable cases mention not found")
    elif evaluable_values != {70}:
        errors.append(f"evaluable case totals inconsistent: found {sorted(evaluable_values)} expected [70]")

    benchmark_values = set()
    for pattern in (
        r"benchmark\s+of\s+(\d+)",
        r"total\s+cases\s+in\s+benchmark\s*&\s*(\d+)",
    ):
        for m in re.finditer(pattern, paper_text, flags=re.IGNORECASE):
            benchmark_values.add(int(m.group(1)))

    if not benchmark_values:
        errors.append("total benchmark cases mention not found")
    elif benchmark_values != {74}:
        errors.append(
            f"benchmark case totals inconsistent: found {sorted(benchmark_values)} expected [74]"
        )

    if errors:
        return CheckResult("fail", "; ".join(errors), blocking=True)
    return CheckResult(
        "pass",
        "Key numbers consistent (" + ", ".join(summary_parts) + ", evaluable=70, benchmark=74)",
    )


def check_required_stats(paper_text: str) -> CheckResult:
    missing: List[str] = []
    for term in ("McNemar", "Wilson", "Cohen", "Fleiss"):
        if not re.search(rf"\b{re.escape(term)}\b", paper_text, flags=re.IGNORECASE):
            missing.append(term)

    has_specific_p = bool(re.search(r"\bp[^\n]{0,30}=\s*0\.\d+", paper_text, flags=re.IGNORECASE))
    if not has_specific_p:
        missing.append("specific p-value (p = 0.xxx)")

    if missing:
        return CheckResult(
            "fail",
            "Missing required statistical content: " + ", ".join(missing),
            blocking=True,
        )
    return CheckResult("pass", "Required stats present (McNemar, Wilson, Cohen, Fleiss, p-value)")


def _extract_cite_keys(paper_text: str) -> List[str]:
    keys: List[str] = []
    for match in re.finditer(r"\\cite[a-zA-Z]*\{([^}]+)\}", paper_text):
        for key in match.group(1).split(","):
            key = key.strip()
            if key:
                keys.append(key)
    return keys


def _extract_bib_keys(bib_text: str) -> List[str]:
    return re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib_text)


def check_citations(paper_text: str, bib_text: str) -> CheckResult:
    cite_keys = set(_extract_cite_keys(paper_text))
    bib_keys = set(_extract_bib_keys(bib_text))
    missing = sorted(cite_keys - bib_keys)
    if missing:
        preview = ", ".join(missing[:8])
        suffix = "" if len(missing) <= 8 else f" (+{len(missing) - 8} more)"
        return CheckResult("warn", f"{len(missing)} missing citation key(s): {preview}{suffix}")
    return CheckResult("pass", "All citations found in references.bib")


def _print_result(result: CheckResult) -> None:
    unicode_symbol = {"pass": "✅", "fail": "❌", "warn": "⚠️"}.get(result.status, "-")
    ascii_symbol = {"pass": "[PASS]", "fail": "[FAIL]", "warn": "[WARN]"}.get(result.status, "[-]")
    text = f"{unicode_symbol} {result.message}"
    try:
        print(text)
    except UnicodeEncodeError:
        print(f"{ascii_symbol} {result.message}")


def main() -> int:
    paper_path = DEFAULT_PAPER_PATH
    bib_path = DEFAULT_BIB_PATH

    print("[CLAIM GATE] Checking paper/main.tex...")

    if not paper_path.exists():
        print(f"❌ Paper file not found: {paper_path}")
        return 1
    if not bib_path.exists():
        print(f"❌ Bibliography file not found: {bib_path}")
        return 1

    paper_text = _read_text(paper_path)
    bib_text = _read_text(bib_path)

    results = [
        check_pending(paper_text),
        check_todo(paper_text),
        check_key_numbers(paper_text),
        check_required_stats(paper_text),
        check_citations(paper_text, bib_text),
    ]

    for result in results:
        _print_result(result)

    has_blocking_failure = any(r.status == "fail" and r.blocking for r in results)
    if has_blocking_failure:
        print("[CLAIM GATE] FAILED - paper is not ready for review")
        return 1

    print("[CLAIM GATE] PASSED - paper ready for review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
