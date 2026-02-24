# Audit Kegagalan Domain Jawa (Strategic Review)

**Tanggal:** 2026-02-24  
**Owner konteks:** Mukhlis Amien (Research Lead)  
**Artefak utama:** `experiments/09_ablation_study/jawa_failure_audit_2026-02-24.json`

---

## Tujuan

Menutup kritik `ME-022` secara operasional: mendiagnosis underperformance domain Jawa dengan metrik yang dapat diuji ulang, lalu menentukan intervensi minimal (simple, testable, fail-fast).

---

## Reproducibility

Perintah:

```bash
python scripts/audit_jawa_failures.py
```

Input default yang diaudit:
1. Canonical 2026-02-20: `asp_only`, `ollama/deepseek-r1`, `deepseek_api`
2. Exploratory 2026-02-23: `asp_only`, `gpt-oss:20b`, `qwen3-14b`

Catatan data:
1. Domain map berisi 17 kasus Jawa.
2. Semua run hanya memuat 16 kasus Jawa evaluable (ID `GS-0032` tidak muncul, konsisten di semua backend).

---

## Ringkasan Angka Inti (Jawa, N=16 evaluable/run)

| Backend | Akurasi | Benar |
|---|---:|---:|
| canonical ASP-only | 31.25% | 5/16 |
| canonical Ollama deepseek-r1 | 25.00% | 4/16 |
| canonical DeepSeek API | 50.00% | 8/16 |
| exploratory ASP-only | 37.50% | 6/16 |
| exploratory gpt-oss:20b | 56.25% | 9/16 |
| exploratory Qwen3-14B | 43.75% | 7/16 |

---

## Temuan Kritis (Hard Findings)

1. **B->A di Jawa adalah kegagalan struktural, bukan sekadar pemilihan model.**  
   Tiga kasus (`GS-0019`, `GS-0020`, `GS-0031`) muncul sebagai B->A di **semua 6 backend** (termasuk ASP-only dan DeepSeek API).  
   Implikasi: ganti backend saja tidak akan menyelesaikan akar masalah.

2. **Canonical local backend (`deepseek-r1` via Ollama) adalah titik terlemah saat ini.**  
   Akurasi 25.00% (4/16), lebih buruk dari canonical ASP-only 31.25%.  
   Ini menandakan layer adjudikasi lokal saat ini menambah noise pada domain Jawa.

3. **Error conflict handling di Jawa terbelah dua, tetapi dominan di upstream.**  
   Agregat canonical:
   - `router_or_fact_extraction`: 8 kejadian
   - `adjudication_collapse_after_conflict`: 1 kejadian  
   Artinya bottleneck utama tetap di deteksi/ekstraksi konflik sebelum adjudikasi.

4. **National-dominance bias konsisten tinggi.**  
   `national_dominance_bias` muncul 9 kali pada agregat canonical dan 9 kali pada agregat exploratory.  
   Ini konsisten dengan pola Jawa: terminologi hukum nasional menelan sinyal adat bilateral.

5. **Instrumentation gap pada exploratory gpt-oss:20b.**  
   Ada 3 kasus `C->D` dengan `conflict_signal=unknown` dan `decision_step=unknown` (`CS-JAW-015`, `CS-JAW-019`, `CS-JAW-030`).  
   Akurasi tertinggi exploratory (56.25%) tetap perlu dibaca hati-hati karena metadata reasoning tidak lengkap.

---

## Dampak Ke Klaim Paper

1. **Boleh diklaim:** domain Jawa masih unresolved dan error pattern-nya reproducible lintas backend.
2. **Tidak boleh diklaim:** bahwa underperformance Jawa dapat diselesaikan hanya dengan pemilihan LLM yang lebih kuat.
3. **Konsekuensi desain:** intervensi pertama harus diarahkan ke router/fact extraction + guard adjudikasi, bukan menambah rule ASP secara masif.

---

## Intervensi Minimal yang Testable (Fail-Fast)

1. **Jawa Guard v1 (Prompt-Level):**  
   Jika kasus Jawa memiliki sinyal adat bilateral kuat dan `konflik_terdeteksi != Ya`, maka label `A` diblok kecuali ada dasar nasional eksplisit yang keras.

2. **Router Conflict Lexicon Patch (Small Scope):**  
   Tambah/mapping keyword konflik Jawa yang saat ini lolos sebagai non-conflict, lalu uji khusus pada kasus C-domain Jawa.

3. **Reasoning Metadata Contract:**  
   Semua backend wajib mengeluarkan `konflik_terdeteksi` dan `langkah_keputusan`; run yang tidak memenuhi kontrak ditandai non-claimable untuk diagnosis layer.

---

## Acceptance Tests untuk Wave Berikutnya

1. Re-run subset Jawa dan targetkan **B->A pada tiga kasus shared** turun dari 3/3 menjadi <=1/3.
2. Untuk kasus gold `C` di Jawa, proporsi `router_or_fact_extraction` turun minimal 30% dari baseline canonical audit ini.
3. Tidak boleh ada `unknown` pada `conflict_signal`/`decision_step` untuk backend yang dipakai klaim metodologis.

---

## Keputusan Review

**Status:** `ADOPT_NOW` untuk diagnosis + intervensi minimal.  
**Rasional:** masalah bersifat struktural, reproducible, dan berisiko tinggi terhadap klaim generalisasi lintas domain jika tidak ditangani cepat.
