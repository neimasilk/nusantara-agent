# Collaboration Guide: Multi-Human & Multi-Agent Workflow

Dokumen ini menjelaskan protokol kerja untuk kolaborator (manusia) dan agen AI dalam ekosistem **Nusantara-Agent**.

## 1. Persiapan Environment Terdistribusi

Setiap komputer yang digunakan untuk pengembangan harus memiliki setup yang identik:

1.  **Python Version:** Gunakan Python 3.11+.
2.  **Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Environment Variables:**
    Dapatkan `DEEPSEEK_API_KEY` dari lead researcher dan simpan di `.env`. **JANGAN PERNAH** melakukan commit pada file `.env`.

## 2. Protokol Git & GitHub

1.  **Pull Before Work:** Selalu jalankan `git pull origin main` sebelum memulai pekerjaan untuk mendapatkan update dari peneliti lain atau agen otomatis.
2.  **Feature Branching:** Gunakan branch baru untuk eksperimen besar.
3.  **Descriptive Commits:** Tulis pesan commit yang menjelaskan *kenapa* perubahan dilakukan (misal: `Refine triple extraction prompt for Bali domain`).

## 3. Mekanisme Kerja Sama Manusia-AI (HITL)

Proyek ini mengandalkan **Human-in-the-Loop** untuk memastikan kualitas data hukum adat:

### A. Ekstraksi Data (AI Task)
- Agen menjalankan pipeline ekstraksi tripel dari PDF.
- Hasil disimpan di `data/processed/triples_[domain].json`.

### B. Validasi & Review (Human Task)
- Peneliti manusia membuka hasil JSON atau melihat visualisasi graf.
- Jika ada kesalahan relasi, peneliti memperbarui file `data/processed/human_feedback.json` atau langsung memperbaiki tripel yang salah.

### C. Refinement (AI Task)
- Agen membaca feedback manusia dan melakukan "fine-tuning" pada prompt atau logika reasoning untuk iterasi berikutnya.

## 4. Berbagi Resources (Shared Infrastructure)

1.  **Data Source of Truth (Aktif):**
    Gunakan artefak lokal terkelola (`data/processed/`, `data/benchmark_manifest.json`) sebagai sumber kebenaran lintas perangkat.
2.  **Graph/Vector Infra (Non-aktif untuk scope paper saat ini):**
    Neo4j/Qdrant tidak menjadi dependency operasional inti pasca-pivot. Jangan menjadikan keduanya sebagai blocker untuk task paper aktif.
3.  **Communication:**
    Gunakan GitHub Issues/PR untuk melacak bug, keputusan metodologi, dan perubahan task prioritas.

## 5. Review Gate Process

Setiap eksperimen dan deliverable WAJIB melalui review sebelum dianggap selesai:

### Layer 1: Self-Critique
- Peneliti (manusia atau AI) menjawab 10 pertanyaan devil's advocate dari `docs/review_protocol.md`
- Tulis hasilnya di `experiments/NN_nama/REVIEW.md`
- Minimum: jawaban substantif untuk setiap pertanyaan

### Layer 2: Adversarial AI Review
- Jalankan reviewer otomatis menggunakan LLM **INDEPENDEN** (bukan DeepSeek):
  ```bash
  python -m src.review.adversarial_reviewer experiments/NN_nama/
  ```
- Membutuhkan `ANTHROPIC_API_KEY` atau `OPENAI_API_KEY` di `.env`
- Output: `experiments/NN_nama/ai_review.json`

### Layer 3: Human Review
- Minimal 1 reviewer manusia membaca REVIEW.md + ai_review.json
- Keputusan: PASS / CONDITIONAL PASS / FAIL
- Dokumentasikan di bagian bawah REVIEW.md

### Kapan Review Diperlukan?
| Milestone | Layers yang Diperlukan |
|-----------|----------------------|
| Eksperimen selesai | Layer 1 + 2 |
| Integrasi ke pipeline | Layer 1 + 2 + 3 |
| Draft paper section | Layer 1 + 2 + 3 |
| Pre-submission | Layer 1 + 2 + 3 |

## 6. Task Assignment Protocol

Pekerjaan diorganisir sebagai Atomic Research Tasks (ART). Untuk scope aktif paper, gunakan `docs/task_registry_simplified.md`. `docs/task_registry.md` dipertahankan sebagai arsip lengkap historis.

### Cara Mengambil Task
1. Buka `docs/task_registry.md`
2. Cari task dengan status PENDING dan prerequisites yang sudah DONE
3. Periksa field **Executor** — pastikan kamu eligible (HUMAN_ONLY / AI_ONLY / EITHER)
4. Update status menjadi IN_PROGRESS dan isi "Assigned To"
5. Setelah selesai, update menjadi DONE

### Aturan Task
- Setiap task memiliki **Acceptance Test** — task baru DONE jika semua test pass
- Jika stuck, buat catatan di task description dan eskalasi
- Task yang memakan waktu > 4 jam harus dipecah menjadi sub-tasks
- Lihat `docs/task_template.md` untuk format lengkap

## 7. Failure Registry

Setiap kegagalan, hasil negatif, atau pendekatan yang ditinggalkan HARUS dicatat di `docs/failure_registry.md`:
- Kegagalan yang terdokumentasi bernilai ilmiah
- Failure registry menjadi sumber utama untuk Limitations section di paper
- Jangan menghapus entry — ini catatan historis

## 8. Filosofi Kerja Terdistribusi
- **Atomic Experiments:** Simpan setiap percobaan di folder `experiments/` dengan PROTOCOL.md, REVIEW.md, dan analysis.md agar peneliti lain bisa mereplikasi hasilnya.
- **Fail Fast, Pivot Early:** Jika hasil eksperimen menunjukkan kegagalan, dokumentasikan segera di `docs/failure_registry.md` dan `docs/critique_and_risk_assessment.md`.
- **No Circular Evaluation:** Jangan gunakan DeepSeek untuk mengevaluasi output DeepSeek. Gunakan LLM independen atau annotator manusia.
- **Quantify Everything:** Hindari bahasa kualitatif seperti "BERHASIL" tanpa metrik. Gunakan angka, statistical tests, dan confidence intervals.
