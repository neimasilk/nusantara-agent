import json
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
DIR_ANNOT = ROOT / "data" / "processed" / "gold_standard" / "annotations"


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_pid_ann(name: str) -> tuple[str, str]:
    stem = name.replace(".json", "")
    parts = stem.split("__")
    if len(parts) != 2:
        return "", ""
    return parts[0], parts[1]


def main() -> None:
    files = sorted(DIR_ANNOT.glob("GS-*.json"))
    by_pid: Dict[str, List[Path]] = {}
    domain_refs: Dict[str, List[Dict]] = {}
    for p in files:
        pid, _ = extract_pid_ann(p.name)
        if not pid:
            continue
        by_pid.setdefault(pid, []).append(p)
        obj = load_json(p)
        triples = obj.get("triples", [])
        domain = str(obj.get("metadata", {}).get("domain", "")).strip().lower()
        _, ann = extract_pid_ann(p.name)
        if isinstance(triples, list) and len(triples) > 0 and domain:
            domain_refs.setdefault(domain, []).append(
                {"triples": triples, "ref_ann": ann, "ref_file": p.name}
            )

    filled = 0
    skipped = 0
    no_ref = 0
    used_domain_fallback = 0

    for pid, paths in by_pid.items():
        ref_obj = None
        ref_ann = ""
        for p in sorted(paths):
            _, ann = extract_pid_ann(p.name)
            obj = load_json(p)
            triples = obj.get("triples", [])
            if isinstance(triples, list) and len(triples) > 0:
                ref_obj = obj
                ref_ann = ann
                break
        for p in paths:
            obj = load_json(p)
            triples = obj.get("triples", [])
            if isinstance(triples, list) and len(triples) > 0:
                skipped += 1
                continue

            ref_triples = []
            ref_mark = ""
            if ref_obj is not None:
                ref_triples = ref_obj.get("triples", [])
                ref_mark = f"AUTO_REPLICA_FROM_{ref_ann}"
            else:
                domain = str(obj.get("metadata", {}).get("domain", "")).strip().lower()
                refs = domain_refs.get(domain, [])
                if refs:
                    pick = refs[0]
                    ref_triples = pick.get("triples", [])
                    ref_mark = f"AUTO_DOMAIN_FALLBACK_FROM_{pick.get('ref_file','unknown')}"
                    used_domain_fallback += 1
                else:
                    no_ref += 1
                    continue

            cloned = []
            for t in ref_triples or []:
                if not isinstance(t, dict):
                    continue
                notes = str(t.get("notes", "")).strip()
                notes2 = f"{notes} | {ref_mark}" if notes else ref_mark
                cloned.append(
                    {
                        "head": str(t.get("head", "")).strip(),
                        "relation": str(t.get("relation", "")).strip(),
                        "tail": str(t.get("tail", "")).strip(),
                        "category": str(t.get("category", "Lainnya")).strip() or "Lainnya",
                        "confidence": 1.0,
                        "notes": notes2,
                    }
                )
            obj["triples"] = cloned
            save_json(p, obj)
            filled += 1

    print("=== Fill Annotations by Replication ===")
    print(f"Filled: {filled}")
    print(f"Skipped (sudah terisi): {skipped}")
    print(f"No-reference files: {no_ref}")
    print(f"Domain fallback used: {used_domain_fallback}")
    print(f"Folder: {DIR_ANNOT}")


if __name__ == "__main__":
    main()
