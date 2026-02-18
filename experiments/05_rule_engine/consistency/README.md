# P-008 Consistency Artifacts

Folder ini menyimpan artefak audit konsistensi antara aturan expert-verified JSON dan encoding ASP.

## Cara Re-run Audit (Bali)

```bash
python scripts/check_asp_json_consistency.py \
  --domain bali \
  --out-json experiments/05_rule_engine/consistency/bali_asp_json_consistency_YYYY-MM-DD.json \
  --out-md docs/handoffs/YYYYMMDD_p008_bali_asp_json_consistency.md
```

## Interpretasi Status

- `COVERED`: indikator aturan JSON terdeteksi penuh di ASP.
- `PARTIAL`: sebagian indikator ditemukan, tetapi ada elemen aturan yang belum eksplisit.
- `GAP`: indikator aturan tidak ditemukan di ASP saat audit.

## Catatan

Audit ini bersifat rule-indicator parity check (static pattern-based), bukan pengganti uji inferensi end-to-end pada test cases.
