import argparse
import json
import os
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


ROOT = Path(__file__).resolve().parents[2]
DIR_ANNOT = ROOT / "data" / "processed" / "gold_standard" / "annotations"
DIR_TEXT = ROOT / "data" / "raw" / "gold_standard_texts"


def get_client(provider: str) -> OpenAI:
    if provider == "kimi":
        api_key = os.getenv("KIMI_API_KEY") or os.getenv("MOONSHOT_API_KEY")
        if not api_key:
            raise ValueError("KIMI_API_KEY/MOONSHOT_API_KEY tidak ditemukan di .env")
        return OpenAI(api_key=api_key, base_url="https://api.moonshot.ai/v1")
    if provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY tidak ditemukan di .env")
        return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY tidak ditemukan di .env")
        return OpenAI(api_key=api_key)
    raise ValueError("provider tidak dikenal. Pilih: kimi | deepseek | openai")


def default_model(provider: str) -> str:
    if provider == "kimi":
        return "kimi-k2-turbo-preview"
    if provider == "deepseek":
        return "deepseek-chat"
    return "gpt-4o-mini"


def read_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def generate_triples(
    client: OpenAI, model: str, domain: str, source_text: str, max_triples: int
) -> List[Dict]:
    system_prompt = (
        "Kamu adalah annotator KG hukum adat Indonesia. "
        "Ekstrak tripel faktual dari teks secara konservatif, tanpa menambah fakta di luar teks. "
        "Gunakan bahasa Indonesia."
    )
    user_prompt = (
        f"Domain: {domain}\n\n"
        f"Teks sumber:\n{source_text}\n\n"
        "Tugas:\n"
        f"1) Ekstrak maksimal {max_triples} tripel.\n"
        "2) Gunakan format field: head, relation, tail, category, confidence, notes.\n"
        "3) category wajib salah satu: Warisan, Tanah, Otoritas, Status, Prosedur, Lainnya.\n"
        "4) relation pakai snake_case.\n"
        "5) confidence harus 1.0 (format anotasi gold).\n\n"
        "Output WAJIB JSON object:\n"
        "{\n"
        '  "triples": [\n'
        "    {\n"
        '      "head": "...",\n'
        '      "relation": "...",\n'
        '      "tail": "...",\n'
        '      "category": "Warisan",\n'
        '      "confidence": 1.0,\n'
        '      "notes": "..." \n'
        "    }\n"
        "  ]\n"
        "}\n"
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    obj = json.loads(resp.choices[0].message.content)
    triples = obj.get("triples", [])
    if not isinstance(triples, list):
        return []
    clean = []
    for t in triples:
        if not isinstance(t, dict):
            continue
        clean.append(
            {
                "head": str(t.get("head", "")).strip(),
                "relation": str(t.get("relation", "")).strip(),
                "tail": str(t.get("tail", "")).strip(),
                "category": str(t.get("category", "Lainnya")).strip() or "Lainnya",
                "confidence": 1.0,
                "notes": str(t.get("notes", "")).strip(),
            }
        )
    return [t for t in clean if t["head"] and t["relation"] and t["tail"]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-fill anotasi stub dengan LLM")
    parser.add_argument("--provider", default="kimi", help="kimi | deepseek | openai")
    parser.add_argument("--model", default="", help="model override")
    parser.add_argument("--max-files", type=int, default=20, help="maks file yang diproses")
    parser.add_argument("--max-triples", type=int, default=8, help="maks triples per file")
    parser.add_argument("--force", action="store_true", help="timpa meski triples sudah ada")
    parser.add_argument("--filter-ann", default="", help="mis. ann01")
    parser.add_argument(
        "--refresh-from-marker",
        action="store_true",
        help="timpa hanya jika notes triple berisi marker AUTO_DOMAIN_FALLBACK/AUTO_REPLICA",
    )
    args = parser.parse_args()

    client = get_client(args.provider)
    model = args.model or default_model(args.provider)

    files = sorted(DIR_ANNOT.glob("GS-*.json"))
    if args.filter_ann:
        files = [p for p in files if p.stem.endswith(f"__{args.filter_ann}")]

    processed = 0
    skipped = 0
    failed = 0

    for path in files:
        if processed >= args.max_files:
            break
        try:
            obj = read_json(path)
            triples = obj.get("triples", [])
            needs_refresh = False
            if isinstance(triples, list) and triples:
                for t in triples:
                    if not isinstance(t, dict):
                        continue
                    notes = str(t.get("notes", ""))
                    if "AUTO_DOMAIN_FALLBACK" in notes or "AUTO_REPLICA" in notes:
                        needs_refresh = True
                        break

            if triples and not args.force:
                if args.refresh_from_marker and needs_refresh:
                    pass
                else:
                    skipped += 1
                    continue

            src_name = obj.get("metadata", {}).get("source_document", "")
            domain = obj.get("metadata", {}).get("domain", "umum")
            src_path = DIR_TEXT / src_name
            if not src_path.exists():
                failed += 1
                print(f"[FAIL] source text tidak ada untuk {path.name}: {src_name}")
                continue
            source_text = src_path.read_text(encoding="utf-8")
            new_triples = generate_triples(client, model, domain, source_text, args.max_triples)
            obj["triples"] = new_triples
            write_json(path, obj)
            processed += 1
            print(f"[OK] {path.name}: {len(new_triples)} triples")
        except Exception as e:
            failed += 1
            print(f"[FAIL] {path.name}: {e}")

    print("\n=== Ringkasan Auto-fill Anotasi ===")
    print(f"Provider/Model: {args.provider}/{model}")
    print(f"Processed: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
