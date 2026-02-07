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
- `ART-025` belum memiliki output artefak (`data/annotation/guidelines.md`, `data/annotation/schema.json`).
- `ART-031` bergantung pada `ART-028`, `ART-029`, `ART-030` yang semuanya belum selesai.
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
  - `ART-025`: `IN_PROGRESS` -> `PENDING`
  - `ART-031`: `PENDING` -> `BLOCKED`
  - `ART-056`: `PENDING` -> `BLOCKED`
  - `ART-065`: `PENDING` -> `BLOCKED`
  - `ART-071`: `PENDING` -> `BLOCKED`
- Ditambahkan catatan progres untuk `ART-020` agar sesuai dengan evidensi artefak saat ini.

---

## Aksi Minimum Agar Kembali "Ready"

1. Selesaikan `ART-025` (guidelines + schema annotation).
2. Lanjutkan `ART-028/029/030` sebelum mencoba `ART-031`.
3. Tuntaskan `ART-049` sebelum mulai baseline config `ART-056`.
4. Siapkan artefak `ART-068/069/070` sebelum menjalankan `ART-071`.
