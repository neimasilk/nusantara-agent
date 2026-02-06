import os
import json
from openai import OpenAI
from src.utils.text_processor import chunk_text

class TripleExtractor:
    def __init__(self, api_key, model="deepseek-chat"):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.model = model

    def extract_from_text(self, text, domain="umum"):
        system_prompt = f"""Kamu adalah ahli hukum adat {domain} dan knowledge engineer.
Tugasmu mengekstrak relasi hukum dalam format JSON terstruktur untuk Knowledge Graph.
Format Output: {{"triples": [{{"head": "...", "relation": "...", "tail": "...", "category": "...", "confidence": 0.0-1.0}}]}}"""
        
        chunks = chunk_text(text)
        all_triples = []
        
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Ekstrak tripel dari teks berikut:\n\n{chunk}"}
                    ],
                    response_format={'type': 'json_object'}
                )
                res_json = json.loads(response.choices[0].message.content)
                all_triples.extend(res_json.get("triples", []))
            except Exception as e:
                print(f"Error in chunk {i+1}: {e}")
                
        return all_triples
