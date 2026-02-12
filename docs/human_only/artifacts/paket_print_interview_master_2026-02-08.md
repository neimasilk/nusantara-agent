# PAKET PRINT INTERVIEW MASTER
## Siap Diprint Besok (Mode Non-Teknis untuk Ahli Hukum)

Dokumen ini adalah checklist operasional agar sesi interview ahli berjalan cepat dan hasilnya bisa langsung di-ingest ke dataset.

---

## 1) Dokumen yang Dicetak

### Untuk Ahli-1, Ahli-2, Ahli-3
1. `docs/human_only/artifacts/paket_interview_online_ahli1_siap_print_2026-02-08.md`
2. `docs/human_only/artifacts/paket_interview_online_ahli2_siap_print_2026-02-08.md`
3. `docs/human_only/artifacts/paket_interview_online_ahli3_siap_print_2026-02-08.md`
4. Cetak 1 copy per ahli.

### Untuk Ahli-4 (adjudikasi kasus split)
1. `docs/human_only/artifacts/paket_interview_online_ahli4_split_siap_print_2026-02-08.md`
2. Cetak 1 copy.
3. Jika ada batch umum tambahan, pakai:
   `docs/human_only/artifacts/paket_interview_online_ahli4_siap_print_2026-02-08.md`

---

## 2) Urutan Eksekusi Sesi

1. Mulai dari Ahli-4 terlebih dahulu (menutup blocker split).
2. Lanjut Ahli-1/2/3 jika ada batch kasus baru.
3. Gunakan format jawaban ringkas:
   - pilih label `A/B/C/D`,
   - alasan maksimal 3 kalimat,
   - 1-2 referensi.

---

## 3) Setelah Interview Selesai (Operator Teknis)

### A. Siapkan template CSV (jika belum)

```bash
python scripts/export_split_cases_for_interview.py --expert-id ahli4
```

### B. Transkrip hasil paper/PDF ke CSV

File target:
`data/processed/gold_standard/interview_online/interview_template_ahli4.csv`

Panduan operator:
`docs/human_only/workflow/operator_transkrip_interview_ke_csv.md`

Kolom minimal yang wajib diisi:
1. `label_ahli4`
2. `confidence_ahli4`
3. `rationale_ahli4`
4. `session_date`
5. `interviewer_name`

### C. Ingest ke dataset (aman, output file baru)

```bash
python scripts/ingest_expert_interview_votes.py --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4.csv --expert-id ahli4
```

### D. Jika sudah diverifikasi, overwrite dataset aktif

```bash
python scripts/ingest_expert_interview_votes.py --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4.csv --expert-id ahli4 --in-place
```

---

## 4) Validasi Setelah Ingest

```bash
python scripts/validate_benchmark_manifest.py
```

Jika ingin audit ketat terhadap klaim referensi:

```bash
python scripts/validate_benchmark_manifest.py --require-reference-match
```

---

## 5) Catatan Praktis

1. Jangan mengubah file JSON gold standard secara manual.
2. Semua perubahan lewat script ingest agar jejak audit rapi.
3. Simpan hasil scan/foto lembar yang sudah ditandatangani sebagai arsip administratif.
