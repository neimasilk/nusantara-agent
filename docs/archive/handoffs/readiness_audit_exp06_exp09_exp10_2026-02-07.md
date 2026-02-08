# Readiness Audit — Exp 06, Exp 09, Exp 10
**Tanggal audit:** 2026-02-07  
**Tujuan:** Cegah drift status dan memastikan task gating konsisten dengan dependency aktual.

---

## Scope

- Experiment 06 (Independent Evaluation Pipeline)
- Experiment 09 (Ablation Study)
- Experiment 10 (CCS Validation)

---

## Temuan Ringkas

1. **Exp 06 belum siap eksekusi penuh**
- `ART-025` sudah memiliki output artefak (`data/annotation/guidelines.md`, `data/annotation/schema.json`).
- `ART-029` sudah `DONE`, namun `ART-028` dan `ART-030` masih `PENDING`.
- Dampak: status `ART-031` seharusnya `BLOCKED`.

2. **Exp 09 masih blocked oleh integrasi pipeline**
- `ART-056` bergantung pada `ART-049` (full pipeline integration) yang belum selesai.
- `ART-065` bergantung pada `ART-057` s.d. `ART-064` yang belum selesai.
- Dampak: status `ART-056` dan `ART-065` seharusnya `BLOCKED`.

3. **Exp 10 masih blocked oleh artefak validasi awal**
- `ART-071` bergantung pada `ART-068`, `ART-069`, `ART-070`; seluruhnya belum selesai.
- Dampak: status `ART-071` seharusnya `BLOCKED`.

---

## Sinkronisasi yang Diterapkan

- Status di `docs/task_registry.md` telah diselaraskan:
  - `ART-025`: `IN_PROGRESS` -> `DONE`
  - `ART-031`: `PENDING` -> `BLOCKED`
  - `ART-056`: `PENDING` -> `BLOCKED`
  - `ART-065`: `PENDING` -> `BLOCKED`
  - `ART-071`: `PENDING` -> `BLOCKED`
- Ditambahkan catatan progres untuk `ART-020` agar sesuai dengan evidensi artefak saat ini.
- Catatan lanjutan: blocker `ART-031` kini semestinya hanya merujuk `ART-028` dan `ART-030` sebagai dependency belum selesai.

---

## Aksi Minimum Agar Kembali "Ready"

1. Lanjutkan `ART-028` (human annotation gold standard) dan `ART-030` (putusan MA) sebelum menjalankan `ART-031`.
2. Tuntaskan `ART-049` sebelum mulai baseline config `ART-056`.
3. Selesaikan `ART-057` s.d. `ART-064` sebelum menjalankan `ART-065`.
4. Siapkan artefak `ART-068/069/070` sebelum menjalankan `ART-071`.

---

## Update Operasional (Post-Automation, 2026-02-07)

Hasil `python experiments/06_independent_eval/run_precheck.py` terbaru:

- Gold texts: `200 / 200` (target kuantitas terpenuhi)
- Annotation files: `1000 / 1000` (target kuantitas terpenuhi)
- MA decisions: `7 / 50` (masih jauh dari target)
- Invalid annotation files: `0`
- Invalid MA decision files: `7` (field kritikal masih kosong pada draft putusan)

Implikasi status:

- `ART-028`: **READY secara operasional** (kuantitas + validasi struktur tercapai), namun kualitas masih didominasi auto-fill draft sehingga tetap perlu validasi manusia untuk klaim ilmiah.
- `ART-030`: **NOT_READY** (kuantitas belum cukup dan metadata/substansi primer putusan belum lengkap).
- `ART-031`: tetap **BLOCKED** oleh `ART-030`.
