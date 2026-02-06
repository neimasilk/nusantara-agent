# PROTOCOL: Eksperimen 03 — Orkestrasi Multi-Agen Dasar

**[RETROSPEKTIF]** — Protokol ini ditulis setelah eksekusi untuk tujuan dokumentasi.

---

## Bagian 1: Pre-Registration (Retrospektif)

### 1.1 Metadata

| Field | Isi |
|-------|-----|
| **ID Eksperimen** | `03_multi_agent_basic` |
| **Peneliti** | AI Agent + Human Researcher |
| **Tanggal Eksekusi** | 2026-02-06 |
| **Tanggal Protokol (Retrospektif)** | 2026-02-06 |
| **Prasyarat** | Exp 01 (result.json), DeepSeek API key |
| **Durasi Aktual** | ~30 menit |

### 1.2 Hipotesis (Retrospektif)

> **H0:** Arsitektur multi-agent (National + Adat + Supervisor) TIDAK menghasilkan sintesis pluralistik yang lebih baik daripada single-agent approach.
>
> **H1:** Arsitektur multi-agent menghasilkan output yang mempertimbangkan kedua perspektif hukum (nasional dan adat) dan mampu mengidentifikasi konvergensi atau konflik norma.

### 1.3 Kriteria Penerimaan (Retrospektif)

| Metrik | Threshold | Catatan |
|--------|-----------|---------|
| Pipeline berjalan | End-to-end tanpa error | 3 agen berjalan berurutan |
| Perspektif nasional | Output berisi analisis KUHPerdata | Agen Nasional |
| Perspektif adat | Output berisi analisis hukum adat | Agen Adat |
| Sintesis | Supervisor menggabungkan kedua perspektif | Bukan copy-paste |
| Deteksi konflik/konvergensi | Supervisor mengidentifikasi hubungan antar perspektif | Konflik atau keselarasan |

### 1.4 Desain Eksperimen

- **Independent Variable:** Arsitektur multi-agent (3 agents via LangGraph)
- **Dependent Variable:** Kualitas sintesis pluralistik
- **Control/Baseline:** Tidak ada — tidak dibandingkan dengan single-agent
- **Confounding Variables:** Kualitas prompt per agent, model temperature, panjang context window

### 1.5 Data & Resources

- **Input Data:** 1 test query (hardcoded), `experiments/01_triple_extraction/result.json` (untuk Agen Adat)
- **Expected Output:** Console output (final synthesis)
- **API:** DeepSeek Chat, 3 API calls (1 per agen), ~3000 tokens total

---

## Bagian 2: Execution

### 2.1 Instruksi Step-by-Step

```bash
# Step 1: Pastikan Exp 01 result.json tersedia
# Step 2: Pastikan .env berisi DEEPSEEK_API_KEY

# Step 3: Jalankan dari project root
python experiments/03_multi_agent_basic/multi_agent.py

# Step 4: Baca console output
# Output: User Query, lalu FINAL SYNTHESIS dari Supervisor
```

### 2.2 Deviasi dari Rencana

| Perubahan | Alasan | Dampak pada Validitas |
|-----------|--------|----------------------|
| 1 test query saja | Pilot test | Tinggi — N=1 |
| Sequential execution | Simplicity | Sedang — bukan true parallelism |
| agents.py kosong (stub) | Agent definitions inline di multi_agent.py | Rendah — code organization issue |
| Output tidak disimpan ke file | Quick test | Sedang — tidak bisa dianalisis ulang |

---

## Bagian 3: Post-Analysis (Retrospektif)

### 3.1 Hasil Kuantitatif

| Metrik | Threshold | Hasil Aktual | PASS/FAIL |
|--------|-----------|--------------|-----------|
| Pipeline berjalan | End-to-end | Berjalan tanpa error | PASS |
| Perspektif nasional | Berisi KUHPerdata | Ya, membahas hak anak | PASS |
| Perspektif adat | Berisi hukum adat | Ya, membahas kemenakan/pusako | PASS |
| Sintesis | Menggabungkan kedua | Ya, supervisor mensintesis | PASS |
| Deteksi konvergensi | Teridentifikasi | Ya, menemukan konvergensi pada Pusako Rendah | PASS |

### 3.2 Analisis Kegagalan

- **Sequential, bukan parallel:** Agen Nasional dan Agen Adat seharusnya bisa berjalan bersamaan. Sequential execution menambah latency tanpa alasan teknis.
- **Tidak ada debate/feedback:** Agen tidak saling mengkritik. Supervisor menerima output tanpa meminta klarifikasi. Ini bukan orchestration — ini adalah pipeline.
- **Tidak ada conditional routing:** Semua query mengikuti jalur yang sama, terlepas dari apakah itu kasus murni nasional, murni adat, atau konflik.
- **1 test query:** Tidak ada variasi query untuk menguji robustness.
- **Supervisor verbosity:** Output supervisor sangat panjang, yang akan menjadi masalah pada skala API calls besar.
- **analysis.md overstatement:** Klaim "SANGAT BERHASIL" dan "elegan" tidak proporsional dengan evidence (N=1, no baseline, no metrics).

### 3.3 Hostile Reviewer Simulation

1. **"Ini hanya 3 sequential API calls. Mengapa butuh framework multi-agent?"** LangGraph di sini tidak memberikan value lebih dari 3 function calls berurutan. Tidak ada state sharing yang meaningful, tidak ada conditional logic, tidak ada error recovery.
   - **Jawaban jujur:** Pada implementasi ini, benar. Framework multi-agent memberikan structure tapi belum memberikan capability yang tidak bisa dicapai tanpa framework. Value akan datang dari Exp 07 (parallel, debate, routing).

2. **"Bagaimana Anda tahu sintesis supervisor 'berkualitas'? Apa metriknya?"** Kualitas sintesis dinilai secara kualitatif. Tidak ada rubrik, tidak ada scoring, tidak ada perbandingan dengan human expert synthesis.
   - **Jawaban jujur:** Tidak bisa dibuktikan secara kuantitatif pada tahap ini. Perlu evaluasi formal.

3. **"Query ini cherry-picked untuk menunjukkan konvergensi. Bagaimana dengan kasus yang genuinely konfliktual?"** Kasus Pusako Rendah memang cenderung konvergen. Kasus yang lebih menantang (Pusako Tinggi vs nasional) tidak diuji.
   - **Jawaban jujur:** Ya, pemilihan query bias ke arah kasus yang "bekerja" dengan baik. Test suite yang comprehensive perlu mencakup adversarial cases.

---

## Bagian 4: Review Gate (Retrospektif)

- [x] ~~Pre-registration~~ — **TIDAK DILAKUKAN**
- [x] Pipeline berjalan end-to-end
- [x] Analisis kegagalan terisi
- [x] Hostile reviewer simulation dijawab
- [x] Dicatat di failure registry (F-003)
- [ ] 10 pertanyaan review protocol — lihat REVIEW.md
- [x] Kode bisa direproduksi (dengan Exp 01 result + API key)
- [ ] Data output disimpan — hanya console

**Keputusan:** CONDITIONAL PASS (pipeline works, tapi bukan real orchestration)

**Reviewer:** Framework SOP (retrospektif)  **Tanggal:** 2026-02-06
