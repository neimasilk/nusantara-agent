# AGENT MATA ELANG - Strategic Review (2026-02-20)

## 1. Executive Summary
- Klaim utama masih terlalu besar untuk data saat ini. Delta ASP-only vs ASP+LLM hanya +5.7pp (58.6% -> 64.3%), dan McNemar tidak signifikan (`p=0.344`), jadi belum cukup kuat untuk narasi "clear improvement" level Q1.
- Power statistik rendah. Dengan pola discordant saat ini (3 vs 7), estimasi power hanya ~0.24; untuk power ~0.8 dibutuhkan kira-kira **275-344 kasus evaluable** (bukan 70).
- Risiko terbesar bukan LLM backend, tapi desain keputusan: error dominan `C->B` (10/25 wrong) dan D-recall 0% (0/2). Sistem masih gagal pada konflik implisit dan abstention.
- Ada confound evaluasi lintas-backend: angka DeepSeek 67.1% berasal dari run 2026-02-19 (pre-rollback), sedangkan angka Ollama canonical 64.3% dari 2026-02-20 (post-rollback). Ini bukan perbandingan apples-to-apples.
- Arsitektur kolaborasi multi-agent rawan distorsi karena human-relay tanpa contract test antar-agent. Tanpa quality gate formal, cascade error bisa lolos ke paper.

## 2. Temuan per Dimensi

### 2.1 Validitas Klaim Ilmiah
- **"Neuro-symbolic"**: valid sebagai **weak neuro-symbolic** (symbolic outputs dipakai sebagai konteks adjudikasi LLM), tetapi belum valid untuk klaim kuat tentang symbolic constraint enforcement end-to-end.
- **Efek 64.3 vs 58.6**: belum cukup untuk klaim efektivitas kuat.
  - McNemar ASP-only vs Ollama: discordant `3 vs 7`, `n_dis=10`, `p_exact=0.3438`.
  - McNemar ASP-only vs DeepSeek: `6 vs 12`, `n_dis=18`, `p_exact=0.2379`.
- **Kecukupan n=70**: tidak memadai untuk power 0.8 pada effect size saat ini.
  - Estimasi kebutuhan total (berdasarkan data aktual): ~344 (ASP-only vs Ollama), ~275 (ASP-only vs DeepSeek).
- **"Expert-verified" dengan 2 ahli**: cukup untuk pilot, belum cukup untuk klaim kuat Q1 tanpa:
  - kappa final di seluruh set evaluasi,
  - protokol adjudikasi stabil,
  - rater cadangan.
- **Klaim yang belum disangga data/statistik di paper**:
  - `paper/main.tex` masih punya beberapa `[PENDING]` (Cohen's kappa Ollama, McNemar table, Fleiss kappa, agreement counts).
  - Ada inkonsistensi angka agreement expanded batch (`94.6%` di abstrak vs `94.0%` di tabel).
  - Cross-validation currently confounded oleh kondisi run yang berbeda (rule state/date berbeda).

### 2.2 Risiko Struktural Proyek
- **Single point of failure #1**: definisi operasional batas B vs C (terbukti dari `C->B` dominan).
- **Single point of failure #2**: ketergantungan pada benchmark kecil yang dipakai berulang untuk tuning prompt/rules (risk leakage/overfitting ke benchmark).
- **Circular dependency risk**: masih ada jejak tuning yang dipandu hasil benchmark sama; perlu strict split (development vs locked test).
- **Reproducibility risk**:
  - local Ollama model versioning (tag bisa drift),
  - API backend berubah dari sisi provider,
  - parser/prompt drift antar-hari.
- **Jika satu ahli keluar**: klaim "expert-verified" runtuh ke single-rater; reliability tidak dapat dipertahankan.

### 2.3 Arsitektur Kolaborasi Human-AI
- Pembagian peran saat ini fungsional, tapi **human relay** adalah bottleneck + noise channel.
- Risiko utama: informasi teknis tereduksi saat dipindahkan lintas agent (ringkasan handoff jadi titik distorsi).
- Tugas yang seharusnya human:
  - keputusan label boundary policy (A/B/C/D rubric governance),
  - accept/reject klaim paper.
- Tugas yang seharusnya AI:
  - verifikasi reproducibility numerik otomatis (CI, McNemar, kappa, artifact checks).
- **Cascade failure detection** saat ini lemah: satu error asumsi bisa diulang oleh agent lain karena referensi sama.
- Efisiensi allocation: masih ada over-dispatch task analitik ringan ke agent berbeda tanpa audit contract tunggal.

### 2.4 Testing Framework
- **Agent->Agent**: belum ada schema contract wajib untuk output yang dikonsumsi agent lain.
- **Agent->Human**: belum ada gate "evidence required" sebelum rekomendasi masuk keputusan.
- **Human->Agent**: prompt belum diperlakukan sebagai artifact versioned + replayable untuk consistency test.
- **Human->Human (expert annotator)**: kappa historis awal 0.394 menunjukkan rubric boundary harus diperlakukan sebagai komponen inti yang diuji rutin.

**Minimal viable test harness yang disarankan (wajib bulan ini):**
- `handoff_contract.json` schema: task_id, commit hash, rule-state hash, dataset hash, metrics, script command.
- `replay_benchmark.py`: menjalankan ulang command dari handoff dan memverifikasi checksum hasil.
- `claim_gate.py`: blokir update paper jika ada `[PENDING]`, mismatch angka, atau statistik utama belum terisi.
- `annotation_qa.py`: hitung Cohen's/Fleiss kappa per batch baru + alarm jika `< 0.6`.

### 2.5 Evaluasi Item untuk Penghentian/Pivot
- **Multi-agent debate protocol (F-009)**: **HENTIKAN** untuk jalur utama paper. Simpan sebagai negative result appendix.
- **Keyword-based router (vs learned classifier)**: **SEDERHANAKAN** sekarang (boundary-safe regex + threshold tuning), lalu ganti ke lightweight learned classifier setelah dataset >200.
- **Neo4j/Qdrant planned tapi belum diimplementasi**: **HENTIKAN** dari scope paper ini. Taruh di future work.
- **95 expert rules vs 71 encoded**: **SEDERHANAKAN** target; jangan kejar 100% coverage buta. Prioritaskan rule gap yang directly memperbaiki `C->B` dan D abstention.
- **D-label (hanya 2 kasus)**: **SEDERHANAKAN** klaim. Saat ini jangan laporkan "D performance" sebagai hasil utama; jadikan warning metric + perluasan data.

### 2.6 Seleksi Kritik (narasi)
- Problem inti bukan kurang agent atau kurang rule; problem inti adalah **evaluation discipline** dan **decision boundary quality**.
- Sampai ada locked test split + power memadai, paper harus diposisikan sebagai pilot metodologis, bukan efficacy claim.

## 3. Top 3 Recommended Actions Bulan Ini
1. **Lock evaluation protocol**: pisahkan `dev set` vs `locked test set`, freeze benchmark hash, dan larang tuning terhadap locked set.
2. **Naikkan sample + reliability bar**: target minimum 250-350 evaluable cases untuk power McNemar yang layak, plus kappa batch-level >=0.6.
3. **Serang bottleneck utama**: fokus eksklusif pada reduksi `C->B` dan aktivasi D-abstention (bukan tambah rule global atau tambah agent).

## 4. Criticism Triage Table

| Kritik | Severity | Effort to Fix | Verdict | Alasan |
|--------|----------|---------------|---------|--------|
| Klaim efektivitas terlalu kuat untuk n=70 | High | Medium | CRITICAL/FIX-NOW | Statistik utama belum signifikan; klaim harus diturunkan atau data ditambah |
| Cross-backend comparison confounded (rule-state/date beda) | High | Low | CRITICAL/FIX-NOW | Perbandingan tidak valid untuk kesimpulan ilmiah |
| Banyak placeholder `[PENDING]` di paper results/statistics | High | Low | CRITICAL/FIX-NOW | Risiko reject langsung pada review metodologi |
| Batas label B vs C tidak stabil (`C->B` dominan) | High | Medium | IMPORTANT/PLAN | Ini error paling mahal terhadap akurasi |
| D-label recall 0% dan data D sangat kecil | High | Medium | IMPORTANT/PLAN | Sistem tidak punya abstention capability yang kredibel |
| Human-relay antar-agent tanpa contract schema | Medium | Medium | IMPORTANT/PLAN | Memicu distorsi dan cascade error |
| Mengejar 95/95 encoding tanpa impact gating | Medium | Medium | IMPORTANT/PLAN | Sudah terbukti bisa menurunkan performa |
| Debate protocol tetap dipakai jalur utama | Medium | Low | IGNORE | Sudah ada negative result; cukup dokumentasikan sebagai gagal |
| Neo4j/Qdrant dimasukkan kembali ke scope paper ini | Low | Low | IGNORE | Tidak relevan dengan klaim inti saat ini |
| Menambah model backend baru sebelum protocol lock | Medium | Low | NICE-TO-HAVE | Tidak menyelesaikan masalah validitas inti |

## 5. Satu Pertanyaan untuk Human (sebelum review berikutnya)

Apakah Anda siap menetapkan **hard policy**: "mulai minggu depan, semua tuning rule/prompt hanya di dev set, dan locked test set tidak disentuh sampai milestone bulanan," ya/tidak?
