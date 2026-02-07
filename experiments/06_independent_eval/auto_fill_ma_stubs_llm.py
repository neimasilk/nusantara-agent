import argparse
import csv
import json
import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


ROOT = Path(__file__).resolve().parents[2]
DIR_MA = ROOT / "data" / "raw" / "ma_decisions"
PATH_CAND = DIR_MA / "candidates_from_internal_outputs.csv"


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


def load_candidate_map() -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    if not PATH_CAND.exists():
        return out
    with PATH_CAND.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nomor = (row.get("nomor_perkara") or "").strip().upper()
            if nomor:
                out[nomor] = row
    return out


def enrich_substansi(client: OpenAI, model: str, nomor: str, context_text: str) -> Dict:
    system_prompt = (
        "Kamu asisten riset hukum. Ekstrak informasi secara konservatif dari konteks yang diberikan. "
        "Jika tidak ada bukti, isi string kosong."
    )
    user_prompt = (
        f"Nomor perkara: {nomor}\n\n"
        f"Konteks internal (bukan sumber primer):\n{context_text}\n\n"
        "Tugas:\n"
        "Isi draft field berikut TANPA overclaim. Jika tidak diketahui, isi kosong.\n"
        "Output WAJIB JSON object:\n"
        "{\n"
        '  "fakta_inti": "",\n'
        '  "isu_hukum": "",\n'
        '  "norma_nasional": [],\n'
        '  "norma_adat": [],\n'
        '  "ratio_decidendi": "",\n'
        '  "amar_putusan": "",\n'
        '  "catatan_keterbatasan": ""\n'
        "}\n"
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    obj = json.loads(resp.choices[0].message.content)
    return {
        "fakta_inti": str(obj.get("fakta_inti", "")).strip(),
        "isu_hukum": str(obj.get("isu_hukum", "")).strip(),
        "norma_nasional": obj.get("norma_nasional", []) if isinstance(obj.get("norma_nasional", []), list) else [],
        "norma_adat": obj.get("norma_adat", []) if isinstance(obj.get("norma_adat", []), list) else [],
        "ratio_decidendi": str(obj.get("ratio_decidendi", "")).strip(),
        "amar_putusan": str(obj.get("amar_putusan", "")).strip(),
        "catatan_keterbatasan": str(obj.get("catatan_keterbatasan", "")).strip(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-fill draft substansi putusan MA dari konteks internal")
    parser.add_argument("--provider", default="kimi", help="kimi | deepseek | openai")
    parser.add_argument("--model", default="", help="model override")
    parser.add_argument("--max-files", type=int, default=7, help="maks file putusan_*.json")
    parser.add_argument("--force", action="store_true", help="timpa substansi meski sudah berisi")
    args = parser.parse_args()

    client = get_client(args.provider)
    model = args.model or default_model(args.provider)
    cmap = load_candidate_map()

    files = sorted(DIR_MA.glob("putusan_*.json"))
    processed = 0
    skipped = 0
    failed = 0

    for path in files:
        if processed >= args.max_files:
            break
        try:
            obj = read_json(path)
            nomor = (obj.get("metadata", {}).get("nomor_perkara") or "").strip().upper()
            substansi = obj.get("substansi", {})
            has_content = any(
                str(substansi.get(k, "")).strip()
                for k in ["fakta_inti", "isu_hukum", "ratio_decidendi", "amar_putusan"]
            )
            if has_content and not args.force:
                skipped += 1
                continue

            row = cmap.get(nomor, {})
            src_rel = row.get("sumber_internal", "")
            context_text = ""
            if src_rel:
                src_path = ROOT / src_rel.replace("/", os.sep)
                if src_path.exists():
                    context_text = src_path.read_text(encoding="utf-8", errors="ignore")[:4000]

            if not context_text:
                context_text = "Tidak ada konteks internal yang memadai."

            new_sub = enrich_substansi(client, model, nomor or path.stem, context_text)
            obj.setdefault("metadata", {})
            obj["metadata"]["sumber_url"] = obj["metadata"].get("sumber_url") or "https://putusan.mahkamahagung.go.id/"
            obj["metadata"]["status_verifikasi"] = "draft"
            obj["substansi"] = new_sub
            if "provenance" in obj and isinstance(obj["provenance"], dict):
                obj["provenance"]["auto_fill_provider"] = args.provider
                obj["provenance"]["auto_fill_model"] = model
            write_json(path, obj)
            processed += 1
            print(f"[OK] {path.name}")
        except Exception as e:
            failed += 1
            print(f"[FAIL] {path.name}: {e}")

    print("\n=== Ringkasan Auto-fill Putusan ===")
    print(f"Provider/Model: {args.provider}/{model}")
    print(f"Processed: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()

