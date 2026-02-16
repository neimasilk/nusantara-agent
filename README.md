# Nusantara-Agent (Research Repository)

**Neuro-Symbolic Legal Reasoning with Expert-Verified Customary Law Rules**

> **PENTING:** Ini repositori riset ilmiah (bukan produk komersial) dengan target publikasi jurnal Scopus Q1, terutama *Knowledge-Based Systems* atau *Expert Systems with Applications*.

## Fokus Penelitian (Post-Pivot 2026-02-12)
1. **Knowledge Base:** 95 aturan hukum adat (Minangkabau, Bali, Jawa) yang diverifikasi expert.
2. **Formal Reasoning:** Encoding aturan ke ASP (Clingo) untuk mendeteksi konflik norma nasional vs adat.
3. **Empirical Evaluation:** Pembandingan LLM+Rules vs LLM-only pada kasus berlabel expert dengan pelaporan statistik yang defensible.

## Filosofi Riset
- **Simple is better:** Hanya komponen yang langsung berkontribusi ke klaim paper dipertahankan.
- **Fail fast, pivot early:** Hasil negatif didokumentasikan sebagai kontribusi ilmiah.
- **Serius dalam standar:** Semua klaim harus evidence-based dan reproducible.

## Status Terkini (as of 2026-02-16)
- `ClingoRuleEngine` aktif di `src/symbolic/rule_engine.py` dengan 95 aturan lintas 4 domain (`minangkabau`, `bali`, `jawa`, `nasional`).
- Gold-standard pool: 82 kasus; benchmark aktif: 24 kasus (14 agreed, 10 disputed menunggu adjudikasi lanjutan).
- Multi-agent debate/self-correction dicatat sebagai hasil negatif (F-009) dan **bukan** jalur utama paper.
- Test suite deterministic lulus `101/101` (`python scripts/run_test_suite.py`).
- Workflow default adalah offline-first; pemanggilan API berbayar hanya jika diperlukan dan disetujui owner.

## Milestone Prioritas
1. Adjudikasi 10 kasus `DISPUTED` oleh rater yang qualified.
2. Ekspansi benchmark ke 100+ kasus terlabel.
3. Re-run pembandingan LLM+Rules vs LLM-only dengan environment setara.
4. Uji statistik (McNemar + 95% CI) dan minimal satu model pembanding non-DeepSeek.

## Struktur Direktori
- `data/`: Artefak data mentah dan olahan (gold standard, benchmark, manifest).
- `src/`: Kode utama pipeline, rule engine, router, orchestrator.
- `experiments/`: Eksperimen terisolasi beserta artefak hasilnya.
- `docs/`: Dokumen metodologi, gate review, registry tugas/failure, handoff.
- `tests/`: Unit tests deterministic.

## Memulai
1. **Setup environment**
   ```bash
   pip install -r requirements.txt
   ```
2. **Konfigurasi**
   - Salin `.env.example` ke `.env`.
   - Isi kredensial yang diperlukan (mis. `DEEPSEEK_API_KEY`) jika menjalankan mode online.

## Tech Stack Aktif
- **Symbolic Reasoning:** Clingo (ASP)
- **LLM Integration:** DeepSeek API (opsional, controlled usage)
- **Orchestration:** LangGraph + offline fallback
- **Retrieval:** Local JSON/keyword fallback

> Catatan scope: Neo4j/Qdrant/GraphRAG dan CCS metric tidak termasuk scope aktif paper pasca-pivot.
