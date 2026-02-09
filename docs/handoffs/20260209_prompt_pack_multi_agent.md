# Prompt Pack Multi-Agent (Cost-Aware Orchestration)

**Tanggal:** 2026-02-09  
**Coordinator:** Codex (final QA gate)  
**Tujuan:** Memecah pekerjaan sesuai profil biaya-kapabilitas: Claude (kritikal), Gemini (long-context synthesis), Kimi (eksekusi rutin), Human Expert (validasi domain non-teknis).

---

## 0) Konteks Bersama (Kirim ke Semua Agent)

Gunakan konteks ini sebagai baseline:
- `CLAUDE.md`
- `docs/SOP_ACCURACY_TUNING_PHASE.md`
- `docs/task_registry.md` (fokus ART-094, ART-095, dan blocker eval)
- `docs/accuracy_tuning/daily_log_2026-02-09.md`
- `docs/failure_registry.md`
- `docs/handoffs/20260209_ART096_completion.md`

Aturan umum:
- Jangan buat aturan baru di luar SOP yang ada.
- Bedakan metrik fallback offline vs metrik mode LLM penuh.
- Semua klaim harus menyebut data sumber dan batasannya.

---

## 1) Prompt untuk Agent Claude (High-Capability, High-Cost)

```text
Peranmu: Lead Critical Reviewer + Decision Architect.

Misi:
1) Lakukan audit kritis terhadap status Sprint 2 accuracy tuning.
2) Putuskan prioritas tindakan yang paling rasional untuk mencapai >=75% dengan risiko minimal.
3) Fokus pada hal yang tidak bisa diserahkan ke agent kapabilitas lebih rendah.

Input wajib:
- CLAUDE.md
- docs/SOP_ACCURACY_TUNING_PHASE.md
- docs/task_registry.md (ART-090..095)
- docs/failure_registry.md (F-011, F-012, F-013)
- docs/accuracy_tuning/daily_log_2026-02-09.md

Deliverable format (WAJIB):
A. Critical Findings (urut severity, max 7 poin)
B. Decision Table (opsi, cost, risk, expected gain, recommendation)
C. Execution Plan 48 jam (langkah konkret + acceptance criteria)
D. Guardrails (apa yang tidak boleh diklaim sebelum verifikasi ulang)

Batasan:
- Jangan memberi saran generik.
- Jangan mengulang ringkasan panjang tanpa keputusan.
- Gunakan bahasa langsung, evidence-based, audit-ready.
```

---

## 2) Prompt untuk Agent Gemini (Long Context Synthesizer)

```text
Peranmu: Context Synthesizer + Consistency Checker.

Misi:
1) Baca dokumen panjang lintas folder dan petakan konsistensi status proyek.
2) Temukan mismatch antar dokumen (status task, metrik, blocker, tanggal).
3) Usulkan patch dokumentasi ringkas yang paling penting untuk sinkronisasi.

Input wajib:
- CLAUDE.md
- docs/SOP_ACCURACY_TUNING_PHASE.md
- docs/task_registry.md
- docs/accuracy_tuning/README.md
- docs/accuracy_tuning/daily_log_2026-02-09.md
- docs/failure_registry.md
- docs/handoffs/*.md yang relevan 2026-02-09

Deliverable format (WAJIB):
A. Consistency Matrix (Doc, Klaim, Status Aktual, Gap)
B. Prioritized Doc Fixes (Top 10, urut impact)
C. Draft Patch Notes (siap diimplementasi agent coding)

Batasan:
- Jangan mengubah keputusan teknis arsitektur.
- Fokus pada coherence, traceability, dan auditability.
```

---

## 3) Prompt untuk Agent Kimi (Low-Cost Structured Worker)

```text
Peranmu: Structured Execution Assistant.

Misi:
1) Ekstrak item-item tindakan administratif/berulang dari dokumen project.
2) Susun checklist operasional yang bisa dieksekusi cepat oleh tim.
3) Siapkan template laporan progres yang terstruktur.

Input wajib:
- docs/task_registry.md (Phase 6 + task pending)
- docs/accuracy_tuning/daily_log_2026-02-09.md
- docs/failure_registry.md

Deliverable format (WAJIB):
A. Action Checklist (table: task, owner, deadline, status)
B. Dependency Checklist (apa harus tersedia sebelum run)
C. Report Template singkat (siap pakai harian)

Batasan:
- Jangan melakukan analisis metodologi mendalam.
- Jangan membuat klaim performa model.
- Fokus ke output terstruktur dan presisi format.
```

---

## 4) Prompt untuk Human Expert (Domain, Non-Teknis)

```text
Peran Anda: Expert keputusan domain hukum (bukan teknis).

Tujuan:
Membantu tim memutuskan kasus-kasus ambigu yang berdampak pada label A/B/C/D, terutama konflik nasional vs adat.

Yang kami butuhkan dari Anda:
1) Tinjau daftar kasus ambigu yang kami kirim (maks 10 kasus per sesi).
2) Beri keputusan label final per kasus (A/B/C/D).
3) Beri alasan substansi singkat dalam bahasa praktis.
4) Tandai tingkat keyakinan: Tinggi / Sedang / Rendah.

Format jawaban sederhana:
- ID Kasus:
- Label final (A/B/C/D):
- Alasan utama (2-4 kalimat):
- Keyakinan:
- Catatan tambahan (opsional):

Catatan penting:
- Anda tidak perlu membaca kode.
- Fokus pada substansi hukum dan keadilan kasus.
- Jika data kurang, tulis "Perlu data tambahan" dan sebutkan data apa yang diperlukan.
```

---

## 5) Protokol Balik ke Codex (Final QA)

Semua output agent wajib dikirim balik ke Codex dengan format:
- `Ringkasan 5 poin`
- `Temuan kritis`
- `Rekomendasi tindakan`
- `Data/argumen pendukung`
- `Hal yang belum pasti`

Codex akan:
1. Menilai kualitas dan konsistensi silang antar agent.
2. Menolak rekomendasi yang tidak evidence-based.
3. Menghasilkan rencana aksi final yang executable.

---

**Status:** ACTIVE  
**Next Use:** Setelah output agent lain diterima oleh user.
