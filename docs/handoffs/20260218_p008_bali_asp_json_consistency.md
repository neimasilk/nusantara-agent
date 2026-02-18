# ASP vs JSON Consistency Report

- Date: 2026-02-18
- Domain: bali
- JSON: `data\rules\bali_rules.json`
- ASP: `src\symbolic\rules\bali.lp`

## Summary

- Total rules: 34
- COVERED: 21
- PARTIAL: 4
- GAP: 9

## GAP Rules

- BAL-022 (distribution_process): Prioritas biaya upacara sebelum distribusi belum ditemukan.
- BAL-025 (divorce_impact): Aturan dampak cerai khusus 'mulih daha' belum ditemukan.
- BAL-026 (divorce_impact): Aturan pasca cerai untuk anak belum ditemukan.
- BAL-027 (dispute_resolution): Prosedur sengketa internal keluarga belum ditemukan.
- BAL-028 (dispute_resolution): Prosedur eskalasi sengketa belum ditemukan.
- BAL-029 (contemporary_change): Perubahan kontemporer beda wangsa belum ditemukan.
- BAL-031 (contemporary_change): Aturan perkawinan pada gelahang belum ditemukan.
- BAL-033 (succession_exception): Ground disinherit karena alpaka guru belum ditemukan.
- BAL-034 (distribution_process): Mekanisme sisih 1/3 sebelum pembagian belum ditemukan.

## PARTIAL Rules

- BAL-014 (heir_rights_female): Hak dasar anak perempuan terencode, namun rasio maksimal 1/2 tidak eksplisit.
- BAL-017 (ownership): Larangan transfer luar desa ada, namun konsep hak pakai/hak kelola tidak eksplisit.
- BAL-019 (community_role): Syarat saksi prajuru spesifik untuk adopsi belum eksplisit; ada mekanisme saksi pada jiwa dana.
- BAL-024 (adoption): Hak waris anak angkat ada; kesetaraan kewajiban (sanggah/ngayah) belum eksplisit.
