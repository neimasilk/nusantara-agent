import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIR_GOLD_TEXT = ROOT / "data" / "raw" / "gold_standard_texts"
DIR_ANNOT = ROOT / "data" / "processed" / "gold_standard" / "annotations"
DIR_MA = ROOT / "data" / "raw" / "ma_decisions"
PATH_SCHEMA_ANNOT = ROOT / "data" / "annotation" / "schema.json"
PATH_SCHEMA_MA = DIR_MA / "schema_putusan.json"

TARGET_PARAGRAF = 200
TARGET_ANNOTATOR = 5
TARGET_PUTUSAN_MA = 50
WAJIB_TRIPLES_NONKOSONG = True
MAX_DETAIL_ERROR = 10
WAJIB_PUTUSAN_FIELD_NONKOSONG = True


def baca_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validasi_annotasi_minimal(obj: dict) -> list[str]:
    error = []
    if "metadata" not in obj or not isinstance(obj["metadata"], dict):
        error.append("field metadata tidak ada/invalid")
    if "triples" not in obj or not isinstance(obj["triples"], list):
        error.append("field triples tidak ada/invalid")
        return error
    if WAJIB_TRIPLES_NONKOSONG and len(obj["triples"]) == 0:
        error.append("triples kosong")

    metadata = obj.get("metadata", {})
    for wajib in ["source_document", "paragraph_id", "domain", "annotator_id"]:
        if wajib not in metadata:
            error.append(f"metadata.{wajib} tidak ada")

    for i, triple in enumerate(obj.get("triples", []), start=1):
        if not isinstance(triple, dict):
            error.append(f"triples[{i}] bukan object")
            continue
        for wajib in ["head", "relation", "tail", "category", "confidence"]:
            if wajib not in triple:
                error.append(f"triples[{i}].{wajib} tidak ada")
    return error


def validasi_putusan_minimal(obj: dict) -> list[str]:
    error = []
    if "metadata" not in obj or not isinstance(obj["metadata"], dict):
        error.append("field metadata tidak ada/invalid")
    if "substansi" not in obj or not isinstance(obj["substansi"], dict):
        error.append("field substansi tidak ada/invalid")
        return error

    for wajib in [
        "nomor_perkara",
        "tanggal_putusan",
        "tingkat_peradilan",
        "domain_adat",
        "sumber_url",
        "status_verifikasi",
    ]:
        if wajib not in obj.get("metadata", {}):
            error.append(f"metadata.{wajib} tidak ada")

    for wajib in ["fakta_inti", "isu_hukum", "ratio_decidendi", "amar_putusan"]:
        if wajib not in obj.get("substansi", {}):
            error.append(f"substansi.{wajib} tidak ada")
        elif WAJIB_PUTUSAN_FIELD_NONKOSONG:
            val = str(obj.get("substansi", {}).get(wajib, "")).strip()
            if not val:
                error.append(f"substansi.{wajib} kosong")

    if WAJIB_PUTUSAN_FIELD_NONKOSONG:
        for wajib in ["tanggal_putusan", "tingkat_peradilan", "sumber_url"]:
            val = str(obj.get("metadata", {}).get(wajib, "")).strip()
            if not val:
                error.append(f"metadata.{wajib} kosong")
    return error


def main():
    print("=== Precheck Exp 06 ===")
    print(f"Root: {ROOT}")

    for path in [DIR_GOLD_TEXT, DIR_ANNOT, DIR_MA, PATH_SCHEMA_ANNOT, PATH_SCHEMA_MA]:
        status = "OK" if path.exists() else "MISSING"
        print(f"- {status}: {path}")

    text_files = sorted(DIR_GOLD_TEXT.glob("*.txt")) if DIR_GOLD_TEXT.exists() else []
    annot_files = [
        p for p in sorted(DIR_ANNOT.glob("*.json"))
        if p.name not in {"template_annotasi.json"}
    ] if DIR_ANNOT.exists() else []
    ma_files = [
        p for p in sorted(DIR_MA.glob("*.json"))
        if p.name not in {"schema_putusan.json", "template_putusan_0001.json"}
    ] if DIR_MA.exists() else []

    print(f"\nJumlah paragraf gold text: {len(text_files)} / target {TARGET_PARAGRAF}")
    print(
        f"Jumlah file anotasi: {len(annot_files)} / target {TARGET_PARAGRAF * TARGET_ANNOTATOR}"
    )
    print(f"Jumlah file putusan MA: {len(ma_files)} / target {TARGET_PUTUSAN_MA}")

    invalid_annot = 0
    detail_annot = 0
    for path in annot_files:
        try:
            obj = baca_json(path)
            errs = validasi_annotasi_minimal(obj)
            if errs:
                invalid_annot += 1
                if detail_annot < MAX_DETAIL_ERROR:
                    print(f"[ANNOT INVALID] {path.name}: {', '.join(errs)}")
                detail_annot += 1
        except Exception as e:
            invalid_annot += 1
            if detail_annot < MAX_DETAIL_ERROR:
                print(f"[ANNOT INVALID] {path.name}: {e}")
            detail_annot += 1

    invalid_ma = 0
    detail_ma = 0
    for path in ma_files:
        try:
            obj = baca_json(path)
            errs = validasi_putusan_minimal(obj)
            if errs:
                invalid_ma += 1
                if detail_ma < MAX_DETAIL_ERROR:
                    print(f"[MA INVALID] {path.name}: {', '.join(errs)}")
                detail_ma += 1
        except Exception as e:
            invalid_ma += 1
            if detail_ma < MAX_DETAIL_ERROR:
                print(f"[MA INVALID] {path.name}: {e}")
            detail_ma += 1

    if invalid_annot > MAX_DETAIL_ERROR:
        print(f"[ANNOT INVALID] ... {invalid_annot - MAX_DETAIL_ERROR} file lainnya disembunyikan")
    if invalid_ma > MAX_DETAIL_ERROR:
        print(f"[MA INVALID] ... {invalid_ma - MAX_DETAIL_ERROR} file lainnya disembunyikan")

    print("\n=== Ringkasan ===")
    print(f"- Invalid anotasi: {invalid_annot}")
    print(f"- Invalid putusan MA: {invalid_ma}")

    siap_art028 = (
        len(text_files) >= TARGET_PARAGRAF
        and len(annot_files) >= TARGET_PARAGRAF * TARGET_ANNOTATOR
        and invalid_annot == 0
    )
    siap_art030 = len(ma_files) >= TARGET_PUTUSAN_MA and invalid_ma == 0

    print("\nStatus kesiapan:")
    print(f"- ART-028 (anotasi): {'READY' if siap_art028 else 'NOT_READY'}")
    print(f"- ART-030 (putusan MA): {'READY' if siap_art030 else 'NOT_READY'}")

    if siap_art028 and siap_art030:
        print("- ART-031: dapat lanjut eksekusi.")
    else:
        print("- ART-031: tetap BLOCKED (menunggu artefak).")


if __name__ == "__main__":
    main()
