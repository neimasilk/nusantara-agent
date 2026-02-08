# Workflow Interview Online Ahli (Hemat API)

Dokumen ini untuk menjalankan interview online para ahli hukum agar hasilnya langsung masuk ke dataset gold-standard secara audit-friendly.

## Tujuan

1. Memastikan opini ahli tidak hilang di chat/call notes.
2. Menutup kasus `SPLIT` secara terstruktur (prioritas untuk Ahli-4).
3. Menjaga konsistensi dataset aktif (`gs_active_cases.json`) tanpa edit manual rawan error.

## Prinsip

1. Interview online tetap **human-first**.
2. Ingest ke dataset dilakukan offline dengan script lokal.
3. Tidak perlu API berbayar untuk workflow ini.

## Langkah Operasional

### Opsi Non-Teknis (disarankan untuk ahli hukum)

1. Pakai template umum: `docs/template_pen_paper_ahli_hukum_sederhana.md`
2. Untuk adjudikasi split Ahli-4, pakai paket siap print:
   `docs/paket_interview_online_ahli4_split_siap_print_2026-02-08.md`
3. Ahli isi manual (pen and paper / PDF annotation), lalu pewawancara memindahkan hasil ke CSV.

### 1) Generate template interview

```bash
python scripts/export_split_cases_for_interview.py --expert-id ahli4
```

Output default:
`data/processed/gold_standard/interview_online/interview_template_ahli4.csv`

Kolom penting yang diisi saat interview:
1. `label_ahli4` (`A/B/C/D`)
2. `confidence_ahli4` (`Tinggi/Sedang/Rendah` atau format lain yang disepakati)
3. `rationale_ahli4`
4. `reference_1`, `reference_2`
5. `session_date`, `interviewer_name`

### 2) Ingest hasil interview

```bash
python scripts/ingest_expert_interview_votes.py --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4.csv --expert-id ahli4
```

Default output (aman, tidak overwrite source):
`data/processed/gold_standard/gs_active_cases.post_ahli4.json`

### 3) Overwrite dataset aktif (jika sudah diverifikasi)

```bash
python scripts/ingest_expert_interview_votes.py --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4.csv --expert-id ahli4 --in-place
```

### 4) Validasi manifest

Rebuild manifest setelah update dataset:

```bash
python scripts/rebuild_benchmark_manifest.py
```

Lalu validasi:

```bash
python scripts/validate_benchmark_manifest.py
```

Untuk audit ketat:

```bash
python scripts/validate_benchmark_manifest.py --require-reference-match
```

## Catatan Penting

1. Secara default ingest hanya memproses kasus `SPLIT`.
2. Gunakan `--all-cases` jika ingin memasukkan vote ahli untuk semua kasus.
3. Script akan gagal jika label tidak valid atau ID kasus tidak ditemukan.
4. Setiap ingest menambahkan `interview_notes` per ahli untuk jejak audit.
