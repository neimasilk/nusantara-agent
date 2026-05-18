"""Strict-mode adat case filter: requires phrase-level evidence (not single tokens).

We rerun the ledwindra filter, but only count hits when the text contains
multi-word adat phrases or names that uniquely identify customary law context.
This trims false positives like "Bali" used as a province or "marga" used as
a clan-style surname.
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
OUTPUT_FILE = RESULTS / "ledwindra_adat_strict.json"
REPORT_FILE = RESULTS / "ledwindra_adat_strict_report.md"

# Strict patterns: multi-word adat phrases that survive most false positives.
STRICT_PATTERNS = {
    "hukum_adat_eksplisit": [
        r"\bhukum\s+adat\b",
        r"\btata\s+cara\s+adat\b",
        r"\bmasyarakat\s+adat\b",
        r"\bmasyarakat\s+hukum\s+adat\b",
        r"\badat\s+istiadat\b",
        r"\bsesuai\s+adat\b",
        r"\bmenurut\s+adat\b",
        r"\bberdasarkan\s+adat\b",
    ],
    "waris_adat": [
        r"\bwaris\s+adat\b",
        r"\bpewarisan\s+adat\b",
        r"\bahli\s+waris\s+adat\b",
        r"\bharta\s+pusaka\b",
        r"\bharato\s+pusako\b",
        r"\bpusako\s+tinggi\b",
        r"\bpusako\s+rendah\b",
    ],
    "tanah_adat": [
        r"\btanah\s+ulayat\b",
        r"\bhak\s+ulayat\b",
        r"\btanah\s+adat\b",
        r"\btanah\s+pusaka\b",
        r"\bdruwe\s+gabro\b",
        r"\bdruwe\s+desa\b",
        r"\bayahan\s+desa\b",
    ],
    "perkawinan_adat": [
        r"\bperkawinan\s+adat\b",
        r"\bperceraian\s+adat\b",
        r"\bharta\s+gono.gini\b",
        r"\bsigar\s+semangka\b",
    ],
    "domain_minangkabau": [
        r"\bminangkabau\b",
        r"\bniniak\s+mamak\b",
        r"\bharta\s+pusaka\s+tinggi\b",
    ],
    "domain_bali": [
        r"\bdesa\s+adat\b",
        r"\bdesa\s+pakraman\b",
        r"\bsentana\s+rajeg\b",
        r"\bawig.awig\b",
    ],
    "domain_jawa": [
        r"\bharta\s+gawan\b",
        r"\bharta\s+bawaan\b",
    ],
    "domain_lain": [
        r"\bdalihan\s+na\s+tolu\b",
        r"\bsuku\s+anak\s+dalam\b",
    ],
}

ALL_PATTERNS = [(domain, re.compile(p, re.IGNORECASE))
                for domain, kws in STRICT_PATTERNS.items()
                for p in kws]

SEARCH_FIELDS = ["klasifikasi", "kata_kunci", "catatan_amar",
                 "kaidah", "abstrak", "putusan"]


def search_record(record: dict) -> dict | None:
    matched_domains: set[str] = set()
    matched_patterns: list[str] = []
    matched_fields: set[str] = set()
    snippets: dict[str, str] = {}

    for field in SEARCH_FIELDS:
        value = record.get(field)
        if not value or not isinstance(value, str):
            continue
        for domain, pattern in ALL_PATTERNS:
            m = pattern.search(value)
            if m:
                matched_domains.add(domain)
                matched_patterns.append(pattern.pattern)
                matched_fields.add(field)
                if field not in snippets:
                    start = max(0, m.start() - 60)
                    end = min(len(value), m.end() + 60)
                    snippets[field] = value[start:end].strip()

    if not matched_domains:
        return None

    return {
        "domains": sorted(matched_domains),
        "patterns": sorted(set(matched_patterns)),
        "fields": sorted(matched_fields),
        "snippets": snippets,
    }


def main() -> None:
    records = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    print(f"[strict] Total records: {len(records):,}")

    hits = []
    domain_counter: Counter[str] = Counter()
    klasifikasi_counter: Counter[str] = Counter()
    pattern_counter: Counter[str] = Counter()

    for record in records:
        match = search_record(record)
        if match is None:
            continue
        hits.append({"match": match, "record": record})
        for d in match["domains"]:
            domain_counter[d] += 1
        for p in match["patterns"]:
            pattern_counter[p] += 1
        klasifikasi_counter[(record.get("klasifikasi") or "").strip()] += 1

    print(f"[strict] Strict adat hits: {len(hits):,}")
    print(f"[strict] Strict hit rate: {len(hits)/len(records):.2%}")

    OUTPUT_FILE.write_text(
        json.dumps(hits, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines: list[str] = []
    lines.append("# Ledwindra Adat Filter (Strict Mode)")
    lines.append("")
    lines.append(f"- Records examined: {len(records):,}")
    lines.append(f"- Strict adat hits: {len(hits):,}")
    lines.append(f"- Strict hit rate: {len(hits)/len(records):.2%}")
    lines.append("")
    lines.append("## Domains (strict)")
    lines.append("")
    for d, c in domain_counter.most_common():
        lines.append(f"- {d}: {c}")
    lines.append("")
    lines.append("## Klasifikasi (strict)")
    lines.append("")
    for k, c in klasifikasi_counter.most_common():
        lines.append(f"- {c}x `{k or '(empty)'}`")
    lines.append("")
    lines.append("## Matched patterns")
    lines.append("")
    for p, c in pattern_counter.most_common():
        lines.append(f"- {c}x `{p}`")
    lines.append("")
    lines.append("## All hits with snippets")
    lines.append("")
    for i, hit in enumerate(hits, 1):
        rec = hit["record"]
        match = hit["match"]
        lines.append(f"### Hit #{i}: {rec.get('nomor', '?')}")
        lines.append(f"- Lembaga: {rec.get('lembaga_peradilan', '?')}")
        lines.append(f"- Klasifikasi: `{(rec.get('klasifikasi') or '').strip()}`")
        lines.append(f"- Kata kunci: `{(rec.get('kata_kunci') or '').strip()}`")
        lines.append(f"- Tahun: {rec.get('tahun', '?')}")
        lines.append(f"- Domains: {match['domains']}")
        for field, snippet in match["snippets"].items():
            lines.append(f"- Snippet ({field}): `...{snippet}...`")
        lines.append("")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"[strict] Wrote {OUTPUT_FILE.name}, {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
