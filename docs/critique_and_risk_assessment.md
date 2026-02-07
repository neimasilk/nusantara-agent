# Critique & Strategic Risk Assessment
**Tanggal:** 7 Februari 2026
**Status:** Internal Review (post Exp 05 & Exp 07)
**Last Updated:** 2026-02-07

---

## 1. Snapshot Risiko Utama

Berdasarkan hasil eksperimen yang sudah berjalan, risiko prioritas saat ini:

* **Circular evaluation risk:** Evaluasi independen belum matang (annotator + agreement + external ground truth belum selesai).
* **Orchestration efficacy risk:** Mekanisme debat/self-correction sudah dibangun, tetapi belum menunjukkan gain kualitas dibanding baseline.
* **Scale risk:** Bukti masih berasal dari dataset kecil; power statistik belum cukup untuk klaim publikasi Q1.
* **External validity risk:** Rule dan gold standard masih perlu verifikasi ahli hukum adat.

---

## 2. Update Berbasis Evidence (hingga 2026-02-07)

### 2.1 Experiment 05 (Rule Engine)

* Komponen symbolic formal sudah tersedia (`ClingoRuleEngine`) dan rule base Minangkabau diperluas.
* Divergence terhadap LLM tercatat 33.3% (N=30), sehingga kebutuhan symbolic anchor terkonfirmasi.
* Namun, akurasi rule engine 70.0% (21/30) dan gold standard masih self-referential.

Implikasi:
Klaim neuro-symbolic bisa dibuka sebagai **partially earned**, tetapi belum cukup untuk klaim superioritas tanpa validasi independen.

### 2.2 Experiment 07 (Advanced Orchestration)

* Arsitektur advanced (parallel + debate + self-correction + routing) sudah dieksekusi pada 12 query.
* Hasil auto-score Kimi menunjukkan penurunan terhadap baseline sequential:
  * Accuracy: -0.67
  * Completeness: -0.67
  * Cultural Sensitivity: -0.33

Implikasi:
Klaim "orchestration improves quality" belum valid. Temuan negatif ini harus diposisikan sebagai evidence desain yang belum optimal, bukan keberhasilan.

---

## 3. Enam Kelemahan Metodologi (Status Terkini)

| # | Weakness | Severity | Status | Catatan |
|---|----------|----------|--------|---------|
| 1 | Neuro-symbolic claim | CRITICAL | PARTIALLY_RESOLVED | Komponen symbolic sudah ada (Exp 05), tetapi validitas eksternal belum kuat |
| 2 | Circular evaluation | CRITICAL | IN_PROGRESS | Exp 06 belum selesai; pipeline evaluasi independen masih dibangun |
| 3 | Orchestration value belum terbukti | MAJOR | IN_PROGRESS | Exp 07 berjalan, hasil awal negatif, perlu iterasi protokol |
| 4 | Scale too small | CRITICAL | IN_PROGRESS | Bukti tetap proof-of-concept; scaling plan belum tereksekusi |
| 5 | Baseline/ablation belum lengkap | CRITICAL | PLANNED | Menunggu Exp 09 dengan baseline kompetitif |
| 6 | CCS metric belum tervalidasi | MAJOR | PLANNED | Menunggu Exp 10 (reliability + validity + calibration) |

---

## 4. Prioritas Perbaikan

1. Selesaikan Exp 06 untuk memutus circularity evaluasi.
2. Iterasi Exp 07 dengan evidence retrieval yang lebih kuat dan validasi manusia (bukan satu evaluator LLM).
3. Sinkronkan baseline dan ablation plan (Exp 09) sebelum klaim kinerja lintas arsitektur.
4. Pertahankan failure logging ketat sebagai sumber utama Limitations di paper.

---

## 5. Referensi Internal

* Failure registry: `docs/failure_registry.md`
* Roadmap metodologi: `docs/methodology_fixes.md`
* Task registry: `docs/task_registry.md`
* Review protocol: `docs/review_protocol.md`
* Artefak Exp 07: `experiments/07_advanced_orchestration/analysis.md`
