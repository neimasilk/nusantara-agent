"""
Adversarial Reviewer — Review otomatis menggunakan LLM independen.

Modul ini menggunakan LLM YANG BERBEDA dari DeepSeek untuk me-review
eksperimen, memecah circular evaluation pada level meta.

Penggunaan:
    python -m src.review.adversarial_reviewer experiments/01_triple_extraction/

LLM yang didukung (pilih salah satu, konfigurasi via environment variable):
    - ANTHROPIC_API_KEY → Claude (Recommended)
    - OPENAI_API_KEY   → GPT-4
    - REVIEW_LLM       → Override model name (default: auto-detect)
"""

import os
import sys
import json
import glob
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# --- Konfigurasi LLM ---

def _init_anthropic_client(api_key):
    """Inisialisasi client Anthropic (Claude)."""
    try:
        import anthropic
        return anthropic.Anthropic(api_key=api_key), "claude"
    except ImportError:
        print("WARNING: anthropic package not installed. Run: pip install anthropic")
        return None, None


def _init_openai_client(api_key):
    """Inisialisasi client OpenAI (GPT-4)."""
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key), "openai"
    except ImportError:
        print("WARNING: openai package not installed. Run: pip install openai")
        return None, None


def get_review_client():
    """
    Pilih LLM reviewer berdasarkan environment variables.
    Prioritas: ANTHROPIC_API_KEY > OPENAI_API_KEY
    PENTING: TIDAK menggunakan DEEPSEEK_API_KEY untuk menghindari circular evaluation.
    """
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if anthropic_key:
        client, provider = _init_anthropic_client(anthropic_key)
        if client:
            print(f"Reviewer LLM: Claude (Anthropic) — independent dari DeepSeek")
            return client, provider

    if openai_key:
        client, provider = _init_openai_client(openai_key)
        if client:
            print(f"Reviewer LLM: GPT-4 (OpenAI) — independent dari DeepSeek")
            return client, provider

    print("ERROR: Tidak ada API key untuk reviewer independen.")
    print("Set salah satu environment variable:")
    print("  ANTHROPIC_API_KEY=sk-ant-...")
    print("  OPENAI_API_KEY=sk-...")
    print("")
    print("PENTING: DEEPSEEK_API_KEY TIDAK digunakan untuk review")
    print("karena DeepSeek sudah digunakan untuk generate output.")
    print("Menggunakan model yang sama untuk generate dan evaluate")
    print("adalah circular evaluation.")
    return None, None


# --- Kumpulkan Artefak Eksperimen ---

def collect_experiment_artifacts(experiment_dir):
    """Kumpulkan semua file relevan dari direktori eksperimen."""
    experiment_path = Path(experiment_dir)
    artifacts = {}

    # File yang dicari (urutan prioritas)
    target_files = [
        "analysis.md",
        "PROTOCOL.md",
        "REVIEW.md",
        "*.py",
        "*.json",
        "*.jsonl",
        "*.txt",
    ]

    for pattern in target_files:
        for filepath in experiment_path.glob(pattern):
            if filepath.is_file():
                try:
                    content = filepath.read_text(encoding="utf-8")
                    # Batasi ukuran per file untuk context window
                    if len(content) > 5000:
                        content = content[:5000] + "\n\n[... TRUNCATED ...]"
                    artifacts[filepath.name] = content
                except Exception as e:
                    artifacts[filepath.name] = f"[Error reading file: {e}]"

    return artifacts


# --- Prompt Review ---

REVIEW_SYSTEM_PROMPT = """Kamu adalah reviewer jurnal Scopus Q1 yang sangat kritis dan berpengalaman.
Tugasmu: menemukan KELEMAHAN, bukan memuji. Kamu harus bersikap seperti Reviewer 2 yang terkenal
keras di jurnal top-tier (Information Fusion, Knowledge-Based Systems, Expert Systems with Applications).

ATURAN REVIEW:
1. Setiap kritik HARUS spesifik dan actionable (bukan "perlu perbaikan" tapi "metric X tidak valid karena Y")
2. Gunakan severity rating: CRITICAL (desk reject level), MAJOR (reject reason), MINOR (revision needed)
3. Jangan terjebak oleh bahasa yang terdengar akademis — evaluasi SUBSTANSI
4. Jika sesuatu diklaim "berhasil" tanpa metrik kuantitatif, itu CRITICAL issue
5. Jika evaluasi circular (model yang sama generate dan evaluate), itu CRITICAL issue
6. Jangan segan memberikan CRITICAL rating — lebih baik kita tahu sekarang daripada saat submission
7. Berikan minimal 5 kritik, idealnya 8-10
8. Untuk setiap kritik, sertakan: deskripsi masalah, severity, dan saran perbaikan konkret

FORMAT OUTPUT (JSON):
{
  "experiment_id": "...",
  "review_date": "...",
  "overall_assessment": "STRONG_REJECT / REJECT / WEAK_REJECT / BORDERLINE / WEAK_ACCEPT",
  "summary": "Ringkasan 2-3 kalimat",
  "critiques": [
    {
      "id": "C1",
      "severity": "CRITICAL / MAJOR / MINOR",
      "category": "methodology / evaluation / novelty / reproducibility / scale / claim",
      "issue": "Deskripsi masalah spesifik",
      "evidence": "Bukti dari artefak eksperimen",
      "suggestion": "Saran perbaikan konkret"
    }
  ],
  "strengths": ["..."],
  "questions_for_authors": ["..."]
}"""


def build_review_prompt(experiment_id, artifacts):
    """Bangun prompt review dari artefak eksperimen."""
    artifacts_text = ""
    for filename, content in artifacts.items():
        artifacts_text += f"\n\n--- FILE: {filename} ---\n{content}"

    return f"""Review eksperimen berikut untuk kelayakan publikasi di jurnal Scopus Q1.

EKSPERIMEN: {experiment_id}

ARTEFAK EKSPERIMEN:
{artifacts_text}

KONTEKS PROYEK:
- Proyek: Neuro-Symbolic Agentic GraphRAG untuk Penalaran Hukum Pluralistik Indonesia
- Target: Jurnal Scopus Q1 (Information Fusion, Knowledge-Based Systems)
- LLM yang digunakan untuk generate output: DeepSeek
- LLM yang melakukan review ini: BUKAN DeepSeek (independent review)

Berikan review dalam format JSON yang diminta. Jangan menahan diri — reviewer Q1 tidak menahan diri."""


# --- Eksekusi Review ---

def run_review_claude(client, experiment_id, artifacts):
    """Jalankan review menggunakan Claude."""
    prompt = build_review_prompt(experiment_id, artifacts)

    response = client.messages.create(
        model=os.getenv("REVIEW_LLM", "claude-sonnet-4-20250514"),
        max_tokens=4096,
        system=REVIEW_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


def run_review_openai(client, experiment_id, artifacts):
    """Jalankan review menggunakan GPT-4."""
    prompt = build_review_prompt(experiment_id, artifacts)

    response = client.chat.completions.create(
        model=os.getenv("REVIEW_LLM", "gpt-4"),
        max_tokens=4096,
        messages=[
            {"role": "system", "content": REVIEW_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content


def run_review(client, provider, experiment_id, artifacts):
    """Dispatch ke provider yang sesuai."""
    if provider == "claude":
        return run_review_claude(client, experiment_id, artifacts)
    elif provider == "openai":
        return run_review_openai(client, experiment_id, artifacts)
    else:
        raise ValueError(f"Provider tidak dikenal: {provider}")


# --- Parsing & Output ---

def parse_review_output(raw_output):
    """Parse JSON dari output LLM (handle markdown code blocks)."""
    text = raw_output.strip()

    # Handle markdown code blocks
    if "```json" in text:
        start = text.index("```json") + len("```json")
        end = text.index("```", start)
        text = text[start:end].strip()
    elif "```" in text:
        start = text.index("```") + len("```")
        end = text.index("```", start)
        text = text[start:end].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Jika parsing gagal, kembalikan sebagai teks
        return {
            "raw_output": raw_output,
            "parse_error": "Output LLM tidak valid JSON. Review tersedia sebagai teks mentah."
        }


def save_review(review_data, experiment_dir):
    """Simpan hasil review ke file."""
    output_path = Path(experiment_dir) / "ai_review.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)
    print(f"\nReview disimpan di: {output_path}")
    return output_path


def print_review_summary(review_data):
    """Cetak ringkasan review ke console."""
    print("\n" + "=" * 60)
    print("ADVERSARIAL REVIEW SUMMARY")
    print("=" * 60)

    if "parse_error" in review_data:
        print(f"\n[Warning] {review_data['parse_error']}")
        print(f"\nRaw output:\n{review_data.get('raw_output', 'N/A')[:500]}")
        return

    print(f"\nOverall: {review_data.get('overall_assessment', 'N/A')}")
    print(f"Summary: {review_data.get('summary', 'N/A')}")

    critiques = review_data.get("critiques", [])
    critical_count = sum(1 for c in critiques if c.get("severity") == "CRITICAL")
    major_count = sum(1 for c in critiques if c.get("severity") == "MAJOR")
    minor_count = sum(1 for c in critiques if c.get("severity") == "MINOR")

    print(f"\nCritiques: {len(critiques)} total")
    print(f"  CRITICAL: {critical_count}")
    print(f"  MAJOR:    {major_count}")
    print(f"  MINOR:    {minor_count}")

    if critical_count > 0:
        print("\n⚠ CRITICAL ISSUES:")
        for c in critiques:
            if c.get("severity") == "CRITICAL":
                print(f"  [{c.get('id', '?')}] {c.get('issue', 'N/A')}")

    strengths = review_data.get("strengths", [])
    if strengths:
        print(f"\nStrengths: {len(strengths)}")
        for s in strengths:
            print(f"  + {s}")

    print("\n" + "=" * 60)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Adversarial Reviewer — Review eksperimen menggunakan LLM independen"
    )
    parser.add_argument(
        "experiment_dir",
        help="Path ke direktori eksperimen (misal: experiments/01_triple_extraction/)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Tampilkan artefak yang akan di-review tanpa memanggil API"
    )
    args = parser.parse_args()

    experiment_dir = args.experiment_dir
    experiment_id = Path(experiment_dir).name

    print(f"Adversarial Review untuk: {experiment_id}")
    print(f"Direktori: {experiment_dir}")

    # Kumpulkan artefak
    artifacts = collect_experiment_artifacts(experiment_dir)
    if not artifacts:
        print(f"ERROR: Tidak ada artefak ditemukan di {experiment_dir}")
        sys.exit(1)

    print(f"\nArtefak ditemukan ({len(artifacts)} file):")
    for name in artifacts:
        print(f"  - {name}")

    if args.dry_run:
        print("\n[DRY RUN] Tidak memanggil API. Artefak di atas akan di-review.")
        sys.exit(0)

    # Inisialisasi client
    client, provider = get_review_client()
    if not client:
        sys.exit(1)

    # Jalankan review
    print(f"\nMemulai review...")
    raw_output = run_review(client, provider, experiment_id, artifacts)

    # Parse dan simpan
    review_data = parse_review_output(raw_output)
    review_data["reviewer_provider"] = provider
    review_data["review_timestamp"] = datetime.now().isoformat()

    save_review(review_data, experiment_dir)
    print_review_summary(review_data)


if __name__ == "__main__":
    main()
