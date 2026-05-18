"""Recover narratives for the 21-case locked test set.

The dev set (49 cases) is already self-contained in
`experiments/09_ablation_study/benchmark_dev_seed42.json`. The test set is
only ID-locked in `dataset_split.json` and its narratives are spread across
multiple `docs/human_only/` artifacts plus existing result files. This
script reconstructs the full test-set JSON in the same shape as the dev seed.

Sources scanned (in priority order):
  1. docs/human_only/paket_labeling_50_kasus_baru.md     (GS-XXXX scenarios)
  2. docs/human_only/artifacts/paket_kerja_4_jam_*.md    (CS-XXX scenarios)
  3. docs/human_only/artifacts/keputusan_ahli_final.md   (4 adjudicated tie cases)
  4. experiments/09_ablation_study/results_dual_asp_llm_2026-02-19.json
     (gold labels)

Output:
  experiments/10_automated_benchmark/data/benchmark_test_recovered.json

Each output record has:
  - id          : case identifier
  - query       : narrative
  - gold_label  : final adjudicated label (A/B/C/D)
  - source      : path the narrative was lifted from (for traceability)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP10 = ROOT / "experiments" / "10_automated_benchmark"
ABLATION = ROOT / "experiments" / "09_ablation_study"
DOCS = ROOT / "docs"

SPLIT_FILE = ABLATION / "dataset_split.json"
GOLD_RESULTS = ABLATION / "results_dual_asp_llm_2026-02-19.json"
GS_PAKET = DOCS / "human_only" / "paket_labeling_50_kasus_baru.md"
ARTIFACTS = DOCS / "human_only" / "artifacts"
KEPUTUSAN_FINAL = ARTIFACTS / "keputusan_ahli_final.md"

OUT_DIR = EXP10 / "data"
OUT_DIR.mkdir(exist_ok=True, parents=True)
OUT_FILE = OUT_DIR / "benchmark_test_recovered.json"
REPORT_FILE = EXP10 / "results" / "test_set_recovery_report.md"


def load_gold_labels() -> dict[str, str]:
    """id -> gold label (A/B/C/D) from the canonical 70-case run."""
    payload = json.loads(GOLD_RESULTS.read_text(encoding="utf-8"))
    return {r["id"]: r["gold"] for r in payload.get("results", [])}


def load_test_ids() -> list[str]:
    payload = json.loads(SPLIT_FILE.read_text(encoding="utf-8"))
    return payload["locked_test_set"]


def parse_gs_paket(target_ids: set[str]) -> dict[str, tuple[str, str]]:
    """Extract `### N. Case ID: GS-XXXX ... Skenario:` blocks."""
    if not GS_PAKET.exists():
        return {}
    text = GS_PAKET.read_text(encoding="utf-8")

    # Each entry block starts with "### N. Case ID: <id>"
    # and a "**Skenario:**" line below it. Scenario continues until next ###.
    pattern = re.compile(
        r"###\s+\d+\.\s+Case\s+ID:\s*(?P<id>GS-\d{4})\s*"
        r"(?P<body>.*?)(?=\n###\s+\d+\.|\Z)",
        re.DOTALL,
    )
    out: dict[str, tuple[str, str]] = {}
    for m in pattern.finditer(text):
        cid = m.group("id")
        if cid not in target_ids:
            continue
        body = m.group("body")
        sken = re.search(r"\*\*Skenario:\*\*\s*(?P<sk>[^\n]+(?:\n(?!\*\*|\n)[^\n]+)*)",
                         body)
        if sken:
            narrative = " ".join(sken.group("sk").split())
            out[cid] = (narrative, str(GS_PAKET.relative_to(ROOT)))
    return out


def parse_paket_kerja(target_ids: set[str]) -> dict[str, tuple[str, str]]:
    """Sweep all paket_kerja files for `| N | CS-XXX-NNN | Domain | Narasi |` rows."""
    out: dict[str, tuple[str, str]] = {}
    if not ARTIFACTS.exists():
        return out
    for md in ARTIFACTS.glob("paket_kerja_*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        # Table rows: | N | CS-XXX-NNN | Domain | narrative... |
        row_pattern = re.compile(
            r"\|\s*\d+\s*\|\s*(CS-[A-Z]+-\d+)\s*\|\s*([A-Za-z]+)\s*\|\s*"
            r"([^|\n]+?)\s*\|",
        )
        for m in row_pattern.finditer(text):
            cid = m.group(1)
            if cid not in target_ids:
                continue
            narrative = m.group(3).strip()
            # Keep the first (and usually richest) narrative encountered.
            if cid not in out and len(narrative) > 10:
                out[cid] = (narrative, str(md.relative_to(ROOT)))
    return out


def parse_interview_files(target_ids: set[str]) -> dict[str, tuple[str, str]]:
    """Pull narratives from `paket_interview_online_ahli*_terisi*.md` detail blocks.

    Pattern:
        ### N) CS-XXX-NNN
        **Kasus:**
        <narrative paragraph until next ### or **Pilih label:**>
    """
    out: dict[str, tuple[str, str]] = {}
    if not ARTIFACTS.exists():
        return out
    detail_pat = re.compile(
        r"###\s+\d+\)\s+(?P<id>(?:CS|GS)-[A-Z\-0-9]+)\s*\n"
        r"\*\*Kasus:\*\*\s*\n?(?P<nar>.*?)(?=\n\s*-\s*\*\*Pilih label|\n###\s|\Z)",
        re.DOTALL,
    )
    for md in ARTIFACTS.glob("paket_interview_online_ahli*_terisi*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for m in detail_pat.finditer(text):
            cid = m.group("id")
            if cid not in target_ids:
                continue
            narrative = " ".join(m.group("nar").split())
            if cid not in out and len(narrative) > 50:
                out[cid] = (narrative, str(md.relative_to(ROOT)))
    return out


def parse_keputusan_final(target_ids: set[str]) -> dict[str, tuple[str, str]]:
    """Pull narratives from the arbiter survey (4 tie cases)."""
    out: dict[str, tuple[str, str]] = {}
    if not KEPUTUSAN_FINAL.exists():
        return out
    text = KEPUTUSAN_FINAL.read_text(encoding="utf-8")
    block_pattern = re.compile(
        r"##\s+Kasus\s+\d+\s+-\s+(?P<id>CS-[A-Z]+-\d+).*?"
        r"Narasi:\s*\n?(?P<nar>.*?)(?=\n\nPosisi Ahli Sebelumnya|$)",
        re.DOTALL,
    )
    for m in block_pattern.finditer(text):
        cid = m.group("id")
        if cid not in target_ids:
            continue
        narrative = " ".join(m.group("nar").split())
        out[cid] = (narrative, str(KEPUTUSAN_FINAL.relative_to(ROOT)))
    return out


def main() -> None:
    test_ids = load_test_ids()
    target = set(test_ids)
    print(f"[recover] Target test set: {len(test_ids)} cases")

    gold = load_gold_labels()
    print(f"[recover] Loaded gold labels for {len(gold)} cases")

    # Resolution priority (richest narrative first):
    #   keputusan_final > interview_terisi > gs_paket_50 > paket_kerja (table)
    sources = (
        parse_keputusan_final(target),
        parse_interview_files(target),
        parse_gs_paket(target),
        parse_paket_kerja(target),
    )

    recovered: dict[str, tuple[str, str]] = {}
    for src in sources:
        for cid, value in src.items():
            recovered.setdefault(cid, value)

    print(f"[recover] Resolved {len(recovered)} / {len(target)} narratives")
    missing = sorted(target - set(recovered))
    if missing:
        print(f"[recover] MISSING ({len(missing)}): {missing}")

    output: list[dict] = []
    for cid in test_ids:
        if cid in recovered:
            narrative, source = recovered[cid]
        else:
            narrative, source = "", ""
        output.append({
            "id": cid,
            "query": narrative,
            "gold_label": gold.get(cid, ""),
            "source": source,
        })

    OUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print(f"[recover] Wrote {OUT_FILE}")

    # Report
    lines: list[str] = []
    lines.append("# Test Set Narrative Recovery Report")
    lines.append("")
    lines.append(f"- Target IDs: {len(test_ids)}")
    lines.append(f"- Resolved: {len(recovered)}")
    lines.append(f"- Missing: {len(missing)}")
    lines.append("")
    if missing:
        lines.append("## Missing")
        for m in missing:
            lines.append(f"- {m}")
        lines.append("")
    lines.append("## Resolved (source file per case)")
    lines.append("")
    for rec in output:
        if not rec["query"]:
            continue
        nar = rec["query"]
        snippet = nar if len(nar) <= 160 else nar[:160] + "..."
        lines.append(f"- **{rec['id']}** (gold={rec['gold_label']}) "
                     f"from `{rec['source']}`")
        lines.append(f"  - {snippet}")
    REPORT_FILE.parent.mkdir(exist_ok=True, parents=True)
    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"[recover] Wrote {REPORT_FILE}")


if __name__ == "__main__":
    main()
