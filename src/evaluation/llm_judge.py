import json
import os
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class TripleEvaluator:
    """Evaluator independen untuk menilai kualitas triple KG menggunakan LLM non-DeepSeek."""
    
    def __init__(self, provider: str = "openai", model: str = "gpt-4o"):
        self.provider = provider
        self.model = model
        self.client = self._get_client(provider)

    def _get_client(self, provider: str) -> OpenAI:
        if provider == "openai":
            return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif provider == "anthropic":
            return OpenAI(api_key=os.getenv("ANTHROPIC_API_KEY"), base_url="https://api.anthropic.com")
        elif provider == "kimi":
            return OpenAI(api_key=os.getenv("KIMI_API_KEY") or os.getenv("MOONSHOT_API_KEY"), 
                          base_url="https://api.moonshot.ai/v1")
        else:
            raise ValueError(f"Provider {provider} tidak didukung.")

    def evaluate_triples(self, source_text: str, extracted_triples: List[Dict], gold_triples: List[Dict]) -> Dict:
        """Membandingkan triple hasil ekstraksi dengan gold standard."""
        
        system_prompt = (
            "Kamu adalah pakar hukum adat Indonesia dan Knowledge Engineer. "
            "Tugasmu mengevaluasi kualitas Knowledge Graph triples yang diekstrak oleh AI "
            "dibandingkan dengan Gold Standard yang dibuat manusia."
        )
        
        user_prompt = f"""TEKS SUMBER:
{source_text}

GOLD STANDARD TRIPLES (Kebenaran Mutlak):
{json.dumps(gold_triples, ensure_ascii=False, indent=2)}

EXTRACTED TRIPLES (Hasil AI):
{json.dumps(extracted_triples, ensure_ascii=False, indent=2)}

Tugas:
Bandingkan EXTRACTED TRIPLES dengan GOLD STANDARD TRIPLES berdasarkan TEKS SUMBER.
Berikan skor 0.0 - 1.0 untuk metrik berikut:
1. Correctness: Apakah triple yang diekstrak benar secara faktual sesuai gold standard?
2. Completeness: Berapa banyak informasi dari gold standard yang berhasil ditangkap oleh AI?
3. Cultural Accuracy: Apakah terminologi budaya (head, relation, tail) digunakan dengan tepat?

OUTPUT WAJIB JSON:
{{
  "scores": {{
    "correctness": 0.0,
    "completeness": 0.0,
    "cultural_accuracy": 0.0
  }},
  "analysis": {{
    "matches": ["list triple yang cocok"],
    "misses": ["list triple gold standard yang terlewat"],
    "hallucinations": ["list triple ekstraksi yang salah/tidak ada di teks"],
    "suggestions": "saran perbaikan prompt"
  }}
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    # Test simple
    evaluator = TripleEvaluator(provider="openai", model="gpt-4o-mini")
    # Contoh penggunaan bisa ditambahkan di sini
