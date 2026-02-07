import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SUMBER_DOMAIN = [
    ("minangkabau", ROOT / "data" / "raw" / "minangkabau" / "pilot_minangkabau.txt"),
    ("bali", ROOT / "data" / "raw" / "bali" / "sentana_rajeg_overview.txt"),
    ("jawa", ROOT / "data" / "raw" / "jawa" / "gonogini_overview.txt"),
]

DIR_GS = ROOT / "data" / "raw" / "gold_standard_texts"
PATH_INDEX = DIR_GS / "index_seed.csv"
PATH_MA_CANDIDATES = ROOT / "data" / "raw" / "ma_decisions" / "candidates_from_internal_outputs.csv"
PATH_ASSIGNMENT = (
    ROOT / "data" / "processed" / "gold_standard" / "pilot_assignment_20_items.csv"
)

DIR_SCAN = [
    ROOT / "experiments" / "07_advanced_orchestration" / "results",
    ROOT / "experiments" / "07_advanced_orchestration" / "baseline_results",
]


def pecah_kalimat(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def chunk_kalimat(kalimat: list[str], ukuran: int = 2) -> list[str]:
    out = []
    for i in range(0, len(kalimat), ukuran):
        chunk = " ".join(kalimat[i : i + ukuran]).strip()
        if chunk:
            out.append(chunk)
    return out


def slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")[:40]


def buat_seed_gold_texts():
    DIR_GS.mkdir(parents=True, exist_ok=True)
    for old in DIR_GS.glob("GS-*.txt"):
        old.unlink()
    rows = []
    gs_counter = 1

    for domain, path in SUMBER_DOMAIN:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        kalimat = pecah_kalimat(text)
        chunks = chunk_kalimat(kalimat, ukuran=1)

        for idx, chunk in enumerate(chunks, start=1):
            pid = f"GS-{gs_counter:04d}"
            topik = slug(chunk.split(".")[0]) or f"topik_{idx:02d}"
            filename = f"{pid}__{domain}__{topik}.txt"
            (DIR_GS / filename).write_text(chunk + "\n", encoding="utf-8")

            rows.append(
                {
                    "paragraph_id": pid,
                    "filename": filename,
                    "domain": domain,
                    "subtopik": topik,
                    "source_title": path.name,
                    "source_author": "internal_seed",
                    "source_year": "2026",
                    "source_url": "internal://seed_from_repo",
                    "status": "pilot_seed",
                }
            )
            gs_counter += 1

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
        writer.writerows(rows)

    print(f"Seed gold texts dibuat: {len(rows)} file")
    print(f"Index: {PATH_INDEX}")
    return rows


def ekstrak_kandidat_putusan() -> list[dict]:
    pola = re.compile(
        r"(?:Putusan\s+MA(?:hkamah\s+Agung)?\s*(?:No\.?|Nomor)?\s*|No\.?\s*)"
        r"([0-9]{1,4}\s?[A-Za-z]{0,3}/[A-Za-z]{1,5}/[0-9]{2,4}|[0-9]{1,4}[A-Za-z]?/[A-Za-z]{1,5}/[0-9]{2,4})",
        re.IGNORECASE,
    )
    results = {}
    for scan_dir in DIR_SCAN:
        if not scan_dir.exists():
            continue
        for path in scan_dir.rglob("*"):
            if path.suffix.lower() not in {".txt", ".json", ".md"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for m in pola.finditer(text):
                nomor = re.sub(r"\s+", "", m.group(1))
                key = nomor.upper()
                if key not in results:
                    results[key] = {
                        "nomor_perkara": key,
                        "sumber_internal": str(path.relative_to(ROOT)).replace("\\", "/"),
                        "status_verifikasi": "belum_terverifikasi",
                        "catatan": "Perlu cek ke putusan.mahkamahagung.go.id",
                    }
    return sorted(results.values(), key=lambda x: x["nomor_perkara"])


def simpan_kandidat_putusan(rows: list[dict]):
    PATH_MA_CANDIDATES.parent.mkdir(parents=True, exist_ok=True)
    with PATH_MA_CANDIDATES.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "nomor_perkara",
                "sumber_internal",
                "status_verifikasi",
                "catatan",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Kandidat putusan MA disimpan: {len(rows)}")
    print(f"File: {PATH_MA_CANDIDATES}")


def simpan_assignment_pilot(rows_seed: list[dict]):
    target_item = min(20, len(rows_seed))
    annotators = [f"ann{i:02d}" for i in range(1, 6)]
    rows_out = []
    for row in rows_seed[:target_item]:
        for ann in annotators:
            rows_out.append(
                {
                    "annotator_id": ann,
                    "paragraph_id": row["paragraph_id"],
                    "filename": row["filename"],
                    "domain": row["domain"],
                    "batch": "pilot_20",
                    "status": "assigned",
                }
            )

    PATH_ASSIGNMENT.parent.mkdir(parents=True, exist_ok=True)
    with PATH_ASSIGNMENT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "annotator_id",
                "paragraph_id",
                "filename",
                "domain",
                "batch",
                "status",
            ],
        )
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"Assignment pilot disimpan: {len(rows_out)} baris")
    print(f"File: {PATH_ASSIGNMENT}")


def main():
    rows_seed = buat_seed_gold_texts()
    simpan_assignment_pilot(rows_seed)
    kandidat = ekstrak_kandidat_putusan()
    simpan_kandidat_putusan(kandidat)


if __name__ == "__main__":
    main()
