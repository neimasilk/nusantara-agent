# Template Standar Eksperimen (Experiment SOP)

Setiap eksperimen dalam proyek Nusantara-Agent **WAJIB** mengikuti template ini. Tidak ada pengecualian.

---

## Bagian 1: Pre-Registration (SEBELUM Eksekusi)

Bagian ini HARUS diisi **sebelum** menjalankan kode apapun. Tujuannya mencegah bias konfirmasi.

### 1.1 Metadata

| Field | Isi |
|-------|-----|
| **ID Eksperimen** | `NN_nama_singkat` (misal: `05_rule_engine`) |
| **Peneliti** | Nama (Manusia/AI Agent) |
| **Tanggal Pre-registration** | YYYY-MM-DD |
| **Prasyarat** | Eksperimen mana yang harus selesai dulu? |
| **Estimasi Durasi** | 1-4 jam (jika > 4 jam, pecah menjadi sub-eksperimen) |

### 1.2 Hipotesis

Nyatakan hipotesis dalam format **falsifiable** (bisa dibuktikan salah):

> **H0 (Null):** [Sistem/metode yang diuji TIDAK menghasilkan perbedaan signifikan dibanding baseline]
>
> **H1 (Alternatif):** [Sistem/metode yang diuji menghasilkan perbedaan signifikan karena X]

### 1.3 Kriteria Penerimaan (Acceptance Criteria)

Definisikan **SEBELUM** eksekusi. Angka-angka ini tidak boleh diubah setelah melihat hasil.

| Metrik | Threshold Minimum | Metode Pengukuran |
|--------|-------------------|-------------------|
| Contoh: Precision | >= 0.80 | Manual annotation oleh 2 annotator |
| Contoh: Cohen's Kappa | >= 0.60 | Inter-annotator agreement |

### 1.4 Desain Eksperimen

- **Independent Variable(s):** Apa yang dimanipulasi?
- **Dependent Variable(s):** Apa yang diukur?
- **Control/Baseline:** Pembanding apa yang digunakan?
- **Confounding Variables:** Variabel pengganggu apa yang harus dikontrol?

### 1.5 Data & Resources

- **Input Data:** Lokasi file, jumlah sampel, sumber
- **Expected Output:** Format, lokasi penyimpanan
- **API/Resources:** LLM model, estimated token usage, biaya

---

## Bagian 2: Execution (SAAT Eksekusi)

### 2.1 Instruksi Step-by-Step

Tulis instruksi dengan detail **copy-paste level** — siapapun (manusia atau AI) harus bisa menjalankan tanpa bertanya.

```bash
# Step 1: Aktivasi environment
python -m venv venv && venv\Scripts\activate  # Windows
# atau: source venv/bin/activate  # Linux/Mac

# Step 2: Install dependencies (jika ada tambahan)
pip install -r requirements.txt

# Step 3: Jalankan eksperimen
python experiments/NN_nama/run_experiment.py

# Step 4: Verifikasi output
# Output harus ada di: experiments/NN_nama/results/
```

### 2.2 Log Eksekusi

| Timestamp | Event | Catatan |
|-----------|-------|---------|
| HH:MM | Mulai eksekusi | - |
| HH:MM | [Event penting] | [Detail] |
| HH:MM | Selesai | Total waktu: X menit |

### 2.3 Deviasi dari Rencana

Jika ada perubahan dari pre-registration, catat di sini dengan alasan:

| Perubahan | Alasan | Dampak pada Validitas |
|-----------|--------|----------------------|
| - | - | - |

---

## Bagian 3: Post-Analysis (SETELAH Eksekusi)

### 3.1 Hasil Kuantitatif

| Metrik | Threshold | Hasil Aktual | PASS/FAIL |
|--------|-----------|--------------|-----------|
| [dari 1.3] | [dari 1.3] | [isi setelah eksekusi] | [PASS/FAIL] |

### 3.2 Analisis Kegagalan (WAJIB)

Bahkan jika eksperimen "berhasil", bagian ini tetap wajib diisi.

- **Apa yang hampir gagal?** Identifikasi titik terlemah.
- **Dalam kondisi apa ini bisa gagal?** Edge cases, asumsi yang belum teruji.
- **Apa yang akan dikatakan reviewer skeptis?** Tulis minimal 3 kritik yang mungkin diajukan.
- **Bagaimana kegagalan ini mempengaruhi klaim paper?** Jangan tulis "tidak ada dampak" — selalu ada.

### 3.3 Hostile Reviewer Simulation

Bayangkan Reviewer 2 yang paling kritis di jurnal target. Tulis 3 pertanyaan yang akan mereka ajukan:

1. **[Pertanyaan tentang validitas internal]:** ...
2. **[Pertanyaan tentang generalizability]:** ...
3. **[Pertanyaan tentang novelty/kontribusi]:** ...

Lalu jawab masing-masing secara jujur. Jika jawabannya lemah, itu adalah kelemahan yang harus ditangani.

### 3.4 Implikasi

- **Untuk paper:** Bagaimana hasil ini mendukung/melemahkan argumen utama?
- **Untuk eksperimen selanjutnya:** Apa yang harus berubah berdasarkan temuan ini?
- **Untuk failure_registry:** Apakah ada kegagalan yang perlu dicatat? (Lihat `docs/failure_registry.md`)

---

## Bagian 4: Review Gate (SEBELUM Lanjut)

### 4.1 Checklist Mandatori

Semua item harus dicentang sebelum eksperimen dinyatakan selesai:

- [ ] Pre-registration diisi SEBELUM eksekusi (timestamp membuktikan)
- [ ] Acceptance criteria tidak diubah setelah melihat hasil
- [ ] Analisis kegagalan terisi lengkap (bukan hanya "tidak ada masalah")
- [ ] Hostile reviewer simulation dijawab secara substantif
- [ ] Hasil dicatat di `docs/failure_registry.md` (baik sukses maupun gagal)
- [ ] 10 pertanyaan review protocol dijawab (lihat `docs/review_protocol.md`)
- [ ] Kode bisa direproduksi oleh orang lain dari instruksi step-by-step
- [ ] Data output disimpan dan di-commit ke repository

### 4.2 Keputusan Gate

| Keputusan | Kriteria |
|-----------|----------|
| **PASS** | Semua acceptance criteria terpenuhi DAN checklist lengkap |
| **CONDITIONAL PASS** | Sebagian criteria terpenuhi, perlu eksperimen tambahan |
| **FAIL** | Criteria tidak terpenuhi — catat di failure registry, evaluasi pivot |

**Keputusan:** [PASS / CONDITIONAL PASS / FAIL]

**Alasan:** [Jelaskan]

**Reviewer:** [Nama]  **Tanggal:** [YYYY-MM-DD]

---

## Catatan Penggunaan

1. Simpan file ini sebagai `experiments/NN_nama/PROTOCOL.md`
2. Untuk eksperimen lama (01-04), buat PROTOCOL.md retrospektif dan tandai dengan jelas: `**[RETROSPEKTIF]** — Protokol ini ditulis setelah eksekusi untuk tujuan dokumentasi.`
3. Template ini adalah **living document** — usulkan perubahan via PR jika ada bagian yang perlu diperbaiki.
