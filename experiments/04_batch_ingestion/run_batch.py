import os
import json
import sys
from dotenv import load_dotenv

# Ensure src is in python path
sys.path.append(os.getcwd())

from src.kg_engine.extractor import TripleExtractor

load_dotenv()

def run_experiment_4():
    print("--- Eksperimen 4: Scalable Batch Ingestion ---")
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY not found in .env")
        return

    extractor = TripleExtractor(api_key)
    
    source_file = "experiments/01_triple_extraction/source_text.txt"
    if not os.path.exists(source_file):
        print(f"Error: Source file {source_file} not found")
        return

    with open(source_file, "r") as f:
        content = f.read()
    
    print(f"Memulai ekstraksi dari {source_file}...")
    triples = extractor.extract_from_text(content, domain="Minangkabau")
    
    output_file = "experiments/04_batch_ingestion/extracted_triples.jsonl"
    with open(output_file, "w") as f:
        for t in triples:
            f.write(json.dumps(t) + "\n")
            
    print(f"Selesai! {len(triples)} tripel berhasil disimpan di {output_file}")

if __name__ == "__main__":
    run_experiment_4()