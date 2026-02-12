# Operator Sheet: Transkrip Hasil Interview ke CSV

Dokumen ini untuk operator teknis yang memindahkan jawaban kertas/PDF ahli ke file CSV ingest.

---

## 1) File Kerja

1. Template CSV:
   `data/processed/gold_standard/interview_online/interview_template_ahli4.csv`
2. Script ingest:
   `scripts/ingest_expert_interview_votes.py`

---

## 2) Mapping Isian Kertas -> Kolom CSV

| Isian Kertas/PDF | Kolom CSV |
|---|---|
| ID Kasus | `id` |
| Label Ahli-4 (A/B/C/D) | `label_ahli4` |
| Keyakinan | `confidence_ahli4` |
| Alasan singkat | `rationale_ahli4` |
| Referensi 1 | `reference_1` |
| Referensi 2 | `reference_2` |
| Tanggal sesi | `session_date` |
| Nama pewawancara | `interviewer_name` |

---

## 3) Checklist Sebelum Ingest

1. Semua `id` ada di dataset aktif.
2. Semua `label_ahli4` valid (`A/B/C/D`).
3. File tersimpan UTF-8.
4. Tidak ada baris kosong yang tidak sengaja.

---

## 4) Perintah Ingest

Mode aman (output file baru):

```bash
python scripts/ingest_expert_interview_votes.py --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4.csv --expert-id ahli4
```

Mode overwrite dataset aktif (hanya jika sudah diverifikasi):

```bash
python scripts/ingest_expert_interview_votes.py --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4.csv --expert-id ahli4 --in-place
```

---

## 5) Setelah Ingest

1. Rebuild manifest:

```bash
python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-08
```

2. Validasi manifest:

```bash
python scripts/validate_benchmark_manifest.py
```
