import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def run_pilot_test():
    # Read source text
    with open("experiments/01_triple_extraction/source_text.txt", "r") as f:
        source_text = f.read()

    system_prompt = """Kamu adalah ahli hukum adat Indonesia dan knowledge engineer.
Tugasmu mengekstrak relasi terstruktur dari teks tentang hukum adat untuk membangun Knowledge Graph.

ATURAN:
1. Ekstrak relasi dalam format tripel: (Subjek, Predikat, Objek).
2. Gunakan bahasa Indonesia yang baku untuk relasi, tapi pertahankan istilah adat asli.
3. Kategorikan setiap tripel: 'kepemilikan', 'pewarisan', 'otoritas', atau 'larangan'.
4. Identifikasi potensi konflik norma jika ada.

FORMAT OUTPUT (JSON):
{
  "triples": [
    {"head": "...", "relation": "...", "tail": "...", "category": "...", "confidence": 0.0-1.0}
  ],
  "conflicts": [
    {"description": "...", "involved_entities": ["...", "..."]}
  ]
}"""

    print("Sending request to DeepSeek...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Ekstrak relasi dari teks berikut:\n\n{source_text}"}
        ],
        response_format={'type': 'json_object'}
    )

    result = response.choices[0].message.content
    
    # Save result
    with open("experiments/01_triple_extraction/result.json", "w") as f:
        f.write(result)
    
    print("Experiment completed. Result saved to experiments/01_triple_extraction/result.json")

if __name__ == "__main__":
    run_pilot_test()
