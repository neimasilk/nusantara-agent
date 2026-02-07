import csv
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIR_ANNOT = ROOT / "data" / "processed" / "gold_standard" / "annotations"
DIR_TEXT = ROOT / "data" / "raw" / "gold_standard_texts"


def buat_stub(row: dict) -> dict:
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return {
        "metadata": {
            "source_document": row["filename"],
            "paragraph_id": row["paragraph_id"],
            "domain": row["domain"],
            "annotator_id": row["annotator_id"],
            "timestamp": ts,
        },
        "triples": [],
    }


def main():
    parser = argparse.ArgumentParser(description="Generate annotation stubs from assignment CSV")
    parser.add_argument(
        "--assignment",
        default="data/processed/gold_standard/pilot_assignment_20_items.csv",
        help="Path assignment CSV relatif root repo",
    )
    args = parser.parse_args()

    path_assign = (ROOT / args.assignment).resolve()
    if not path_assign.exists():
        # fallback when user passes absolute path string
        path_assign = Path(args.assignment)

    if not path_assign.exists():
        raise FileNotFoundError(f"File assignment tidak ditemukan: {args.assignment}")

    DIR_ANNOT.mkdir(parents=True, exist_ok=True)
    dibuat = 0
    dilewati = 0
    missing_text = 0

    with path_assign.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row["filename"]
            text_path = DIR_TEXT / filename
            if not text_path.exists():
                missing_text += 1
                print(f"[SKIP] sumber teks tidak ada: {filename}")
                continue

            out_name = f"{row['paragraph_id']}__{row['annotator_id']}.json"
            out_path = DIR_ANNOT / out_name
            if out_path.exists():
                dilewati += 1
                continue

            stub = buat_stub(row)
            with out_path.open("w", encoding="utf-8") as out:
                json.dump(stub, out, ensure_ascii=False, indent=2)
            dibuat += 1

    print("=== Generate Annotation Stubs ===")
    print(f"Dibuat: {dibuat}")
    print(f"Dilewati (sudah ada): {dilewati}")
    print(f"Dilewati (source text hilang): {missing_text}")
    print(f"Assignment: {path_assign}")
    print(f"Folder output: {DIR_ANNOT}")


if __name__ == "__main__":
    main()
