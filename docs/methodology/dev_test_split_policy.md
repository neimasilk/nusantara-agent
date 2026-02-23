# Dev/Test Split Policy

**Tanggal Ditetapkan:** 2026-02-23
**Ditetapkan oleh:** Opus 4.6 (strategic review) + Sonnet 4.6 (dokumentasi)
**Berlaku untuk:** Semua evaluasi benchmarking Exp 09 dan seterusnya

---

## Latar Belakang

70 kasus yang ada saat ini telah terkontaminasi oleh aktivitas prompt tuning (accuracy naik dari 54% → 68.6% selama iterasi Prompt 1–23). Oleh karena itu, klaim generalisasi sistem memerlukan data yang belum pernah dilihat selama development. Ini adalah persyaratan standar untuk publikasi Q1.

---

## Struktur Split (Saat Ini, n=70)

File canonical: `experiments/09_ablation_study/dataset_split.json` (seed=42)

| Split | Jumlah Kasus | Tujuan |
|-------|-------------|--------|
| **DEV set** | 49 kasus | Development, prompt tuning, error analysis, debugging |
| **LOCKED TEST set** | 21 kasus | Evaluasi internal — hanya untuk milestone final reporting |
| **FUTURE TEST set** | semua kasus baru dari Ahli-2 | Evaluasi generalisasi sejati |

Split internal 49/21 menggunakan stratified sampling (domain × label) dengan seed=42 untuk menjaga proporsionalitas distribusi label dan domain.

---

## Aturan Penggunaan

### DEV Set (49 kasus)
1. Boleh digunakan untuk prompt tuning, error analysis, debugging
2. Boleh di-inspect kasus per kasus
3. Semua benchmark run sehari-hari menggunakan set ini

### LOCKED TEST Set (21 kasus dari 70 existing)
1. **DILARANG** inspect atau menganalisis kasus secara individual selama development
2. Hanya digunakan untuk milestone evaluation yang sudah dijadwalkan
3. Setelah satu kali evaluasi resmi, hasilnya dilaporkan apa adanya — tidak ada iterasi berdasarkan hasil ini
4. Berisi 10 label C, 3 label A, 8 label B (tidak ada D — karena D hanya 2 kasus, semua di DEV)

### FUTURE TEST Set (kasus baru dari Ahli-2, post-2026-02-23)
1. Semua kasus yang dilabeli Ahli-2 setelah tanggal 2026-02-23 masuk ke set ini
2. Tidak boleh ada "peeking" — begitu kasus masuk FUTURE TEST, tidak boleh dipakai untuk development
3. Evaluasi FUTURE TEST hanya dilakukan sekali, pada milestone final paper
4. Ini adalah sumber data untuk klaim generalisasi di paper

---

## Rasional

- **Kontaminasi**: 70 kasus existing sudah dilihat selama prompt tuning → tidak bisa jadi test set bersih
- **Statistical power**: n=70 menghasilkan power ~0.3 untuk mendeteksi perbedaan 10pp; butuh ≥344 kasus untuk power=0.8
- **Reviewer expectation**: reviewer Q1 akan menanyakan apakah ada data unseen yang digunakan untuk evaluasi final
- **Integrity**: tanpa split yang diaudit, klaim accuracy di paper tidak kredibel

---

## Distribusi Label (Canonical, n=70)

| Label | Total | DEV (49) | LOCKED TEST (21) |
|-------|-------|----------|------------------|
| A (Nasional) | 6 | 3 | 3 |
| B (Adat) | 31 | 23 | 8 |
| C (Konflik) | 31 | 21 | 10 |
| D (Tidak cukup info) | 2 | 2 | 0 |

---

## Nomor Kasus

Daftar lengkap case IDs per split tersedia di:
`experiments/09_ablation_study/dataset_split.json`

---

## Changelog

| Tanggal | Perubahan |
|---------|-----------|
| 2026-02-23 | Policy ditetapkan. Formalisasi split 49/21 yang sudah ada di dataset_split.json. Tambah definisi FUTURE TEST set untuk kasus Ahli-2 baru. |
