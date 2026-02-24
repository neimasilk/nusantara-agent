# Rubric Refinement Log (Batch 1 -> Batch 2)

**Status:** FINAL (owner-confirmed for Q4)
**Tanggal dibuat:** 2026-02-24
**Last update:** 2026-02-24
**Tujuan:** dokumentasi metodologis agar lonjakan agreement 58.3% -> 94.0% dapat diaudit reviewer.

---

## Ringkasan Eksekutif

Status jawaban 4 pertanyaan kritikal:
1. **Q1 (apa yang berubah di rubrik):** sudah terjawab berbasis artefak.
2. **Q2 (kapan perubahan dibuat):** terjawab parsial (timeline artefak tersedia, tanggal keputusan final owner belum eksplisit).
3. **Q3 (apakah batch 2 independen):** terjawab parsial dengan bukti operasional kuat.
4. **Q4 (siapa yang memutuskan):** sudah dikonfirmasi owner.

---

## Bukti Primer yang Dipakai

1. `docs/ira_analysis_2026-02-12.md` (angka baseline 24 kasus: 14/24, kappa=0.394).
2. `docs/human_only/artifacts/paket_kerja_4_jam_ahli2_batch1_ready_to_handout.md` (instruksi awal, belum ada rubric boundary test eksplisit).
3. `docs/human_only/artifacts/paket_kerja_4_jam_ahli2_batch2_kalibrasi_ready_to_handout.md` (definisi label dikunci).
4. `docs/human_only/artifacts/paket_kerja_4_jam_ahli2_batch3_kalibrasi_lanjutan_ready_to_handout.md` (aturan tambahan A/B vs C).
5. `docs/human_only/artifacts/paket_kerja_4_jam_ahli2_batch5_ready_to_handout.md` (decision checklist Dominansi/Dualitas/Fakta).
6. `docs/human_only/paket_labeling_50_kasus_baru.md` (paket expanded 50 kasus, rubric lengkap + instruksi blind labeling).
7. `data/processed/gold_standard/gs_active_cases.json` (komposisi 24 CS + 50 GS, agreement GS=47/50).
8. `git log` untuk jejak commit artefak rubric/instruksi (contoh: `3330118`, `80d562f`).

---

## Jawaban Owner (Draft Berbasis Evidence)

| ID | Pertanyaan | Status | Jawaban Draft (Evidence) | Bukti |
|---|---|---|---|---|
| Q1 | Apa yang berubah di rubrik antara Batch 1 dan Batch 2? | ANSWERED-EVIDENCE | Rubrik berubah dari instruksi label generik menjadi rubric terstruktur: definisi label dikunci, boundary test A vs C ditambahkan, contoh boundary cases ditambahkan, dan checklist keputusan dibuat eksplisit. | File 2-6 pada daftar bukti primer |
| Q2 | Kapan perubahan rubrik dibuat? | PARTIAL | Refinement berlangsung bertahap: fase kalibrasi pada 2026-02-08, lalu paket expanded 50 kasus bertanggal 2026-02-19 sudah memakai rubric lengkap. Tanggal approval formal owner belum terdokumentasi eksplisit. | File 3-6 + metadata commit (`3330118`, `80d562f`) |
| Q3 | Apakah Batch 2 sepenuhnya independent dari Batch 1? | PARTIAL-EVIDENCE | Bukti operasional menunjukkan independensi pada level data/protokol: pool kasus disjoint (24 `CS-*` vs 50 `GS-*`, overlap ID = 0), dan paket 50 kasus memuat instruksi "JANGAN melihat referensi atau label orang lain". Namun bukti ini belum bisa memverifikasi faktor di luar artefak (out-of-band leakage). | File 6-7 |
| Q4 | Siapa yang memutuskan perubahan rubrik? | ANSWERED-OWNER | Pengambil keputusan final refinement rubric: **Mukhlis Amien** (`amien@ubhinus.ac.id`), peran **Research Lead**. Konfirmasi diberikan pada **24 Februari 2026**. | Konfirmasi owner (sesi 2026-02-24) + jejak artefak |

---

## Detail Q1: Perubahan Rubrik

Perubahan yang terobservasi dari artefak:
1. **Batch 1 (agreement prep):** form meminta label A/B/C/D tanpa boundary policy eksplisit.
2. **Batch 2 kalibrasi:** definisi A/B/C/D dikunci sebagai standar wajib.
3. **Batch 3 kalibrasi lanjutan:** jika memilih C wajib jelaskan dua komponen; jika memilih A/B wajib jelaskan kenapa tidak perlu sintesis.
4. **Batch 5 ekspansi:** ditambahkan urutan cek keputusan (Dominansi -> Dualitas -> Fakta).
5. **Expanded 50-case packet (2026-02-19):** rubric lengkap dengan "Panduan Batas Kritis (A vs C)" + contoh boundary A/C/B/D.

Interpretasi metodologis:
- Refinement berfokus pada error boundary utama B/C (dan A/C), bukan mengubah task definition inti.

---

## Detail Q2: Timeline Refinement

| Tanggal | Event | Bukti |
|---|---|---|
| 2026-02-08 | Baseline agreement prep Ahli-2 Batch 1 (instruksi generik) | `paket_kerja_4_jam_ahli2_batch1_ready_to_handout.md` |
| 2026-02-08 | Kalibrasi Batch 2 memperkenalkan definisi label dikunci | `paket_kerja_4_jam_ahli2_batch2_kalibrasi_ready_to_handout.md` |
| 2026-02-08 | Kalibrasi Batch 3 menambahkan aturan justifikasi C vs A/B | `paket_kerja_4_jam_ahli2_batch3_kalibrasi_lanjutan_ready_to_handout.md` |
| 2026-02-08 | Batch 5 menambahkan checklist keputusan Dominansi/Dualitas/Fakta | `paket_kerja_4_jam_ahli2_batch5_ready_to_handout.md` |
| 2026-02-19 | Paket expanded 50 kasus memakai rubric lengkap + boundary tests + blind instruction | `paket_labeling_50_kasus_baru.md` |
| 2026-02-23 | Artefak labeling/rubric di-commit ke repo (import dokumentasi) | Commit `80d562f` |

Catatan:
- Jejak di atas adalah **timeline artefak**. Tanggal keputusan formal owner untuk final approval rubric masih perlu dikonfirmasi.

---

## Detail Q3: Independence Audit (Batch 2 Expanded)

### Bukti yang mendukung independensi

1. **Disjoint case pool:**
   - Initial batch: 24 kasus dengan prefix `CS-*`.
   - Expanded batch: 50 kasus dengan prefix `GS-*`.
   - Overlap ID: **0**.

2. **Blind-labeling instruction tertulis:**
   - Paket 50 kasus memuat instruksi: *"JANGAN melihat referensi atau label orang lain"*.

3. **Agreement expanded batch konsisten dengan klaim paper:**
   - Ahli-1 vs Ahli-2 pada 50 kasus `GS-*`: **47/50 (94.0%)**.
   - 3 mismatch: `GS-0022`, `GS-0023`, `GS-0032`.
   - Ketiganya pattern **B vs C** dan status gold saat ini `DISPUTED`.

### Batas bukti

- Bukti di atas kuat pada level artefak repository, tetapi tidak bisa membuktikan secara absolut tidak adanya komunikasi informal di luar sistem dokumentasi.

Kesimpulan audit saat ini:
- **Independen secara operasional (artifact-level): YA.**
- **Independen absolut (termasuk out-of-band): BELUM BISA DIPASTIKAN.**

---

## Detail Q4: Decision Authority (Owner Confirmed)

Konfirmasi owner yang diterima pada 2026-02-24:
1. **Nama:** Mukhlis Amien
2. **Kontak:** amien@ubhinus.ac.id
3. **Peran:** Peneliti / Research Lead
4. **Tanggal konfirmasi keputusan:** 24 Februari 2026

Implikasi:
- Q4 ditutup sebagai **answered**.
- Status dokumen dinaikkan menjadi **FINAL** untuk konteks metodologi yang saat ini terdokumentasi.

---

## Decision Log Rubrik (Evidence-Backed)

| Tanggal | Peristiwa | Perubahan Rubrik | Alasan Perubahan | Pengambil Keputusan | Evidence |
|---|---|---|---|---|---|
| 2026-02-08 | Batch 1 agreement prep | Instruksi label masih generik | Persiapan agreement awal Ahli-2 | Tim riset (operasional), final authority dikonfirmasi owner | Paket batch1 ready |
| 2026-02-08 | Batch 2 kalibrasi | Definisi A/B/C/D dikunci | Menurunkan mismatch pasca 33.3% agreement awal | Tim riset (operasional), final authority dikonfirmasi owner | Paket batch2 ready + report batch2 |
| 2026-02-08 | Batch 3 kalibrasi lanjutan | Aturan justifikasi C vs A/B ditambahkan | Memperjelas boundary label | Tim riset (operasional), final authority dikonfirmasi owner | Paket batch3 ready + report batch3 |
| 2026-02-08 | Batch 5 ekspansi terarah | Checklist Dominansi/Dualitas/Fakta | Standarisasi reasoning lintas kasus baru | Tim riset (operasional), final authority dikonfirmasi owner | Paket batch5 ready |
| 2026-02-19 | Expanded batch 50 kasus | Rubric lengkap + boundary tests + contoh + blind instruction | Scale-up annotation dengan boundary policy lebih ketat | Tim riset (operasional), final authority dikonfirmasi owner | Paket labeling 50 kasus |
| 2026-02-24 | Konfirmasi authority | Penetapan pengambil keputusan final rubric refinement | Menutup gap metodologi untuk reviewer | **Mukhlis Amien (Research Lead)** | Konfirmasi owner sesi 2026-02-24 |

---

## Checklist Audit Cepat

- [x] Batch 2 menggunakan pool kasus yang berbeda dari Batch 1 (ID disjoint CS vs GS).
- [x] Paket expanded memuat instruksi blind labeling.
- [x] Rubrik final terdokumentasi (definisi + boundary tests + contoh).
- [x] Tidak ada target distribusi label tertentu pada instruksi expanded.
- [x] Otoritas keputusan final refinement rubric tercatat eksplisit (nama/peran/tanggal).

---

## Narasi Siap Pakai (Paper / Response Reviewer)

Versi konservatif (tanpa klaim authority final):

> Inter-rater agreement improved from 58.3% (kappa=0.394, 24 cases) to 94.0% (47/50) after staged rubric refinement focused on decision boundaries (especially A/B vs C). The refined protocol introduced locked label definitions, explicit boundary tests, and standardized decision checks, and the expanded batch used a disjoint case pool with blind-labeling instructions.

Versi final:

> Inter-rater agreement improved from 58.3% (kappa=0.394, 24 cases) to 94.0% (47/50) after staged rubric refinement introducing locked label definitions, explicit A-vs-C boundary tests, and standardized decision checks. The expanded batch was annotated on a disjoint case pool under blind-labeling instructions. Final rubric-governance authority is documented as Mukhlis Amien (Research Lead), confirmed on 24 February 2026.

---

## Action Items

1. Pertahankan konsistensi narasi antara file ini dan `paper/main.tex` jika ada revisi lanjutan.
2. Gunakan file ini sebagai lampiran metodologi untuk paket submission/rebuttal reviewer.

---

## Changelog

| Tanggal | Perubahan |
|---|---|
| 2026-02-24 | Draft awal template dibuat (tanpa evidence detail). |
| 2026-02-24 | Upgraded menjadi evidence-backed draft: Q1/Q2/Q3 terisi berbasis artefak, Q4 tetap menunggu owner sign-off. |
| 2026-02-24 | Q4 dikonfirmasi owner (Mukhlis Amien, Research Lead, 24 Februari 2026); status dokumen diubah menjadi FINAL. |
