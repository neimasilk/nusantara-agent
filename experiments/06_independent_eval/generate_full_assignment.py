import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DIR_GS = ROOT / "data" / "raw" / "gold_standard_texts"
PATH_OUT = ROOT / "data" / "processed" / "gold_standard" / "full_assignment_200x5.csv"

TARGET_ITEM = 200
ANNOTATORS = [f"ann{i:02d}" for i in range(1, 6)]


def parse_id(name: str) -> int:
    m = re.match(r"GS-(\d{4})__", name)
    if not m:
        return 10**9
    return int(m.group(1))


def main() -> None:
    files = sorted(DIR_GS.glob("GS-*.txt"), key=lambda p: parse_id(p.name))
    files = files[:TARGET_ITEM]
    if len(files) < TARGET_ITEM:
        print(f"Peringatan: hanya ada {len(files)} file GS, target {TARGET_ITEM}")

    rows = []
    for p in files:
        name = p.name
        parts = name.split("__")
        if len(parts) < 3:
            continue
        pid = parts[0]
        domain = parts[1]
        for ann in ANNOTATORS:
            rows.append(
                {
                    "annotator_id": ann,
                    "paragraph_id": pid,
                    "filename": name,
                    "domain": domain,
                    "batch": "full_200",
                    "status": "assigned",
                }
            )

    PATH_OUT.parent.mkdir(parents=True, exist_ok=True)
    with PATH_OUT.open("w", newline="", encoding="utf-8") as f:
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
        writer.writerows(rows)

    print("=== Generate Full Assignment ===")
    print(f"GS dipakai: {len(files)}")
    print(f"Baris assignment: {len(rows)}")
    print(f"Output: {PATH_OUT}")


if __name__ == "__main__":
    main()

