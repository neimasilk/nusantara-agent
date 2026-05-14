import json
import os
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class TripleEvaluator:
    """Independent evaluator for assessing Knowledge Graph triple quality using a non-DeepSeek LLM."""
    
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
            raise ValueError(f"Provider {provider} is not supported.")

    def evaluate_triples(self, source_text: str, extracted_triples: List[Dict], gold_triples: List[Dict]) -> Dict:
        """Compare AI-extracted triples against the gold standard."""

        system_prompt = (
            "You are an expert in Indonesian adat law and a Knowledge Engineer. "
            "Your task is to evaluate the quality of Knowledge Graph triples extracted by an AI "
            "against a human-curated Gold Standard."
        )

        user_prompt = f"""SOURCE TEXT:
{source_text}

GOLD STANDARD TRIPLES (Absolute Ground Truth):
{json.dumps(gold_triples, ensure_ascii=False, indent=2)}

EXTRACTED TRIPLES (AI Output):
{json.dumps(extracted_triples, ensure_ascii=False, indent=2)}

Task:
Compare the EXTRACTED TRIPLES against the GOLD STANDARD TRIPLES with reference to the SOURCE TEXT.
Assign a score from 0.0 to 1.0 for each of the following metrics:
1. Correctness: Are the extracted triples factually accurate relative to the gold standard?
2. Completeness: How much of the gold standard information was successfully captured by the AI?
3. Cultural Accuracy: Are the cultural terminology entries (head, relation, tail) used appropriately?

Output MUST be JSON:
{{
  "scores": {{
    "correctness": 0.0,
    "completeness": 0.0,
    "cultural_accuracy": 0.0
  }},
  "analysis": {{
    "matches": ["list of matching triples"],
    "misses": ["list of gold standard triples that were missed"],
    "hallucinations": ["list of extracted triples that are incorrect or absent from the source text"],
    "suggestions": "prompt improvement suggestions"
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
    # Simple test
    evaluator = TripleEvaluator(provider="openai", model="gpt-4o-mini")
    # Example usage can be added here
