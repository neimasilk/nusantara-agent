# PROTOCOL: Eksperimen 01 — Ekstraksi Tripel Hukum Adat

**[RETROSPEKTIF]** — Protokol ini ditulis setelah eksekusi untuk tujuan dokumentasi. Pre-registration tidak dilakukan sebelum eksperimen ini dijalankan.

---

## Bagian 1: Pre-Registration (Retrospektif)

### 1.1 Metadata

| Field | Isi |
|-------|-----|
| **ID Eksperimen** | `01_triple_extraction` |
| **Peneliti** | AI Agent + Human Researcher |
| **Tanggal Eksekusi** | 2026-02-06 |
| **Tanggal Protokol (Retrospektif)** | 2026-02-06 |
| **Prasyarat** | Setup repository, DeepSeek API key |
| **Durasi Aktual** | ~30 menit |

### 1.2 Hipotesis (Retrospektif)

> **H0:** DeepSeek TIDAK mampu mengekstrak relasi hukum terstruktur dari teks naratif hukum adat Minangkabau dengan akurasi yang memadai untuk membangun Knowledge Graph.
>
> **H1:** DeepSeek mampu mengekstrak relasi hukum terstruktur (tripel) yang mencakup hierarki, otoritas, dan konflik norma dari teks naratif hukum adat Minangkabau.

### 1.3 Kriteria Penerimaan (Retrospektif)

| Metrik | Threshold | Catatan |
|--------|-----------|---------|
| Tripel diekstrak | > 0 | Minimal model menghasilkan output terstruktur |
| Format JSON valid | 100% | Output harus parseable |
| Kategori terdeteksi | >= 3 dari 4 | kepemilikan, pewarisan, otoritas, larangan |
| Konflik terdeteksi | >= 1 | Harus mendeteksi konflik adat vs nasional |

**CATATAN:** Kriteria ini ditentukan retrospektif. Tidak ada pre-registration yang dilakukan. Ini adalah kelemahan metodologi yang diakui.

### 1.4 Desain Eksperimen

- **Independent Variable:** Prompt engineering (system prompt dengan instruksi triple extraction)
- **Dependent Variable:** Kualitas dan kuantitas tripel yang diekstrak
- **Control/Baseline:** Tidak ada baseline — ini adalah pilot test
- **Confounding Variables:** Kualitas teks sumber, model temperature (default), prompt wording

### 1.5 Data & Resources

- **Input Data:** `experiments/01_triple_extraction/source_text.txt` — 1 paragraf (~118 kata) tentang hukum waris adat Minangkabau
- **Expected Output:** `experiments/01_triple_extraction/result.json` — JSON dengan triples dan conflicts
- **API:** DeepSeek Chat (deepseek-chat), ~1 API call, ~500 tokens

---

## Bagian 2: Execution

### 2.1 Instruksi Step-by-Step

```bash
# Step 1: Aktivasi environment
python -m venv venv && venv\Scripts\activate

# Step 2: Set API key
# Pastikan .env berisi DEEPSEEK_API_KEY

# Step 3: Jalankan eksperimen dari project root
python experiments/01_triple_extraction/run_experiment.py

# Step 4: Verifikasi output
# Cek: experiments/01_triple_extraction/result.json
```

### 2.2 Deviasi dari Rencana

| Perubahan | Alasan | Dampak pada Validitas |
|-----------|--------|----------------------|
| Tidak ada pre-registration | Pilot test, belum ada framework SOP | Tinggi — bias konfirmasi tidak terkontrol |
| 1 teks saja | Proof of concept | Tinggi — N=1 tidak generalizable |

---

## Bagian 3: Post-Analysis (Retrospektif)

### 3.1 Hasil Kuantitatif

| Metrik | Threshold | Hasil Aktual | PASS/FAIL |
|--------|-----------|--------------|-----------|
| Tripel diekstrak | > 0 | ~30 tripel | PASS |
| Format JSON valid | 100% | 100% (parseable) | PASS |
| Kategori terdeteksi | >= 3 | 4/4 (semua kategori) | PASS |
| Konflik terdeteksi | >= 1 | 1 konflik terdeteksi | PASS |

### 3.2 Analisis Kegagalan

- **Confidence score overconfidence:** Semua tripel mendapat confidence 1.0 — model tidak bisa self-assess uncertainty. Ini menjadikan confidence score tidak berguna tanpa kalibrasi eksternal.
- **Object phrases terlalu panjang:** Beberapa objek tripel berbentuk frasa panjang, bukan entitas tunggal. Ini bisa menyulitkan graph construction.
- **Tidak ada ground truth:** Keberhasilan dinilai oleh mata — tidak ada annotator independen atau gold standard.

### 3.3 Hostile Reviewer Simulation

1. **Validitas internal:** "Bagaimana Anda tahu tripel ini benar? Siapa yang memvalidasi? Apakah ada inter-rater agreement?"
   - **Jawaban jujur:** Tidak ada validasi independen. Ini pilot test. Kelemahan ini diakui dan akan ditangani di Exp 06.

2. **Generalizability:** "N=1 teks dari satu domain. Bagaimana ini bisa mendukung klaim tentang hukum adat Indonesia?"
   - **Jawaban jujur:** Tidak bisa. Ini hanya proof of concept. Scaling diperlukan.

3. **Novelty:** "Apa bedanya ini dari memanggil GPT-4 API dengan prompt serupa?"
   - **Jawaban jujur:** Pada tahap ini, tidak ada perbedaan signifikan. Novelty akan datang dari integrasi symbolic reasoning dan multi-agent orchestration.

---

## Bagian 4: Review Gate (Retrospektif)

- [x] ~~Pre-registration diisi SEBELUM eksekusi~~ — **TIDAK DILAKUKAN** (retrospektif)
- [x] Format output valid
- [x] Analisis kegagalan terisi
- [x] Hostile reviewer simulation dijawab
- [x] Dicatat di failure registry (F-001, F-002, F-004)
- [ ] 10 pertanyaan review protocol — lihat REVIEW.md
- [x] Kode bisa direproduksi
- [x] Data output di-commit

**Keputusan:** CONDITIONAL PASS (sebagai pilot, tapi tidak publishable tanpa scaling dan validasi independen)

**Reviewer:** Framework SOP (retrospektif)  **Tanggal:** 2026-02-06
