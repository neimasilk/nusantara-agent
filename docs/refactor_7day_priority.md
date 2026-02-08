# Refactor Minimum 7 Hari — Prioritas Pasca Mata Elang Review

**Tanggal**: 2026-02-08
**Sumber**: `review.md` + verifikasi langsung
**Prinsip**: Perbaiki yang mengancam defensibility Q1. Jangan perbaiki yang nice-to-have.

---

## Prioritas Dikerjakan (urut dampak)

### Hari 1-2: Symbolic Core Repair [DONE]

**Status: SELESAI** — Diperbaiki dalam sesi ini.

- [x] Ganti placeholder facts di `nasional.lp`, `bali.lp`, `jawa.lp`, `minangkabau.lp` dengan `#defined` directives
- [x] Fix pipeline key mismatch (`graph_context`, `vector_context` ditambahkan ke return dict)
- [x] Verifikasi: 78/79 test pass (dari sebelumnya 66/79)

**Dampak ke paper**: Klaim "neuro-symbolic anchor" sekarang didukung oleh test yang pass. Sebelumnya, placeholder facts membuat symbolic core menghasilkan model yang tidak valid.

### Hari 2-3: Re-run Exp 05 (Symbolic Divergence)

- [ ] Jalankan ulang `experiments/05_symbolic_divergence/run_experiment.py` dengan ASP files yang sudah diperbaiki
- [ ] Bandingkan hasil divergence rate baru vs baseline 33.3%
- [ ] Update `experiments/05_symbolic_divergence/analysis.md` dengan hasil baru
- [ ] Jika divergence rate berubah signifikan, update klaim di CLAUDE.md

**Dampak**: Exp 05 adalah bukti utama bahwa symbolic anchor mencegah halusinasi. Jika hasil berubah setelah fix, klaim lama harus direvisi.

### Hari 3-4: Validasi Baseline B1-B5

- [ ] Audit `experiments/09_ablation_study/baselines/_common.py` — pastikan `fallback_answer()` bukan sekadar template
- [ ] Fix B4 (`b4_no_rules.py`) yang membaca `graph_context`/`vector_context` dari pipeline — sekarang key ini tersedia setelah fix
- [ ] Jalankan setiap baseline (B1-B5) pada minimal 5 kasus sampel untuk verifikasi output masuk akal
- [ ] Dokumentasikan output aktual per baseline di `experiments/09_ablation_study/baseline_outputs/`

**Dampak**: Reviewer akan langsung menolak ablation study dengan strawman baselines. B1 minimal harus melakukan actual LLM prompting, bukan fallback template.

### Hari 4-5: Pipeline Test Robustness

- [ ] Fix `test_pipeline_consensus` — query terlalu ambigu untuk LLM router. Opsi:
  - (a) Ubah query menjadi lebih eksplisit tentang consensus, atau
  - (b) Mark test sebagai `@unittest.skip("LLM-dependent")` dan buat test deterministik terpisah yang mock router
- [ ] Tambah test untuk edge case: query kosong, query non-hukum, query bahasa Inggris
- [ ] Pastikan `test_nusantara_pipeline.py` konsisten dengan return dict aktual

**Dampak**: Test yang flaky mengikis kepercayaan pada CI pipeline. Reviewer bisa mempertanyakan reproducibility.

### Hari 5-6: Data Governance Manifest

- [ ] Buat `data/benchmark_manifest.json` dengan format:
  ```json
  {
    "version": "1.0",
    "total_cases": 82,
    "created_date": "2026-02-08",
    "sources": [...],
    "per_case": [
      {"id": "TC-XX-YYY", "domain": "...", "gold_label": "...", "annotator_1": "...", "annotator_2": "...", "consensus": "..."}
    ]
  }
  ```
- [ ] Hash dataset untuk reproducibility: `sha256sum data/benchmark/*.json`
- [ ] Cross-check jumlah kasus di manifest vs gold standard report (82 kasus)

**Dampak**: Tanpa data manifest, reviewer akan mempertanyakan data provenance. Ini minimum untuk reproducibility.

### Hari 6-7: CLAUDE.md dan Documentation Sync

- [x] Update test coverage count (60 → 78/79)
- [x] Fix ART-049/ART-056 status (PENDING → DONE)
- [x] Update phase 4 summary count
- [ ] Review semua tanggal 2026-02-09 — normalkan ke tanggal aktual atau beri catatan
- [ ] Audit `docs/methodology_fixes.md` — update setiap item dengan status terkini
- [ ] Pastikan `docs/testing_framework.md` sesuai dengan jumlah tes aktual

---

## Tidak Dikerjakan Minggu Ini (DEFER)

| Item | Alasan | Trigger untuk Revisit |
|------|--------|----------------------|
| Exp 06 independent evaluation | Butuh human annotation yang belum selesai | Ketika batch annotasi berikutnya selesai |
| Debate protocol v2 | Exp 07 negative result masih valid | Ketika baseline accuracy >80% |
| Scale to 200+ test cases | Butuh lebih banyak gold standard | Ketika inter-rater agreement >0.6 (Fleiss kappa) |
| Human variability formal model | Data belum cukup | Ketika ahli ke-3 selesai semua batch |
| Advanced orchestration justification | Cost-benefit belum terbukti | Ketika sequential baseline sudah optimal |

---

## Kriteria Keberhasilan Sprint Ini

Pada akhir 7 hari, proyek harus bisa menjawab:

1. "Apakah symbolic core menghasilkan model yang valid?" → Ya, dibuktikan 32/32 rule engine tests pass
2. "Apakah test suite reliable?" → Ya, 78/79 pass (1 LLM-dependent, documented)
3. "Apakah status tracking akurat?" → Ya, CLAUDE.md dan registry konsisten
4. "Apakah baselines bukan strawman?" → Tergantung hasil audit hari 3-4
5. "Apakah data provenance terdokumentasi?" → Tergantung hasil manifest hari 5-6
