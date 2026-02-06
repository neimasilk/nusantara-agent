# Failure Registry

Living document yang mencatat setiap kegagalan, hasil negatif, dan pendekatan yang ditinggalkan. Dokumen ini memiliki **prominence yang sama** dengan daftar keberhasilan dan akan menjadi sumber utama untuk Limitations section di paper.

**Prinsip:** Kegagalan yang terdokumentasi adalah kontribusi ilmiah. Kegagalan yang disembunyikan adalah fraud akademik.

---

## Cara Menggunakan

1. Setiap eksperimen yang selesai (baik sukses maupun gagal) HARUS menambahkan entry di sini
2. Gunakan format di bawah untuk konsistensi
3. Jangan hapus entry — ini adalah catatan historis
4. Entry ditambahkan secara kronologis

---

## Format Entry

```markdown
### F-[NNN]: [Judul Singkat]

- **Tanggal:** YYYY-MM-DD
- **Eksperimen:** [ID eksperimen terkait]
- **Kategori:** [NEGATIVE_RESULT / ABANDONED_APPROACH / TECHNICAL_FAILURE / ASSUMPTION_VIOLATED / LIMITATION_DISCOVERED]
- **Severity:** [CRITICAL / MAJOR / MINOR]
- **Deskripsi:** [Apa yang terjadi]
- **Expected vs Actual:** [Apa yang diharapkan vs apa yang terjadi]
- **Root Cause:** [Mengapa ini terjadi]
- **Implikasi untuk Paper:** [Bagaimana ini mempengaruhi klaim]
- **Tindakan:** [MITIGATED / ACKNOWLEDGED / PIVOT / UNRESOLVED]
- **Detail Tindakan:** [Apa yang dilakukan sebagai respons]
```

---

## Registry

### F-001: Confidence Score Overconfidence

- **Tanggal:** 2026-02-06
- **Eksperimen:** 01_triple_extraction
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** MAJOR
- **Deskripsi:** DeepSeek memberikan confidence score 1.0 secara konsisten untuk semua tripel yang diekstrak, terlepas dari ambiguitas teks sumber.
- **Expected vs Actual:** Expected: distribusi confidence 0.6-1.0 berdasarkan kejelasan teks. Actual: semua 1.0.
- **Root Cause:** Model LLM cenderung overconfident dalam self-assessment. Confidence score yang di-generate oleh model yang sama yang mengekstrak tripel tidak meaningful secara statistik.
- **Implikasi untuk Paper:** Klaim tentang "confidence-weighted reasoning" tidak valid tanpa kalibrasi eksternal. Confidence score dari LLM bukan probability estimate yang calibrated.
- **Tindakan:** ACKNOWLEDGED — akan ditangani di Exp 06 (independent evaluation pipeline)
- **Detail Tindakan:** Perlu external confidence calibration, bukan self-reported scores

### F-002: Circular Evaluation (DeepSeek generates + evaluates)

- **Tanggal:** 2026-02-06
- **Eksperimen:** 01-04 (semua)
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** CRITICAL
- **Deskripsi:** DeepSeek digunakan untuk mengekstrak tripel DAN hasilnya dinilai berdasarkan inspeksi kualitatif tanpa ground truth independen. Tidak ada annotator manusia terlatih atau model independen yang memvalidasi.
- **Expected vs Actual:** Expected: evaluasi independen. Actual: self-evaluation.
- **Root Cause:** Pilot phase — belum ada infrastruktur evaluasi independen.
- **Implikasi untuk Paper:** Semua klaim "BERHASIL" dari Exp 1-4 bersifat preliminary dan tidak publishable tanpa validasi independen. Paper Q1 akan menolak self-evaluation.
- **Tindakan:** MITIGATED — Exp 06 dirancang khusus untuk membangun independent evaluation pipeline
- **Detail Tindakan:** Rencana: (1) LLM berbeda sebagai judge, (2) 5 annotator manusia, (3) putusan MA sebagai ground truth

### F-003: Linear Multi-Agent Chain (bukan real orchestration)

- **Tanggal:** 2026-02-06
- **Eksperimen:** 03_multi_agent_basic
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** MAJOR
- **Deskripsi:** Arsitektur multi-agent hanyalah sequential chain (Nasional → Adat → Supervisor) tanpa paralelisme, debate, self-correction, atau conditional routing. Ini secara teknis bukan "orchestration" dalam arti literatur multi-agent systems.
- **Expected vs Actual:** Expected: demonstrasi orchestration capability. Actual: linear pipeline yang bisa dicapai dengan 3 API calls berurutan.
- **Root Cause:** Ini adalah baseline/pilot — sengaja disederhanakan.
- **Implikasi untuk Paper:** Klaim "agentic" harus di-qualify. Tanpa parallel execution, debate protocol, atau adaptive routing, kontribusi multi-agent sulit dibedakan dari prompt chaining.
- **Tindakan:** MITIGATED — Exp 07 akan mengimplementasikan parallel retrieval, debate protocol, dan conditional routing
- **Detail Tindakan:** Lihat docs/methodology_fixes.md #3

### F-004: Scale Terlalu Kecil untuk Klaim Generalization

- **Tanggal:** 2026-02-06
- **Eksperimen:** 01-04 (semua)
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** CRITICAL
- **Deskripsi:** Total data: 1 teks sumber (~118 kata), ~30 tripel, 1 test query. Ini jauh dari cukup untuk klaim apapun tentang generalizability atau effectiveness.
- **Expected vs Actual:** Expected: proof of concept. Actual: memang proof of concept, tapi analysis.md menggunakan bahasa yang terlalu kuat ("BERHASIL", "SANGAT BERHASIL") untuk skala ini.
- **Root Cause:** Fase pilot — skala kecil by design.
- **Implikasi untuk Paper:** N=1 tidak publishable di jurnal manapun. Perlu scaling signifikan: 10K+ triples, 200+ test cases, 3+ domains.
- **Tindakan:** ACKNOWLEDGED — scaling plan sudah ada (Phase 2-3 di PRD)
- **Detail Tindakan:** Target: 10K triples, 200 test cases, 5 annotators, 3 domains

### F-005: Syntax Errors dalam AI-Generated Code

- **Tanggal:** 2026-02-06
- **Eksperimen:** 04_batch_ingestion
- **Kategori:** TECHNICAL_FAILURE
- **Severity:** MINOR
- **Deskripsi:** Banyak SyntaxError saat AI agent menulis script — baris baru yang tidak disengaja dalam string templates.
- **Expected vs Actual:** Expected: clean code generation. Actual: multiple iterations needed.
- **Root Cause:** Keterbatasan AI code generation dalam format tertentu (heredoc, multiline strings).
- **Implikasi untuk Paper:** Tidak langsung berdampak pada paper, tapi menunjukkan bahwa HITL tetap perlu untuk code quality.
- **Tindakan:** MITIGATED
- **Detail Tindakan:** Menggunakan format string yang lebih bersih, testing sebelum commit

### F-006: Draft Rules Tanpa Verifikasi Domain Expert

- **Tanggal:** 2026-02-06
- **Eksperimen:** 05_rule_engine (preparation)
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** MAJOR
- **Deskripsi:** Aturan Minangkabau yang dikumpulkan dari sumber open-access disusun sebagai draft oleh AI tanpa verifikasi langsung dari domain expert.
- **Expected vs Actual:** Expected: rules tervalidasi oleh pakar adat. Actual: rules masih provisional dan rawan salah tafsir.
- **Root Cause:** Tidak ada akses langsung ke ahli adat Minangkabau selama fase awal.
- **Implikasi untuk Paper:** Klaim rule engine bersifat sementara; validitas eksternal dibatasi sampai verifikasi manusia tersedia.
- **Tindakan:** ACKNOWLEDGED
- **Detail Tindakan:** Label semua rules sebagai DRAFT_NEEDS_HUMAN_REVIEW; verifikasi manual akan dijadwalkan sebelum paper final.

---

## Statistik Ringkasan

| Kategori | Count | Critical | Major | Minor |
|----------|-------|----------|-------|-------|
| NEGATIVE_RESULT | 0 | 0 | 0 | 0 |
| ABANDONED_APPROACH | 0 | 0 | 0 | 0 |
| TECHNICAL_FAILURE | 1 | 0 | 0 | 1 |
| ASSUMPTION_VIOLATED | 0 | 0 | 0 | 0 |
| LIMITATION_DISCOVERED | 5 | 2 | 3 | 0 |
| **TOTAL** | **6** | **2** | **3** | **1** |

*Last updated: 2026-02-06*
