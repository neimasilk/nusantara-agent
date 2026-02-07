import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATH_CANDIDATES = ROOT / "data" / "raw" / "ma_decisions" / "candidates_from_internal_outputs.csv"
DIR_MA = ROOT / "data" / "raw" / "ma_decisions"


def sanitize_nomor(nomor: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", nomor).strip("_")


def tebakan_domain(sumber_internal: str) -> str:
    s = sumber_internal.lower()
    if "bali" in s:
        return "bali"
    if "jawa" in s:
        return "jawa"
    if "minang" in s:
        return "minangkabau"
    return "campuran"


def buat_stub(row: dict) -> dict:
    nomor = row["nomor_perkara"]
    return {
        "metadata": {
            "nomor_perkara": nomor,
            "tanggal_putusan": "",
            "tingkat_peradilan": "",
            "domain_adat": tebakan_domain(row.get("sumber_internal", "")),
            "sumber_url": "",
            "status_verifikasi": "draft",
        },
        "substansi": {
            "fakta_inti": "",
            "isu_hukum": "",
            "norma_nasional": [],
            "norma_adat": [],
            "ratio_decidendi": "",
            "amar_putusan": "",
            "catatan_keterbatasan": (
                "Stub otomatis dari kandidat internal. Isi wajib diverifikasi "
                "ke putusan.mahkamahagung.go.id sebelum dipakai sebagai ground truth."
            ),
        },
        "provenance": {
            "sumber_internal": row.get("sumber_internal", ""),
            "status_verifikasi_awal": row.get("status_verifikasi", ""),
            "catatan_awal": row.get("catatan", ""),
        },
    }


def main():
    if not PATH_CANDIDATES.exists():
        raise FileNotFoundError(f"File kandidat tidak ditemukan: {PATH_CANDIDATES}")

    DIR_MA.mkdir(parents=True, exist_ok=True)
    dibuat = 0
    dilewati = 0

    with PATH_CANDIDATES.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nomor = row["nomor_perkara"].strip()
            if not nomor:
                continue
            fname = f"putusan_{sanitize_nomor(nomor)}.json"
            out_path = DIR_MA / fname
            if out_path.exists():
                dilewati += 1
                continue

            stub = buat_stub(row)
            with out_path.open("w", encoding="utf-8") as out:
                json.dump(stub, out, ensure_ascii=False, indent=2)
            dibuat += 1

    print("=== Generate MA Stubs ===")
    print(f"Dibuat: {dibuat}")
    print(f"Dilewati (sudah ada): {dilewati}")
    print(f"Folder output: {DIR_MA}")


if __name__ == "__main__":
    main()

