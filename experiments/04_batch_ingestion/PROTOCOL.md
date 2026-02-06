# PROTOCOL: Eksperimen 04 — Scalable Batch Ingestion

**[RETROSPEKTIF]** — Protokol ini ditulis setelah eksekusi untuk tujuan dokumentasi.

---

## Bagian 1: Pre-Registration (Retrospektif)

### 1.1 Metadata

| Field | Isi |
|-------|-----|
| **ID Eksperimen** | `04_batch_ingestion` |
| **Peneliti** | AI Agent + Human Researcher |
| **Tanggal Eksekusi** | 2026-02-06 |
| **Tanggal Protokol (Retrospektif)** | 2026-02-06 |
| **Prasyarat** | src/kg_engine/extractor.py, src/utils/text_processor.py, DeepSeek API key |
| **Durasi Aktual** | ~45 menit (termasuk debugging SyntaxErrors) |

### 1.2 Hipotesis (Retrospektif)

> **H0:** Pipeline ingesti modular (menggunakan TripleExtractor dari src/) TIDAK bisa memproses teks secara batch dan menghasilkan output JSONL yang valid.
>
> **H1:** Pipeline ingesti modular mampu memproses teks dalam chunks, mengekstrak tripel dari setiap chunk, dan menyimpan hasilnya dalam format JSONL yang siap untuk skala besar.

### 1.3 Kriteria Penerimaan (Retrospektif)

| Metrik | Threshold | Catatan |
|--------|-----------|---------|
| Script berjalan | Tanpa error (setelah debugging) | Import modular dari src/ |
| Output JSONL valid | Setiap baris parseable JSON | Format standar |
| Tripel diekstrak | > 0 | Dari source text |
| Modular imports | Menggunakan src/ modules | Bukan inline code |

### 1.4 Desain Eksperimen

- **Independent Variable:** Penggunaan modular TripleExtractor vs inline extraction
- **Dependent Variable:** Keberhasilan batch processing dan output format
- **Control/Baseline:** Exp 01 (inline extraction) sebagai comparison point
- **Confounding Variables:** Chunk size, API reliability, network latency

### 1.5 Data & Resources

- **Input Data:** `experiments/01_triple_extraction/source_text.txt` (sama dengan Exp 01)
- **Expected Output:** `experiments/04_batch_ingestion/extracted_triples.jsonl`
- **API:** DeepSeek Chat, jumlah calls = jumlah chunks

---

## Bagian 2: Execution

### 2.1 Instruksi Step-by-Step

```bash
# Step 1: Pastikan virtual environment aktif
# Step 2: Pastikan .env berisi DEEPSEEK_API_KEY

# Step 3: Jalankan dari project root (PENTING untuk sys.path)
python experiments/04_batch_ingestion/run_batch.py

# Step 4: Verifikasi output
# Cek: experiments/04_batch_ingestion/extracted_triples.jsonl
# Setiap baris harus valid JSON

# Step 5: Validasi JSONL
python -c "import json; [json.loads(l) for l in open('experiments/04_batch_ingestion/extracted_triples.jsonl')]"
```

### 2.2 Deviasi dari Rencana

| Perubahan | Alasan | Dampak pada Validitas |
|-----------|--------|----------------------|
| Multiple SyntaxError iterations | AI code generation issues | Rendah — fixed sebelum run final |
| Input sama dengan Exp 01 | Simplicity — fokus pada pipeline, bukan data baru | Sedang — tidak menguji data baru |

---

## Bagian 3: Post-Analysis (Retrospektif)

### 3.1 Hasil Kuantitatif

| Metrik | Threshold | Hasil Aktual | PASS/FAIL |
|--------|-----------|--------------|-----------|
| Script berjalan | Tanpa error | Berjalan setelah debug | PASS |
| Output JSONL valid | Parseable | Valid JSON per line | PASS |
| Tripel diekstrak | > 0 | Tripel berhasil diekstrak | PASS |
| Modular imports | Menggunakan src/ | Ya (TripleExtractor, chunk_text) | PASS |

### 3.2 Analisis Kegagalan

- **SyntaxErrors berulang:** AI agent yang menulis script menghasilkan banyak syntax error (baris baru dalam string). Membutuhkan beberapa iterasi untuk menghasilkan kode yang bersih. Ini menunjukkan HITL tetap penting untuk code quality.
- **Input data tidak baru:** Menggunakan source_text.txt yang sama dengan Exp 01. Tidak menguji kemampuan batch pada data baru atau multiple files.
- **Tidak ada error handling per-chunk:** Jika satu chunk gagal, `except Exception` mencetak error tapi lanjut. Ini bisa menyembunyikan masalah pada skala besar.
- **Tidak ada deduplication:** Jika chunk overlap, tripel duplikat bisa muncul di output.
- **Tidak ada metrics:** Tidak ada tracking jumlah tripel per chunk, extraction rate, atau error rate.

### 3.3 Hostile Reviewer Simulation

1. **"Batch processing satu file kecil bukan bukti skalabilitas."** Memproses 1 file ~118 kata dalam chunks tidak menguji: multiple files, large files, concurrent processing, error recovery, rate limiting.
   - **Jawaban jujur:** Benar. Ini menguji modularitas kode, bukan skalabilitas sesungguhnya. Skalabilitas nyata perlu diuji dengan 100+ files.

2. **"Apa nilai JSONL dibanding JSON array?"** JSONL dipresentasikan sebagai keunggulan, tapi untuk ~30 tripel ini tidak membuat perbedaan. Value JSONL muncul pada streaming large datasets.
   - **Jawaban jujur:** Pada skala ini, tidak ada perbedaan meaningful. Pilihan JSONL adalah forward-looking untuk skala besar.

3. **"Pipeline 'modular' ini hanya 42 baris kode yang memanggil TripleExtractor. Apa kontribusinya?"**
   - **Jawaban jujur:** Kontribusi teknis minimal. Ini memvalidasi bahwa src/ modules bisa digunakan oleh experiment scripts. Sebagai engineering, trivial.

---

## Bagian 4: Review Gate (Retrospektif)

- [x] ~~Pre-registration~~ — **TIDAK DILAKUKAN**
- [x] Output valid (JSONL)
- [x] Analisis kegagalan terisi
- [x] Hostile reviewer simulation dijawab
- [x] Dicatat di failure registry (F-005)
- [ ] 10 pertanyaan review protocol — lihat REVIEW.md
- [x] Kode bisa direproduksi
- [x] Data output di-commit (extracted_triples.jsonl)

**Keputusan:** CONDITIONAL PASS (modular pipeline works, tapi skalabilitas belum terbukti)

**Reviewer:** Framework SOP (retrospektif)  **Tanggal:** 2026-02-06
