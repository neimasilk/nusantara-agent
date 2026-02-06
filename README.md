# Nusantara-Agent

**Neuro-Symbolic Agentic GraphRAG untuk Penalaran Hukum Pluralistik Indonesia**

> **Status:** Riset Aktif ("Serius tapi Santai")  
> **Target:** Scopus Q1 (Information Fusion / KBS)

## Visi Proyek
Nusantara-Agent adalah sistem Multi-Agent Retrieval-Augmented Generation (RAG) berbasis arsitektur Neuro-Simbolik yang dirancang untuk menavigasi kompleksitas hukum pluralistik di Indonesia (Hukum Nasional, Adat, dan Islam).

Proyek ini bukan sekadar pengembangan software, melainkan **penelitian eksperimental** untuk menjawab tantangan:
*   Bagaimana AI bernalar di tengah konflik norma?
*   Bagaimana membangun Knowledge Graph hukum adat dari teks antropologi yang tidak terstruktur?
*   Bagaimana mengukur "pemahaman budaya" (cultural alignment) dalam AI?

## Filosofi "Serius tapi Santai"
*   **Serius:** Target impak tinggi, metodologi rigor, kontribusi novel untuk komunitas ilmiah global.
*   **Santai:** Timeline fleksibel (6-12 bulan), mengutamakan intuisi peneliti, terbuka terhadap *trial and error* atau pivot di tengah jalan.

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