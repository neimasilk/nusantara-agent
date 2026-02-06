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

1.  **Shared Database (Neo4j):**
    Kita menggunakan Neo4j Aura (Cloud) atau shared instance agar semua komputer mengakses graf yang sama.
2.  **Shared Vector DB (Qdrant):**
    Gunakan shared Qdrant collection untuk memastikan pencarian semantik konsisten lintas perangkat.
3.  **Communication:**
    Gunakan GitHub Issues untuk melacak bug dan ide-ide eksperimen baru.

## 5. Filosofi Kerja Terdistribusi
- **Atomic Experiments:** Simpan setiap percobaan di folder `experiments/` dengan dokumentasi lengkap agar peneliti lain bisa mereplikasi hasilnya di komputer mereka.
- **Fail Fast, Pivot Early:** Jika hasil eksperimen di komputer Anda menunjukkan kegagalan teknis yang signifikan, dokumentasikan segera di `docs/critique_and_risk_assessment.md`.
