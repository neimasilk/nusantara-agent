# Eagle Review — Hard Critique, Redesign, and Cleanup Plan
**Tanggal:** 2026-02-07  
**Mode:** Kritik keras + desain ulang operasional

---

## 1. Temuan Kritis (Severity: CRITICAL)

### C-01 — Klaim readiness evaluasi masih rapuh secara epistemik
- Fakta:
  - `ART-031` masih `BLOCKED` karena `ART-028` dan `ART-030` belum selesai (`docs/task_registry.md`).
  - Auto-fill anotasi dan putusan sudah besar skalanya, tapi belum valid sebagai gold final (`docs/failure_registry.md`, F-010).
- Risiko:
  - Tim bisa salah membaca “siap operasional” sebagai “siap klaim ilmiah”.
- Tindakan:
  - Pisahkan terminologi: `operational_ready` vs `scientific_ready`.

### C-02 — Tidak ada guardrail test formal sebelumnya
- Fakta:
  - Sebelumnya repo belum punya suite test deterministik yang bisa dijalankan lintas device.
- Risiko:
  - Regressions di parser/routing/utilitas akan lolos dan merusak eksperimen berikutnya.
- Tindakan:
  - Framework testing ditambahkan (`tests/`, `scripts/run_test_suite.py`, `docs/testing_framework.md`).

### C-03 — Drift dokumentasi dari file handoff sementara
- Fakta:
  - Dokumen handoff bertanggal menumpuk di `docs/` root.
- Risiko:
  - Source of truth membengkak, onboarding agent/manusia menjadi ambigu.
- Tindakan:
  - Dokumen handoff dipindah ke `docs/archive/handoffs/2026-02-07/`.

---

## 2. Temuan Mayor (Severity: MAJOR)

### M-01 — Robustness parser output LLM belum konsisten
- Fakta:
  - Parser di pipeline debat sebelumnya rentan terhadap fenced output yang tidak tertutup rapih.
- Tindakan:
  - Ditambahkan parser fenced-content yang lebih aman di `src/agents/debate.py`.

### M-02 — Integrasi evaluator Anthropic berisiko salah konfigurasi
- Fakta:
  - Pendekatan lama menggunakan OpenAI client untuk Anthropic endpoint.
- Tindakan:
  - `src/evaluation/llm_judge.py` diperbarui: OpenAI-compatible provider dipisah dari Anthropic SDK native.

### M-03 — Duplikasi return dan technical debt kecil
- Fakta:
  - Return duplikat di `src/agents/debate.py`.
- Tindakan:
  - Return duplikat dihapus.

---

## 3. Desain Ulang Operasional (Multi-Agent, Multi-Human, Multi-Device)

### A. Multi-Agent
1. Semua parser output agent harus fail-safe (jangan crash bila JSON invalid).
2. Semua eksperimen agent wajib menyimpan artefak run index yang machine-readable.
3. Prompt iteration harus lewat subset regression queries tetap.

### B. Multi-Human
1. Task `HUMAN_ONLY` tidak boleh ditutup hanya berbasis auto-fill.
2. Label `DRAFT_NEEDS_HUMAN_REVIEW` harus dipertahankan sampai validasi ahli.
3. Task status hanya valid jika sinkron dengan bukti artefak + acceptance test.

### C. Multi-Device
1. Setiap kontributor wajib menjalankan `python scripts/run_test_suite.py`.
2. Dokumen sementara dipindahkan ke archive, bukan root docs.
3. Tidak ada update status task tanpa referensi artefak objektif.

---

## 4. Rencana Eksekusi 2 Minggu

1. Minggu 1:
   - Stabilkan test suite deterministik sampai hijau di seluruh device kolaborator.
   - Tambahkan smoke test subset untuk Exp 07 runner (N kecil).
2. Minggu 2:
   - Fokus ART-030 (putusan primer MA) agar blocker `ART-031` berkurang.
   - Jalankan audit kualitas annotation draft untuk memisahkan sample yang layak evaluasi awal.

---

## 5. Prinsip Cleanup

1. Arsipkan, jangan hapus brutal, untuk menjaga audit trail.
2. Root `docs/` hanya berisi dokumen operasional aktif.
3. Semua dokumen historis bertanggal dipindahkan ke `docs/archive/`.
