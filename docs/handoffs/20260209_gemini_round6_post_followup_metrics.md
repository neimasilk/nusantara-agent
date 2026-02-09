# Round 6 Report: Post-Followup Statistical QA
**Date:** 2026-02-09
**Status:** STABILIZED (PILOT SCALE)

## 1. Snapshot Statistik (N=24)
Pembersihan status `SPLIT` pada dataset aktif menghasilkan dataset evaluasi yang lebih bersih secara struktural, namun tetap terbatas secara statistik.

- **Total Cases:** 24
- **Evaluable (Non-D):** 23 (Asumsi CS-LIN-052 tetap Label D)
- **Consensus Strength:** 83.3% (Majority + Unanimous)
- **Label Mismatch Risk:** 4 kasus `TIE` (2-2) menjadi titik kritis akurasi.

## 2. Akurasi & Sensitivitas
Setiap satu kesalahan prediksi AI akan menurunkan akurasi sebesar **4.17%**.
- **Skenario Optimis:** AI benar pada 4 kasus TIE -> Akurasi berpotensi naik signifikan.
- **Skenario Pesimis:** AI salah pada 4 kasus TIE -> Akurasi bisa jatuh ke zona <60%.

## 3. 95% Confidence Interval (Binomial)
Pada estimasi akurasi 72.7%:
- **95% CI:** [51.8% — 86.8%]
- **Interpretasi:** Kita memiliki keyakinan 95% bahwa akurasi sistem berada di rentang tersebut. Rentang yang lebar ini (35%) adalah indikator bahwa klaim "Performance Gain" bersifat spekulatif sampai jumlah sampel ditingkatkan.

## 4. Decision Gate (Numerical Gatekeeping)
**REKOMENDASI: TAHAN (HOLD) EVALUASI AKHIR.**

| Syarat | Target | Aktual | Hasil |
| :--- | :---: | :---: | :--- |
| Jumlah Sampel | N ≥ 60 | 24 | **Fail** |
| Power (CI Width) | < 20% | 35% | **Fail** |
| Data Consistency | 0 Mismatch | TBD | **Pending** |

## 5. Panduan Publikasi
- **Klaim yang diizinkan:** Deskripsi arsitektur, hasil pilot pada 24 kasus, dan efektivitas mekanisme *safety net* pada sampel kritis.
- **Klaim yang dilarang:** Pernyataan generalisasi performa, klaim signifikansi statistik lintas domain, atau klaim akurasi tanpa menyebutkan ukuran sampel pilot.

**Next Action:** Ekspansi dataset aktif ke **N=82** (Full Consensus Set) untuk menekan CI Width dan melegitimasi klaim ilmiah.
