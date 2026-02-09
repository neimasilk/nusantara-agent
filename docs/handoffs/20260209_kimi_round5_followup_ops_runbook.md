# Runbook: Ingest Follow-up Ahli-4 (4 Kasus)

**Tanggal:** 2026-02-09 | **Versi:** 1.0 | **Operator:** Kimi

---

## A. PRE-CHECK (Sebelum Ingest)

```
□ CSV terisi lengkap: interview_template_ahli4_followup_4cases.csv
□ 4 kasus: CS-MIN-005, CS-MIN-015, CS-NAS-041, CS-LIN-018
□ Semua label valid (A/B/C/D)
□ Semua confidence terisi (Tinggi/Sedang/Rendah)
□ File encoding: UTF-8
□ Backup dataset aktif tersedia
```

**Validasi cepat:**
```bash
cd D:\documents\nusantara-agent
python -c "import csv; f=open('data/processed/gold_standard/interview_online/interview_template_ahli4_followup_4cases.csv'); r=list(csv.DictReader(f)); print(f'Baris: {len(r)}'); [print(f\"  {x['id']}: {x['label_ahli4'] or 'KOSONG'}\") for x in r]"
```

---

## B. INGEST SAFE MODE

```bash
python scripts/ingest_expert_interview_votes.py \
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4_followup_4cases.csv \
  --expert-id ahli4
```

**Output:** `gs_active_cases.post_ahli4.json`

---

## C. VERIFIKASI

```bash
# Cek status konsensus
python -c "
import json
with open('data/processed/gold_standard/gs_active_cases.post_ahli4.json') as f:
    cases = {c['id']: c for c in json.load(f)}
    
target = ['CS-MIN-005', 'CS-MIN-015', 'CS-NAS-041', 'CS-LIN-018']
for tid in target:
    c = cases.get(tid, {})
    votes = c.get('expert_votes', {})
    cons = c.get('consensus', 'N/A')
    print(f\"{tid}: {votes} -> {cons}\")
"
```

**Target:**
- CS-MIN-005: SPLIT → majority/unanimous
- CS-MIN-015: SPLIT → majority/unanimous  
- CS-NAS-041: partial → unanimous
- CS-LIN-018: partial → unanimous

---

## D. IN-PLACE + MANIFEST

**Hanya jika verifikasi lolos:**

```bash
# 1. Ingest final
python scripts/ingest_expert_interview_votes.py \
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4_followup_4cases.csv \
  --expert-id ahli4 --in-place

# 2. Rebuild manifest
python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-09

# 3. Validasi
python scripts/validate_benchmark_manifest.py
```

---

## E. CHECKLIST DOKUMENTASI PASCA-INGEST

```
□ Dataset aktif: gs_active_cases.json (updated)
□ Backup tersimpan: gs_active_cases.pre_ahli4_followup.json
□ Manifest: benchmark_manifest.json (rebuild sukses)
□ Validasi: benchmark_manifest.py (lulus)
□ Git commit: "data: ingest ahli4 follow-up 4 kasus (2026-02-09)"
□ Update: task_registry.md (ART-094 jika ada)
□ Arsip: Paket interview ke docs/archive/
□ Laporan: Buat summary perubahan konsensus
```

---

## F. RINGKASAN KASUS

| ID Kasus | Status Awal | Target | Kunci Keputusan |
|----------|-------------|--------|-----------------|
| CS-MIN-005 | SPLIT (A/B/C) | Resolved | Hibah pusako vs kemenakan |
| CS-MIN-015 | SPLIT (A/B/C) | Resolved | Sanksi inkes vs nikah KUA |
| CS-NAS-041 | Partial (A/C/C) | Unanimous | IUP vs FPIC masyarakat adat |
| CS-LIN-018 | Partial (C/C/A) | Unanimous | SHM sah vs klaim ulayat |

---

**ESTIMASI WAKTU:** 10 menit (pre-check sampai dokumentasi)
