# Nusantara-Agent (Research Repository)

**Neuro-Symbolic Agentic GraphRAG untuk Penalaran Hukum Pluralistik Indonesia**

> **🚨 PENTING:** Ini bukan proyek pengembangan software komersial. Repositori ini adalah **repositori riset ilmiah** dengan target publikasi pada jurnal internasional bereputasi (**Scopus Q1**: *Information Fusion*, *Knowledge-Based Systems*, atau *Expert Systems with Applications*).

## Fokus Penelitian
Fokus utama proyek ini adalah pada **kontribusi ilmiah** dan **novelty** di bidang AI & Hukum, mencakup:
1.  **Arsitektur Novel**: Integrasi Neuro-Simbolik dengan Multi-Agent GraphRAG untuk menangani konflik norma.
2.  **Konstruksi Pengetahuan**: Metodologi otomatisasi ekstraksi tripel dari teks hukum adat yang tidak terstruktur.
3.  **Metrik Baru**: Pengembangan *Cultural Consistency Score (CCS)* untuk mengukur keselarasan AI dengan budaya *high-context*.

## Filosofi Riset: "Serius tapi Santai"
*   **Serius:** Mengikuti metodologi ilmiah yang ketat (Rigorous), melakukan *Ablation Study*, dan memastikan *Reproducibility*.
*   **Santai:** Pendekatan eksperimental (Trial & Error). Kegagalan teknis dalam eksperimen dianggap sebagai temuan riset yang valid dan akan didokumentasikan sebagai limitasi atau *future work*.

## Struktur Direktori
*   `data/`: Penyimpanan data mentah (PDF Jurnal) dan olahan (Knowledge Graph dumps).
*   `src/`: Source code untuk agen, pipeline ekstraksi, dan logika orkestrasi.
    *   `src/agents/`: Definisi agen (Nasional, Adat, Supervisor).
    *   `src/kg/`: Pipeline konstruksi Knowledge Graph (DeepSeek extraction).
*   `notebooks/`: Eksperimen, prototyping, dan analisis data.
*   `docs/`: Dokumentasi tambahan.
*   `PRD_Nusantara_Agent.md`: Dokumen persyaratan produk dan roadmap penelitian.

## Memulai
1.  **Setup Environment:**
    Pastikan Python 3.11+ terinstall.
    ```bash
    pip install -r requirements.txt # (Akan datang)
    ```
2.  **Konfigurasi:**
    Salin `.env.example` ke `.env` dan masukkan API Key yang diperlukan (DeepSeek, dll).

## Tech Stack
*   **LLM & Reasoning:** DeepSeek API
*   **Orchestration:** LangGraph
*   **Knowledge Graph:** Neo4j
*   **Vector DB:** Qdrant