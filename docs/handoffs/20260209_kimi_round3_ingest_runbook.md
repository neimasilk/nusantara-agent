# Runbook Ingest: Ahli-4 Round 3 (Kasus Split & Kontroversial)

**Tanggal:** 2026-02-09  
**Versi:** 1.0  
**Tujuan:** Panduan cepat ingest data Ahli-4 untuk arbitrase kasus konflik

---

## 1. Prasyarat

Sebelum menjalankan ingest, pastikan:
- [ ] Paket interview Ahli-4 sudah terisi (`docs/human_only/artifacts/paket_interview_online_ahli4_split_round3_siap_print_2026-02-09.md`)
- [ ] Data sudah ditranskrip ke CSV (`data/processed/gold_standard/interview_online/interview_template_ahli4_round3.csv`)
- [ ] Semua kolom wajib terisi (id, label_ahli4, confidence_ahli4)

---

## 2. Mapping Kolom CSV

| Kolom CSV | Sumber dari Paket | Keterangan |
|-----------|-------------------|------------|
| `id` | ID Kasus | CS-XXX-NNN |
| `label_ahli4` | Label (A/B/C/D) | Keputusan final Ahli-4 |
| `confidence_ahli4` | Keyakinan | Tinggi/Sedang/Rendah |
| `rationale_ahli4` | Alasan arbitrase | Teks lengkap |
| `reference_1` | Referensi 1 | Sumber hukum/adat |
| `reference_2` | Referensi 2 | Sumber tambahan |
| `session_date` | Tanggal interview | Format: YYYY-MM-DD |
| `interviewer_name` | Nama pewawancara | Default: Tim Nusantara-Agent |
| `follow_up_needed` | Follow-up | Ya/Tidak |
| `follow_up_notes` | Klarifikasi yang diperlukan | Teks jika Ya |
| `mode` | Mode interview | online_interview (default) |
| `ingested_at_utc` | Timestamp | Auto-generate saat ingest |

---

## 3. Langkah Ingest

### Step 1: Validasi CSV
```bash
cd D:\documents\nusantara-agent

# Cek CSV valid
python -c "
import csv
with open('data/processed/gold_standard/interview_online/interview_template_ahli4_round3.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f'Total kasus: {len(rows)}')
    for row in rows:
        print(f\"  {row['id']}: label={row['label_ahli4'] or 'EMPTY'}, conf={row['confidence_ahli4'] or 'EMPTY'}\")
"
```

### Step 2: Ingest Mode Aman (Default)
```bash
python scripts/ingest_expert_interview_votes.py \
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4_round3.csv \
  --expert-id ahli4
```

**Output:**
- File baru: `data/processed/gold_standard/gs_active_cases.post_ahli4.json`
- Log: `logs/ingest_ahli4_YYYYMMDD_HHMMSS.log`

### Step 3: Verifikasi Output
```bash
# Cek hasil ingest
python -c "
import json
with open('data/processed/gold_standard/gs_active_cases.post_ahli4.json') as f:
    cases = json.load(f)
    
split_resolved = 0
for c in cases:
    if c.get('consensus') == 'unanimous':
        split_resolved += 1
        
print(f'Kasus dengan konsensus unanimous: {split_resolved}')
print(f'Kasus masih split: {len(cases) - split_resolved}')
"
```

### Step 4: Ingest Final (Setelah Review)
```bash
# Hanya jalankan jika Step 3 valid
python scripts/ingest_expert_interview_votes.py \
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4_round3.csv \
  --expert-id ahli4 \
  --in-place
```

---

## 4. Post-Ingest Checklist

```
□ Dataset aktif terupdate (gs_active_cases.json)
□ Backup dataset lama tersimpan (gs_active_cases.pre_ahli4.json)
□ Manifest direbuild:
  python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-09

□ Manifest divalidasi:
  python scripts/validate_benchmark_manifest.py

□ Git commit dengan pesan:
  git add data/processed/gold_standard/
  git add docs/handoffs/
  git commit -m "data: ingest interview ahli4 round 3 - split resolution (YYYY-MM-DD)"

□ Update task_registry.md (jika terkait ART)
```

---

## 5. Kasus Split yang Diharapkan Ter-resolve

| ID Kasus | Status Awal | Target Status |
|----------|-------------|---------------|
| CS-MIN-005 | SPLIT (A vs B vs C) | Resolved (unanimous/majority) |
| CS-MIN-015 | SPLIT (A vs B vs C) | Resolved (unanimous/majority) |

---

## 6. Troubleshooting

### Error: Label tidak valid
**Gejala:** Script error "Invalid label: X"
**Solusi:** Pastikan label hanya A, B, C, atau D (huruf kapital)

### Error: ID kasus tidak ditemukan
**Gejala:** Script error "Case ID not found"
**Solusi:** Cek ID di CSV cocok dengan ID di gs_active_cases.json

### Error: CSV encoding
**Gejala:** Unicode decode error
**Solusi:** Pastikan CSV tersimpan dalam UTF-8:
```bash
file data/processed/gold_standard/interview_online/interview_template_ahli4_round3.csv
# Harus menunjukkan: UTF-8 Unicode text
```

---

## 7. Referensi Cepat

| Dokumen | Lokasi | Fungsi |
|---------|--------|--------|
| Paket Ahli-4 (ini) | `docs/human_only/artifacts/paket_interview_online_ahli4_split_round3_siap_print_2026-02-09.md` | Template interview |
| CSV Template | `data/processed/gold_standard/interview_online/interview_template_ahli4_round3.csv` | Data untuk ingest |
| Workflow Interview | `docs/human_only/workflow/interview_online_workflow.md` | Panduan lengkap |
| Operator Sheet | `docs/human_only/workflow/operator_transkrip_interview_ke_csv.md` | Mapping kertas ke CSV |
| Dataset Post-Ahli3 | `data/processed/gold_standard/gs_active_cases.post_ahli3.json` | Baseline sebelum Ahli-4 |

---

**Next Step Setelah Ingest:** Update consensus report dan lanjut ke ART-095 (draft kasus baru) jika target 200 kasus belum tercapai.
