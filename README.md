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

## Status Terkini (2026-02-07)
*   `ClingoRuleEngine` (ASP) sudah fungsional di `src/symbolic/rule_engine.py` dengan 30+ aturan formal di `src/symbolic/rules/minangkabau.lp`.
*   Experiment 05 (Formal Rule Engine vs LLM) selesai: ditemukan 33.3% divergensi pada N=30 test cases.
*   Advanced agent architecture: parallel execution, debate, self-correction, dan routing tersedia di `src/agents/`.
*   Experiment 07 sudah dijalankan pada 12 query, namun advanced orchestration belum mengungguli baseline sequential (lihat `experiments/07_advanced_orchestration/analysis.md` dan F-009 di `docs/failure_registry.md`).
*   Token usage tracking terintegrasi di seluruh pipeline. Proyeksi biaya 6 model Kimi tersedia di `experiments/07_advanced_orchestration/kimi_budget_projection_from_probe.json`.
*   Draft rules di `data/rules/minangkabau_rules.json` (**DRAFT_NEEDS_HUMAN_REVIEW**).

## Milestone Berikutnya
1.  Jalankan Experiment 06 (Independent Evaluation Pipeline).
2.  Iterasi Experiment 07: perbaiki protokol debat berbasis evidence retrieval dan validasi dengan human annotation.
3.  Scaling: 10K+ triples, 200+ test cases, 3 domains.

## Struktur Direktori
*   `data/`: Penyimpanan data mentah (PDF Jurnal) dan olahan (Knowledge Graph dumps).
*   `src/`: Source code untuk agen, pipeline ekstraksi, dan logika orkestrasi.
    *   `src/agents/`: Orchestrator, debate, router, dan self-correction modules.
    *   `src/kg_engine/`: Pipeline konstruksi Knowledge Graph (DeepSeek extraction).
    *   `src/symbolic/`: Rule engine (ASP/Clingo) dan aturan formal hukum adat.
*   `docs/`: Dokumentasi tambahan.
*   `PRD_Nusantara_Agent.md`: Dokumen persyaratan produk dan roadmap penelitian.

## Memulai
1.  **Setup Environment:**
    Pastikan Python 3.11+ terinstall.
    ```bash
    pip install -r requirements.txt
    ```
2.  **Konfigurasi:**
    Salin `.env.example` ke `.env` dan masukkan API Key yang diperlukan (DeepSeek, dll).

## Tech Stack
*   **LLM & Reasoning:** DeepSeek API
*   **Orchestration:** LangGraph
*   **Symbolic Reasoning:** Clingo (ASP)
*   **Knowledge Graph:** Neo4j (planned)
*   **Vector DB:** Qdrant (planned)
