# Mata Elang Weekly Gate

Template untuk review strategis mingguan. Dijalankan 1x/minggu oleh agent kapabilitas tertinggi.
Tujuan: deteksi dini kegagalan struktural, bukan eksekusi harian.

## Prinsip

- Simple is better. Fail fast. Pivot early.
- Santai dalam waktu, serius dalam standar ilmiah.
- Review hanya menilai **delta sejak minggu lalu**, bukan memulai thread baru.

---

## 1. Gate Checklist (wajib setiap minggu)

### A. Symbolic Core Health
- [ ] Semua `.lp` files lolos parse test (0 UNSATISFIABLE tanpa input)
- [ ] Semua domain rule tests pass (`python -m unittest tests.test_rule_engine -v`)
- [ ] Tidak ada placeholder facts yang mempengaruhi logic (scan untuk `dummy`, unconditional global facts)

### B. Test Integrity
- [ ] Full test suite: `python -m unittest discover -s tests -p "test_*.py" -v`
- [ ] Jumlah test total: ___
- [ ] Jumlah pass: ___
- [ ] Jumlah fail: ___
- [ ] Angka di atas konsisten dengan klaim di CLAUDE.md (update jika tidak)

### C. Status Consistency
- [ ] CLAUDE.md "Current State" sesuai dengan `docs/task_registry.md`
- [ ] Tidak ada task DONE di registry yang masih BLOCKED di CLAUDE.md
- [ ] Phase summary counts (done/total) akurat
- [ ] Tanggal di artefak konsisten (tidak ada tanggal masa depan)

### D. Data Governance
- [ ] Benchmark dataset count terverifikasi: ___ kasus
- [ ] Gold standard file utuh dan consistent: `docs/human_only/artifacts/gold_standard_consensus_report_complete_82_cases_2026-02-08.md`
- [ ] Tidak ada test case baru ditambahkan tanpa provenance (siapa, kapan, sumber)

### E. Methodology Defensibility
- [ ] Klaim "neuro-symbolic" didukung oleh tes yang pass
- [ ] Tidak ada circular evaluation (DeepSeek mengevaluasi output DeepSeek)
- [ ] Baseline ablation bukan strawman (B1-B5 berjalan dan output valid)
- [ ] Experiment directories punya PROTOCOL.md dan REVIEW.md

---

## 2. Critique Registry

Semua kritik disimpan dengan field berikut:

| Field | Deskripsi | Skala |
|---|---|---|
| `severity` | Dampak jika diabaikan | 1-5 (5=fatal) |
| `evidence_strength` | Bukti pendukung kritik | 1-5 (5=empiris kuat) |
| `rejection_risk` | Risiko ditolak reviewer Q1 | 1-5 (5=pasti ditolak) |
| `testability` | Apakah bisa diverifikasi dengan tes | 1-5 (5=fully testable) |
| `cost` | Effort untuk memperbaiki | 1-5 (5=sangat mahal) |
| `collab_disruption` | Gangguan pada kolaborasi aktif | 1-5 (5=sangat mengganggu) |

### Skor Prioritas

```
priority = (severity + rejection_risk + evidence_strength + testability) - (cost + collab_disruption)
```

Range: -10 sampai +20. Semakin tinggi, semakin urgent.

---

## 3. Keputusan (hanya 3 pilihan)

| Keputusan | Artinya |
|---|---|
| **ADOPT_NOW** | Kerjakan minggu ini. Masuk ke sprint. |
| **DEFER_WITH_TRIGGER** | Tunda sampai trigger event terjadi. Wajib definisikan trigger. |
| **IGNORE_WITH_RATIONALE** | Abaikan. Wajib punya alasan eksplisit + expiry date review ulang. |

### Aturan

1. Setiap keputusan **wajib** menyebut dampak ke klaim paper (apa yang bisa/tidak bisa diklaim).
2. Kritik yang di-IGNORE wajib punya expiry date (max 2 minggu).
3. Kritik severity 5 (fatal) **tidak boleh** di-IGNORE tanpa persetujuan human lead.

---

## 4. Template Entry Mingguan

```markdown
## Week [YYYY-MM-DD]

### Delta dari minggu lalu
- [Apa yang berubah sejak review terakhir]

### Gate Results
- Symbolic Core: PASS/FAIL (detail jika fail)
- Test Integrity: NN/NN pass (delta: +X/-Y dari minggu lalu)
- Status Consistency: PASS/FAIL
- Data Governance: PASS/FAIL
- Methodology: PASS/FAIL

### Kritik Baru

| ID | Kritik | Sev | Evid | Rej | Test | Cost | Disr | Score | Keputusan |
|----|--------|-----|------|-----|------|------|------|-------|-----------|
| ME-XXX | ... | | | | | | | | |

### Kritik Lama (status update)
- ME-XXX: [update status, masih relevan?]

### Dampak ke Klaim Paper
- Bisa diklaim: [...]
- Belum bisa diklaim: [...]
- Tidak akan bisa diklaim tanpa: [...]
```

---

## 5. Baseline Minggu Pertama (2026-02-08)

### Gate Results
- Symbolic Core: **FAIL** (placeholder facts membuat bali.lp dan jawa.lp UNSATISFIABLE; nasional.lp conflict rules mati)
- Test Integrity: **66/79 pass** (13 fail: 10 rule engine, 3 pipeline) — klaim CLAUDE.md "60 passed" tidak akurat
- Status Consistency: **FAIL** (ART-049 DONE di registry tapi PENDING di CLAUDE.md; phase 4 summary 0 done)
- Data Governance: **PARTIAL** (82 kasus terdokumentasi, tapi provenance hash/date/owner belum ada per-case)
- Methodology: **PARTIAL** (Exp 06 masih placeholder; baseline B1 adalah fallback template bukan real prompting)

### Kritik (dari review.md)

| ID | Kritik | Sev | Evid | Rej | Test | Cost | Disr | Score | Keputusan |
|----|--------|-----|------|-----|------|------|------|-------|-----------|
| ME-001 | Symbolic core placeholder facts invalidate "anchor" claim | 5 | 5 | 5 | 5 | 2 | 1 | 17 | ADOPT_NOW |
| ME-002 | Status inconsistency CLAUDE.md vs registry | 3 | 5 | 3 | 5 | 1 | 1 | 14 | ADOPT_NOW |
| ME-003 | Test coverage claim mismatch | 4 | 5 | 4 | 5 | 1 | 1 | 16 | ADOPT_NOW |
| ME-004 | Pipeline key mismatch (graph/vector context) | 3 | 5 | 3 | 5 | 1 | 1 | 14 | ADOPT_NOW |
| ME-005 | Exp 06 still placeholder, no independent eval | 4 | 4 | 5 | 3 | 4 | 3 | 9 | DEFER_WITH_TRIGGER |
| ME-006 | Ablation baselines B1/B2 are strawman | 4 | 4 | 5 | 4 | 3 | 2 | 12 | ADOPT_NOW |
| ME-007 | Advanced orchestration not justified | 3 | 4 | 3 | 3 | 2 | 3 | 8 | DEFER_WITH_TRIGGER |
| ME-008 | Human variability not modeled as uncertainty | 3 | 4 | 4 | 2 | 3 | 2 | 8 | DEFER_WITH_TRIGGER |

### Trigger Definitions
- ME-005: Trigger ketika human annotation batch selesai ATAU ada alternatif evaluator tersedia
- ME-007: Trigger ketika baseline accuracy >80% dan debate protocol v2 ready
- ME-008: Trigger ketika ahli ke-3 selesai semua batch DAN data cukup untuk Fleiss kappa

### Dampak ke Klaim Paper
- **Bisa diklaim**: Arsitektur neuro-symbolic (setelah fix ME-001), multi-agent sequential, 95 aturan adat terverifikasi expert
- **Belum bisa diklaim**: Symbolic anchor mencegah halusinasi (perlu re-run Exp 05 setelah fix), ablation gain (B1-B5 belum valid)
- **Tidak akan bisa diklaim tanpa**: Independent evaluation (ME-005), proper ablation (ME-006), statistical significance (N>82)

---

## Week 2026-02-24

### Delta dari minggu lalu
- Review eksternal Gemini di-triase formal untuk menentukan adopsi kritik berbasis evidence, bukan reaksi instan.
- Gate governance runner benchmark diseragamkan (`scientific_claimable` fail-hard, split contract runtime aktif).
- Claim gate paper diperketat untuk membedakan angka canonical vs exploratory tanpa mematikan transparansi.
- Audit khusus domain Jawa telah dijalankan dengan artefak reproducible (`jawa_failure_audit_2026-02-24.json`) untuk mengeksekusi ME-022.
- Governance manifest benchmark direkonsiliasi: referensi benchmark aktif dibekukan ke 74 kasus dan validasi strict lulus (`errors=0`, `warns=0`).

### Gate Results
- Symbolic Core: PASS (tidak ada perubahan rule `.lp` minggu ini).
- Test Integrity: 118/118 pass.
- Status Consistency: PARTIAL (status inti selaras, tetapi sebagian dokumen historis masih memuat angka lama).
- Data Governance: PASS (manifest strict-check kini koheren, `count_matches_reference_claim=true`, scientific gate tidak lagi terblokir oleh mismatch referensi).
- Methodology: PARTIAL (kontaminasi dev/eval dan power statistik tetap blocker untuk efficacy claim penuh).

### Kritik Baru

| ID | Kritik | Sev | Evid | Rej | Test | Cost | Disr | Score | Keputusan |
|----|--------|-----|------|-----|------|------|------|-------|-----------|
| ME-020 | Data contamination membuat klaim akurasi rentan overfitting | 5 | 5 | 5 | 5 | 3 | 1 | 16 | ADOPT_NOW |
| ME-021 | Power statistik n=70 belum cukup untuk klaim konklusif | 4 | 5 | 5 | 5 | 2 | 1 | 16 | ADOPT_NOW |
| ME-022 | Domain Jawa underperformance butuh diagnosis yang lebih testable | 4 | 4 | 4 | 4 | 2 | 1 | 13 | ADOPT_NOW |
| ME-023 | Framing paper harus dominan sebagai pilot/resource benchmark | 4 | 4 | 4 | 5 | 1 | 1 | 15 | ADOPT_NOW |
| ME-024 | Pivot langsung ke workshop/short paper sekarang juga | 3 | 3 | 3 | 2 | 2 | 2 | 7 | DEFER_WITH_TRIGGER |

### Kritik Lama (status update)
- ME-005 (independent evaluation): masih relevan, belum tuntas karena FUTURE TEST set belum tersedia.
- ME-006 (baseline defensibility): status membaik, gate mode runner sudah diseragamkan.

### Trigger Definitions
- ME-024 diputuskan ulang jika hingga 2026-03-15 belum ada FUTURE TEST set unseen atau belum ada peningkatan power yang memadai.

### Dampak ke Klaim Paper
- Bisa diklaim: kontribusi rule base, kontribusi metodologis neuro-symbolic, serta transparansi failure/limitation.
- Belum bisa diklaim: efficacy superiority yang konklusif.
- Tidak akan bisa diklaim tanpa: data unseen baru dan power statistik yang lebih kuat.
