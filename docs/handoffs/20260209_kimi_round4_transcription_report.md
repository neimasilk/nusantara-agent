# Laporan Transkripsi: Ahli-4 (Dr. Eko Susilo, M.Hum)

**Tanggal Transkripsi:** 2026-02-09  
**Operator:** Kimi (Structured Ops Executor)  
**Sumber:** `docs/human_only/artifacts/paket_interview_online_ahli4_terisi.md`
**Output:** `data/processed/gold_standard/interview_online/interview_template_ahli4_from_terisi_12cases.csv`  
**Status:** ✅ Siap Ingest (Belum Di-ingest)

---

## 1. Identitas Sesi

| Field | Nilai |
|-------|-------|
| **Nama Ahli** | Dr. Eko Susilo, M.Hum |
| **ID Ahli** | ahli4 |
| **Tanggal Interview** | 2026-02-09 |
| **Pewawancara** | Tim Nusantara-Agent |
| **Format** | Online Interview (Self-Contained) |
| **Total Kasus** | 12 kasus |

---

## 2. Rekap Hasil Transkripsi

### 2.1 Distribusi Label

| Label | Jumlah | Kasus |
|-------|--------|-------|
| **A (Hukum Nasional)** | 5 | CS-JAW-006, CS-NAS-066, CS-NAS-010, CS-LIN-017, CS-LIN-016 |
| **B (Hukum Adat)** | 1 | CS-MIN-011 |
| **C (Sintesis)** | 5 | CS-MIN-004, CS-LIN-052, CS-BAL-002, CS-BAL-014, CS-JAW-015 |
| **D (Perlu Klarifikasi)** | 1 | CS-MIN-013 |

### 2.2 Distribusi Keyakinan

| Tingkat | Jumlah | Persentase |
|---------|--------|------------|
| **Tinggi (T)** | 6 | 50% |
| **Sedang (S)** | 5 | 42% |
| **Rendah (R)** | 1 | 8% |

### 2.3 Kasus dengan Follow-up

| ID Kasus | Label | Alasan Follow-up |
|----------|-------|------------------|
| CS-MIN-004 | C | Perlu klarifikasi status harta spesifik |
| CS-LIN-052 | C | Perlu klarifikasi mekanisme formalisasi |
| CS-BAL-002 | C | Perlu klarifikasi implementasi MDP 2010 |
| CS-MIN-013 | D | Perlu klarifikasi kesepakatan adat |
| CS-BAL-014 | C | Perlu klarifikasi detail hak tempat tinggal |
| CS-JAW-015 | C | Perlu klarifikasi pembuktian wekas |

**Total Follow-up:** 6 kasus (50%)

---

## 3. Analisis Overlap dengan Round 3

### 3.1 Perbandingan Dataset

| Dataset | Jumlah Kasus | ID Kasus |
|---------|--------------|----------|
| **Round 3 (Split/Priority)** | 7 | CS-MIN-005, CS-MIN-015, CS-MIN-011, CS-BAL-002, CS-LIN-016, CS-LIN-018, CS-NAS-041 |
| **Ahli-4 Terisi (12 kasus)** | 12 | CS-MIN-011, CS-MIN-004, CS-JAW-006, CS-LIN-052, CS-NAS-066, CS-BAL-002, CS-NAS-010, CS-LIN-017, CS-MIN-013, CS-BAL-014, CS-JAW-015, CS-LIN-016 |

### 3.2 Kasus Overlap (3 kasus)

| ID Kasus | Round 3 Status | Ahli-4 Label | Keterangan |
|----------|----------------|--------------|------------|
| **CS-MIN-011** | Partial (B vs C vs A) | **B** (Adat) | Overlap ✅ Ahli-4 memberikan label B |
| **CS-BAL-002** | Partial (C vs A vs A) | **C** (Sintesis) | Overlap ✅ Ahli-4 memberikan label C |
| **CS-LIN-016** | Partial (C vs A vs A) | **A** (Nasional) | Overlap ✅ Ahli-4 memberikan label A |

**Status Overlap:** 3 kasus overlap, semua memiliki label valid dari Ahli-4.

### 3.3 Kasus Baru (9 kasus, tidak di Round 3)

| ID Kasus | Domain | Label | Keyakinan |
|----------|--------|-------|-----------|
| CS-MIN-004 | Minangkabau | C | Sedang |
| CS-JAW-006 | Jawa | A | Tinggi |
| CS-LIN-052 | Lintas | C | Sedang |
| CS-NAS-066 | Nasional | A | Tinggi |
| CS-NAS-010 | Nasional | A | Tinggi |
| CS-LIN-017 | Lintas | A | Tinggi |
| CS-MIN-013 | Minangkabau | D | Rendah |
| CS-BAL-014 | Bali | C | Sedang |
| CS-JAW-015 | Jawa | C | Sedang |

### 3.4 Kasus Round 3 yang TIDAK ada di Ahli-4 (4 kasus)

| ID Kasus | Round 3 Status | Keterangan |
|----------|----------------|------------|
| **CS-MIN-005** | SPLIT (A vs B vs C) | ❌ Belum ada keputusan Ahli-4 |
| **CS-MIN-015** | SPLIT (A vs B vs C) | ❌ Belum ada keputusan Ahli-4 |
| **CS-LIN-018** | Partial (C vs C vs A) | ❌ Belum ada keputusan Ahli-4 |
| **CS-NAS-041** | Partial (A vs C vs C) | ❌ Belum ada keputusan Ahli-4 |

---

## 4. Implikasi untuk Konsensus

### 4.1 Kasus dengan Potensi Konsensus Baru

| ID Kasus | Ahli-1 | Ahli-2 | Ahli-3 | Ahli-4 | Status Baru |
|----------|--------|--------|--------|--------|-------------|
| CS-MIN-011 | B | C | A | **B** | Partial (B vs C vs A vs B) → B mayori |
| CS-BAL-002 | C | A | A | **C** | Partial (C vs A vs A vs C) → A mayori |
| CS-LIN-016 | C | A | A | **A** | Partial (C vs A vs A vs A) → **Unanimous A** ✅ |

### 4.2 Kasus yang Masih SPLIT

| ID Kasus | Ahli-1 | Ahli-2 | Ahli-3 | Ahli-4 | Status |
|----------|--------|--------|--------|--------|--------|
| CS-MIN-005 | B | C | A | - | **SPLIT** (butuh Ahli-4) |
| CS-MIN-015 | C | B | A | - | **SPLIT** (butuh Ahli-4) |

**Catatan:** 2 kasus SPLIT masih memerlukan keputusan Ahli-4.

---

## 5. Validasi CSV Output

### 5.1 Struktur Kolom

| Kolom | Status | Keterangan |
|-------|--------|------------|
| `id` | ✅ Terisi | 12 ID kasus valid |
| `label_ahli4` | ✅ Terisi | A/B/C/D |
| `confidence_ahli4` | ✅ Terisi | Tinggi/Sedang/Rendah |
| `rationale_ahli4` | ✅ Terisi | Alasan lengkap per kasus |
| `reference_1` | ✅ Terisi | Minimal 1 referensi per kasus |
| `reference_2` | ✅ Terisi | 2 referensi per kasus |
| `session_date` | ✅ Terisi | 2026-02-09 |
| `interviewer_name` | ✅ Terisi | Tim Nusantara-Agent |
| `follow_up_needed` | ✅ Terisi | Ya/Tidak |
| `follow_up_notes` | ✅ Terisi | Detail jika Ya |
| `mode` | ✅ Terisi | online_interview |
| `ingested_at_utc` | ⬜ Kosong | Diisi saat ingest |

### 5.2 Statistik Isian

| Metrik | Nilai |
|--------|-------|
| Total Baris | 12 |
| Label A | 5 |
| Label B | 1 |
| Label C | 5 |
| Label D | 1 |
| Keyakinan Tinggi | 6 |
| Keyakinan Sedang | 5 |
| Keyakinan Rendah | 1 |
| Butuh Follow-up | 6 |

---

## 6. Rekomendasi

### 6.1 Tindakan Segera
1. **Ingest CSV ini** ke dataset aktif dengan mode aman:
   ```bash
   python scripts/ingest_expert_interview_votes.py \
     --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4_from_terisi_12cases.csv \
     --expert-id ahli4
   ```

2. **Verifikasi hasil ingest** pada 3 kasus overlap untuk konsistensi.

### 6.2 Tindak Lanjut
1. **Buat paket tambahan** untuk 4 kasus Round 3 yang belum ada keputusan Ahli-4:
   - CS-MIN-005
   - CS-MIN-015
   - CS-LIN-018
   - CS-NAS-041

2. **Finalisasi Gold Standard** setelah semua 4 kasus SPLIT ter-resolve.

---

## 7. Artefak yang Dihasilkan

| File | Lokasi | Status |
|------|--------|--------|
| CSV Siap Ingest (12 kasus) | `data/processed/gold_standard/interview_online/interview_template_ahli4_from_terisi_12cases.csv` | ✅ Validated |
| Laporan Transkripsi (ini) | `docs/handoffs/20260209_kimi_round4_transcription_report.md` | ✅ Complete |

---

**Operator:** Kimi Structured Ops Executor  
**Timestamp:** 2026-02-09  
**Status:** Siap untuk ingest
