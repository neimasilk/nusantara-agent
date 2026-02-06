import json
import os
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Tambahkan root ke sys.path untuk import src
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.symbolic.rule_engine import ClingoRuleEngine

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

def query_llm(scenario):
    if not api_key:
        return "API Key not found"
    
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    system_prompt = "Kamu adalah ahli hukum pluralistik Indonesia (Hukum Nasional & Adat Minangkabau). Jawablah pertanyaan hukum berikut dengan ringkas dan tepat. Tentukan apakah warisan diperbolehkan, dilarang, atau ada konflik."
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": scenario}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def evaluate_llm_answer(answer, expected):
    answer = answer.lower()
    if expected == "deny_inheritance":
        # Mencari indikasi penolakan
        keywords = ["tidak berhak", "tidak boleh", "dilarang", "bukan ahli waris", "tidak mewarisi"]
        return any(k in answer for k in keywords)
    elif expected == "allow_inheritance":
        # Mencari indikasi izin
        keywords = ["berhak", "boleh", "mewarisi", "dapat menerima"]
        return any(k in answer for k in keywords)
    elif expected == "conflict_detected" or expected == "punah_detected":
        keywords = ["konflik", "sengketa", "punah", "perdebatan", "masalah"]
        return any(k in answer for k in keywords)
    return False

def run_experiment():
    print("=== Eksperimen 05: Formal Rule Engine vs LLM Comparison ===")
    
    # Path setup
    lp_path = "src/symbolic/rules/minangkabau.lp"
    test_cases_path = "experiments/05_rule_engine/test_cases.json"
    
    if not Path(lp_path).exists():
        print(f"Error: {lp_path} tidak ditemukan.")
        return

    with open(test_cases_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []
    
    for tc in test_cases:
        print(f"\nRunning {tc['id']}: {tc['scenario'][:60]}...")
        
        # 1. Rule Engine Execution
        engine = ClingoRuleEngine(lp_path)
        facts = tc.get("fact_check", {})
        if "person" in facts and "gender" in facts:
            engine.add_fact(f"{facts['gender']}({facts['person'].lower()})")
        if "relationships" in facts:
            for rel in facts["relationships"]:
                if rel != "not_female_exists":
                    engine.add_fact(rel)
        if "action" in facts:
            engine.add_fact(f"action({facts['asset']}, {facts['action']})")
        if facts.get("consensus") is True:
            engine.add_fact("consensus_reached")

        models = engine.solve()
        expected = tc["expected_symbolic_result"]
        person = facts.get("person", "").lower()
        asset = facts.get("asset", "").lower()

        actual_symbolic = "unknown"
        if expected == "deny_inheritance":
            can_inherit = any(f"can_inherit({person},{asset})" in atom for m in models for atom in m)
            actual_symbolic = "deny_inheritance" if not can_inherit else "allow_inheritance"
        elif expected == "allow_inheritance":
            can_inherit = any(f"can_inherit({person},{asset})" in atom for m in models for atom in m)
            actual_symbolic = "allow_inheritance" if can_inherit else "deny_inheritance"
        elif expected == "conflict_detected":
            action = facts.get("action", "").lower()
            conflict = any(f"conflict({asset},{action})" in atom for m in models for atom in m)
            actual_symbolic = "conflict_detected" if conflict else "no_conflict"
        elif expected == "punah_detected":
            punah = any(f"punah({asset})" in atom for m in models for atom in m)
            actual_symbolic = "punah_detected" if punah else "not_punah"

        # 2. LLM Execution
        print("  Querying LLM...")
        llm_response = query_llm(tc["scenario"])
        llm_success = evaluate_llm_answer(llm_response, expected)
        
        symbolic_success = (actual_symbolic == expected)
        
        print(f"  Symbolic: {actual_symbolic} ({'PASS' if symbolic_success else 'FAIL'})")
        print(f"  LLM:      {'PASS' if llm_success else 'FAIL'}")
        
        results.append({
            "id": tc["id"],
            "scenario": tc["scenario"],
            "expected": expected,
            "symbolic": {
                "actual": actual_symbolic,
                "success": symbolic_success
            },
            "llm": {
                "response": llm_response,
                "success": llm_success
            },
            "divergence": (symbolic_success != llm_success)
        })

    # Summary
    sym_passed = sum(1 for r in results if r["symbolic"]["success"])
    llm_passed = sum(1 for r in results if r["llm"]["success"])
    divergences = sum(1 for r in results if r["divergence"])
    total = len(results)
    
    print(f"\n=== Ringkasan Eksperimen ===")
    print(f"Total Cases:     {total}")
    print(f"Symbolic Passed: {sym_passed}/{total} ({sym_passed/total*100:.1f}%)")
    print(f"LLM Passed:      {llm_passed}/{total} ({llm_passed/total*100:.1f}%)")
    print(f"Divergences:     {divergences} cases where they differ")
    
    # Save results
    output_path = "experiments/05_rule_engine/result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nHasil lengkap disimpan di {output_path}")

if __name__ == "__main__":
    run_experiment()
