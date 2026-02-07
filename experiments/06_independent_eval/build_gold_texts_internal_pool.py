import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
DIR_OUT = ROOT / "data" / "raw" / "gold_standard_texts"
PATH_INDEX = DIR_OUT / "index_internal_pool.csv"

TARGET_TOTAL = 200
TARGET_PER_DOMAIN = {
    "minangkabau": 67,
    "bali": 67,
    "jawa": 66,
}

SCAN_DIRS = [
    ROOT / "data" / "raw" / "minangkabau",
    ROOT / "data" / "raw" / "bali",
    ROOT / "data" / "raw" / "jawa",
    ROOT / "experiments" / "07_advanced_orchestration" / "results",
    ROOT / "experiments" / "07_advanced_orchestration" / "baseline_results",
    ROOT / "experiments" / "07_advanced_orchestration" / "results_token_probe",
    ROOT / "experiments" / "07_advanced_orchestration" / "baseline_results_token_probe",
]


def slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")[:40]


def split_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for p in parts:
        p = p.strip()
        if len(p) < 30:
            continue
        if p.startswith("{") or p.startswith("["):
            continue
        if "```" in p:
            continue
        out.append(p)
    return out


def chunk_sentences(sents: List[str], min_len: int = 120, max_len: int = 550) -> List[str]:
    chunks: List[str] = []
    cur = ""
    for s in sents:
        candidate = f"{cur} {s}".strip() if cur else s
        if len(candidate) <= max_len:
            cur = candidate
        else:
            if len(cur) >= min_len:
                chunks.append(cur.strip())
            cur = s
    if len(cur) >= min_len:
        chunks.append(cur.strip())
    return chunks


def detect_domain(text: str, rel_path: str) -> str:
    t = f"{rel_path.lower()} {text.lower()}"
    skor = {
        "minangkabau": 0,
        "bali": 0,
        "jawa": 0,
    }
    minang_kw = [
        "minangkabau", "pusako", "kemenakan", "mamak", "matrilineal", "penghulu",
    ]
    bali_kw = [
        "bali", "kapurusa", "sentana", "nyentana", "druwe", "desa pakraman", "awig",
    ]
    jawa_kw = [
        "jawa", "gono-gini", "gono gini", "sepikul", "segendongan", "bilateral",
    ]
    for kw in minang_kw:
        if kw in t:
            skor["minangkabau"] += 1
    for kw in bali_kw:
        if kw in t:
            skor["bali"] += 1
    for kw in jawa_kw:
        if kw in t:
            skor["jawa"] += 1
    domain = max(skor, key=skor.get)
    if skor[domain] == 0:
        if "bali" in rel_path.lower():
            return "bali"
        if "jawa" in rel_path.lower():
            return "jawa"
        return "minangkabau"
    return domain


def normalize_for_dedup(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def collect_candidates() -> List[Tuple[str, str, str]]:
    candidates: List[Tuple[str, str, str]] = []
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.suffix.lower() not in {".txt", ".md", ".json"}:
                continue
            if p.name.lower().startswith("readme"):
                continue
            try:
                raw = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            sents = split_sentences(raw)
            chunks = chunk_sentences(sents)
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            for ch in chunks:
                domain = detect_domain(ch, rel)
                candidates.append((domain, rel, ch))
    return candidates


def list_existing_ids() -> List[int]:
    ids = []
    for p in DIR_OUT.glob("GS-*.txt"):
        m = re.match(r"GS-(\d{4})__", p.name)
        if m:
            ids.append(int(m.group(1)))
    return sorted(ids)


def main() -> None:
    DIR_OUT.mkdir(parents=True, exist_ok=True)
    existing_ids = list_existing_ids()
    next_id = (max(existing_ids) + 1) if existing_ids else 1
    existing_count = len(existing_ids)

    if existing_count >= TARGET_TOTAL:
        print(f"Sudah >= target. existing={existing_count}, target={TARGET_TOTAL}")
        return

    remain = TARGET_TOTAL - existing_count
    candidates = collect_candidates()
    print(f"Kandidat terkumpul: {len(candidates)}")

    # hitung existing per domain dari index_seed/index_internal_pool jika ada
    current_domain_count: Dict[str, int] = {"minangkabau": 0, "bali": 0, "jawa": 0}
    for index_path in [DIR_OUT / "index_seed.csv", DIR_OUT / "index_internal_pool.csv"]:
        if not index_path.exists():
            continue
        with index_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                d = (row.get("domain") or "").strip().lower()
                if d in current_domain_count:
                    current_domain_count[d] += 1

    target_need = {
        d: max(TARGET_PER_DOMAIN[d] - current_domain_count[d], 0)
        for d in TARGET_PER_DOMAIN
    }

    seen_norm = set()
    rows_out = []
    created = 0
    created_by_domain = {"minangkabau": 0, "bali": 0, "jawa": 0}

    for domain, rel, text in candidates:
        if created >= remain:
            break
        if domain not in target_need:
            continue
        if created_by_domain[domain] >= target_need[domain]:
            continue
        norm = normalize_for_dedup(text)
        if len(norm) < 80:
            continue
        if norm in seen_norm:
            continue
        seen_norm.add(norm)

        pid = f"GS-{next_id:04d}"
        topik = slug(text.split(".")[0]) or "internal_pool"
        fname = f"{pid}__{domain}__{topik}.txt"
        (DIR_OUT / fname).write_text(text + "\n", encoding="utf-8")

        rows_out.append(
            {
                "paragraph_id": pid,
                "filename": fname,
                "domain": domain,
                "subtopik": topik,
                "source_title": Path(rel).name,
                "source_author": "internal_pool",
                "source_year": "2026",
                "source_url": f"internal://{rel}",
                "status": "internal_pool_seed",
            }
        )
        next_id += 1
        created += 1
        created_by_domain[domain] += 1

    with PATH_INDEX.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "paragraph_id",
                "filename",
                "domain",
                "subtopik",
                "source_title",
                "source_author",
                "source_year",
                "source_url",
                "status",
            ],
        )
        writer.writeheader()
        writer.writerows(rows_out)

    print("=== Build Gold Texts Internal Pool ===")
    print(f"Existing awal: {existing_count}")
    print(f"Dibuat baru: {created}")
    print(f"By domain: {created_by_domain}")
    print(f"Total akhir (perkiraan): {existing_count + created}")
    print(f"Index baru: {PATH_INDEX}")


if __name__ == "__main__":
    main()
