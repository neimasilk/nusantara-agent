# Strategic Review: Nusantara-Agent
**Tanggal:** 2026-02-12
**Reviewer:** Top-level strategic agent (Opus 4.6)
**Scope:** Full project audit untuk Q1 publication feasibility

---

## Executive Summary

Proyek ini memiliki **2 aset genuine** yang bernilai publikasi:
1. **95 aturan hukum adat terverifikasi expert** di 3 domain (Minangkabau, Bali, Jawa)
2. **82 kasus hukum berlabel expert** dengan 3-rater voting

Tetapi proyek ini juga memiliki **4 klaim fatal** yang tidak didukung evidensi:
1. "GraphRAG" — tidak ada graph database maupun RAG pipeline
2. "Multi-Agent Agentic" — sequential prompt chain dengan negative result
3. "High accuracy" — 41.67% offline, 72.73% hanya pada N=22 non-reproducible
4. "Scale" — 24 active cases, jauh dari target 200+

**Rekomendasi: PIVOT** dari "Neuro-Symbolic Agentic GraphRAG" ke **"Neuro-Symbolic Legal Reasoning with Expert-Verified Customary Law Rules"**.

---

## 1. Audit Arsitektur

### 1.1 Apa yang Benar-Benar Ada (Inventaris Kode)

| Komponen | File | LOC | Status |
|---|---|---|---|
| Triple Extractor | `src/kg_engine/extractor.py` | 35 | Wrapper DeepSeek, minimal |
| KG Search | `src/kg_engine/search.py` | 46 | Simple keyword matching |
| Text Processor | `src/utils/text_processor.py` | 36 | PDF extraction, chunking |
| Rule Engine | `src/symbolic/rule_engine.py` | 143 | **Functional** — Clingo ASP |
| Orchestrator | `src/agents/orchestrator.py` | 434 | Sequential chain + offline fallback |
| Router | `src/agents/router.py` | 179 | Keyword-based classification |
| Debate | `src/agents/debate.py` | 298 | **Unused** — negative result |
| Self-Correction | `src/agents/self_correction.py` | 147 | **Unused** — no measurable improvement |
| Pipeline | `src/pipeline/nusantara_agent.py` | 521 | Keyword matching + rules fallback |
| LLM Judge | `src/evaluation/llm_judge.py` | 85 | Skeleton |
| Adversarial Reviewer | `src/review/adversarial_reviewer.py` | 348 | Review automation |
| **Total** | | **~2,300** | |

### 1.2 Apa yang TIDAK Ada (Klaim Tanpa Implementasi)

| Klaim | Status | Detail |
|---|---|---|
| Neo4j Graph Database | **TIDAK ADA** | ART-036 PENDING. `JsonGraphRetriever` membaca 1 file JSON |
| Qdrant Vector Database | **TIDAK ADA** | ART-037 PENDING. `InMemoryVectorRetriever` = keyword matching 5 kalimat |
| Real RAG Pipeline | **TIDAK ADA** | Tidak ada embedding, tidak ada semantic search |
| Parallel Agent Execution | **Nominal** | LangGraph parallel edges ada, tapi kedua agent independen (tidak ada komunikasi) |
| Debate Protocol (Genuine) | **ABANDONED** | F-009: negative result, tidak digunakan di pipeline |
| Self-Correction Loop | **ABANDONED** | Tidak ada evidence improvement |
| NusaCulture-Bench | **TIDAK ADA** | ART-052 PENDING |
| Independent Evaluation | **BLOCKED** | ART-031 BLOCKED pada ART-028 dan ART-030 |

### 1.3 Analisis Ketergantungan Kritis

```
Pipeline aktual (offline mode):
Query → Keyword Router → Keyword Fact Extraction → if/else Rules Fallback → JSON label

Pipeline aktual (LLM mode):
Query → Keyword Router → Keyword Fact Extraction → Clingo ASP → DeepSeek (3 calls) → JSON label
```

**Insight**: Bahkan di LLM mode, "retrieval" hanyalah keyword matching. Tidak ada actual retrieval dari knowledge base yang substantial.

---

## 2. Audit Metodologi

### 2.1 Evaluation Chain of Trust

```
Siapa yang membuat gold standard?  → 3 ahli hukum (genuine human)
Siapa yang mengisi annotations?    → Kimi/DeepSeek auto-fill (F-010: circular)
Siapa yang evaluasi output?        → Offline: if/else Python, LLM: DeepSeek (circular)
Statistical tests?                 → TIDAK ADA (zero p-values, zero CIs)
Inter-rater agreement?             → TIDAK DIHITUNG (Krippendorff Alpha absent)
```

**Verdict**: Chain of trust BROKEN di 3 tempat.

### 2.2 Sample Size Analysis

| Dataset | N | Minimum untuk Q1 | Gap |
|---|---|---|---|
| Active benchmark cases | 24 | 200+ | 176 kasus |
| Gold standard (human pool) | 82 | 200+ | 118 kasus |
| Rule engine test cases | 30 | 100+ | 70 kasus |
| Source texts per domain | 1-3 | 30+ | 27+ texts |
| Expert raters | 3 | 5+ | 2 raters |

Bahkan tanpa kekurangan lain, **N=24 tidak publishable di jurnal manapun**. Tidak ada tes statistik yang memiliki power pada N ini.

### 2.3 Accuracy Reality Check

| Run | N | Accuracy | Mode | Reproducible? |
|---|---|---|---|---|
| Phase 1 (pre-patch) | 22 | 54.55% | Mixed | No |
| Sprint 2 peak | 22 | 72.73% | LLM | No (env-dependent) |
| Post-patch N=24 | 24 | 41.67% | Offline | Yes |

**Masalah**: Hasil terbaik (72.73%) dicapai di mode LLM yang tidak bisa direproduksi karena dependency issues (F-013). Satu-satunya angka reproducible adalah 41.67% — dan ini bukan "AI reasoning", ini adalah keyword matching Python.

---

## 3. Audit Proses dan Kolaborasi

### 3.1 Overhead Dokumentasi

```
Jumlah file docs/handoffs/         : 35 dokumen
Jumlah file docs/human_only/       : 60+ artefak
Jumlah file docs/archive/          : 20+ dokumen
Jumlah PROTOCOL.md + REVIEW.md     : 16+ dokumen
Total ARTs di registry              : 91
```

**Rasio dokumentasi : kode ≈ 170:1 (dalam jumlah file)**

Setiap handoff antar-agent AI menghasilkan 1-3 dokumen baru. Setiap review menghasilkan 1-2 dokumen baru. Proyek ini mengkonsumsi energy untuk mendokumentasikan proses, bukan menghasilkan output.

### 3.2 Multi-AI Collaboration Anti-Pattern

Proyek menggunakan 5+ AI agents (Claude, Gemini, Kimi, DeepSeek, Trae) dalam workflow yang complex:

```
Round 1: Gemini annotate → Round 2: Kimi annotate → Round 3: Claude review
→ Round 4: Trae audit → Round 5: Human decision → Round 6: Kimi patch
→ Round 7: Multi-agent debate (ballot system)
```

**Anti-pattern yang teridentifikasi:**
1. **Annotation Laundering**: AI-generated labels diproses melalui voting multi-AI untuk terlihat seperti "independent annotation"
2. **Context Inflation**: Setiap handoff menambah context document, creating information overload
3. **Decision Diffusion**: Keputusan sederhana (label A/B/C/D) memerlukan 7 round karena setiap AI memiliki "pendapat"
4. **Accountability Gap**: Tidak jelas siapa yang bertanggung jawab atas keputusan final

### 3.3 Human Bottleneck

82 kasus dihasilkan oleh **satu ahli utama** (Dr. Hendra) dalam 7 batch marathon. Ahli ke-2 dan ke-3 berkontribusi sebagai rater, bukan generator. Ini berarti:
- Gold standard dipengaruhi bias 1 orang
- Diversity perspektif terbatas
- Single point of failure

---

## 4. Failure Registry Gap Analysis

13 failures terdokumentasi — ini bagus sebagai prinsip scientific honesty. Tapi:

| Failure | Tindakan yang Diklaim | Tindakan Aktual |
|---|---|---|
| F-001: Overconfident scores | ACKNOWLEDGED | Tidak ada fix |
| F-002: Circular evaluation | MITIGATED via Exp 06 | Exp 06 masih BLOCKED |
| F-003: Linear multi-agent | MITIGATED via Exp 07 | Exp 07 = negative result |
| F-007: Rule engine 70% | ACKNOWLEDGED | Tidak ada fix |
| F-008: Self-referential gold | ACKNOWLEDGED | Partially fixed (3 raters) |
| F-009: Orchestration negative | ACKNOWLEDGED | Tidak ada iterasi |
| F-011: Accuracy drop | MITIGATED via ART-090-096 | Offline = 41.67% |
| F-013: Env dependency | MITIGATED operasional | Scientific gap tetap |

**Pattern**: Banyak yang "ACKNOWLEDGED" atau "MITIGATED" tapi sebenarnya **UNRESOLVED**.

---

## 5. Rekomendasi Pivot

### 5.1 Paper Scope Baru (Proposed)

**Judul**: *"Formal Customary Law Rules as Symbolic Anchors for LLM-based Legal Reasoning: Evidence from Indonesian Pluralistic Law"*

**Journal Target**: Knowledge-Based Systems atau Expert Systems with Applications (keduanya Q1 dan menerima legal AI + symbolic reasoning).

**Kontribusi yang bisa diklaim:**
1. **Knowledge Base**: 95 aturan hukum adat terverifikasi expert dari 3 domain Indonesia — kontribusi domain knowledge yang unik
2. **Formal Encoding**: ASP encoding yang bisa detect norm conflicts antar-sistem hukum
3. **Empirical Finding**: Divergence 33.3% antara symbolic reasoning dan LLM menunjukkan bahwa symbolic anchor diperlukan
4. **Benchmark Dataset**: 82+ kasus dengan expert annotation (perlu diperluas ke 100+)

**Klaim yang HARUS di-drop:**
- "GraphRAG" — tidak ada graph database
- "Agentic" / "Multi-Agent" — tidak ada genuine orchestration
- "High accuracy" — 41.67% offline bukan evidence apapun
- "Cultural Consistency Score" — belum tervalidasi

### 5.2 Minimum Viable Paper (MVP)

Untuk menghasilkan paper Q1 dari posisi saat ini, diperlukan:

| # | Task | Effort | Blocker |
|---|---|---|---|
| 1 | Hitung Inter-Rater Agreement (3 raters, 24 overlapping cases) | 1 hari | None — data ada |
| 2 | Re-run Exp 05 dengan fixed ASP pada N > 50 | 2-3 hari | Perlu test cases |
| 3 | Expand gold standard ke 100+ kasus | 2-4 minggu | Human effort |
| 4 | Run LLM+Rules vs LLM-only comparison pada 100+ kasus | 3-5 hari | API cost |
| 5 | Statistical tests (McNemar, paired t-test, CIs) | 1-2 hari | Depends on #4 |
| 6 | Compare 2-3 LLM (DeepSeek, GPT-4, Claude) | 3-5 hari | API cost |
| 7 | Write paper | 2-3 minggu | Depends on all above |

**Total: ~6-8 minggu** dari sekarang dengan fokus.

### 5.3 Apa yang Harus Dibuang/Diarsipkan

| Komponen | Keputusan | Alasan |
|---|---|---|
| Neo4j / Qdrant planning | CANCEL | Tidak ada, tidak akan ada dalam timeline |
| Debate protocol | ARCHIVE | Negative result — bisa jadi "future work" |
| Self-correction loop | ARCHIVE | No evidence of improvement |
| CCS Metric (Exp 10) | CANCEL | Unvalidated, premature |
| NusaCulture-Bench (ART-052) | DEFER | Nice-to-have, bukan core contribution |
| Multi-agent handoff system | SIMPLIFY | Satu agent, satu pipeline, satu evaluasi |
| 90% of docs/handoffs/ | ARCHIVE | Historical record, not active docs |

### 5.4 Apa yang Harus Dikerjakan Segera

**Minggu 1: Foundation**
- [ ] Hitung Fleiss Kappa / Krippendorff Alpha dari 24 overlapping cases
- [ ] Bersihkan gold standard: resolve 2 SPLIT cases (CS-MIN-005, CS-MIN-015)
- [ ] Fix environment: install clingo + langchain sehingga LLM mode berjalan
- [ ] Re-run benchmark di LLM mode untuk dapatkan angka reproducible

**Minggu 2-3: Expand**
- [ ] Expand test cases ke 100+ (perlu human expert)
- [ ] Generate test cases untuk Bali dan Jawa rules (saat ini mostly Minangkabau)
- [ ] Run LLM+Rules vs LLM-only comparison

**Minggu 4-5: Validate**
- [ ] Statistical significance tests
- [ ] Try 1-2 LLM alternatif (tanpa DeepSeek)
- [ ] Error analysis: di mana rules membantu, di mana rules gagal?

**Minggu 6-8: Write**
- [ ] Draft paper
- [ ] Internal review
- [ ] Submit

---

## 6. Risiko Setelah Pivot

| Risiko | Likelihood | Mitigation |
|---|---|---|
| N=82 masih terlalu kecil | HIGH | Target 100 minimum, 150 ideal |
| Inter-rater agreement rendah (<0.6) | MEDIUM | Jika ya, ini menjadi limitation yang harus diakui |
| Rules tidak signifikan improve LLM | MEDIUM | Jika ya, ini negative result — tetap publishable |
| DeepSeek quality terlalu rendah | LOW | Sudah punya data; bisa switch model |
| Expert availability | HIGH | Dr. Hendra adalah bottleneck; perlu backup |

---

## 7. Penilaian Jujur: Apakah Paper Q1 Feasible?

**Dengan pivot**: **Ya, feasible**, tapi ketat.

Kontribusinya tidak akan "revolutionary" — tapi solid dan defensible:
- Expert-verified legal rules encoded formally = genuine contribution
- Evidence bahwa symbolic anchoring membantu LLM = useful finding
- Indonesian customary law domain = underexplored in NLP literature

**Tanpa pivot**: **Tidak feasible**. Tidak ada reviewer yang akan menerima paper yang klaim "GraphRAG" tapi tidak punya graph database.

---

## 8. Checklist untuk Owner

- [ ] Apakah setuju dengan pivot dari "GraphRAG" ke "Neuro-Symbolic Legal Reasoning"?
- [ ] Apakah bisa mendapatkan 20-30 kasus tambahan dari expert dalam 2-3 minggu?
- [ ] Apakah bersedia investasi API cost untuk re-run benchmark di LLM mode?
- [ ] Apakah bersedia drop klaim multi-agent orchestration (negative result)?
- [ ] Apakah punya akses ke 1-2 LLM alternatif (GPT-4 atau Claude) untuk comparison?

---

---

## 9. Code Quality Notes (from Architecture Review)

### Positif
- Code quality: 7.5/10 — clean structure, defensive programming, well-tested rule engine
- 79 tests passing, deterministic, edge cases covered
- Fallback chains work correctly

### Harus Diperbaiki
1. **`_get_llm()` diduplikasi 4x** — di orchestrator.py, debate.py, router.py, self_correction.py. Extract ke shared utils.
2. **Supervisor agent (80+ LOC if/else) ZERO tests** — ini logic terpenting tapi tidak punya unit test.
3. **PrologEngine (54 LOC) = dead code** — tidak pernah digunakan. Hapus.
4. **Debate flow (299 LOC) tidak dipanggil pipeline** — hanya digunakan di Exp 07 (negative result). Archive.
5. **Rule engine atoms passed as text strings** — LLM agents menerima atoms tapi tidak diwajibkan menghormatinya. Integrasi symbolic-neural masih loose.

### Implikasi untuk Paper
- Klaim "neuro-symbolic integration" harus di-qualify: "loosely-coupled" bukan "deeply integrated"
- Klaim "multi-agent debate" harus diganti: sequential agents + heuristic supervisor
- Supervisor heuristic perlu unit tests sebelum accuracy claims dianggap reproducible

---

*Review ini bersifat konstruktif. Proyek ini memiliki fondasi yang nyata (rules + expert data) — hanya perlu difokuskan.*
