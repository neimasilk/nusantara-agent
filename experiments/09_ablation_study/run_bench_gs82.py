import json
import os
import sys
from typing import Dict, List

# Tambahkan root ke sys.path untuk import src
sys.path.append(os.getcwd())

from src.pipeline.nusantara_agent import NusantaraAgentPipeline
from src.agents.router import _get_llm, _json_or_raw
from langchain_core.messages import SystemMessage

def extract_label_from_agent(agent_analysis: str) -> str:
    """Mengekstrak label A/B/C/D dari output JSON supervisor agent."""
    try:
        data = _json_or_raw(agent_analysis)
        label = str(data.get("label", "D")).upper().strip()
        return label if label in ["A", "B", "C", "D"] else "D"
    except:
        return "D"

def run_benchmark(gs_path: str):
    if not os.path.exists(gs_path):
        print(f"Error: {gs_path} not found.")
        return

    with open(gs_path, "r", encoding="utf-8") as f:
        gs_data = json.load(f)

    pipeline = NusantaraAgentPipeline()
    results = []
    correct = 0
    total = 0

    print(f"Starting Benchmark on {len(gs_data)} cases (AGENT INTEGRATED)...")

    for entry in gs_data:
        if entry["gold_label"] == "SPLIT":
            continue
        
        total += 1
        query = entry["query"]
        gold = entry["gold_label"]
        
        print(f"[{total}] Processing {entry['id']}...", end=" ", flush=True)
        
        # 1. Jalankan Pipeline (dengan Orchestrator)
        ai_output = pipeline.process_query(query)
        
        # 2. Extract Label langsung dari Agent Synthesis
        predicted = extract_label_from_agent(ai_output.get("agent_analysis", ""))
        
        match = (predicted == gold)
        if match:
            correct += 1
        
        results.append({
            "id": entry["id"],
            "gold": gold,
            "predicted": predicted,
            "match": match,
            "reasoning": ai_output.get("agent_analysis", "")
        })
        print(f"Gold: {gold} | Pred: {predicted} | {'OK' if match else 'FAIL'}")

    accuracy = correct / total if total > 0 else 0
    
    summary = {
        "total_evaluated": total,
        "correct": correct,
        "accuracy": accuracy,
        "results": results
    }
    
    output_path = "experiments/09_ablation_study/results_phase1.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*30)
    print(f"BENCHMARK COMPLETE")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Results saved to: {output_path}")
    print("="*30)

if __name__ == "__main__":
    run_benchmark("data/processed/gold_standard/gs_82_cases.json")