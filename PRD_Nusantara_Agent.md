# Product Requirements Document (PRD)
# Nusantara-Agent: Neuro-Symbolic Agentic GraphRAG untuk Penalaran Hukum Pluralistik Indonesia

**Versi:** 1.0  
**Tanggal:** 6 Februari 2026  
**Penulis:** Amien (STIKI/UBHINUS)  
**Status:** Eksperimentasi Tahap Awal — Riset Aktif  
**Klasifikasi:** Proyek Riset Fundamental & Eksperimental (Bukan Software Development)  
**Tujuan Akhir:** Kontribusi Ilmiah (Novelty) & Publikasi Jurnal Scopus Q1

---

## Daftar Isi

1. [Ringkasan Eksekutif](#1-ringkasan-eksekutif)
2. [Latar Belakang & Motivasi](#2-latar-belakang--motivasi)
3. [Research Gap & Positioning](#3-research-gap--positioning)
4. [Tujuan & Deliverables](#4-tujuan--deliverables)
5. [Arsitektur Sistem](#5-arsitektur-sistem)
6. [Peran Strategis DeepSeek API](#6-peran-strategis-deepseek-api)
7. [Pipeline Data & Knowledge Graph](#7-pipeline-data--knowledge-graph)
8. [Desain Multi-Agent](#8-desain-multi-agent)
9. [Strategi Evaluasi & Metrik](#9-strategi-evaluasi--metrik)
10. [Technology Stack](#10-technology-stack)
11. [Timeline & Milestones](#11-timeline--milestones)
12. [Manajemen Risiko](#12-manajemen-risiko)
13. [Strategi Publikasi](#13-strategi-publikasi)
14. [Budget & Resource Estimation](#14-budget--resource-estimation)
15. [Collaborative Framework (Multi-Human, Multi-Agent, Multi-Computer)](#15-collaborative-framework)
16. [Appendix](#16-appendix)

---

## 1. Ringkasan Eksekutif

### Apa yang Kita Bangun?

**Nusantara-Agent** adalah sistem Multi-Agent Retrieval-Augmented Generation (RAG) berbasis arsitektur Neuro-Simbolik yang dirancang untuk melakukan penalaran hukum pluralistik di Indonesia. Sistem ini mengorkestrasi kolaborasi antara **agen AI spesialis** dan **kolaborator manusia** (peneliti/annotator) dalam lingkungan kerja terdistribusi (multi-computer).

### Mengapa Ini Penting?

Indonesia memiliki sistem hukum pluralistik yang sangat kompleks. Menangani hal ini memerlukan fusi antara kecepatan pemrosesan AI dan intuisi mendalam dari banyak peneliti manusia. Nusantara-Agent dibangun sebagai ekosistem di mana banyak manusia dan banyak agen bisa bekerja sama secara sinkron lintas perangkat.

### Mengapa "Santai"?

Proyek ini **tidak** memerlukan pelatihan model dari nol, klaster GPU mahal, atau dataset berskala terabyte. Inti inovasi ada pada **desain arsitektur orkestrasi** dan **konstruksi Knowledge Graph** — keduanya bisa dikerjakan dengan laptop standar, API DeepSeek yang affordable, dan tools open-source gratis.

### Mengapa "Serius"?

Kontribusi riset mencakup tiga dimensi yang sangat dihargai reviewer Q1: (a) arsitektur novel (Agentic GraphRAG + Neuro-Symbolic), (b) dataset/resource baru (Knowledge Graph Hukum Adat pertama), dan (c) metrik evaluasi baru (Cultural Consistency Score). Tiga kontribusi dalam satu paper = peluang penerimaan sangat tinggi.

---

## 2. Latar Belakang & Motivasi

### 2.1 Pergeseran Paradigma: Generative AI → Agentic AI (2025-2026)

Lanskap AI global sedang bertransformasi dari model generatif pasif menuju sistem agen otonom. Paper yang hanya menyajikan "fine-tuning model X pada dataset Y" mulai kehilangan daya tarik di jurnal top. Sebaliknya, arsitektur agenik yang menyelesaikan masalah domain spesifik mendapatkan perhatian besar karena menawarkan kontribusi metodologis yang lebih dalam.

Tren kunci yang mendukung timing riset ini:

- **Self-Correcting Agentic RAG** baru muncul di domain medis (Frontiers in Medicine, 2025) — belum ada di domain hukum.
- **KG-R1** (arXiv, Sep 2025) membuktikan bahwa single agent + KG + Reinforcement Learning bisa outperform multi-module systems.
- **Evaluasi RAG masih krisis**: 70% sistem RAG tidak memiliki framework evaluasi sistematik (NStarX Report, 2025).
- **Cultural alignment benchmark** bermunculan (ALM-Bench CVPR 2025, Global MMLU) tapi TIDAK ADA yang spesifik untuk Southeast Asian high-context cultures.

### 2.2 Konteks Indonesia yang Unik

Indonesia menawarkan "laboratorium alami" yang tidak dimiliki negara lain untuk riset ini:

- **Pluralisme hukum aktif**: Bukan artefak sejarah — konflik hukum nasional vs adat terjadi setiap hari di pengadilan.
- **Budaya high-context**: Penolakan disampaikan tidak langsung, hierarki tutur mempengaruhi makna, sarkasme bergantung pada pelanggaran norma pragmatik.
- **Code-switching masif**: Campuran Indonesia-Jawa-Sunda-Inggris adalah norma komunikasi, bukan pengecualian.
- **Low-resource setting**: Teks hukum adat tersebar, tidak terstruktur, dan jarang terdigitalisasi.

Kombinasi faktor-faktor ini menciptakan **problem space yang secara inheren sulit** bagi AI — dan itulah yang membuat riset ini bernilai tinggi.

### 2.3 Motivasi Personal

Sebagai peneliti NLP di STIKI/UBHINUS dengan background bioinformatics dan machine learning, proyek ini berada di sweet spot antara keahlian teknis (NLP, data science) dan domain yang belum tersentuh (hukum pluralistik Indonesia). Akses ke DeepSeek API memberikan keunggulan praktis untuk data augmentation dan KG construction tanpa biaya besar.

---

## 3. Research Gap & Positioning

### 3.1 Gap Matrix

| Dimensi | State-of-the-Art Global | State-of-the-Art Indonesia | Gap yang Kita Isi |
|---------|------------------------|---------------------------|-------------------|
| **Agentic RAG** | Sudah ada untuk medical (hepatology), legal (commercial contracts), education | Belum ada implementasi | Agentic RAG pertama untuk hukum pluralistik |
| **GraphRAG** | Microsoft GraphRAG, KG-R1, INRAExplorer | LexID (metadata KG saja, bukan reasoning) | GraphRAG dengan KG hukum adat yang bisa di-traverse |
| **Neuro-Symbolic** | Fokus pada robustness & explainability di domain WEIRD | Tidak ada riset NeSy untuk konteks Indonesia | NeSy pertama yang mengintegrasikan logika hukum adat |
| **Cultural Alignment** | ALM-Bench (100 bahasa), AraDiCE (Arabic) | IndoBERT, NusaCrowd (klasifikasi saja) | Benchmark & metrik untuk high-context culture SEA |
| **Legal Reasoning** | Legal BERT, CaseLaw BERT (common law, Barat) | IndoLaw dataset (flat text, tanpa reasoning) | Sistem penalaran yang memahami hierarki norma pluralistik |
| **Code-Switching NLP** | Hindi-English, Dravidian languages | Deteksi bahasa & sentimen sederhana | Agen yang bernalar lintas-bahasa dengan kesadaran speech level |

### 3.2 Novelty Statement (untuk Paper)

> *"To the best of our knowledge, this is the first work that (1) constructs a Knowledge Graph for Indonesian customary law (Adat) from unstructured anthropological texts using LLM-automated triple extraction, (2) proposes a self-correcting multi-agent architecture that performs normative reasoning across plural legal systems, and (3) introduces the Cultural Consistency Score metric for evaluating cultural alignment in high-context linguistic environments."*

### 3.3 Positioning terhadap Literatur Terdekat

| Paper Terdekat | Apa yang Mereka Lakukan | Apa yang Kita Tambahkan |
|----------------|------------------------|------------------------|
| Self-Correcting Agentic GraphRAG (Frontiers Med, 2025) | Self-correction loop untuk hepatology KG | Adaptasi ke domain hukum pluralistik + multi-KG (nasional + adat) |
| KG-R1 (arXiv, Sep 2025) | Single agent + KG + RL untuk KGQA | Multi-agent untuk konflik norma + cultural reasoning |
| INRAExplorer (arXiv, Jul 2025) | Agentic RAG untuk scientific publications INRAE | Domain shift ke legal + budaya + low-resource languages |
| LexID (UI, Indonesia) | Metadata KG untuk hukum nasional Indonesia | Extend ke hukum adat + reasoning capability |
| KA-RAG (MDPI, Nov 2025) | KG + Agentic RAG untuk educational QA | Domain complexity jauh lebih tinggi (konflik norma) |

---

## 4. Tujuan & Deliverables

### 4.1 Tujuan Riset (Research Objectives)

**RO1**: Merancang dan mengimplementasikan arsitektur multi-agen Neuro-Simbolik yang mampu melakukan penalaran hukum pluralistik dengan mengorkestrasi retrieval dari multiple knowledge bases (vector DB + Knowledge Graph).

**RO2**: Membangun Knowledge Graph Hukum Adat Indonesia pertama secara semi-otomatis menggunakan LLM-based triple extraction (DeepSeek API) dari teks antropologi dan jurnal hukum adat.

**RO3**: Mengembangkan dan memvalidasi metrik evaluasi baru — Cultural Consistency Score (CCS) — untuk mengukur kemampuan model AI memahami nuansa budaya high-context.

**RO4**: Mendemonstrasikan melalui ablation study bahwa arsitektur yang diusulkan secara signifikan mengungguli baseline (single LLM, vector-only RAG, non-agentic RAG) dalam tugas penalaran hukum pluralistik.

### 4.2 Deliverables Konkret

| # | Deliverable | Deskripsi | Timeline |
|---|------------|-----------|----------|
| D1 | **Knowledge Graph Hukum Adat** | KG berisi minimal 5.000 tripel untuk 3 domain adat (Minangkabau, Bali, Jawa) di Neo4j | Bulan 3-4 |
| D2 | **Prototipe Nusantara-Agent** | Sistem multi-agen fungsional di LangGraph dengan 4 agen spesialis | Bulan 5-7 |
| D3 | **Golden Test Set** | 100 kasus hukum pluralistik ber-anotasi (50 mudah, 30 sedang, 20 sulit) | Bulan 4-5 |
| D4 | **NusaCulture-Bench** | Dataset benchmark 500+ pasangan skenario-respons budaya | Bulan 3-5 |
| D5 | **Manuskrip Jurnal** | Paper siap submit ke target jurnal Q1 | Bulan 10-12 |
| D6 | **Open-Source Repository** | Kode, data, dan dokumentasi di GitHub (meningkatkan reproducibility & peluang citasi) | Bulan 11-12 |

### 4.3 Success Criteria

| Kriteria | Target | Metode Pengukuran |
|----------|--------|-------------------|
| Faithfulness (RAGAS) | ≥ 0.85 | Evaluasi otomatis pada golden test set |
| Answer Relevancy (RAGAS) | ≥ 0.80 | Evaluasi otomatis pada golden test set |
| Cultural Consistency Score | ≥ 0.75 (vs baseline ≤ 0.40) | Evaluasi pada NusaCulture-Bench |
| Ablation improvement | ≥ 15% over best baseline | Perbandingan dengan 4 konfigurasi baseline |
| KG Triple accuracy | ≥ 0.80 precision (human-validated sample) | Random sample 200 tripel, validasi manual |
| Paper submission | Submitted ke jurnal Q1 | Tanggal submit |

---

## 5. Arsitektur Sistem

### 5.1 Overview Arsitektur

```
┌─────────────────────────────────────────────────────────────────┐
│                    NUSANTARA-AGENT SYSTEM                       │
│                                                                 │
│  ┌──────────┐    ┌──────────────────────────────────────────┐   │
│  │  User    │───▶│  AGEN SUPERVISOR (The Adjudicator)       │   │
│  │  Query   │    │  - Intent Decomposition                  │   │
│  └──────────┘    │  - Task Routing                          │   │
│                  │  - Conflict Resolution                   │   │
│                  │  - Self-Reflection Loop                  │   │
│                  └──┬──────────┬──────────┬─────────────────┘   │
│                     │          │          │                      │
│              ┌──────▼──┐ ┌────▼────┐ ┌───▼──────────┐          │
│              │ AGEN 1  │ │ AGEN 2  │ │   AGEN 3     │          │
│              │ Hukum   │ │ Hukum   │ │  Linguistik  │          │
│              │Nasional │ │  Adat   │ │   Budaya     │          │
│              └────┬────┘ └────┬────┘ └──────┬───────┘          │
│                   │          │              │                    │
│              ┌────▼────┐ ┌───▼─────┐ ┌─────▼──────┐           │
│              │ Vector  │ │Knowledge│ │  LLM with  │           │
│              │   DB    │ │  Graph  │ │  Cultural   │           │
│              │ (Qdrant)│ │ (Neo4j) │ │  Prompting  │           │
│              └─────────┘ └─────────┘ └────────────┘           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  SELF-CORRECTION LOOP                                    │   │
│  │  1. Retrieve → 2. Evaluate Sufficiency → 3. Refine      │   │
│  │  4. Cross-Validate → 5. Synthesize → 6. Reflect         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Komponen Inti

**Komponen Neural (Learning & Language Understanding):**
- LLM backend (via DeepSeek API / Ollama lokal) untuk memahami variabilitas linguistik
- Dense retrieval embeddings untuk vector search
- Instruction-tuned model untuk cultural reasoning

**Komponen Simbolik (Logic & Knowledge Representation):**
- Knowledge Graph di Neo4j untuk relasi hukum adat
- Ontologi hierarki norma (lex specialis, lex generalis, lex posterior)
- Rule-based conflict detection antar sistem hukum

**Komponen Agenik (Planning & Orchestration):**
- LangGraph state machine untuk orchestrasi multi-agen
- Self-correction loop dengan evaluate-refine cycle
- Cross-evaluation antar agen

### 5.3 Alur Kerja Detail

```
User Query
    │
    ▼
[1. INTENT DECOMPOSITION] ← Supervisor
    │ Memecah pertanyaan menjadi sub-queries
    │ Contoh: "Bagaimana pembagian waris tanah di Bali?"
    │   → Sub-Q1: "Aturan waris menurut KUHPerdata?"
    │   → Sub-Q2: "Aturan waris adat Bali (patrilineal)?"  
    │   → Sub-Q3: "Istilah budaya apa yang relevan?"
    │
    ▼
[2. PARALLEL RETRIEVAL]
    ├── Agen Nasional → Vector Search (Qdrant)
    │   └── Retrieve pasal KUHPerdata tentang waris
    ├── Agen Adat → Graph Traversal (Neo4j)  
    │   └── Traverse: Waris_Bali → Sentana → Patrilineal → Hak_Tanah
    └── Agen Linguistik → Cultural Context
        └── Translate: "Sentana" = anak laki-laki pewaris utama
    │
    ▼
[3. SUFFICIENCY EVALUATION] ← Self-Correction
    │ "Apakah konteks yang diambil cukup?"
    │ Jika TIDAK → Re-query dengan expanded terms
    │ Jika YA → Lanjut ke cross-evaluation
    │
    ▼
[4. CROSS-EVALUATION]
    │ Agen Nasional ←→ Agen Adat
    │ "Apakah norma adat bertentangan dengan UU HAM?"
    │ "Apakah ada putusan MA yang mengakui hak adat ini?"
    │
    ▼
[5. CONFLICT RESOLUTION] ← Symbolic Reasoning
    │ Terapkan aturan prioritas:
    │   - Lex Specialis: Adat sebagai hukum khusus?
    │   - Lex Generalis: Hukum nasional sebagai hukum umum?
    │   - Highlight ambiguitas jika tidak bisa diputuskan
    │
    ▼
[6. SELF-REFLECTION]
    │ "Apakah jawaban menghormati sensibilitas budaya?"
    │ "Apakah referensi hukum akurat?"
    │ "Apakah ada bias terhadap satu sistem hukum?"
    │
    ▼
[7. FINAL SYNTHESIS]
    └── Output: Narasi koheren dari kedua perspektif hukum
```

---

## 6. Peran Strategis DeepSeek API

DeepSeek API adalah **force multiplier** utama proyek ini. Ia berperan di hampir setiap fase untuk meminimalkan kerja manual yang melelahkan.

### 6.1 Peta Penggunaan DeepSeek API

| Fase | Tugas | Peran DeepSeek | Estimasi Panggilan API | Effort Manual Tanpa DeepSeek |
|------|-------|----------------|----------------------|------------------------------|
| **Data Collection** | OCR Correction | Memperbaiki hasil OCR dari PDF jurnal adat | ~2.000 calls | 200+ jam manual proofreading |
| **KG Construction** | Triple Extraction | Ekstrak (Subjek, Predikat, Objek) dari teks adat | ~5.000 calls | 500+ jam manual annotation |
| **KG Construction** | Ontology Alignment | Validasi & normalisasi tripel ke ontologi standar | ~1.000 calls | 100+ jam domain expert review |
| **Data Augmentation** | Synthetic Q&A Generation | Generate pasangan pertanyaan-jawaban hukum untuk testing | ~3.000 calls | 300+ jam manual crafting |
| **Benchmark Creation** | Cultural Scenario Generation | Generate skenario budaya untuk NusaCulture-Bench | ~2.000 calls | 200+ jam manual writing |
| **Evaluation** | LLM-as-Judge | Automated scoring untuk Cultural Consistency | ~5.000 calls | Butuh 3+ human annotators |
| **Agent Backend** | Reasoning Engine | Backend LLM untuk agen-agen dalam sistem | Runtime calls | N/A (harus ada LLM) |

**Total estimasi: ~18.000 API calls** → sangat terjangkau dengan DeepSeek pricing.

### 6.2 DeepSeek untuk Knowledge Graph Construction (KUNCI UTAMA)

Ini adalah penggunaan paling kritis dan inovatif dari DeepSeek API. Pipeline-nya:

**Step 1: Text Cleaning & Segmentation**
```
Input:  Raw OCR text dari PDF jurnal hukum adat
Prompt: "Bersihkan teks berikut dari artefak OCR. Pertahankan semua 
         istilah hukum adat dalam bahasa aslinya. Segmentasi menjadi 
         paragraf yang koheren."
Output: Clean text segments
```

**Step 2: Triple Extraction**
```
Input:  Clean text segment
Prompt: "Dari teks berikut tentang hukum adat [Minangkabau/Bali/Jawa], 
         ekstrak semua relasi hukum dalam format JSON:
         {
           'triples': [
             {
               'head': 'entitas subjek (dalam bahasa Indonesia)',
               'relation': 'hubungan/relasi',
               'tail': 'entitas objek',
               'domain': 'Minangkabau|Bali|Jawa',
               'source_type': 'norma|konsep|prosedur|entitas',
               'confidence': 0.0-1.0
             }
           ]
         }
         
         Contoh relasi yang dicari:
         - 'dimiliki_oleh', 'diwariskan_kepada', 'diatur_oleh'
         - 'bertentangan_dengan', 'merupakan_bagian_dari'
         - 'memiliki_hierarki', 'berlaku_di_wilayah'
         
         Teks: [TEXT]"
Output: JSON triples
```

**Step 3: Ontology Alignment & Validation**
```
Input:  Extracted triples batch
Prompt: "Validasi tripel-tripel berikut terhadap ontologi hukum:
         1. Apakah relasi konsisten? (contoh: 'Tanah Ulayat' 
            tidak bisa 'dimiliki_oleh' individu)
         2. Apakah ada duplikasi semantik? 
            (merge 'Pusako Tinggi' dan 'Harta Pusaka Tinggi')
         3. Berikan skor confidence 0-1 untuk setiap tripel.
         
         Tripel: [TRIPLES_JSON]"
Output: Validated & deduplicated triples
```

**Step 4: Cross-Domain Linking**
```
Input:  Triples dari domain berbeda
Prompt: "Identifikasi hubungan lintas-domain antara tripel hukum 
         adat berikut. Cari:
         1. Konsep yang ekuivalen antar-adat 
            (misal: 'Pusako Tinggi' Minang ≈ 'Druwe Tengah' Bali)
         2. Konflik norma antar-adat
         3. Konsep adat yang bertentangan dengan hukum nasional
         
         Domain A: [TRIPLES_A]
         Domain B: [TRIPLES_B]"
Output: Cross-domain links & conflict annotations
```

### 6.3 DeepSeek untuk Synthetic Data Generation

**Golden Test Set Generation:**
```
Prompt: "Kamu adalah ahli hukum Indonesia yang memahami pluralisme hukum.
         Buat sebuah kasus hukum fiktif tapi realistis dengan kriteria:
         - Domain: [waris/tanah/perkawinan/perceraian]
         - Adat: [Minangkabau/Bali/Jawa]
         - Tingkat kesulitan: [mudah/sedang/sulit]
         - Harus melibatkan konflik antara hukum nasional dan adat
         
         Format output:
         {
           'kasus': 'deskripsi kasus 2-3 paragraf',
           'pertanyaan': 'pertanyaan hukum spesifik',
           'jawaban_nasional': 'perspektif hukum nasional',
           'jawaban_adat': 'perspektif hukum adat',
           'jawaban_ideal': 'sintesis pluralistik yang benar',
           'konsep_budaya_kunci': ['list istilah adat relevan'],
           'tingkat_konflik': 'rendah|sedang|tinggi'
         }"
```

**NusaCulture-Bench Generation:**
```
Prompt: "Buat skenario interaksi sosial dalam budaya [Jawa/Sunda/Bali] 
         yang menguji pemahaman AI tentang:
         - Komunikasi tidak langsung (indirect speech acts)
         - Hierarki sosial dan tingkat tutur
         - Konsep harmoni vs konfrontasi
         
         Format:
         {
           'skenario': 'situasi sosial dalam 1-2 paragraf',
           'pertanyaan': 'apa intent sebenarnya dari tokoh X?',
           'jawaban_surface': 'interpretasi literal (SALAH)',
           'jawaban_cultural': 'interpretasi budaya (BENAR)',
           'dimensi_hofstede': 'power_distance|collectivism|...',
           'bahasa': 'Indonesia|Jawa_Ngoko|Jawa_Krama|Sunda'
         }"
```

### 6.4 DeepSeek sebagai LLM-as-Judge

Untuk evaluasi otomatis yang scalable:

```
Prompt: "Kamu adalah evaluator untuk sistem AI hukum Indonesia.
         Evaluasi jawaban berikut pada 4 dimensi (skor 1-5):
         
         1. AKURASI HUKUM: Apakah referensi pasal/norma benar?
         2. KELENGKAPAN PLURALISTIK: Apakah mencakup perspektif 
            nasional DAN adat?
         3. KONSISTENSI BUDAYA: Apakah menghormati nuansa budaya 
            dan tidak bias ke satu sistem?
         4. KUALITAS PENALARAN: Apakah logika resolusi konflik valid?
         
         Pertanyaan: [Q]
         Ground Truth: [GT]
         Jawaban Sistem: [A]
         
         Output JSON dengan skor dan justifikasi singkat per dimensi."
```

### 6.5 Cost Estimation DeepSeek API

| Model | Harga Input | Harga Output | Estimasi Total Calls | Est. Cost |
|-------|-------------|--------------|---------------------|-----------|
| DeepSeek-V3 (atau terbaru) | ~$0.27/M tokens | ~$1.10/M tokens | 18.000 calls × ~1K tokens avg | ~$25-50 |
| DeepSeek-R1 (reasoning) | ~$0.55/M tokens | ~$2.19/M tokens | 3.000 calls (complex reasoning) | ~$10-20 |

**Total estimasi biaya API: $35-70 untuk seluruh proyek.** Ini sangat "santai" dari segi budget.

---

## 7. Pipeline Data & Knowledge Graph

### 7.1 Sumber Data

**Tier 1: Data Siap Pakai (Effort: Rendah)**

| Dataset | Sumber | Format | Ukuran | Kegunaan |
|---------|--------|--------|--------|----------|
| IndoLaw | HuggingFace (bstds/indo_law) | Structured text | ~10K dokumen | Korpus hukum nasional |
| SEACrowd/indo_law | HuggingFace | Structured text | Varies | Pelengkap hukum nasional |
| KUHP, KUHPerdata | JDIH (database hukum pemerintah) | PDF/HTML | Ratusan pasal | Referensi hukum positif |

**Tier 2: Data Perlu Diolah (Effort: Sedang — dibantu DeepSeek)**

| Dataset | Sumber | Format | Target | Kegunaan |
|---------|--------|--------|--------|----------|
| Jurnal Hukum Adat Minangkabau | Repository Unand, UGM | PDF (OA) | 200-300 artikel | KG Adat Minang |
| Jurnal Hukum Adat Bali | Repository Udayana, UI | PDF (OA) | 200-300 artikel | KG Adat Bali |
| Jurnal Hukum Adat Jawa | Repository UGM, Undip | PDF (OA) | 200-300 artikel | KG Adat Jawa |
| Yurisprudensi MA terkait adat | Direktori Putusan MA | PDF | 50-100 putusan | Cross-validation nasional vs adat |

**Tier 3: Data Sintetis (Effort: Rendah — DeepSeek generates)**

| Dataset | Metode | Target Ukuran | Kegunaan |
|---------|--------|---------------|----------|
| Golden Test Set | DeepSeek generation + human validation | 100 kasus | Evaluasi utama |
| NusaCulture-Bench | DeepSeek generation + human validation | 500 skenario | Evaluasi cultural alignment |
| Augmented Q&A pairs | DeepSeek paraphrasing & variation | 2.000 pairs | Training & testing |

### 7.2 Pipeline Konstruksi Knowledge Graph

```
[PDF Jurnal Adat]
       │
       ▼
[OCR + Text Extraction] ← PyMuPDF / pdfplumber
       │
       ▼
[Text Cleaning] ← DeepSeek API (batch processing)
       │
       ▼
[Segmentation] ← Paragraph-level chunking
       │
       ▼
[Triple Extraction] ← DeepSeek API (core pipeline)
       │
       ▼
[Validation & Dedup] ← DeepSeek API + rule-based checks
       │
       ▼
[Ontology Mapping] ← Manual ontology + DeepSeek alignment
       │
       ▼
[Neo4j Import] ← Cypher bulk import
       │
       ▼
[Cross-Domain Linking] ← DeepSeek API + manual spot-check
       │
       ▼
[Quality Assurance] ← Random sample human validation (200 tripel)
```

### 7.3 Ontologi Hukum Adat (Desain Awal)

```
ROOT: Hukum_Adat_Indonesia
├── Hukum_Adat_Minangkabau
│   ├── Sistem_Kekerabatan: Matrilineal
│   ├── Properti
│   │   ├── Pusako_Tinggi (harta turun-temurun, milik kaum)
│   │   ├── Pusako_Rendah (harta pencaharian sendiri)
│   │   └── Tanah_Ulayat (tanah komunal nagari)
│   ├── Struktur_Sosial
│   │   ├── Mamak (paman dari pihak ibu)
│   │   ├── Kaum (kelompok keturunan seibu)
│   │   └── Penghulu (kepala adat)
│   └── Mekanisme_Waris: Matrilineal_Descent
│
├── Hukum_Adat_Bali
│   ├── Sistem_Kekerabatan: Patrilineal
│   ├── Properti
│   │   ├── Druwe_Tengah (harta bersama desa adat)
│   │   ├── Druwe_Pura (harta pura/tempat ibadah)
│   │   └── Pekarangan_Desa (tanah pekarangan)
│   ├── Struktur_Sosial
│   │   ├── Sentana (anak laki-laki pewaris)
│   │   ├── Banjar (organisasi kemasyarakatan)
│   │   └── Desa_Adat (unit pemerintahan adat)
│   └── Mekanisme_Waris: Patrilineal_Descent
│
├── Hukum_Adat_Jawa
│   ├── Sistem_Kekerabatan: Bilateral/Parental
│   ├── Properti
│   │   ├── Harta_Gono_Gini (harta bersama suami-istri)
│   │   ├── Harta_Bawaan (harta sebelum nikah)
│   │   └── Tanah_Bengkok (tanah jabatan desa)
│   ├── Struktur_Sosial
│   │   ├── Lurah/Kepala_Desa
│   │   ├── Sesepuh (tetua adat)
│   │   └── Musyawarah_Desa
│   └── Mekanisme_Waris: Bilateral_Equal
│
└── Relasi_dengan_Hukum_Nasional
    ├── Lex_Specialis (adat sebagai hukum khusus)
    ├── Bertentangan_dengan (konflik norma)
    ├── Diakui_oleh (pengakuan dalam UU)
    └── Dikesampingkan_oleh (hukum nasional menang)
```

---

## 8. Desain Multi-Agent

### 8.1 Spesifikasi Agen

#### Agen 1: Pustakawan Hukum Nasional (The Legal Librarian)

| Aspek | Detail |
|-------|--------|
| **Fungsi** | Retrieval dan reasoning dari hukum positif tertulis |
| **Sumber Data** | Vector DB (Qdrant) berisi KUHP, KUHPerdata, UU Agraria, putusan MA |
| **Teknologi Retrieval** | Dense retrieval (semantic search) — cocok untuk teks baku dan eksplisit |
| **LLM Backend** | DeepSeek API |
| **System Prompt Inti** | "Kamu adalah ahli hukum perdata Indonesia. Jawab HANYA berdasarkan dokumen hukum yang diberikan. Jika tidak ada dasar hukum yang jelas, katakan 'tidak ditemukan dasar hukum tertulis'." |
| **Output** | Pasal/ayat relevan + interpretasi singkat |

#### Agen 2: Penjaga Adat (The Adat Custodian)

| Aspek | Detail |
|-------|--------|
| **Fungsi** | Retrieval dan reasoning dari norma adat kontekstual |
| **Sumber Data** | Knowledge Graph (Neo4j) + literatur antropologi |
| **Teknologi Retrieval** | GraphRAG — traverse relasi, bukan keyword matching |
| **LLM Backend** | DeepSeek API |
| **System Prompt Inti** | "Kamu adalah tetua adat yang memahami hukum adat [domain]. Jawab berdasarkan graf pengetahuan adat. Jelaskan konteks budaya di balik setiap norma. Gunakan istilah adat asli dengan penjelasan." |
| **Query Strategy** | Cypher query generation → graph traversal → context assembly |
| **Output** | Norma adat relevan + konteks budaya + path dalam graf |

#### Agen 3: Ahli Linguistik Budaya (The Cultural Linguist)

| Aspek | Detail |
|-------|--------|
| **Fungsi** | Penerjemahan istilah budaya, deteksi speech level, analisis code-switching |
| **Sumber Data** | Glossarium istilah hukum adat + model deteksi bahasa |
| **Teknologi** | LLM dengan cultural prompting |
| **LLM Backend** | DeepSeek API dengan specialized prompt |
| **System Prompt Inti** | "Kamu adalah ahli linguistik Nusantara. Tugasmu: (1) Terjemahkan istilah budaya ke konsep hukum yang dipahami agen lain tanpa menghilangkan nuansa. (2) Deteksi tingkat tutur dan implikasinya. (3) Identifikasi apakah ada komunikasi tidak langsung." |
| **Output** | Istilah → konsep mapping + analisis pragmatik |

#### Agen 4: Hakim Supervisor (The Adjudicator)

| Aspek | Detail |
|-------|--------|
| **Fungsi** | Orkestrasi, sintesis, resolusi konflik, self-reflection |
| **Input** | Output dari Agen 1 + 2 + 3 |
| **Logika Resolusi** | Rule-based (lex specialis, lex posterior) + LLM reasoning |
| **Self-Reflection Prompt** | "Periksa draf jawabanmu: (1) Apakah kedua perspektif hukum terwakili? (2) Apakah ada bias terhadap satu sistem? (3) Apakah istilah budaya dijelaskan dengan tepat? (4) Apakah konflik norma di-highlight, bukan disembunyikan?" |
| **Output** | Narasi koheren multi-perspektif + confidence score |

### 8.2 State Machine (LangGraph)

```python
# Pseudocode arsitektur LangGraph
from langgraph.graph import StateGraph

class NusantaraState(TypedDict):
    query: str
    sub_queries: list[str]
    national_law_context: str
    adat_law_context: str
    cultural_context: str
    conflict_detected: bool
    conflict_type: str  # "lex_specialis" | "contradictory" | "complementary"
    sufficiency_score: float
    draft_answer: str
    reflection_notes: str
    final_answer: str
    iteration_count: int

workflow = StateGraph(NusantaraState)

# Nodes
workflow.add_node("decompose", intent_decomposition)
workflow.add_node("retrieve_national", agent_national_law)
workflow.add_node("retrieve_adat", agent_adat_custodian)
workflow.add_node("analyze_culture", agent_cultural_linguist)
workflow.add_node("evaluate_sufficiency", sufficiency_checker)
workflow.add_node("cross_evaluate", cross_evaluation)
workflow.add_node("resolve_conflict", conflict_resolution)
workflow.add_node("synthesize", draft_synthesis)
workflow.add_node("reflect", self_reflection)
workflow.add_node("finalize", final_output)

# Edges
workflow.add_edge("decompose", "retrieve_national")
workflow.add_edge("decompose", "retrieve_adat")
workflow.add_edge("decompose", "analyze_culture")
workflow.add_edge(["retrieve_national", "retrieve_adat", "analyze_culture"], 
                  "evaluate_sufficiency")

# Conditional: loop back if insufficient
workflow.add_conditional_edges("evaluate_sufficiency", 
    lambda s: "cross_evaluate" if s["sufficiency_score"] > 0.7 
              else "decompose",  # re-query with expanded terms
    max_iterations=3)

workflow.add_edge("cross_evaluate", "resolve_conflict")
workflow.add_edge("resolve_conflict", "synthesize")
workflow.add_edge("synthesize", "reflect")

# Conditional: loop back if reflection fails
workflow.add_conditional_edges("reflect",
    lambda s: "finalize" if s["iteration_count"] >= 2 
              or "PASS" in s["reflection_notes"]
              else "synthesize")
```

---

## 9. Strategi Evaluasi & Metrik

### 9.1 Framework Evaluasi Tiga Lapis

**Lapis 1: Evaluasi RAG Otomatis (RAGAS Framework)**

| Metrik | Apa yang Diukur | Tool |
|--------|----------------|------|
| Faithfulness | Apakah jawaban setia pada dokumen yang di-retrieve? | RAGAS |
| Answer Relevancy | Seberapa relevan jawaban terhadap pertanyaan? | RAGAS |
| Context Precision | Apakah dokumen yang di-retrieve benar-benar relevan? | RAGAS |
| Context Recall | Apakah semua informasi penting ter-retrieve? | RAGAS |

**Lapis 2: Cultural Consistency Score (INOVASI METRIK BARU)**

Metrik baru yang kita usulkan, diukur pada NusaCulture-Bench:

```
CCS = (w1 × Pluralism_Coverage) + (w2 × Cultural_Nuance_Detection) 
    + (w3 × Indirect_Intent_Recognition) + (w4 × Bias_Neutrality)

Di mana:
- Pluralism_Coverage: Apakah model menyebut KEDUA perspektif hukum? (0/1)
- Cultural_Nuance_Detection: Apakah model mengenali istilah adat dan 
  konteksnya? (0-1, scored by DeepSeek-as-Judge)
- Indirect_Intent_Recognition: Apakah model memahami komunikasi tidak 
  langsung? (0-1)
- Bias_Neutrality: Apakah model tidak bias ke satu sistem hukum? (0-1)
- w1=0.3, w2=0.3, w3=0.2, w4=0.2 (adjustable)
```

**Lapis 3: Ablation Study (KRUSIAL untuk Reviewer)**

| Konfigurasi | Deskripsi | Apa yang Dibuktikan |
|-------------|-----------|-------------------|
| **Baseline 1** | Single LLM (DeepSeek) zero-shot | Tanpa retrieval, tanpa agen |
| **Baseline 2** | Single LLM + Vector RAG (tanpa KG) | Tanpa knowledge graph |
| **Baseline 3** | Single LLM + GraphRAG (tanpa multi-agent) | Tanpa orkestrasi agen |
| **Baseline 4** | Multi-Agent + Vector RAG (tanpa KG) | Agen ada, tapi tanpa symbolic reasoning |
| **Full System** | Multi-Agent + GraphRAG + Self-Correction | Sistem lengkap |

**Hipotesis ablation:**
- Baseline 1 → Full: Peningkatan besar di semua metrik (membuktikan keseluruhan arsitektur)
- Baseline 2 vs Full: KG meningkatkan Context Precision secara signifikan pada pertanyaan adat
- Baseline 3 vs Full: Multi-agent meningkatkan Conflict Resolution dan CCS
- Baseline 4 vs Full: KG meningkatkan Faithfulness (mengurangi halusinasi fakta adat)

### 9.2 Human Evaluation (Sampel Kecil tapi Rigorous)

Untuk memenuhi standar Q1, tetap perlu validasi manusia meskipun skala kecil:

- **Annotator**: 2-3 mahasiswa hukum atau antropologi (bisa dari kampus sendiri)
- **Sampel**: 50 kasus dari golden test set
- **Dimensi**: Akurasi hukum (1-5), Kelengkapan (1-5), Kesesuaian budaya (1-5)
- **Inter-annotator agreement**: Fleiss' Kappa ≥ 0.6
- **Effort**: ~20 jam per annotator (bisa dikerjakan dalam 1-2 minggu)

---

## 10. Technology Stack

### 10.1 Stack Utama

| Layer | Tool | Alasan Pemilihan | Biaya |
|-------|------|------------------|-------|
| **LLM Backend (Primary)** | DeepSeek API (V3/R1) | Affordable, kualitas tinggi, bahasa Indonesia decent | ~$50-70 total |
| **LLM Backend (Fallback)** | Ollama + Llama 3/Gemma 2 | Lokal, gratis, untuk eksperimen offline | Gratis |
| **Orchestration** | LangGraph | State machine control terbaik untuk riset, lebih fleksibel dari CrewAI | Gratis (OSS) |
| **Vector DB** | Qdrant | Performa tinggi, mudah setup, versi gratis cukup | Gratis (self-hosted) |
| **Graph DB** | Neo4j Community Edition | Standar industri untuk KG, Cypher query language | Gratis |
| **Embedding Model** | sentence-transformers (multilingual) | all-MiniLM atau multilingual-e5 | Gratis |
| **Evaluation** | RAGAS + custom CCS | Framework evaluasi RAG paling lengkap | Gratis (OSS) |
| **PDF Processing** | PyMuPDF / pdfplumber | Ekstraksi teks dari PDF jurnal | Gratis |
| **Development** | Python 3.11+, Jupyter | Standar riset | Gratis |
| **Version Control** | Git + GitHub | Reproducibility & open-source release | Gratis |

### 10.2 Hardware Requirements

| Komponen | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 cores | 8 cores |
| RAM | 16 GB | 32 GB |
| Storage | 50 GB SSD | 100 GB SSD |
| GPU | Tidak wajib (API-based) | RTX 3060+ (jika pakai Ollama) |
| Internet | Stabil untuk API calls | Stabil untuk API calls |

**Catatan**: Karena menggunakan DeepSeek API sebagai backend utama, GPU lokal TIDAK wajib. Ini adalah fitur "santai" yang signifikan.

### 10.3 Development Environment

```bash
# Core dependencies
pip install langgraph langchain-core langchain-community
pip install qdrant-client neo4j
pip install sentence-transformers
pip install ragas
pip install pymupdf pdfplumber
pip install openai  # DeepSeek API compatible with OpenAI SDK
pip install pandas numpy scikit-learn
pip install jupyter notebook

# Optional (local LLM)
# curl -fsSL https://ollama.com/install.sh | sh
# ollama pull llama3:8b
```

---

## 11. Timeline & Milestones

### 11.1 Overview 12 Bulan

```
Bulan:  1    2    3    4    5    6    7    8    9    10   11   12
        ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
Fase 1: ████████                                               
Fase 2:           ████████                                     
Fase 3:                     ████████████                       
Fase 4:                                    ████████            
Fase 5:                                              ████████ 
        Riset &   Data &    Develop &     Evaluasi   Penulisan
        Desain    KG Build  Prototype     & Iterasi  & Submit  
```

### 11.2 Detail per Fase

#### FASE 1: Riset & Desain Arsitektur (Bulan 1-2)

| Minggu | Aktivitas | Output | Effort/Minggu |
|--------|-----------|--------|---------------|
| 1-2 | Deep dive literatur: Agentic RAG, GraphRAG, NeSy terbaru | Annotated bibliography (30+ papers) | 10 jam |
| 3-4 | Desain arsitektur detail + ontologi awal | Architecture diagram, ontology draft | 8 jam |
| 5-6 | Setup environment, install tools, test DeepSeek API | Working dev environment | 6 jam |
| 7-8 | Tulis Bab 1-2 paper (Introduction, Related Work) | Draft Bab 1-2 (~4.000 kata) | 10 jam |

**Milestone 1**: Arsitektur tervalidasi + environment ready + draft Bab 1-2

#### FASE 2: Data Collection & KG Construction (Bulan 3-4)

| Minggu | Aktivitas | Output | Effort/Minggu |
|--------|-----------|--------|---------------|
| 9-10 | Download PDF jurnal adat (OA) + setup IndoLaw | Raw corpus (~700 PDFs) | 8 jam |
| 11-12 | OCR + text extraction + DeepSeek cleaning | Clean text corpus | 6 jam |
| 13-14 | Triple extraction pipeline (DeepSeek batch) | Raw triples (~8.000) | 8 jam |
| 15-16 | Validation, dedup, Neo4j import, spot-check | KG v1.0 (~5.000 validated triples) | 10 jam |

**Milestone 2**: Knowledge Graph Hukum Adat v1.0 di Neo4j

#### FASE 3: Agent Development & Prototyping (Bulan 5-7)

| Minggu | Aktivitas | Output | Effort/Minggu |
|--------|-----------|--------|---------------|
| 17-18 | Agen 1 (National Law) + Qdrant setup | Working retrieval agent | 10 jam |
| 19-20 | Agen 2 (Adat Custodian) + GraphRAG integration | Working graph agent | 12 jam |
| 21-22 | Agen 3 (Cultural Linguist) + prompting design | Working cultural agent | 8 jam |
| 23-24 | Agen 4 (Supervisor) + LangGraph orchestration | Integrated multi-agent v0.5 | 12 jam |
| 25-26 | Self-correction loop + cross-evaluation | System v0.8 with self-correction | 10 jam |
| 27-28 | Integration testing, bug fixes, prompt tuning | System v1.0 | 8 jam |

**Milestone 3**: Prototipe Nusantara-Agent v1.0 berfungsi end-to-end

#### FASE 4: Evaluasi & Iterasi (Bulan 8-9)

| Minggu | Aktivitas | Output | Effort/Minggu |
|--------|-----------|--------|---------------|
| 29-30 | Generate Golden Test Set (DeepSeek + manual review) | 100 test cases | 8 jam |
| 31-32 | Generate NusaCulture-Bench (DeepSeek + manual review) | 500 cultural scenarios | 8 jam |
| 33-34 | Run semua baseline + full system evaluation | Raw evaluation data | 10 jam |
| 35-36 | Ablation study + statistical analysis | Ablation results + tables | 10 jam |

**Milestone 4**: Hasil evaluasi lengkap + bukti superioritas sistem

#### FASE 5: Penulisan & Submission (Bulan 10-12)

| Minggu | Aktivitas | Output | Effort/Minggu |
|--------|-----------|--------|---------------|
| 37-38 | Tulis Bab 3-4 (Methodology, Experiments) | Draft Bab 3-4 (~5.000 kata) | 12 jam |
| 39-40 | Tulis Bab 5-6 (Results, Discussion) | Draft Bab 5-6 (~4.000 kata) | 12 jam |
| 41-42 | Visualisasi arsitektur & hasil, buat tabel profesional | Figures & tables | 8 jam |
| 43-44 | Internal review, revisi, polish abstract | Near-final manuscript | 10 jam |
| 45-46 | Siapkan GitHub repo, supplementary material | Open-source release | 6 jam |
| 47-48 | Final proofread, format sesuai jurnal, SUBMIT | Submitted manuscript | 8 jam |

**Milestone 5**: Paper submitted ke jurnal Q1

### 11.3 Effort Summary

| Fase | Durasi | Jam/Minggu (rata-rata) | Total Jam |
|------|--------|----------------------|-----------|
| Fase 1 | 8 minggu | 8.5 jam | 68 jam |
| Fase 2 | 8 minggu | 8.0 jam | 64 jam |
| Fase 3 | 12 minggu | 10.0 jam | 120 jam |
| Fase 4 | 8 minggu | 9.0 jam | 72 jam |
| Fase 5 | 12 minggu | 9.3 jam | 112 jam |
| **TOTAL** | **48 minggu** | **~9.2 jam** | **~436 jam** |

Rata-rata sekitar **9 jam per minggu** — sangat "santai" untuk proyek berkaliber Q1. Setara dengan ~1.3 jam per hari jika dikerjakan 7 hari/minggu, atau ~1.8 jam per hari jika 5 hari/minggu.

---

## 12. Manajemen Risiko

### 12.1 Risk Register

| # | Risiko | Probabilitas | Dampak | Mitigasi |
|---|--------|-------------|--------|----------|
| R1 | DeepSeek API down atau pricing berubah drastis | Rendah | Tinggi | Fallback ke Ollama lokal (Llama 3 8B). KG construction bisa juga pakai Claude API sebagai cadangan. |
| R2 | Kualitas triple extraction rendah (<70% precision) | Sedang | Tinggi | Iterasi prompt engineering. Tambah few-shot examples. Jika masih rendah, perkecil scope ke 2 domain adat saja. |
| R3 | PDF jurnal adat sulit di-OCR (scan berkualitas rendah) | Sedang | Sedang | Prioritaskan jurnal yang sudah born-digital. Gunakan Google Cloud Vision OCR untuk scan sulit. |
| R4 | Neo4j Community Edition terbatas fiturnya | Rendah | Rendah | Untuk skala riset ini, Community Edition lebih dari cukup. |
| R5 | Evaluator manusia tidak konsisten (low inter-annotator agreement) | Sedang | Sedang | Buat rubrik evaluasi sangat detail. Lakukan calibration session sebelum annotasi. |
| R6 | Paper ditolak reviewer pertama | Tinggi | Sedang | Siapkan 3 target jurnal berurutan. Feedback reviewer selalu bermanfaat untuk revisi. |
| R7 | Scope creep — terlalu banyak fitur | Sedang | Tinggi | Patuhi PRD ini. Minimum Viable Paper = KG + Multi-Agent + Ablation. NusaCulture-Bench adalah bonus. |
| R8 | Burnout karena proyek terlalu panjang | Sedang | Tinggi | Patuhi jadwal ~9 jam/minggu. Milestone kecil memberi rasa progres. |

### 12.2 Contingency: Minimum Viable Paper (MVP)

Jika waktu atau resource terbatas, prioritaskan komponen berikut:

**MUST HAVE (tanpa ini, paper tidak bisa submit):**
1. Knowledge Graph Hukum Adat (minimal 1 domain: Minangkabau)
2. Multi-Agent System (minimal 3 agen: Nasional + Adat + Supervisor)
3. Golden Test Set (minimal 50 kasus)
4. Ablation Study (minimal 3 baseline)

**SHOULD HAVE (menguatkan paper secara signifikan):**
5. Self-correction loop
6. Agen Cultural Linguist
7. NusaCulture-Bench
8. Cultural Consistency Score metric

**NICE TO HAVE (bonus untuk mempercantik):**
9. 3 domain adat lengkap (Minangkabau + Bali + Jawa)
10. Web demo interface
11. Cross-domain linking dalam KG
12. Real-time user study

---

## 13. Strategi Publikasi

### 13.1 Target Jurnal (Berurutan)

**Target Primer:**

| Jurnal | Penerbit | Quartile | Impact Factor | Alasan |
|--------|----------|----------|---------------|--------|
| **Information Fusion** | Elsevier | Q1 (Top) | ~18.6 | Fusi multi-sumber (teks + graf), decision-making kompleks. Framing: "Fusi pengetahuan simbolik dan neural untuk resolusi konflik hukum" |
| **Knowledge-Based Systems** | Elsevier | Q1 | ~8.1 | Neuro-symbolic AI, Knowledge Graphs. Framing: "Konstruksi graf otomatis dan penalaran hibrida" |

**Target Sekunder (jika primer ditolak):**

| Jurnal | Penerbit | Quartile | Impact Factor | Alasan |
|--------|----------|----------|---------------|--------|
| **Expert Systems with Applications** | Elsevier | Q1 | ~8.5 | Aplikasi AI praktis. Framing: "Sistem pakar hukum cerdas untuk masyarakat pluralistik" |
| **Artificial Intelligence and Law** | Springer | Q1 | ~3.1 | Niche tapi sangat prestigious di komunitas AI+Law |
| **IEEE Trans. Computational Social Systems** | IEEE | Q1 | ~5.0 | Interaksi AI dengan sistem sosial. Framing: aspek budaya |

### 13.2 Strategi Penulisan

**Judul yang Menjual:**
> "Nusantara-Agent: Self-Correcting Neuro-Symbolic Multi-Agent GraphRAG for Pluralistic Legal Reasoning in Low-Resource Cultural Environments"

**Kata kunci strategis:** Agentic RAG, Neuro-Symbolic AI, Knowledge Graph, Legal Pluralism, Low-Resource NLP, Cultural Alignment, Multi-Agent Systems

**Struktur Paper yang Disarankan:**

| Bagian | Halaman | Konten |
|--------|---------|--------|
| Abstract | 0.5 | Problem → Gap → Method → Results → Impact |
| 1. Introduction | 2 | Motivasi, research questions, kontribusi (3 poin) |
| 2. Related Work | 2.5 | Agentic RAG, Legal NLP, NeSy, Cultural AI — posisikan gap |
| 3. Methodology | 4 | Arsitektur, agen, KG construction, pipeline |
| 4. Experiments | 3 | Setup, baselines, metrik, ablation design |
| 5. Results & Discussion | 3 | Tabel hasil, ablation, case studies, error analysis |
| 6. Conclusion | 1 | Kontribusi, limitasi, future work |
| References | 2 | 50-70 referensi (mix klasik + 2024-2026) |
| **Total** | **~18** | Sesuai standar jurnal Elsevier |

### 13.3 Tips Kritis dari Pengalaman

1. **Diagram arsitektur profesional**: Buat dengan draw.io atau Figma. Reviewer sering menilai dari diagram terlebih dahulu.
2. **Klaim kontribusi eksplisit**: Jangan bilang "kami membuat aplikasi". Katakan "kami mengusulkan kerangka kerja novel yang..." 
3. **Reproducibility pledge**: Janjikan kode + data di GitHub. Ini meningkatkan peluang penerimaan 20-30%.
4. **Limitations section yang jujur**: Reviewer menghargai kejujuran tentang keterbatasan — ini menunjukkan maturitas riset.
5. **Response letter strategy**: Siapkan template response letter yang sopan dan detail untuk reviewer comments.

---

## 14. Budget & Resource Estimation

### 14.1 Biaya Langsung

| Item | Estimasi Biaya | Catatan |
|------|---------------|---------|
| DeepSeek API | $50-70 | ~18.000 calls selama 12 bulan |
| Cloud OCR (jika diperlukan) | $0-20 | Google Cloud Vision free tier mungkin cukup |
| Domain + hosting untuk demo (opsional) | $0-50 | Bisa pakai GitHub Pages gratis |
| Annotator honorarium (opsional) | $0-100 | Bisa pakai mahasiswa sebagai bimbingan skripsi |
| Journal submission fee (jika ada) | $0-100 | Banyak jurnal Q1 yang free untuk submit |
| **Total** | **$50-340** | |

### 14.2 Biaya Tak Langsung (Sudah Tersedia)

| Item | Status |
|------|--------|
| Laptop/PC untuk development | Sudah ada |
| Internet | Sudah ada |
| Akses jurnal (Sci-Hub / kampus) | Sudah ada |
| Software (semua open-source) | Gratis |
| Waktu peneliti (~436 jam / 12 bulan) | Bagian dari workload dosen |

**Kesimpulan budget: Proyek ini bisa berjalan dengan total out-of-pocket cost di bawah $100.** Ini mendefinisikan ulang kata "santai".

---

## 15. Collaborative Framework (Multi-Human, Multi-Agent, Multi-Computer)

Untuk mendukung riset yang dikerjakan oleh banyak orang dan dijalankan di banyak mesin, Nusantara-Agent mengadopsi prinsip **Distributed Research Environment**.

### 15.1 Sinkronisasi Lintas Komputer

| Komponen | Solusi Sinkronisasi | Alasan |
|----------|---------------------|--------|
| **Source Code** | Git + GitHub | Standar kolaborasi kode & versioning |
| **Knowledge Graph** | Neo4j Aura / Shared DB | Satu sumber kebenaran (Single Source of Truth) untuk data graf |
| **Vector Database** | Qdrant Cloud / Dockerized Shared | Konsistensi hasil retrieval lintas komputer |
| **API Keys/Secrets** | `.env` (Local) + Vault (Shared) | Keamanan akses DeepSeek API |
| **Data Mentah (PDF)** | Shared Cloud Drive / DVC | Memastikan semua peneliti bekerja pada korpus yang sama |

### 15.2 Interaksi Multi-Human & Multi-Agent

Sistem dirancang dengan mekanisme **Human-in-the-Loop (HITL)**:

1.  **AI sebagai Drafter**: Agen mengekstrak tripel dan menyusun draf jawaban.
2.  **Human sebagai Validator**: Peneliti meninjau hasil ekstraksi (Eksperimen 1) dan memberikan feedback melalui file anotasi.
3.  **Collaborative Refinement**: Feedback manusia diumpankan kembali ke agen supervisor untuk memperbaiki penalaran dalam siklus *self-correction*.

### 15.3 Workflow Peneliti Terdistribusi

Setiap anggota tim riset mengikuti protokol berikut:
1.  **Environment Parity**: Menggunakan `requirements.txt` dan Docker untuk memastikan hasil eksperimen konsisten di komputer manapun.
2.  **Atomic Commits**: Mendokumentasikan setiap eksperimen (seperti folder `experiments/`) secara mandiri sehingga bisa di-review oleh anggota tim lain.
3.  **Shared Memory**: Menggunakan sistem logging terpusat untuk melacak API cost dan efektivitas prompt lintas pengguna.

---

## 16. Appendix

### A. Contoh Kasus Uji (Golden Test Set Preview)

**Kasus 1 (Sedang): Waris Tanah di Minangkabau**

```json
{
  "id": "GTS-001",
  "domain": "waris",
  "adat": "Minangkabau", 
  "difficulty": "sedang",
  "kasus": "Seorang laki-laki Minangkabau bernama Rajo meninggal dunia. 
    Ia memiliki sebidang tanah yang ia beli sendiri dari hasil usaha dagangnya 
    di Jakarta selama 20 tahun. Anak-anak Rajo menuntut tanah tersebut sebagai 
    warisan. Namun, kemenakan Rajo (anak dari saudara perempuan Rajo) juga 
    menuntut berdasarkan hukum adat Minangkabau.",
  "pertanyaan": "Siapa yang berhak atas tanah tersebut?",
  "jawaban_nasional": "Menurut KUHPerdata Pasal 832, anak-anak Rajo sebagai 
    ahli waris utama berhak atas harta peninggalan ayah mereka.",
  "jawaban_adat": "Dalam adat Minangkabau, perlu dibedakan antara Pusako 
    Tinggi dan Pusako Rendah. Tanah yang dibeli sendiri oleh Rajo termasuk 
    Pusako Rendah (harta pencaharian). Untuk Pusako Rendah, ada perbedaan 
    pendapat: sebagian ulama adat mengatakan ini jatuh ke kemenakan 
    (matrilineal), sebagian lagi mengakui hak anak.",
  "jawaban_ideal": "Kasus ini melibatkan konflik antara hukum nasional 
    (KUHPerdata) dan hukum adat Minangkabau. Tanah tersebut terklasifikasi 
    sebagai Pusako Rendah (harta pencaharian, bukan harta turun-temurun). 
    Menurut hukum nasional, anak-anak berhak. Menurut adat tradisional, 
    kemenakan berhak. Namun, yurisprudensi MA (Putusan MA No. 179 K/Sip/1961) 
    cenderung mengakui hak anak atas harta pencaharian orang tua. Dengan 
    demikian, dalam praktik hukum modern, anak-anak Rajo memiliki klaim 
    yang lebih kuat, meskipun kemenakan bisa mengajukan keberatan 
    berdasarkan adat.",
  "konsep_kunci": ["Pusako Tinggi", "Pusako Rendah", "Kemenakan", "Mamak"],
  "tingkat_konflik": "sedang"
}
```

**Kasus 2 (Sulit): Hak Waris Perempuan di Bali**

```json
{
  "id": "GTS-002",
  "domain": "waris",
  "adat": "Bali",
  "difficulty": "sulit",
  "kasus": "Ni Kadek, seorang perempuan Bali, menuntut bagian warisan dari 
    tanah keluarga (pekarangan desa) setelah ayahnya meninggal. Ia adalah 
    anak tunggal — tidak memiliki saudara laki-laki. Menurut adat Bali yang 
    patrilineal, hak waris utama ada pada anak laki-laki (sentana). Namun 
    Ni Kadek berargumen berdasarkan Putusan MDP Bali No. 01/KEP/PSM-3/
    MDP Bali/X/2010 yang mulai mengakui hak waris perempuan Bali.",
  "pertanyaan": "Apakah Ni Kadek berhak atas warisan tanah keluarga?",
  "jawaban_ideal": "Kasus ini sangat kompleks karena melibatkan evolusi 
    hukum adat Bali itu sendiri. Secara tradisional, adat Bali (patrilineal) 
    tidak memberikan hak waris tanah kepada perempuan. Namun, Keputusan 
    Pesamuhan Agung III MUDP Bali tahun 2010 telah mengakui hak terbatas 
    perempuan Bali atas warisan. Ditambah lagi, hukum nasional (UU HAM, 
    CEDAW) menjamin kesetaraan gender. Sebagai anak tunggal, Ni Kadek 
    memiliki klaim kuat baik dari hukum nasional maupun dari evolusi 
    adat Bali modern, meskipun sebagian masyarakat adat konservatif 
    mungkin masih menolak.",
  "tingkat_konflik": "tinggi"
}
```

### B. Contoh Prompt DeepSeek untuk Triple Extraction

```python
SYSTEM_PROMPT = """Kamu adalah ahli hukum adat Indonesia dan knowledge engineer.
Tugasmu mengekstrak relasi terstruktur dari teks tentang hukum adat.

ATURAN:
1. Ekstrak HANYA relasi yang eksplisit atau sangat kuat tersirat dalam teks.
2. Gunakan bahasa Indonesia untuk semua entitas dan relasi.
3. Pertahankan istilah adat dalam bahasa aslinya.
4. Berikan confidence score berdasarkan kejelasan relasi dalam teks.
5. Kategorikan setiap tripel ke salah satu: norma, konsep, prosedur, entitas, hierarki.

FORMAT OUTPUT (JSON):
{
  "triples": [
    {
      "head": "string",
      "relation": "string", 
      "tail": "string",
      "category": "norma|konsep|prosedur|entitas|hierarki",
      "confidence": 0.0-1.0,
      "source_sentence": "kalimat asal dalam teks"
    }
  ],
  "domain_terms": ["istilah adat yang ditemukan"],
  "ambiguities": ["hal-hal yang ambigu dan butuh validasi manusia"]
}"""

USER_PROMPT_TEMPLATE = """Domain Adat: {domain}
Teks sumber:
---
{text_chunk}
---

Ekstrak semua relasi hukum adat dari teks di atas."""
```

### C. Referensi Kunci (Top 20 untuk Paper)

1. Hu et al. (2025). "Self-correcting Agentic Graph RAG for clinical decision support." *Frontiers in Medicine*.
2. Song et al. (2025). "KG-R1: Efficient and Transferable Agentic KG RAG via RL." *arXiv:2509.26383*.
3. Zhou & Wang (2025). "From RAG to Agentic AI." *VLDB Workshop*.
4. Ma et al. (2025). "KA-RAG: Integrating KG and Agentic RAG." *Applied Sciences*.
5. Colelough et al. (2025). "Neuro-Symbolic AI in 2024: A Systematic Review." *arXiv:2501.05435*.
6. LexID Team (UI). "Metadata and Semantic KG Construction of Indonesian Legal Document."
7. Griffiths, J. (1986). "What is Legal Pluralism?" *Journal of Legal Pluralism*.
8. Hofstede, G. (2011). *Dimensionalizing Cultures: The Hofstede Model in Context.*
9. Singh et al. (2025). "Global MMLU." *arXiv:2412.03304*.
10. ALM-Bench Team (2025). "All Languages Matter Benchmark." *CVPR 2025*.
11. IndoLaw Dataset. HuggingFace: bstds/indo_law.
12. NusaCrowd Consortium. "NusaCrowd: Open Source for Indonesian NLP."
13. Edge et al. (2025). "GraphRAG: Graph-based RAG." *Microsoft Research*.
14. Es et al. (2024). "RAGAS: Automated Evaluation of RAG." *EACL 2024*.
15. Masoud et al. (2023). "Cultural Alignment in LLMs: Hofstede's Dimensions." *arXiv:2309.12342*.
16. Kautz, H. (2022). "The Third AI Summer." *AAAI Presidential Address*.
17. Lewis et al. (2020). "Retrieval-Augmented Generation." *NeurIPS 2020*.
18. Yao et al. (2023). "ReAct: Synergizing Reasoning and Acting." *ICLR 2023*.
19. Shinn et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement." *NeurIPS 2023*.
20. Besta et al. (2024). "Graph of Thoughts." *AAAI 2024*.

---

*Dokumen ini bersifat hidup (living document) dan akan diperbarui seiring kemajuan proyek. Versi terbaru selalu tersedia di repository proyek.*

**Last updated**: 6 Februari 2026  
**Next review**: Akhir Februari 2026 (setelah Fase 1 Minggu 1-2)
