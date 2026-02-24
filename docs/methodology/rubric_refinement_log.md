# Rubric Refinement Log (Batch 1 -> Batch 2)

**Status:** DRAFT - menunggu input owner
**Tanggal dibuat:** 2026-02-24
**Tujuan:** dokumentasi transparansi metodologi untuk reviewer Q1 terkait lonjakan agreement batch labeling.

---

## Ringkasan Fakta Terkonfirmasi

Sumber angka saat ini:
- `paper/main.tex` (Table dataset status dan agreement profile)
- `data/benchmark_manifest.json`
- `docs/handoffs/20260224_prompt_lanjutan.md`

Fakta yang sudah terkonfirmasi:
1. Batch 1 (24 kasus) agreement = 58.3% (14/24), Cohen's kappa = 0.394.
2. Batch 2 (50 kasus baru) agreement = 94.0% (47/50).
3. Gap utama disagreement berada pada boundary label B vs C.
4. Kenaikan agreement dari batch 1 ke batch 2 sangat besar dan harus dijelaskan eksplisit di paper/dokumen metodologi.

---

## Pertanyaan Owner (Wajib Diisi)

| ID | Pertanyaan | Status | Jawaban Owner | Catatan Bukti |
|---|---|---|---|---|
| Q1 | Apa yang berubah di rubrik antara Batch 1 dan Batch 2? | PENDING |  |  |
| Q2 | Kapan perubahan rubrik dibuat (tanggal/periode)? | PENDING |  |  |
| Q3 | Apakah Batch 2 sepenuhnya independent dari Batch 1 (tanpa leakage kasus/label)? | PENDING |  |  |
| Q4 | Siapa yang memutuskan perubahan rubrik (nama/peran)? | PENDING |  |  |

Instruksi pengisian:
- Isi kolom **Jawaban Owner** sejelas mungkin dan sebutkan artefak pendukung di **Catatan Bukti** (dokumen, chat, catatan meeting, commit).

---

## Decision Log Rubrik

| Tanggal | Peristiwa | Perubahan Rubrik | Alasan Perubahan | Pengambil Keputusan | Evidence Link |
|---|---|---|---|---|---|
| TBD | Draft awal rubrik Batch 1 | TBD | TBD | TBD | TBD |
| TBD | Refinement sebelum Batch 2 | TBD | TBD | TBD | TBD |
| TBD | Finalisasi rubrik operasional | TBD | TBD | TBD | TBD |

Catatan:
- Isi tabel ini kronologis. Reviewer biasanya menilai apakah perubahan rubric dilakukan sebelum labeling batch berikutnya dimulai.

---

## Independence Audit (Batch 2)

Checklist audit independensi:
- [ ] Batch 2 tidak menggunakan kasus yang sama dari Batch 1.
- [ ] Label Batch 1 tidak dibuka ulang saat melakukan labeling Batch 2.
- [ ] Definisi label yang dipakai Batch 2 berasal dari rubric final yang terdokumentasi.
- [ ] Tidak ada prompt/briefing yang memberi target distribusi label tertentu.

Kesimpulan sementara:
- **Belum dapat dinyatakan** sebelum Q1-Q4 di atas diisi.

---

## Narasi Siap Pakai (Template untuk Paper/Response Reviewer)

Template (isi placeholder setelah Q1-Q4 lengkap):

> Inter-rater agreement improved from 58.3% (kappa=0.394, 24 cases) in Batch 1 to 94.0% (47/50) in Batch 2 after a predefined rubric refinement focused on the B/C boundary. The refinement was approved on [DATE] by [DECISION MAKER], before Batch 2 labeling started, and Batch 2 was annotated independently from Batch 1 labels.

Gunakan template ini hanya setelah field [DATE] dan [DECISION MAKER] terisi berbasis bukti.

---

## Action Items

1. Owner mengisi Q1-Q4.
2. Setelah Q1-Q4 terisi, update subsection "Rubric refinement" di `paper/main.tex` dengan detail yang bisa diaudit.
3. Tambahkan referensi silang dari paper ke file ini (misalnya di appendix atau reproducibility docs).
4. Kunci dokumen ini sebagai versi final untuk paket submission.

---

## Changelog

| Tanggal | Perubahan |
|---|---|
| 2026-02-24 | Draft awal dibuat untuk menangkap gap metodologi rubric refinement dan menyiapkan input owner. |
