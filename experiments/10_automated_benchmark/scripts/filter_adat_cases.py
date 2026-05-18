"""Filter ledwindra/mahkamah-agung sample for adat-related cases.

Goal: count and categorize Indonesian Supreme Court (MA) cases that involve
customary law (hukum adat) in some way. Used to decide whether enough
adat-relevant cases exist for an automated benchmark pivot.

Searches across fields: klasifikasi, kata_kunci, catatan_amar, kaidah, abstrak.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True, parents=True)

INPUT_FILE = SAMPLES / "ledwindra-putusan-per-kasus.json"
OUTPUT_FILE = RESULTS / "ledwindra_adat_filtered.json"
REPORT_FILE = RESULTS / "ledwindra_adat_report.md"

# Adat keyword sets per domain (case insensitive, word-boundary matched).
DOMAIN_KEYWORDS = {
    "minangkabau": [
        r"\bminang", r"\bminangkabau\b", r"\bpusako\b", r"\bpusaka\s+tinggi\b",
        r"\bpusaka\s+rendah\b", r"\bharato\b", r"\bmamak\b", r"\bkaum\b",
        r"\bsuku\s+matrilineal\b", r"\bniniak\s+mamak\b", r"\bsako\b",
        r"\btanah\s+pusako\b", r"\bharato\s+pusako\b",
    ],
    "bali": [
        r"\bbali\b", r"\bbalinese\b", r"\bdruwe\b", r"\bsentana\b",
        r"\bpekraman\b", r"\bbanjar\b", r"\bdesa\s+adat\b", r"\bpurusa\b",
        r"\bpredana\b", r"\bawig.awig\b", r"\bsentana\s+rajeg\b",
    ],
    "jawa": [
        r"\bjawa\b", r"\bgono.gini\b", r"\bsigar\s+semangka\b",
        r"\bharta\s+gono.gini\b", r"\bharta\s+gawan\b",
    ],
    "batak": [
        r"\bbatak\b", r"\bdalihan\s+na\s+tolu\b", r"\bmarga\b",
    ],
    "umum_adat": [
        r"\bhukum\s+adat\b", r"\btanah\s+ulayat\b", r"\bhak\s+ulayat\b",
        r"\bmasyarakat\s+hukum\s+adat\b", r"\bwaris\s+adat\b",
        r"\bpewarisan\s+adat\b", r"\badat\s+istiadat\b",
        r"\bmasyarakat\s+adat\b", r"\btanah\s+adat\b",
        r"\bperceraian\s+adat\b", r"\bperkawinan\s+adat\b",
    ],
}

ALL_PATTERNS = [(domain, re.compile(p, re.IGNORECASE))
                for domain, kws in DOMAIN_KEYWORDS.items()
                for p in kws]

# Fields in each record that we search.
SEARCH_FIELDS = ["klasifikasi", "kata_kunci", "catatan_amar",
                 "kaidah", "abstrak", "putusan"]


def search_record(record: dict) -> dict | None:
    """Return match info if record mentions any adat keyword, else None."""
    matched_domains: set[str] = set()
    matched_patterns: list[str] = []
    matched_fields: set[str] = set()

    for field in SEARCH_FIELDS:
        value = record.get(field)
        if not value or not isinstance(value, str):
            continue
        for domain, pattern in ALL_PATTERNS:
            if pattern.search(value):
                matched_domains.add(domain)
                matched_patterns.append(pattern.pattern)
                matched_fields.add(field)

    if not matched_domains:
        return None

    return {
        "domains": sorted(matched_domains),
        "patterns": sorted(set(matched_patterns)),
        "fields": sorted(matched_fields),
    }


def main() -> None:
    if not INPUT_FILE.exists():
        raise SystemExit(f"Input not found: {INPUT_FILE}")

    print(f"[filter] Reading {INPUT_FILE.name}...")
    records = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    print(f"[filter] Total records: {len(records):,}")

    hits: list[dict] = []
    domain_counter: Counter[str] = Counter()
    field_counter: Counter[str] = Counter()
    klasifikasi_counter: Counter[str] = Counter()
    pattern_counter: Counter[str] = Counter()

    for record in records:
        match = search_record(record)
        if match is None:
            continue

        hits.append({"match": match, "record": record})
        for d in match["domains"]:
            domain_counter[d] += 1
        for f in match["fields"]:
            field_counter[f] += 1
        for p in match["patterns"]:
            pattern_counter[p] += 1
        klasifikasi_counter[(record.get("klasifikasi") or "").strip()] += 1

    print(f"[filter] Adat-relevant hits: {len(hits):,}")
    print(f"[filter] Hit rate: {len(hits)/len(records):.2%}")

    # Save matches.
    OUTPUT_FILE.write_text(
        json.dumps(hits, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Build report.
    lines: list[str] = []
    lines.append("# Ledwindra Adat Filter Report")
    lines.append("")
    lines.append(f"- Input: `{INPUT_FILE.name}`")
    lines.append(f"- Total records examined: {len(records):,}")
    lines.append(f"- Adat-relevant hits: {len(hits):,}")
    lines.append(f"- Hit rate: {len(hits)/len(records):.2%}")
    lines.append("")
    lines.append("## Hits per domain")
    lines.append("")
    for domain, count in domain_counter.most_common():
        lines.append(f"- **{domain}**: {count}")
    lines.append("")
    lines.append("## Hits per field")
    lines.append("")
    for field, count in field_counter.most_common():
        lines.append(f"- `{field}`: {count}")
    lines.append("")
    lines.append("## Top klasifikasi among hits")
    lines.append("")
    for klas, count in klasifikasi_counter.most_common(15):
        klas_display = klas if klas else "(empty)"
        lines.append(f"- {count}x `{klas_display}`")
    lines.append("")
    lines.append("## Top matched patterns")
    lines.append("")
    for pattern, count in pattern_counter.most_common(20):
        lines.append(f"- {count}x `{pattern}`")
    lines.append("")
    lines.append("## Sample hits (first 5)")
    lines.append("")
    for i, hit in enumerate(hits[:5], 1):
        rec = hit["record"]
        match = hit["match"]
        lines.append(f"### Hit #{i}: {rec.get('nomor', '?')}")
        lines.append(f"- **Lembaga**: {rec.get('lembaga_peradilan', '?')}")
        lines.append(f"- **Klasifikasi**: `{(rec.get('klasifikasi') or '').strip()}`")
        lines.append(f"- **Kata kunci**: `{(rec.get('kata_kunci') or '').strip()}`")
        lines.append(f"- **Tahun**: {rec.get('tahun', '?')}")
        lines.append(f"- **Domains matched**: {match['domains']}")
        lines.append(f"- **Fields matched**: {match['fields']}")
        catatan = (rec.get("catatan_amar") or "").strip()
        if catatan:
            snippet = catatan[:300] + ("..." if len(catatan) > 300 else "")
            lines.append(f"- **Catatan amar (truncated)**: {snippet}")
        lines.append("")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"[filter] Wrote {OUTPUT_FILE.name} ({len(hits)} hits)")
    print(f"[filter] Wrote {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
