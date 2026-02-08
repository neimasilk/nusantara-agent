# Handoff: Mata Elang Strategic Weekly Review — 2026-02-08

**Mode:** Weekly strategic gate (bukan eksekusi harian)  
**Fokus:** deteksi dini kegagalan struktural, coherence metodologi, kualitas kolaborasi multi-agent/multi-human/multi-device, dan readiness menuju paper Q1.

---

## 1) Putusan Strategis Mingguan

Proyek berada pada kondisi **over-complexity + governance drift**.  
Arah saat ini masih recoverable, tetapi klaim ilmiah perlu ditahan sampai kontrak evaluasi, integritas dataset, dan testability sistem kembali konsisten.

Posisi tegas:
- **Simple is better:** jalur produksi harus dipersempit ke pipeline yang dapat diuji deterministik.
- **Fail fast:** elemen yang tidak testable atau tidak menambah gain harus difreeze.
- **Pivot early:** evaluasi independen dan governance data harus didahulukan dari fitur baru.

---

## 2) Evidence Snapshot (verifikasi sesi ini)

1. Klaim gold standard 82 kasus terdokumentasi di `docs/gold_standard_consensus_report_complete_82_cases_2026-02-08.md` (baris statistik total 82).  
2. File benchmark aktif yang dipakai runner `experiments/09_ablation_study/run_bench_active.py` (alias legacy: `run_bench_gs82.py`) menunjuk `data/processed/gold_standard/gs_active_cases.json` (via manifest).  
3. Isi aktual `data/processed/gold_standard/gs_active_cases.json` saat ini adalah list **24 kasus** (dengan 2 split, efektif 22 terukur).  
4. Ini konsisten dengan `experiments/09_ablation_study/analysis.md` yang menyebut **Sampel: 22**.  
5. Baseline B1 masih template fallback (`experiments/09_ablation_study/baselines/b1_direct_prompting.py` + `experiments/09_ablation_study/baselines/_common.py`), belum direct prompting yang fair.  
6. Test rule engine pass `32/32`; full deterministic suite pass `79/79` via `python -m unittest discover -s tests -p "test_*.py" -v`.  
7. `tests/test_nusantara_pipeline.py` sudah dimitigasi menjadi offline dengan mock builder orchestrator; guardrail ini mencegah call `llm.invoke` live saat unit test.  
8. Terdapat artefak tanggal **2026-02-09** di `CLAUDE.md`, `docs/task_registry.md`, `docs/failure_registry.md` meski gate ini bertanggal 2026-02-08.

---

## 3) Temuan Kritis (Hard but Constructive)

### CRITICAL-01 — Dataset Governance Incoherence
**Masalah:** Narasi eksperimen menyebut N=82, tetapi file benchmark aktif berisi 24 kasus.  
**Risiko:** Klaim statistik dan reproducibility dapat dipatahkan reviewer Q1 dalam satu pertanyaan.  
**Aksi wajib:** Satu sumber kebenaran dataset + manifest hash + penamaan file jujur (jangan `gs_82` jika isinya 24).

### CRITICAL-02 — Evaluation Contract Belum Defensible
**Masalah:** Exp06 tetap blocked; evaluasi independen manusia belum selesai, tetapi metrik akurasi terus dipakai sebagai headline.  
**Risiko:** Circularity berpindah bentuk, bukan selesai.  
**Aksi wajib:** Freeze klaim performa final sampai jalur evaluasi independen memenuhi acceptance criteria.

### CRITICAL-03 — Baseline Fairness Rusak
**Masalah:** B1/B2/B3/B4/B5 masih bertumpu pada fallback synthesizer template; bukan baseline kompetitif.  
**Risiko:** Ablation tidak sah secara metodologis (strawman).  
**Aksi wajib:** Rebuild baseline minimal agar setiap baseline benar-benar menjalankan komponen yang diklaim.

### MAJOR-01 — Testability Drift pada Pipeline Utama (Mitigated, keep guard)
**Masalah:** Sebelumnya test pipeline memanggil komponen LLM live dan rawan timeout/flaky.  
**Status kini:** Mitigated (pipeline test sudah mock orchestrator, full-suite 79/79 pass offline).  
**Risiko residual:** Drift bisa kembali jika test baru memanggil LLM langsung tanpa mock.  
**Aksi wajib:** Pertahankan pemisahan offline deterministic tests vs online integration tests.

### MAJOR-02 — Arsitektur Melebihi Bukti Nilai
**Masalah:** Exp07 menunjukkan advanced orchestration lebih mahal dan skornya turun dari baseline.  
**Risiko:** Kompleksitas operasional naik tanpa gain kualitas.  
**Aksi wajib:** Freeze debate/self-correction sebagai branch eksperimen, bukan jalur default.

### MAJOR-03 — Governance Timestamp Drift
**Masalah:** tanggal “masa depan” bercampur dalam dokumen status operasional.  
**Risiko:** audit trail lemah; menurunkan trust terhadap provenance.  
**Aksi wajib:** normalisasi tanggal + field `as_of_date` eksplisit di setiap ringkasan status.

---

## 4) Evaluasi Arsitektur Kolaborasi Manusia-AI

Diagnosis:
- Arsitektur teknis bergerak cepat, tetapi arsitektur governance manusia belum mengimbangi.
- Variasi kapabilitas agent dan manusia belum dimodelkan sebagai uncertainty formal dalam keputusan.
- Konflik antar-output agent saat ini lebih banyak diselesaikan lewat prompt tuning daripada protokol validasi lintas peran.

Arahan desain:
1. Bedakan 3 jalur kerja:
   - `Production-Research Core`: komponen yang deterministic + teruji.
   - `Experimental Branch`: debate/self-correction/routing heuristik.
   - `Human Validation Track`: anotasi, adjudication, agreement analytics.
2. Tetapkan authority:
   - Agent tidak boleh “menutup” sengketa label yang statusnya split/low-agreement.
   - Human adjudicator tetap penentu final untuk kasus high-impact.
3. Lindungi kolaborasi aktif:
   - Refactor dilakukan di adapter/contract layer, bukan mengubah format kerja manusia yang sedang berjalan.

---

## 5) Refactor / Pivot / Stop Map

### ADOPT NOW (minggu ini)
1. **Data truth repair:** buat `data/benchmark_manifest.json` berisi `dataset_id`, `count`, `hash`, `owner`, `as_of_date`, `provenance`.  
2. **Rename/realign dataset artifacts:** sinkronkan nama file, isi aktual, dan klaim di analisis.  
3. **Testing split:** pisah `tests_offline/` vs `tests_online/`; test pipeline unit wajib mock LLM.  
4. **Baseline rehab:** ubah B1 menjadi true direct prompting; baseline lain jangan pakai template fallback sebagai jawaban utama.

### DEFER WITH TRIGGER
1. Debate protocol v2: trigger saat baseline fair sudah valid + ada gain terukur pada evaluasi independen.  
2. Scale 200+ kasus final: trigger saat governance manifest dan agreement pipeline stabil.

### STOP / FREEZE
1. Freeze klaim “siap paper-level performance” sampai kontrak evaluasi dan dataset governance sinkron.  
2. Freeze penggunaan hasil Exp09 sebagai bukti utama jika baseline fairness belum diperbaiki.

---

## 6) Framework Testing Interaksi (A2A, A2H, H2H)

### Layer T0 — Contract & Schema Tests (offline, wajib)
- Validasi schema input/output antar agent, pipeline, dan evaluator.
- Guardrail: perubahan schema tanpa migrasi otomatis = fail.

### Layer T1 — Deterministic Component Tests (offline, wajib)
- Router rules, parser JSON, retriever lokal, symbolic engine, scoring utilities.
- Tidak boleh ada network/API call.

### Layer T2 — Interaction Replay Tests (A2A, offline replay)
- Replay log agent-agent dari artefak tetap.
- Ukur contradiction rate, evidence coverage, dan unresolved conflict ratio.

### Layer T3 — Human-in-the-Loop Protocol Tests (A2H/H2H)
- Uji reproducibility keputusan manusia (agreement trend, split-rate, adjudication lag).
- Kasus split wajib menghasilkan keputusan prosedural, bukan dipaksa “otomatis selesai”.

### Layer T4 — Online Canary (terbatas, berbiaya)
- Jalankan sampel kecil dengan LLM live untuk memantau drift.
- Tidak dipakai sebagai bukti tunggal quality.

### Taksonomi kegagalan lintas interaksi
- `A2A_CONTRADICTION`: agent saling meniadakan tanpa resolusi.
- `A2A_EVIDENCE_GAP`: klaim tidak ditopang retrieval/rules.
- `A2H_OVERRULE_SILENT`: keputusan manusia di-override agent tanpa audit trail.
- `H2H_DISAGREEMENT_PERSISTENT`: split berulang tanpa protokol pemutus.
- `PIPELINE_NONDETERMINISTIC`: test inti tidak reproducible offline.

---

## 7) Mekanisme Seleksi Kritik (Akomodasi vs Abaikan)

Setiap kritik masuk ke `critique_registry` dengan field:
- `severity`, `evidence_strength`, `rejection_risk`, `testability`, `cost`, `collab_disruption`, `claim_impact`.

Skor prioritas:
`priority = (severity + evidence_strength + rejection_risk + testability + claim_impact) - (cost + collab_disruption)`

Keputusan hanya:
1. `ADOPT_NOW`
2. `DEFER_WITH_TRIGGER`
3. `IGNORE_WITH_RATIONALE`

Aturan disiplin:
1. Maksimal 3 item `ADOPT_NOW` per minggu agar eksekusi fokus.
2. `IGNORE_WITH_RATIONALE` wajib punya expiry review (maks 14 hari).
3. Semua keputusan wajib menyebut dampak ke klaim paper: bisa diklaim / belum bisa / tidak bisa.

---

## 8) Klaim Paper: Boleh vs Belum

### Bisa diklaim (dengan batasan)
- Sistem memiliki komponen neuro-symbolic fungsional (rule engine + integrasi pipeline).
- Terdapat bukti negative result yang terdokumentasi (nilai ilmiah tinggi jika jujur).

### Belum bisa diklaim
- Akurasi final pada N=82 yang reproducible.
- Superioritas arsitektur advanced orchestration.
- Validitas ablation lintas baseline kompetitif.

### Tidak boleh diklaim sebelum perbaikan
- Generalisasi Q1-level performance tanpa evaluasi independen dan governance dataset yang konsisten.

---

## 9) Instruksi untuk Agent Berikutnya (Non-disruptive Execution)

1. Sinkronkan dataset governance:
   - buat `benchmark_manifest.json`;
   - cocokkan isi dataset aktif dengan klaim dokumen;
   - perbaiki label nama file yang menyesatkan.
2. Refactor test harness:
   - mock `llm.invoke` untuk pipeline unit tests;
   - pisahkan suite offline vs online.
3. Rehab baseline ablation:
   - hilangkan template fallback sebagai jawaban utama;
   - validasi output baseline pada sampel kecil dengan log artefak.
4. Update dokumen status (`CLAUDE.md`, `docs/task_registry.md`, `docs/testing_framework.md`) dengan tanggal `as_of` eksplisit.

Jika empat langkah ini belum selesai, jangan lanjut ekspansi fitur baru.

---

## 10) Mode Operasional Biaya API (Instruksi Owner)

Efektif mulai 2026-02-08:
1. Default mode adalah **tanpa API berbayar** (DeepSeek/Kimi/offline-first).
2. Jika ada blocker kritis yang benar-benar butuh API, agent wajib meminta persetujuan eksplisit owner terlebih dahulu.
3. Saat meminta persetujuan, agent wajib menyebut:
   - tujuan pemanggilan API,
   - artefak yang akan dihasilkan,
   - estimasi jumlah call atau token,
   - alasan kenapa alternatif offline tidak cukup.
4. Untuk kebutuhan eksplorasi non-kritis, prioritaskan jalur non-API dulu (analisis lokal, replay artefak, dan review berbasis dokumen).
