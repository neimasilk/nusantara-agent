# Error Analysis: C->B Misclassification Pattern

## 1. Volume Analysis

### Ringkasan C->B per sistem

| Sistem | Support gold=C | Pred=B (C->B) | Rasio C->B |
|---|---:|---:|---:|
| ASP-only | 31 | 10 | 32.3% |
| ASP+Ollama | 31 | 10 | 32.3% |
| ASP+DeepSeek | 31 | 9 | 29.0% |

### Confusion matrix (baris gold=C)

| Sistem | Pred=A | Pred=B | Pred=C | Pred=D |
|---|---:|---:|---:|---:|
| ASP-only | 3 | 10 | 18 | 0 |
| ASP+Ollama | 3 | 10 | 18 | 0 |
| ASP+DeepSeek | 2 | 9 | 20 | 0 |

Catatan traceability:
- Angka diambil dari `experiments/09_ablation_study/statistical_comparison_final_2026-02-20.json` (`modes.*.confusion_matrix`).
- Untuk Ollama, nilai `c_to_b_count=10` juga konsisten dengan `experiments/09_ablation_study/error_analysis_phase1.json`.

## 2. Domain Distribution

Total event C->B lintas sistem = 29 event (10+10+9).

| Domain | ASP-only | ASP+Ollama | ASP+DeepSeek | Total Event | Proporsi Event |
|---|---:|---:|---:|---:|---:|
| Minangkabau | 4 | 4 | 4 | 12 | 41.4% |
| Jawa | 2 | 3 | 2 | 7 | 24.1% |
| Bali | 1 | 1 | 2 | 4 | 13.8% |
| Nasional | 2 | 1 | 1 | 4 | 13.8% |
| Lintas | 1 | 1 | 0 | 2 | 6.9% |

Distribusi kasus unik (union, n=16):
- Minangkabau: 6 kasus (37.5%)
- Jawa: 4 kasus (25.0%)
- Bali: 3 kasus (18.8%)
- Nasional: 2 kasus (12.5%)
- Lintas: 1 kasus (6.2%)

Kesimpulan domain:
- Domain paling terdampak adalah **Minangkabau** (41.4% dari seluruh event C->B).

## 3. Linguistic Patterns

### Keyword adat yang dominan pada kasus C->B

| Keyword | Kasus unik (n=16) | Event C->B (n=29) | Contoh case_id |
|---|---:|---:|---|
| `kemenakan` | 4 | 8 | `CS-MIN-004`, `CS-MIN-005` |
| `mamak` | 4 | 7 | `CS-MIN-025`, `GS-0041` |
| `kaum` | 4 | 7 | `CS-MIN-004`, `CS-MIN-025` |
| `pusako` | 3 | 5 | `CS-MIN-005`, `GS-0041` |
| `ulayat` | 2 | 3 | `CS-LIN-052`, `GS-0036` |
| `druwe` | 2 | 2 | `GS-0049`, `GS-0048` |
| `gono-gini` | 1 | 1 | `GS-0049` |
| `awig-awig` | 1 | 1 | `GS-0049` |

### Pola "adat kuat tanpa konflik eksplisit"

Kasus dengan marker adat, tetapi tanpa kata konflik eksplisit (`konflik`, `bertentangan`, `sengketa`, `menggugat`, `menuntut`, `sementara`, `namun`, `vs`, `melawan`, `perselisihan`):
- `CS-MIN-015`
- `CS-MIN-025`
- `GS-0041`
- `GS-0049`

Besaran pola:
- 4/16 kasus unik (25.0%)
- 8/29 event C->B (27.6%)

Interpretasi:
- Ada pola konsisten bahwa sinyal adat kuat (mamak/kemenakan/pusako/druwe/awig-awig) dapat mendorong prediksi ke B ketika konflik nasional-adat tidak diekspresikan secara eksplisit.

## 4. Shared vs System-specific Failures

### Shared failure (terjadi di semua sistem)

Jumlah: **4 kasus**
- `CS-JAW-019`
- `CS-MIN-004`
- `CS-MIN-005`
- `GS-0041`

### Hanya terjadi di satu sistem

Jumlah: **7 kasus**
- `CS-NAS-041` (hanya ASP-only)
- `GS-0048` (hanya ASP-only)
- `GS-0049` (hanya ASP+Ollama)
- `CS-JAW-030` (hanya ASP+DeepSeek)
- `GS-0035` (hanya ASP+DeepSeek)
- `GS-0036` (hanya ASP+DeepSeek)
- `GS-0102` (hanya ASP+DeepSeek)

### Tambahan konteks split-case (dua sistem setuju)

Jumlah: **5 kasus**
- `CS-BAL-012`
- `CS-JAW-015`
- `CS-LIN-052`
- `CS-MIN-015`
- `CS-MIN-025`

Catatan traceability:
- Split-case di atas konsisten dengan `two_agree` dan `all_disagree` pada `experiments/09_ablation_study/statistical_comparison_final_2026-02-20.json`.

## 5. ASP Signal Analysis

Catatan predicate:
- String literal `nasional_adat_conflict` tidak ditemukan di codebase saat ini.
- Sinyal konflik ASP yang aktif direpresentasikan lewat atom bertipe `conflict*`, terutama:
  - `conflict_norm(nasional_vs_adat,...)` di `src/symbolic/rules/nasional.lp`
  - `conflict/2` di rule adat (termasuk `src/symbolic/rules/minangkabau.lp`)
- Pada hasil benchmark, sinyal ini terefleksi di field `reasoning.konflik_terdeteksi`.

### C->B vs sinyal konflik ASP (berdasarkan reasoning ASP-only)

| Sistem | Total C->B | ASP signal `Tidak` | ASP signal `Ya` |
|---|---:|---:|---:|
| ASP-only | 10 | 10 | 0 |
| ASP+Ollama | 10 | 9 | 1 |
| ASP+DeepSeek | 9 | 4 | 5 |

Agregat lintas event (n=29):
- ASP signal `Tidak`: 23 event (79.3%)
- ASP signal `Ya`: 6 event (20.7%)

Interpretasi layer error:
- Mayoritas error C->B terkait **ketiadaan sinyal konflik di layer ASP/fact extraction** (23/29 event).
- Subset error terjadi saat **sinyal konflik ASP sudah ada tetapi adjudikasi tetap memilih B** (6/29 event), paling terlihat di DeepSeek.

Kasus C->B dengan ASP signal `Ya`:
- `CS-BAL-012` (Ollama, DeepSeek)
- `CS-JAW-030` (DeepSeek)
- `GS-0035` (DeepSeek)
- `GS-0036` (DeepSeek)
- `GS-0102` (DeepSeek)

## 6. Actionable Recommendations

1. Terapkan **conflict-preserving gate** di post-adjudication (tanpa rule baru).
   - Jika output simbolik mengandung atom `conflict*`, default final label jangan turun ke B kecuali ada alasan eksplisit bahwa tidak ada klaim nasional yang berlawanan.
   - Target langsung: 6 event C->B yang saat ini terjadi meski sinyal konflik ASP sudah `Ya`.

2. Perkuat **fact/keyword extraction** untuk men-trigger rule konflik yang sudah ada.
   - Fokus pada pemetaan leksikal, bukan tambah ASP rule: contoh frasa `menjaminkan/jaminan bank` -> `action(...,collateral)`, frasa klaim komunal/kemenakan -> `action(...,communal_claim)`.
   - Ini relevan untuk cluster Minangkabau/Lintas yang dominan (41.4% + 6.9% event).

3. Re-kalibrasi prompt adjudikator untuk boundary C vs B.
   - Saat ini ada bias default "ragu C vs B -> B"; ubah menjadi "jika marker nasional dan adat sama-sama kuat, naikkan ke C".
   - Jalankan regression gate tetap pada set 16 kasus C->B (union) agar perbaikan tidak mengulang regresi tipe F-018 (mengejar coverage tapi menurunkan akurasi).

## Sumber Data yang Dipakai

- `experiments/09_ablation_study/error_analysis_phase1.json`
- `experiments/09_ablation_study/hard_cases_analysis_2026-02-19.json`
- `experiments/09_ablation_study/statistical_comparison_final_2026-02-20.json`
- `experiments/09_ablation_study/HARD_CASES_PAPER_SUMMARY.md`
- `src/symbolic/rules/minangkabau.lp`
- `experiments/09_ablation_study/results_fixed_asp_only_2026-02-20.json`
- `experiments/09_ablation_study/results_wordboundary_ollama_2026-02-20.json`
- `experiments/09_ablation_study/results_deepseek_rollback_2026-02-20.json`
- `experiments/09_ablation_study/case_id_domain_map.json`
- `data/processed/gold_standard/gs_active_cases.json`
