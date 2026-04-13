# External Peer Review Triage (Gemini)

**Tanggal:** 2026-02-24  
**Sumber kritik:** Review eksternal Gemini atas paper terbaru  
**Tujuan:** Menentukan kritik mana yang diadopsi, ditunda, atau diabaikan secara sadar.

---

## Ringkasan Keputusan

| ID | Kritik Ringkas | Keputusan | Alasan Inti |
|---|---|---|---|
| GEX-001 | Data contamination (70 kasus dipakai tuning + evaluasi) adalah red flag utama | ADOPT_NOW | Ini blocker metodologis paling kuat dan sudah didukung evidence internal paper + policy. |
| GEX-002 | Power statistik rendah (n=70, p non-signifikan) membuat klaim efektivitas belum kuat | ADOPT_NOW | Konsisten dengan analisis internal; wajib dipakai sebagai batas klaim. |
| GEX-003 | Gap performa domain Jawa perlu justifikasi yang lebih kuat | ADOPT_NOW | Ini risiko validitas eksternal lintas domain; perlu rencana testable. |
| GEX-004 | Framing lebih tepat sebagai pilot/resource benchmark daripada efficacy claim | ADOPT_NOW | Selaras dengan kondisi evidence saat ini dan memperkecil rejection risk. |
| GEX-005 | Pivot langsung target ke workshop/short paper sekarang juga | DEFER_WITH_TRIGGER | Belum wajib diputuskan sekarang; target Q1 tetap valid jika blocker data ditutup tepat waktu. |
| GEX-006 | Kekuatan novelty, transparansi, dan neuro-symbolic separation sudah kuat | ADOPT_NOW | Diterima sebagai narasi kekuatan inti yang dipertahankan. |

---

## Mekanisme Skoring Kritik

Skala mengikuti `docs/mata_elang_weekly_gate.md`:  
`priority = (severity + rejection_risk + evidence_strength + testability) - (cost + collab_disruption)`

| ID | Sev | Evid | Rej | Test | Cost | Disr | Priority | Keputusan |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| GEX-001 | 5 | 5 | 5 | 5 | 3 | 1 | 16 | ADOPT_NOW |
| GEX-002 | 4 | 5 | 5 | 5 | 2 | 1 | 16 | ADOPT_NOW |
| GEX-003 | 4 | 4 | 4 | 4 | 2 | 1 | 13 | ADOPT_NOW |
| GEX-004 | 4 | 4 | 4 | 5 | 1 | 1 | 15 | ADOPT_NOW |
| GEX-005 | 3 | 3 | 3 | 2 | 2 | 2 | 7 | DEFER_WITH_TRIGGER |
| GEX-006 | 2 | 4 | 2 | 2 | 1 | 1 | 8 | ADOPT_NOW |

---

## Dampak Ke Klaim Paper (Setelah Triase)

### Klaim yang tetap boleh dipertahankan
1. Kontribusi utama: formalisasi rule adat terverifikasi expert ke ASP lintas domain.
2. Kontribusi metodologis: neuro-symbolic pipeline menghasilkan perilaku lebih terkontrol dibanding pure neural.
3. Transparansi keterbatasan: non-significant results, failure modes, dan bias backend dilaporkan eksplisit.

### Klaim yang harus dibatasi
1. Klaim efektivitas kuantitatif harus diposisikan sebagai **pilot evidence**, bukan final efficacy proof.
2. Klaim generalisasi lintas domain tidak boleh dinaikkan sebelum ada held-out/FUTURE TEST yang bersih.

### Klaim yang belum boleh dibuat
1. Superioritas statistik yang konklusif terhadap baseline (power belum memadai).
2. Generalizability beyond development-contaminated set.

---

## Action Items yang Diadopsi

1. Pertahankan framing paper sebagai **pilot/resource benchmark** sampai FUTURE TEST tersedia.
2. Pertahankan gate keras bahwa `scientific_claimable` tidak boleh dipakai jika manifest governance belum koheren.
3. Jalankan audit khusus domain Jawa:
   - ukur kontribusi error router vs adjudication layer per label (A/B/C/D),
   - catat confusion patterns yang reproducible,
   - siapkan rekomendasi prompt/rule minimal yang testable.
4. Siapkan strategi venue dua jalur:
   - Jalur utama: Q1 journal (tetap),
   - Jalur kontinjensi: workshop/short paper jika blocker data tidak tertutup sebelum deadline internal.

---

## Trigger untuk Keputusan GEX-005 (Venue Pivot)

Keputusan pivot ke workshop/short paper dipicu jika salah satu kondisi terjadi:
1. Hingga **2026-03-15** belum ada FUTURE TEST set yang benar-benar unseen.
2. Hingga **2026-03-15** belum ada peningkatan power yang cukup untuk evaluasi utama.
3. Supervisor/co-author meminta submit cepat untuk hasil pilot tanpa menunggu ekspansi data.

Jika tidak ada trigger, target utama tetap Q1 journal.
