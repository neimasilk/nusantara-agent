import json
import re

with open('data/processed/gold_standard/gs_active_cases.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)

domain_map = {}
for c in cases:
    cid = c['id']
    query = c['query'].lower()
    
    if "bali" in query:
        domain = "Bali"
    elif "minangkabau" in query or "pusako" in query:
        domain = "Minangkabau"
    elif "jawa" in query or "gono-gini" in query:
        domain = "Jawa"
    elif "kuhperdata" in query or "pasal" in query or "nasional" in query:
        domain = "Nasional"
    else:
        domain = "Other"
    
    # Specific ID overrides based on patterns
    if cid.startswith("CS-MIN-"): domain = "Minangkabau"
    elif cid.startswith("CS-BAL-"): domain = "Bali"
    elif cid.startswith("CS-JAW-"): domain = "Jawa"
    elif cid.startswith("CS-NAS-"): domain = "Nasional"
    elif cid.startswith("CS-LIN-"): domain = "Lintas"
    
    domain_map[cid] = domain

with open('experiments/09_ablation_study/case_id_domain_map.json', 'w', encoding='utf-8') as f:
    json.dump(domain_map, f, indent=2)

print(f"Mapped {len(domain_map)} cases.")
for d in set(domain_map.values()):
    count = list(domain_map.values()).count(d)
    print(f"- {d}: {count}")
