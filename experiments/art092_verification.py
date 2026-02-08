import json
import os
import sys
from typing import Dict, List

# Tambahkan root ke sys.path untuk import src
sys.path.append(os.getcwd())

from src.pipeline.nusantara_agent import NusantaraAgentPipeline
from src.agents.router import _json_or_raw

def extract_label_from_agent(agent_analysis: str) -> str:
    """Mengekstrak label A/B/C/D dari output JSON supervisor agent."""
    try:
        data = _json_or_raw(agent_analysis)
        label = str(data.get("label", "D")).upper().strip()
        return label if label in ["A", "B", "C", "D"] else "D"
    except:
        return "D"

def run_verification():
    cases = [
        {
            "id": "CS-MIN-011",
            "query": "Seorang anggota kaum di Minangkabau mengonversi tanah ulayat kaum menjadi Sertifikat Hak Milik (SHM) atas nama pribadi tanpa melalui musyawarah mufakat kaum dan tanpa persetujuan Kerapatan Adat Nagari (KAN).",
            "gold_label": "C",
            "desc": "Label C Detection (Critical)"
        },
        {
            "id": "CS-NAS-066",
            "query": "Sebuah desa adat memberikan sanksi pengucilan (kasepekang) kepada satu keluarga karena pelanggaran norma adat. Dampaknya, anak-anak dari keluarga tersebut dilarang bersekolah di sekolah desa setempat dan dilarang mendapatkan layanan kesehatan di puskesmas pembantu desa.",
            "gold_label": "A",
            "desc": "HAM Violation -> National Law (Critical)"
        },
        {
            "id": "CS-BAL-002",
            "query": "Seorang anak perempuan tunggal di Bali mengklaim hak waris atas harta peninggalan ayahnya (harta purusa). Keluarga besar menolak dengan alasan hukum adat Bali menganut sistem patrilineal murni, padahal sudah ada Keputusan MDP 2010.",
            "gold_label": "C",
            "desc": "Adat vs MDP Conflict (Critical)"
        },
        {
            "id": "CS-MIN-004",
            "query": "Sepasang suami istri di Minangkabau memiliki harta dari hasil usaha bersama (pencaharian). Suami meninggal tanpa meninggalkan wasiat/hibah tertulis. Kemenakan suami mengklaim harta tersebut harus kembali ke kaum sebagai harta pusaka, sementara anak kandung mengklaim harta tersebut milik mereka.",
            "gold_label": "B",
            "desc": "Pure Adat / Internal Dispute (False Positive Check)"
        },
        {
            "id": "CS-JAW-006",
            "query": "Dalam sebuah pernikahan poligami yang sah di Jawa, terjadi perceraian dengan istri kedua. Terjadi sengketa pembagian harta yang diperoleh selama masa pernikahan kedua tersebut.",
            "gold_label": "A",
            "desc": "National Law Dominance (False Positive Check)"
        }
    ]

    pipeline = NusantaraAgentPipeline()
    results = []
    correct = 0
    total = len(cases)

    print(f"Starting ART-092 Verification on {total} critical cases...")
    print("="*60)

    for entry in cases:
        print(f"[{entry['id']}] {entry['desc']}")
        print(f"Query: {entry['query'][:80]}...")
        
        # 1. Jalankan Pipeline
        ai_output = pipeline.process_query(entry["query"])
        
        # 2. Cek Route Label (Intermediate Check)
        route_label = ai_output.get("route", {}).get("label", "unknown")
        print(f"Router Label: {route_label}")

        # 3. Extract Label langsung dari Agent Synthesis
        agent_analysis = ai_output.get("agent_analysis", "")
        predicted = extract_label_from_agent(agent_analysis)
        
        gold = entry["gold_label"]
        match = (predicted == gold)
        if match:
            correct += 1
        
        print(f"Result: Gold={gold} | Pred={predicted} | Match={'✅' if match else '❌'}")
        
        # Optional: Print reasoning snippet
        try:
            analysis_json = _json_or_raw(agent_analysis)
            reason = analysis_json.get("alasan_utama", "No reason provided")
            print(f"Reason: {reason[:100]}...")
        except:
            print("Reason: Could not parse JSON")
            
        print("-" * 60)
        
        results.append({
            "id": entry["id"],
            "match": match,
            "predicted": predicted,
            "gold": gold
        })

    accuracy = correct / total
    print(f"\nVerification Complete. Accuracy: {accuracy:.2%}")
    
    if accuracy >= 0.75:
        print("SUCCESS: Target accuracy >= 75% achieved.")
    else:
        print("WARNING: Target accuracy not met.")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        import traceback
        traceback.print_exc()

