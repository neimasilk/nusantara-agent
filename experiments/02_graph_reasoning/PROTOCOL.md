# PROTOCOL: Eksperimen 02 — Integrasi Graf & Penalaran Simbolik

**[RETROSPEKTIF]** — Protokol ini ditulis setelah eksekusi untuk tujuan dokumentasi.

---

## Bagian 1: Pre-Registration (Retrospektif)

### 1.1 Metadata

| Field | Isi |
|-------|-----|
| **ID Eksperimen** | `02_graph_reasoning` |
| **Peneliti** | AI Agent + Human Researcher |
| **Tanggal Eksekusi** | 2026-02-06 |
| **Tanggal Protokol (Retrospektif)** | 2026-02-06 |
| **Prasyarat** | Eksperimen 01 selesai (result.json tersedia) |
| **Durasi Aktual** | ~20 menit |

### 1.2 Hipotesis (Retrospektif)

> **H0:** Tripel hasil ekstraksi neural (Exp 01) TIDAK dapat digunakan untuk penalaran logis melalui struktur graf.
>
> **H1:** Tripel hasil ekstraksi neural dapat direpresentasikan sebagai graf berarah dan mendukung query penalaran simbolik dasar (authority search, conflict detection, path traversal).

### 1.3 Kriteria Penerimaan (Retrospektif)

| Metrik | Threshold | Catatan |
|--------|-----------|---------|
| Graf terbentuk | Nodes > 0, Edges > 0 | Graf valid dari tripel |
| Authority search | Jawaban relevan | Menemukan otoritas yang benar |
| Conflict detection | >= 1 konflik teridentifikasi | Dari data Exp 01 |
| Path traversal | Path ditemukan | Jalur pewarisan tertelusuri |

### 1.4 Desain Eksperimen

- **Independent Variable:** Representasi tripel sebagai graf (NetworkX MultiDiGraph)
- **Dependent Variable:** Kemampuan menjawab query penalaran simbolik
- **Control/Baseline:** Tidak ada — proof of concept
- **Confounding Variables:** Kualitas tripel dari Exp 01, pilihan query test

### 1.5 Data & Resources

- **Input Data:** `experiments/01_triple_extraction/result.json`
- **Expected Output:** Console output (tidak disimpan ke file)
- **API:** Tidak ada API call — pure local computation (NetworkX)

---

## Bagian 2: Execution

### 2.1 Instruksi Step-by-Step

```bash
# Step 1: Pastikan result.json dari Exp 01 tersedia
# experiments/01_triple_extraction/result.json harus ada

# Step 2: Jalankan dari project root
python experiments/02_graph_reasoning/graph_logic.py

# Step 3: Baca console output
# Output berupa: node/edge count, authority search results, conflict context, path traversal
```

### 2.2 Deviasi dari Rencana

| Perubahan | Alasan | Dampak pada Validitas |
|-----------|--------|----------------------|
| Tidak ada output file | Quick proof of concept | Sedang — hasil tidak persistent |
| Query hardcoded | Pilot test | Tinggi — tidak generalizable |

---

## Bagian 3: Post-Analysis (Retrospektif)

### 3.1 Hasil Kuantitatif

| Metrik | Threshold | Hasil Aktual | PASS/FAIL |
|--------|-----------|--------------|-----------|
| Graf terbentuk | Nodes > 0 | Nodes dan Edges terbentuk | PASS |
| Authority search | Jawaban relevan | Mamak Kepala Waris ditemukan | PASS |
| Conflict detection | >= 1 | 1 konflik teridentifikasi | PASS |
| Path traversal | Path ditemukan | Relasi Pusako Rendah ditelusuri | PASS |

### 3.2 Analisis Kegagalan

- **Bukan symbolic reasoning sebenarnya:** Graph traversal dan filtering bukan penalaran simbolik dalam pengertian AI formal. Tidak ada inference rules, tidak ada forward/backward chaining, tidak ada constraint satisfaction. Ini hanyalah graph query.
- **Query hardcoded:** Ketiga reasoning task menggunakan node names yang hardcoded (`Harta Pusako Tinggi`, `Harta Pusako Rendah`). Tidak ada mekanisme dynamic query.
- **Output tidak persistent:** Hasil hanya dicetak ke console, tidak disimpan untuk analisis lanjutan.

### 3.3 Hostile Reviewer Simulation

1. **"Ini bukan symbolic reasoning, ini graph query."** Graph traversal dengan filter sederhana bukan penalaran simbolik. Tidak ada logical inference, tidak ada rule application, tidak ada proof generation. Label "symbolic reasoning" di analysis.md terlalu kuat.
   - **Jawaban jujur:** Benar. Exp 02 mendemonstrasikan graph queryability, bukan symbolic reasoning. Formal reasoning akan ditambahkan di Exp 05.

2. **"Semua ini bisa dilakukan dengan SQL query. Apa kontribusi grafnya?"** Jika data sudah terstruktur sebagai tripel, relational database bisa menjawab query yang sama.
   - **Jawaban jujur:** Untuk skala saat ini, benar. Keuntungan graf akan terasa pada skala besar (10K+ tripel) di mana multi-hop reasoning dan path discovery menjadi non-trivial.

3. **"3 hardcoded queries bukan evaluasi."** Tidak ada systematic evaluation, tidak ada precision/recall, tidak ada test suite.
   - **Jawaban jujur:** Benar. Ini perlu test suite yang proper di Exp 05.

---

## Bagian 4: Review Gate (Retrospektif)

- [x] ~~Pre-registration~~ — **TIDAK DILAKUKAN**
- [x] Output valid
- [x] Analisis kegagalan terisi
- [x] Hostile reviewer simulation dijawab
- [x] Dicatat di failure registry (F-003 terkait)
- [ ] 10 pertanyaan review protocol — lihat REVIEW.md
- [x] Kode bisa direproduksi (dengan Exp 01 result)
- [ ] Data output disimpan — hanya console output

**Keputusan:** CONDITIONAL PASS (membuktikan graph terbentuk, tapi bukan symbolic reasoning)

**Reviewer:** Framework SOP (retrospektif)  **Tanggal:** 2026-02-06
