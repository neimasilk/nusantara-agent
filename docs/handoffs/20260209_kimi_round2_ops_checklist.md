# Handoff Ops: Checklist Ingest Ahli Domain (Kimi Round 2)

**Tanggal:** 2026-02-09  
**Versi:** 1.0  
**Tujuan:** Artefak operasional rapi pasca-ingest Ahli-1 untuk kelanjutan tim dan audit-readiness  

---

## A. Status Ingest Ahli-1

### A.1 Identitas Sesi
| Field | Nilai |
|-------|-------|
| Nama Ahli | Dr. Hendra Kusuma, S.H., M.Hum. |
| ID Ahli | ahli1 |
| Tanggal Sesi | 8 Februari 2026 |
| Durasi | 45 Menit (estimasi) |
| Pewawancara | Tim Teknis Nusantara-Agent |
| Format | Interview online (Paket Self-Contained) |

### A.2 Rekap Kasus
| Domain | Jumlah | Label A | Label B | Label C | Label D |
|--------|--------|---------|---------|---------|---------|
| Minangkabau | 3 | 1 | 2 | 0 | 0 |
| Jawa | 2 | 1 | 0 | 1 | 0 |
| Bali | 2 | 0 | 1 | 1 | 0 |
| Lintas | 3 | 2 | 0 | 1 | 1 |
| Nasional | 2 | 2 | 0 | 0 | 0 |
| **Total** | **12** | **6** | **3** | **3** | **1** |

### A.3 Status Per Kasus
| ID Kasus | Label | Keyakinan | Follow-up |
|----------|-------|-----------|-----------|
| CS-MIN-011 | B | Tinggi | Ya |
| CS-MIN-004 | A | Tinggi | Tidak |
| CS-JAW-006 | A | Tinggi | Tidak |
| CS-LIN-052 | D | Rendah | Ya |
| CS-NAS-066 | A | Tinggi | Tidak |
| CS-BAL-002 | C | Sedang | Ya |
| CS-NAS-010 | A | Tinggi | Tidak |
| CS-LIN-017 | A | Tinggi | Tidak |
| CS-MIN-013 | B | Sedang | Ya |
| CS-BAL-014 | B | Tinggi | Tidak |
| CS-JAW-015 | C | Sedang | Ya |
| CS-LIN-016 | C | Sedang | Ya |

### A.4 Deliverable Status
| Deliverable | Lokasi | Status |
|-------------|--------|--------|
| Paket Interview Terisi | `docs/human_only/artifacts/paket_interview_online_ahli1_terisi_2026-02-09.md` | ✅ Done |
| CSV Template | `data/processed/gold_standard/interview_online/interview_template_ahli1.csv` | ⏳ Pending Transkrip |
| Ingest ke Dataset | `data/processed/gold_standard/gs_active_cases.post_ahli1.json` | ⏳ Pending |
| Manifest Update | `data/benchmark_manifest.json` | ⏳ Pending |

### A.5 Item Follow-up Ahli-1 (6 Kasus)
- CS-MIN-011: Klarifikasi prosedur pelepasan hak ulayat
- CS-LIN-052: Butuh informasi status tanah (sudah dilepaskan/belum)
- CS-BAL-002: Mediasi hak perempuan vs purusa
- CS-MIN-013: Status ruko hasil transformasi aset
- CS-JAW-015: Implementasi pambageyan dengan rukun
- CS-LIN-016: Prosedur choice of law untuk HATAH internal

---

## B. Reusable Checklist (Ahli-2/Ahli-3/Ahli-4)

### B.1 Pre-Ingest (Sebelum Interview)

```
□ Generate template interview
  python scripts/export_split_cases_for_interview.py --expert-id ahli{N}

□ Verifikasi output di: data/processed/gold_standard/interview_online/

□ Konversi ke paket print (opsional untuk offline)
  cp data/processed/gold_standard/interview_online/interview_template_ahli{N}.csv \
     docs/human_only/artifacts/paket_interview_online_ahli{N}_siap_print.md

□ Siapkan kertas kerja atau dokumen PDF annotable

□ Kirim ke ahli (email/print) dengan instruksi pengisian
```

### B.2 Ingest (Proses Interview & Transkrip)

```
□ Jalankan interview atau terima dokumen terisi dari ahli

□ Verifikasi identitas ahli dan tanggal sesi

□ Transkrip hasil kertas/PDF ke CSV (acuan: docs/human_only/workflow/operator_transkrip_interview_ke_csv.md)
  - Kolom wajib: id, label_ahli{N}, confidence_ahli{N}, rationale_ahli{N}
  - Kolom opsional: reference_1, reference_2, session_date, interviewer_name

□ Validasi CSV sebelum ingest:
  - Semua id ada di dataset aktif
  - Semua label valid (A/B/C/D)
  - File tersimpan UTF-8
  - Tidak ada baris kosong

□ Jalankan ingest (mode aman):
  python scripts/ingest_expert_interview_votes.py \
    --input-csv data/processed/gold_standard/interview_online/interview_template_ahli{N}.csv \
    --expert-id ahli{N}

□ Verifikasi output .post_ahli{N}.json tanpa error
```

### B.3 Post-Ingest (Setelah Verifikasi)

```
□ Overwrite dataset aktif (jika sudah diverifikasi):
  python scripts/ingest_expert_interview_votes.py \
    --input-csv data/processed/gold_standard/interview_online/interview_template_ahli{N}.csv \
    --expert-id ahli{N} --in-place

□ Rebuild manifest:
  python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-09

□ Validasi manifest:
  python scripts/validate_benchmark_manifest.py

□ Validasi ketat (untuk audit):
  python scripts/validate_benchmark_manifest.py --require-reference-match

□ Buat laporan pasca-ingest (gunakan Template D di bawah)

□ Commit dan push ke git dengan pesan:
  "data: ingest interview ahli{N} (YYYY-MM-DD)"

□ Update task_registry.md jika terkait ART tertentu

□ Arsipkan paket interview terisi ke docs/archive/
```

### B.4 Checklist Kasus Split (Khusus Ahli-4)

```
□ Pastikan hanya kasus berstatus SPLIT yang di-assign
  (cek di gs_active_cases.json, field consensus_status: "SPLIT")

□ Siapkan paket dengan label Ahli-1, Ahli-2, Ahli-3 untuk perbandingan

□ Generate paket split:
  python scripts/export_split_cases_for_interview.py --expert-id ahli4

□ Siapkan lembar perbandingan 3 ahli sebelumnya

□ Jalankan interview dengan fokus arbitrase

□ Dokumentasi rationale keputusan Ahli-4 harus detail (alasan memilih A vs B vs C)
```

---

## C. Command Snippets

### C.1 Generate Template
```bash
# Default (kasus SPLIT)
python scripts/export_split_cases_for_interview.py --expert-id ahli2

# Semua kasus (jika ingin re-annotate)
python scripts/export_split_cases_for_interview.py --expert-id ahli2 --all-cases
```

### C.2 Ingest Mode Aman
```bash
python scripts/ingest_expert_interview_votes.py \
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli2.csv \
  --expert-id ahli2

# Output: gs_active_cases.post_ahli2.json
```

### C.3 Ingest Mode Overwrite
```bash
python scripts/ingest_expert_interview_votes.py \
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli2.csv \
  --expert-id ahli2 \
  --in-place
```

### C.4 Validasi Dataset
```bash
# Rebuild manifest
python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-09

# Validasi dasar
python scripts/validate_benchmark_manifest.py

# Validasi ketat (audit)
python scripts/validate_benchmark_manifest.py --require-reference-match
```

### C.5 Cek Status Kasus
```bash
# Lihat kasus SPLIT yang butuh Ahli-4
grep -n '"consensus_status": "SPLIT"' data/processed/gold_standard/gs_active_cases.json

# Hitung total kasus per status
python -c "
import json
with open('data/processed/gold_standard/gs_active_cases.json') as f:
    cases = json.load(f)
statuses = {}
for c in cases:
    s = c.get('consensus_status', 'UNKNOWN')
    statuses[s] = statuses.get(s, 0) + 1
for s, n in sorted(statuses.items()):
    print(f'{s}: {n}')
"
```

---

## D. Template Laporan Pasca-Ingest

```markdown
# Laporan Pasca-Ingest: Interview Ahli-{N}

**Tanggal Laporan:** YYYY-MM-DD  
**ID Ahli:** ahli{N}  
**Nama Ahli:** [Nama Lengkap]  
**Tanggal Interview:** YYYY-MM-DD  
**Pelaksana Ingest:** [Nama Operator]

---

## 1. Ringkasan

| Metrik | Nilai |
|--------|-------|
| Total Kasus Diberikan | X |
| Total Kasus Direspons | Y |
| Kasus dengan Label A | count |
| Kasus dengan Label B | count |
| Kasus dengan Label C | count |
| Kasus dengan Label D | count |
| Kasus Follow-up | count |

## 2. Daftar Kasus

| ID Kasus | Domain | Label | Keyakinan | Follow-up | Rationale Summary |
|----------|--------|-------|-----------|-----------|-------------------|
| CS-XXX-001 | [Domain] | [A/B/C/D] | [T/S/R] | [Ya/Tidak] | [1-2 kata kunci] |
| ... | ... | ... | ... | ... | ... |

## 3. Temuan Signifikan

### 3.1 Kasus Kontroversial / Split Potential
- [ID Kasus]: [Deskripsi mengapa berpotensi split dengan ahli lain]

### 3.2 Insight Ahli
- [Poin penting dari rationale yang berharga untuk metodologi]

### 3.3 Referensi Baru
- [Referensi hukum yang disebutkan ahli dan belum ada di dataset]

## 4. Status Konsensus

| Status | Jumlah Kasus | ID Kasus |
|--------|--------------|----------|
| CONSENSUS (3+ ahli setuju) | X | CS-XXX, CS-YYY |
| SPLIT (butuh arbitrase) | Y | CS-ZZZ |
| PARTIAL (2 vs 1) | Z | CS-WWW |

## 5. Tindakan Follow-up

| ID Kasus | Tindakan | PIC | Deadline |
|----------|----------|-----|----------|
| CS-XXX | [Deskripsi tindakan] | [Nama] | YYYY-MM-DD |

## 6. Artefak

| File | Lokasi | Status |
|------|--------|--------|
| Paket Interview Terisi | `docs/human_only/artifacts/paket_interview_online_ahli{N}_terisi_YYYY-MM-DD.md` | ✅ |
| CSV Transkrip | `data/processed/gold_standard/interview_online/interview_template_ahli{N}.csv` | ✅ |
| Dataset Post-Ingest | `data/processed/gold_standard/gs_active_cases.post_ahli{N}.json` | ✅ |
| Dataset Final | `data/processed/gold_standard/gs_active_cases.json` | ✅ |
| Manifest | `data/benchmark_manifest.json` | ✅ |

## 7. Validasi

- [ ] Semua label valid (A/B/C/D)
- [ ] Semua ID kasus ditemukan di dataset
- [ ] Manifest rebuild sukses
- [ ] Validasi manifest lulus
- [ ] Git commit tersimpan

---

**Catatan Audit:**
- Ingest dilakukan dengan script: `scripts/ingest_expert_interview_votes.py`
- Mode ingest: [SAFE / IN-PLACE]
- Timestamp ingest: YYYY-MM-DD HH:MM:SS
```

---

## E. Referensi Cepat

| Dokumen | Lokasi | Kegunaan |
|---------|--------|----------|
| Workflow Interview | `docs/human_only/workflow/interview_online_workflow.md` | Panduan end-to-end |
| Operator Transkrip | `docs/human_only/workflow/operator_transkrip_interview_ke_csv.md` | Mapping kertas ke CSV |
| Paket Master Print | `docs/human_only/artifacts/paket_print_interview_master_2026-02-08.md` | Template generik |
| Paket Ahli-4 Split | `docs/human_only/artifacts/paket_interview_online_ahli4_split_siap_print_2026-02-08.md` | Arbitrase kasus split |
| Task Registry | `docs/task_registry.md` | Status ART terkait |

---

**Status Handoff:** Siap digunakan untuk Ahli-2, Ahli-3, Ahli-4  
**Next Action:** Transkrip Ahli-1 ke CSV dan jalankan ingest pertama  
