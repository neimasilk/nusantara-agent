"""Scan the full indo-law dataset (22,630 XML files) for adat-related cases.

Indo-law is dominated by criminal cases (pidana umum), but some may have
adat-related context (e.g. inheritance disputes that escalated to fraud,
land conflicts that became criminal). This scan tells us how many criminal
cases mention adat, which helps us understand whether indo-law has any
residual value as a complement to civil-perdata sources.

Run after indo-law.zip has been extracted to indo-law-main/dataset/.
"""
from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "indo-law-main" / "dataset"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True, parents=True)

REPORT = RESULTS / "indo_law_scan_report.md"
HITS_JSON = RESULTS / "indo_law_adat_hits.json"

# Strict patterns — same as filter_adat_strict.py.
STRICT_PATTERNS = [
    r"\bhukum\s+adat\b",
    r"\btata\s+cara\s+adat\b",
    r"\bmasyarakat\s+adat\b",
    r"\bmasyarakat\s+hukum\s+adat\b",
    r"\badat\s+istiadat\b",
    r"\bsesuai\s+adat\b",
    r"\bmenurut\s+adat\b",
    r"\bberdasarkan\s+adat\b",
    r"\bwaris\s+adat\b",
    r"\bpewarisan\s+adat\b",
    r"\bharta\s+pusaka\b",
    r"\bharato\s+pusako\b",
    r"\bpusako\s+tinggi\b",
    r"\bpusako\s+rendah\b",
    r"\btanah\s+ulayat\b",
    r"\bhak\s+ulayat\b",
    r"\btanah\s+adat\b",
    r"\btanah\s+pusaka\b",
    r"\bperkawinan\s+adat\b",
    r"\bperceraian\s+adat\b",
    r"\bsigar\s+semangka\b",
    r"\bminangkabau\b",
    r"\bniniak\s+mamak\b",
    r"\bdesa\s+adat\b",
    r"\bdesa\s+pakraman\b",
    r"\bsentana\s+rajeg\b",
    r"\bdalihan\s+na\s+tolu\b",
]

COMPILED = [re.compile(p, re.IGNORECASE) for p in STRICT_PATTERNS]


def scan_file(path: Path) -> dict | None:
    """Return hit info or None."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None

    matches: list[tuple[str, str]] = []
    for pattern in COMPILED:
        m = pattern.search(text)
        if m:
            start = max(0, m.start() - 80)
            end = min(len(text), m.end() + 80)
            matches.append((pattern.pattern, text[start:end].strip()))

    if not matches:
        return None

    # Try to extract metadata from <putusan> root attributes via regex
    # (avoid full XML parse overhead when possible).
    klas = re.search(r'klasifikasi="([^"]+)"', text)
    sub = re.search(r'sub_klasifikasi="([^"]*)"', text)
    prov = re.search(r'provinsi="([^"]*)"', text)
    lembaga = re.search(r'lembaga_peradilan="([^"]*)"', text)
    putusan_id = re.search(r'id="([^"]*)"', text)

    return {
        "file": path.name,
        "id": putusan_id.group(1) if putusan_id else "",
        "klasifikasi": klas.group(1) if klas else "",
        "sub_klasifikasi": sub.group(1) if sub else "",
        "provinsi": prov.group(1) if prov else "",
        "lembaga_peradilan": lembaga.group(1) if lembaga else "",
        "matched_patterns": [m[0] for m in matches],
        "snippets": [m[1] for m in matches[:3]],
    }


def main() -> None:
    if not DATASET_DIR.exists():
        raise SystemExit(
            f"indo-law dataset directory not found: {DATASET_DIR}\n"
            f"Extract indo-law.zip first."
        )

    files = sorted(DATASET_DIR.glob("*.xml"))
    print(f"[scan] Found {len(files):,} XML files in {DATASET_DIR}")

    hits: list[dict] = []
    klasifikasi_counter: Counter[str] = Counter()
    sub_counter: Counter[str] = Counter()
    prov_counter: Counter[str] = Counter()
    pattern_counter: Counter[str] = Counter()

    for i, f in enumerate(files):
        if i % 1000 == 0 and i > 0:
            print(f"[scan]   processed {i:,} / {len(files):,} "
                  f"(hits so far: {len(hits):,})")
        info = scan_file(f)
        if info is None:
            continue
        hits.append(info)
        klasifikasi_counter[info["klasifikasi"]] += 1
        sub_counter[info["sub_klasifikasi"]] += 1
        prov_counter[info["provinsi"]] += 1
        for p in info["matched_patterns"]:
            pattern_counter[p] += 1

    print(f"[scan] Done. Total adat hits: {len(hits):,} "
          f"({len(hits)/len(files):.2%} of files)")

    HITS_JSON.write_text(json.dumps(hits, ensure_ascii=False, indent=2),
                         encoding="utf-8")

    lines: list[str] = []
    lines.append("# Indo-Law Adat Scan Report")
    lines.append("")
    lines.append(f"- Files scanned: {len(files):,}")
    lines.append(f"- Adat-related hits: {len(hits):,}")
    lines.append(f"- Hit rate: {len(hits)/len(files):.2%}")
    lines.append("")
    lines.append("## Klasifikasi distribution (adat hits)")
    lines.append("")
    for k, c in klasifikasi_counter.most_common():
        lines.append(f"- {c}x `{k}`")
    lines.append("")
    lines.append("## Sub-klasifikasi (top 20)")
    lines.append("")
    for s, c in sub_counter.most_common(20):
        lines.append(f"- {c}x `{s}`")
    lines.append("")
    lines.append("## Provinsi (top 20)")
    lines.append("")
    for p, c in prov_counter.most_common(20):
        lines.append(f"- {c}x `{p}`")
    lines.append("")
    lines.append("## Matched patterns")
    lines.append("")
    for p, c in pattern_counter.most_common():
        lines.append(f"- {c}x `{p}`")
    lines.append("")
    lines.append("## Sample hits (first 10)")
    lines.append("")
    for i, hit in enumerate(hits[:10], 1):
        lines.append(f"### Hit #{i}: {hit['file']}")
        lines.append(f"- Klasifikasi: `{hit['klasifikasi']}` / "
                     f"sub: `{hit['sub_klasifikasi']}`")
        lines.append(f"- Provinsi: `{hit['provinsi']}` | "
                     f"Lembaga: `{hit['lembaga_peradilan']}`")
        lines.append(f"- Patterns: {hit['matched_patterns']}")
        for j, snippet in enumerate(hit["snippets"], 1):
            lines.append(f"- Snippet {j}: `...{snippet}...`")
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[scan] Wrote {REPORT.name} and {HITS_JSON.name}")


if __name__ == "__main__":
    main()
