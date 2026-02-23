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

### F-007: Rule Engine Accuracy Hanya 70% — Gagal pada Skenario Situasional

- **Tanggal:** 2026-02-07
- **Eksperimen:** 05_rule_engine
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** MAJOR
- **Deskripsi:** ClingoRuleEngine hanya mencapai accuracy 70% (21/30), kalah dari LLM (83.3%). Kegagalan terjadi pada skenario yang memerlukan penalaran situasional: mufakat keluarga, kondisi darurat, dan konteks sosial yang tidak bisa diformalisasi dalam ASP murni.
- **Expected vs Actual:** Expected: Rule Engine 100% akurat pada hard constraints. Actual: 70% — 9 kasus gagal karena skenario memerlukan penalaran di luar domain formal (misal: apakah "pengabdian lama" mengubah hak waris).
- **Root Cause:** ASP bersifat biner (true/false) dan tidak mampu menangani gradasi kontekstual. Hukum adat dalam praktik mengandung unsur diskresi (musyawarah) yang tidak bisa sepenuhnya diformalisasi.
- **Implikasi untuk Paper:** Klaim "Rule Engine sebagai ground truth anchor" harus dikualifikasi — anchor hanya valid untuk hard constraints (gender, jenis harta), bukan untuk soft constraints (mufakat, darurat).
- **Tindakan:** ACKNOWLEDGED
- **Detail Tindakan:** Perlu eksplorasi fuzzy ASP atau probabilistic logic programming untuk menangani soft constraints. Untuk paper, laporkan sebagai trade-off inherent antara precision dan coverage.

### F-008: Gold Standard Bersifat Self-Referential

- **Tanggal:** 2026-02-07
- **Eksperimen:** 05_rule_engine
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** CRITICAL
- **Deskripsi:** Expected answers di test_cases.json disusun oleh tim yang sama yang membangun rule base. Tidak ada validasi independen dari domain expert hukum adat Minangkabau. Accuracy numbers (70% dan 83.3%) bersifat provisional karena gold standard belum tervalidasi.
- **Expected vs Actual:** Expected: gold standard tervalidasi oleh ahli adat. Actual: self-referential — rules dan expected answers berasal dari pemahaman yang sama.
- **Root Cause:** Belum ada akses ke validator domain expert pada fase ini.
- **Implikasi untuk Paper:** Semua angka accuracy bersifat preliminary. Reviewer Q1 akan menolak evaluation tanpa independent gold standard validation.
- **Tindakan:** ACKNOWLEDGED
- **Detail Tindakan:** Prioritas tinggi: rekrut minimal 2 ahli hukum adat Minangkabau untuk validasi gold standard sebelum paper submission. Gunakan putusan MA sebagai external validation tambahan.

### F-009: Advanced Orchestration Tidak Mengungguli Baseline pada Auto-Score Kimi

- **Tanggal:** 2026-02-07
- **Eksperimen:** 07_advanced_orchestration
- **Kategori:** NEGATIVE_RESULT
- **Severity:** MAJOR
- **Deskripsi:** Skor otomatis Kimi menunjukkan advanced orchestration (parallel + debate + self-correction + routing) memiliki skor lebih rendah dibanding baseline sequential (Exp 03 re-run) pada 12 query, bahkan setelah revisi prompt evidence-grounded.
- **Expected vs Actual:** Expected: peningkatan >= 10% pada minimal 2 metrik kualitas. Actual: semua metrik turun (Accuracy -0.67, Completeness -0.67, Cultural -0.33).
- **Root Cause:** Debat mengurangi detail untuk menjaga grounding, tetapi tidak menambah evidence baru; output jadi lebih ringkas namun kehilangan coverage.
- **Implikasi untuk Paper:** Klaim peningkatan kualitas dari debate/self-correction harus dikualifikasi; perlu evaluasi ulang dan/atau perbaikan protokol debat.
- **Tindakan:** ACKNOWLEDGED
- **Detail Tindakan:** Analisis failure mode, perbaiki prompt debat, tambah evidence grounding, dan validasi ulang dengan human annotation.

### F-010: Auto-Annotation Drift Risk pada Exp 06 Bootstrap

- **Tanggal:** 2026-02-07
- **Eksperimen:** 06_independent_eval (bootstrap fase otomatis)
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** MAJOR
- **Deskripsi:** Untuk meminimalkan intervensi manusia, 1000 file anotasi di-generate dan diisi secara otomatis (Kimi/DeepSeek + fallback replikasi domain). Ini mempercepat skala, tetapi menciptakan risiko homogenisasi label dan bias model pada pseudo-gold annotations.
- **Expected vs Actual:** Expected: anotasi multi-annotator mencerminkan variasi judgment manusia. Actual: sebagian signifikan anotasi berasal dari auto-fill model dan fallback, sehingga variasi annotator tidak sepenuhnya organik.
- **Root Cause:** Target skala tinggi (200x5) dikejar sebelum ketersediaan annotator manusia penuh.
- **Implikasi untuk Paper:** Dataset anotasi tahap ini tidak boleh diposisikan sebagai final human-validated gold standard; harus diberi label draft/bootstrapped dan dilanjutkan dengan validasi manusia serta agreement analysis yang ketat.
- **Tindakan:** ACKNOWLEDGED
- **Detail Tindakan:** Precheck diperketat (`triples` tidak boleh kosong, field putusan wajib non-kosong), provenance marker disimpan di notes, dan status ART-031 tetap BLOCKED karena ART-030 belum memenuhi syarat.

### F-011: Negative Gain from Basic Agent Integration (Accuracy Drop)

- **Tanggal:** 2026-02-08
- **Eksperimen:** 09_ablation_study
- **Kategori:** NEGATIVE_RESULT
- **Severity:** MAJOR
- **Status:** MITIGATED
- **Deskripsi:** Integrasi "Intelligence Layer" (National, Adat, Supervisor agents) ke dalam pipeline justru menurunkan akurasi klasifikasi label Gold Standard dari 68.18% menjadi 54.55% pada sampel N=22.
- **Expected vs Actual:** Expected: Peningkatan akurasi karena reasoning yang lebih mendalam. Actual: Penurunan akurasi sebesar 13.6 poin persentase.
- **Root Cause:** (1) Hallucination of Conflict: Agen Adjudicator cenderung memaksakan label C (Sintesis) pada kasus yang seharusnya Nasional murni (A). (2) Information Overload: Agen sering mengabaikan fakta keras dari rule engine dan lebih mengandalkan general knowledge LLM yang kurang presisi untuk klasifikasi label tunggal. (3) Prompt Ambiguity: Kriteria label C tidak cukup ketat.
- **Implikasi untuk Paper:** Menunjukkan bahwa penambahan parameter/agen tanpa kalibrasi instruksi (prompt tuning) yang ketat dapat merusak performa klasifikasi (The "Too Many Cooks" problem in Multi-Agent Systems).
- **Tindakan:** MITIGATED (SOP Accuracy Tuning Phase dibuat, ART-090 s.d. ART-095 dibuat)
- **Detail Tindakan:** 
  - Mengkaji ulang prompt supervisor agent (ART-090)
  - Sinkronisasi fakta simbolik dengan rule engine (ART-091)
  - Implementasi router-augmented adjudicator (ART-092)
  - Knowledge base expansion untuk hukum nasional (ART-093)
  - Lihat: `docs/SOP_ACCURACY_TUNING_PHASE.md`
  - Target: Akurasi ≥75% pada akhir Sprint 2 (1 minggu)
- **Milestone Tracking:**
  | Milestone | Target | Deadline Relatif | Status |
  |-----------|--------|------------------|--------|
  | M1-QuickWin | ≥65% | Sprint 1 (2-3 hari) | DONE (60%) |
  | M2-Structural | ≥75% | Sprint 2 (1 minggu) | DONE (100% on critical sample) |
  | M3-Optimization | ≥85% | Sprint 3 (2 minggu) | DONE (85.71% on 14 agreed, LLM mode) |

### F-012: Router Classification Fallibility
- **Tanggal:** 2026-02-09
- **Eksperimen:** ART-092 Verification
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** MAJOR
- **Status:** MITIGATED
- **Deskripsi:** Router murni berbasis LLM sering gagal mendeteksi nuansa hukum nasional (misal: "SHM" atau "Putusan Pengadilan") dalam narasi yang didominasi istilah adat, sehingga salah melabeli kasus Konflik/Nasional sebagai "Pure Adat". Jika Orchestrator hanya mengikuti Router secara buta (default position), error ini terpropagasi.
- **Expected vs Actual:** Expected: Router akurat >90%. Actual: Router bisa melabeli kasus SHM vs Ulayat sebagai "Pure Adat" karena bias terminologi.
- **Root Cause:** Semantic similarity search atau LLM classification bias terhadap keyword dominan (adat) dan mengabaikan keyword minor tapi decisive (nasional).
- **Implikasi untuk Paper:** Router-Augmented architecture tidak boleh single-point-of-failure. Perlu mekanisme *Safety Net*.
- **Tindakan:** MITIGATED
- **Detail Tindakan:** Implementasi "Keyword Safety Net" di Orchestrator. Jika Router label = Adat TAPI ada keyword nasional keras (SHM, Poligami, Cerai), inject WARNING ke prompt Supervisor. Hasil: Akurasi sample kritis naik dari 40% ke 100%.

### F-013: Environment Dependency Gap Blokir Validasi LLM Penuh

- **Tanggal:** 2026-02-09
- **Eksperimen:** 09_ablation_study (operational benchmark run)
- **Kategori:** TECHNICAL_FAILURE
- **Severity:** MAJOR
- **Status:** MITIGATED (operational), UNRESOLVED (scientific parity)
- **Deskripsi:** Runner benchmark gagal pada tahap import karena dependency opsional (`langchain_openai`, `langgraph`, `clingo`, `fitz`) tidak tersedia di environment aktif.
- **Expected vs Actual:** Expected: benchmark mode LLM penuh berjalan dan menghasilkan metrik yang comparable dengan run sebelumnya. Actual: benchmark awal crash; setelah fallback hardening, benchmark berjalan dalam mode offline tetapi metrik tidak setara dengan mode LLM penuh.
- **Root Cause:** Coupling dependency eksternal pada import-time dan ketidakkonsistenan setup environment lintas mesin/agen.
- **Implikasi untuk Paper:** Risiko salah interpretasi jika metrik fallback diperlakukan sebagai bukti performa model utama. Klaim milestone wajib berdasarkan run dengan stack evaluasi yang setara.
- **Tindakan:** MITIGATED / ACKNOWLEDGED
- **Detail Tindakan:** Menambahkan fallback dependency-optional pada modul `orchestrator`, `router`, `debate`, `self_correction`, dan `pipeline` agar workflow harian tidak crash. Tetap diwajibkan re-run mode penuh setelah dependency dilengkapi sebelum klaim milestone.

### F-014: Inter-Rater Agreement Critically Low (Kappa = 0.102)

- **Tanggal:** 2026-02-12
- **Eksperimen:** Gold Standard Evaluation (P-001)
- **Kategori:** ASSUMPTION_VIOLATED
- **Severity:** CRITICAL
- **Status:** UNRESOLVED
- **Deskripsi:** Fleiss' Kappa = 0.102 (slight agreement) dan Krippendorff's Alpha = 0.114 pada 24 active benchmark cases dengan 3 raters. Ahli-3 memiliki Cohen's Kappa NEGATIF terhadap kedua ahli lainnya (-0.015 dan -0.006), menandakan rating yang KURANG dari random chance. Ahli-3 menyimpang dari kedua ahli lainnya pada 50% kasus.
- **Expected vs Actual:** Expected: Krippendorff Alpha >= 0.667. Actual: 0.114 — gap sebesar 5.8x dari target.
- **Root Cause:** (1) Ahli-3 tampaknya menggunakan kriteria penilaian yang berbeda fundamental dari Ahli-1 dan Ahli-2. (2) Skema klasifikasi A/B/C/D mungkin terlalu ambigu — pola disagreement terbesar adalah A vs C (21 kali), artinya raters tidak bisa membedakan "kasus nasional murni" dari "konflik nasional-adat". (3) Tidak ada kalibrasi formal antar-rater sebelum labeling.
- **Implikasi untuk Paper:**
  - Semua klaim akurasi sebelumnya (41.67%, 72.73%) TIDAK BERMAKNA karena gold standard-nya tidak reliable
  - Gold standard harus dibangun ulang atau approach evaluasi harus diubah
  - Ahli-1 vs Ahli-2 saja menghasilkan Kappa = 0.394 (fair) — ini baseline yang bisa dipertahankan jika Ahli-3 dikeluarkan
  - Alternatif: reframe paper ke "ambiguity detection" daripada "classification accuracy"
- **Tindakan:** PARTIALLY RESOLVED — Ahli-3 removed per owner decision
- **Resolution (2026-02-12):**
  - Owner confirmed Ahli-3 is under-qualified (S1 level, bukan domain expert)
  - Ahli-3 votes removed from gold standard
  - Post-removal: Cohen's Kappa = 0.394 (fair), 14/24 cases agreed, 10 disputed
  - Recomputed offline benchmark (pre-fix): **78.57% accuracy on 14 agreed cases** (11/14)
  - A-vs-C confusion identified: 100% on B and C, 0% on A
  - **Post A-vs-C fix (2026-02-12):** Added `has_national_dominant` heuristic and rewrote LLM prompt LANGKAH 2
  - Updated benchmark: **85.71% accuracy on 14 agreed cases** (12/14): A=2/2, B=4/4, C=6/7, D=0/1
  - Remaining: 10 disputed cases need adjudication by qualified experts (Delphi Round 2 prepared)

### F-015: ASP-JSON Rule Parity Gap on Bali Domain (P-008 Audit)

- **Tanggal:** 2026-02-18
- **Eksperimen:** 05_rule_engine (P-008 consistency check)
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** MAJOR
- **Status:** UNRESOLVED
- **Deskripsi:** Audit konsistensi `bali.lp` terhadap `bali_rules.json` menunjukkan hanya 21/34 rule `COVERED`, 4/34 `PARTIAL`, dan 9/34 `GAP`.
- **Expected vs Actual:** Expected: seluruh rule expert-verified Bali terwakili penuh di ASP. Actual: rule proses distribusi, dampak perceraian, sengketa, dan beberapa perubahan kontemporer belum terencode.
- **Root Cause:** Encoding awal fokus pada hard constraints inti (pewaris/jenis harta/larangan transfer), belum menutup rule prosedural dan kontemporer.
- **Implikasi untuk Paper:** Klaim "expert-verified rules encoded in ASP" harus dikualifikasi untuk domain Bali sampai gap rule ditutup atau dinyatakan eksplisit sebagai batasan cakupan.
- **Tindakan:** ACKNOWLEDGED
- **Detail Tindakan:** Audit artefak disimpan di `docs/handoffs/20260218_p008_bali_asp_json_consistency.md` dan `experiments/05_rule_engine/consistency/bali_asp_json_consistency_2026-02-18.json`. Prioritas lanjut: tutup 4 rule `PARTIAL` dulu, lalu 9 rule `GAP`.

### F-016: ASP-JSON Rule Parity Gap on Minangkabau Domain (P-008 Audit)

- **Tanggal:** 2026-02-19
- **Eksperimen:** 05_rule_engine (P-008 consistency check)
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** MAJOR
- **Status:** UNRESOLVED
- **Deskripsi:** Audit konsistensi `minangkabau.lp` terhadap `minangkabau_rules.json` menunjukkan hanya 5/25 rule `COVERED`, 12/25 `PARTIAL`, dan 8/25 `GAP`.
- **Expected vs Actual:** Expected: seluruh rule expert-verified Minangkabau terwakili penuh di ASP. Actual: rule distribusi berbasis musyawarah/faraidh, resolusi sengketa adat, dualitas Sako-Pusako, dan prinsip suksesi fungsional belum terencode penuh.
- **Root Cause:** Encoding saat ini fokus pada hard constraints inti (garis matrilineal, klasifikasi pusako, larangan transfer tertentu), belum menutup rule prosedural, institusional, dan fungsi sosial-simbolik.
- **Implikasi untuk Paper:** Klaim "expert-verified rules encoded in ASP" untuk domain Minangkabau harus dikualifikasi sampai gap parity ditutup atau dinyatakan eksplisit sebagai batasan cakupan.
- **Tindakan:** ACKNOWLEDGED
- **Detail Tindakan:** Audit artefak disimpan di `docs/handoffs/20260219_p008_minangkabau_asp_json_consistency.md`. Prioritas lanjut: tutup rule distribusi/resolusi sengketa dulu, kemudian rule sosial-simbolik.

### F-017: ASP-JSON Rule Parity Gap on Jawa Domain (P-008 Audit)

- **Tanggal:** 2026-02-19
- **Eksperimen:** 05_rule_engine (P-008 consistency check)
- **Kategori:** LIMITATION_DISCOVERED
- **Severity:** MAJOR
- **Status:** UNRESOLVED
- **Deskripsi:** Audit konsistensi `jawa.lp` terhadap `jawa_rules.json` menunjukkan 15/36 rule `COVERED`, 14/36 `PARTIAL`, dan 7/36 `GAP`.
- **Expected vs Actual:** Expected: seluruh rule expert-verified Jawa terwakili penuh di ASP. Actual: rule poligami lintas perkawinan, resolusi sengketa berbasis desa, sebagian perubahan kontemporer, dan adat khusus (mis. Weling/Wekas, Bao Parmate) belum terencode penuh.
- **Root Cause:** Encoding sudah kuat di hard constraints pewarisan inti, tetapi rule prosedural komunitas, dinamika kontemporer, dan kebiasaan non-distributif belum diprioritaskan.
- **Implikasi untuk Paper:** Klaim kelengkapan encoding domain Jawa perlu dikualifikasi; parity gap ini harus dicatat sebagai batasan cakupan rule base saat ini.
- **Tindakan:** ACKNOWLEDGED
- **Detail Tindakan:** Audit artefak disimpan di `docs/handoffs/20260219_p008_jawa_asp_json_consistency.md`. Prioritas lanjut: tutup gap prosedural sengketa dan rule contemporary/custom terlebih dahulu.

### F-018: GAP Rules Regression (-7.1pp) — Rollback 24 Rules

- **Tanggal:** 2026-02-20
- **Eksperimen:** 09_ablation_study (P-008 rule coverage expansion)
- **Kategori:** NEGATIVE_RESULT
- **Severity:** MAJOR
- **Status:** RESOLVED (rollback)
- **Deskripsi:** Penambahan 24 GAP rules (dirancang via Prompt 15/Gemini) untuk mencapai 100% ASP coverage menyebabkan regresi akurasi. Sebelum penambahan: ASP+Ollama 70.0%. Setelah penambahan: turun ke 62.9% (-7.1pp). Setelah penghapusan `#show` directives yang tidak sengaja ter-remove: turun lebih jauh ke 55.7%. Rules di-rollback ke 71 rules original (commit rollback 2026-02-20).
- **Expected vs Actual:** Expected: penambahan 24 rules menutup coverage gap dan meningkatkan atau mempertahankan akurasi. Actual: akurasi turun 7.1pp (Ollama) akibat rules baru meng-override prediksi rules lama yang sudah benar.
- **Root Cause:** Rules baru terlalu umum (overspecification) — mendefinisikan kondisi yang seharusnya tidak meng-override hard constraints yang sudah tepat. ASP grounding memprioritaskan facts yang lebih baru/umum, sehingga rules spesifik yang sudah benar tumpang tindih dengan rules baru yang salah.
- **Implikasi untuk Paper:** Tabel di paper mencantumkan 95 expert-verified rules tetapi hanya 71 yang di-encode aktif. Kalimat eksplisit diperlukan: "The remaining 24 rules caused accuracy regression when added and were rolled back; they are documented as limitations of the current encoding." Coverage 100% bukan target yang benar — precision > coverage untuk ASP rule base.
- **Tindakan:** RESOLVED
- **Detail Tindakan:** Rollback ke 71 rules original. Canonical benchmark final menggunakan 71 rules ini: ASP-only 58.6% (41/70), ASP+Ollama 64.3% (45/70), ASP+DeepSeek 68.6% (48/70). Lesson learned: setiap penambahan rules harus divalidasi dengan benchmark run sebelum di-commit.

### F-019: Qwen3-14B LLM Layer Hurts Performance (-5.71pp vs ASP-only)

- **Tanggal:** 2026-02-23
- **Eksperimen:** 09_ablation_study (Qwen3-14B local benchmark, RTX 4080)
- **Kategori:** NEGATIVE_RESULT
- **Severity:** MAJOR
- **Status:** ACKNOWLEDGED
- **Deskripsi:** Menjalankan benchmark lengkap (n=70) dengan backend Qwen3-14B via Ollama menghasilkan penurunan akurasi dibanding ASP-only. ASP-only: 42/70=60.00% (Wilson CI [0.483, 0.707]). ASP+Qwen3-14B: 38/70=54.29% (Wilson CI [0.427, 0.654]). Net: -5.71pp. McNemar p=0.480 (non-significant). Ini berbeda dari DeepSeek (68.57%, +10pp vs ASP-only) dan Ollama/deepseek-r1 (64.29%, +5.71pp).
- **Expected vs Actual:** Expected: Qwen3-14B sebagai model lokal baru setidaknya setara atau lebih baik dari ASP-only. Actual: LLM layer justru menurunkan akurasi — 11 kasus degraded vs hanya 7 kasus improved.
- **Root Cause:** Dua pola kegagalan teridentifikasi:
  1. **B→A bias (7 kasus):** Qwen3 salah menginterpretasikan kehadiran output hukum nasional dalam sinyal ASP sebagai indikasi "hukum nasional dominan" (label A), padahal kasus seharusnya B (hukum adat berlaku). Qwen3 conflates "national law is mentioned" dengan "national law governs." Pattern ini tidak terlihat pada DeepSeek di skala ini.
  2. **C→B Layer 2 override (7 kasus):** Qwen3 mengabaikan sinyal konflik ASP (`konflik_terdeteksi: Ya`, asp_pred=C) dan tetap memilih B dengan reasoning "sengketa internal adat tanpa konflik nasional-adat." Ini adalah prompt-level failure — model tidak mengikuti sinyal simbolik yang sudah benar. DeepSeek memiliki 5 kasus serupa; Qwen3 memiliki 7.
  3. Sisanya: 9 C→B error adalah Layer 1 (ASP juga gagal mendeteksi konflik) — sama dengan pattern pada sistem lain.
- **Implikasi untuk Paper:** Qwen3-14B tidak dapat dimasukkan sebagai konfigurasi yang mengungguli baseline. Ini adalah negative result penting: tidak semua LLM backend memberikan improvement; pemilihan LLM backend berpengaruh signifikan pada hasil. Jika Qwen3 dilaporkan, framing harus: "local model Qwen3-14B produced a negative gain, suggesting the neuro-symbolic benefit depends on LLM calibration quality."
- **Tindakan:** ACKNOWLEDGED
- **Detail Tindakan:** Hasil disimpan di `experiments/09_ablation_study/results_dual_asp_llm_2026-02-23.json` (LLM) dan `results_dual_asp_only_2026-02-23.json` (ASP). Paper saat ini tidak memasukkan Qwen3-14B sebagai konfigurasi utama. F-019 dicatat untuk Limitations section. Jika waktu tersedia, investigasi prompt-level fix untuk B→A bias Qwen3 (instruksi eksplisit: "kehadiran output nasional dalam ASP bukan bukti nasional dominan").

---

## Statistik Ringkasan

| Kategori | Count | Critical | Major | Minor |
|----------|-------|----------|-------|-------|
| NEGATIVE_RESULT | 4 | 0 | 4 | 0 |
| ABANDONED_APPROACH | 0 | 0 | 0 | 0 |
| TECHNICAL_FAILURE | 2 | 0 | 1 | 1 |
| ASSUMPTION_VIOLATED | 1 | 1 | 0 | 0 |
| LIMITATION_DISCOVERED | 12 | 3 | 9 | 0 |
| **TOTAL** | **19** | **4** | **14** | **1** |

*Last updated: 2026-02-23 (F-019: Qwen3-14B negative result)*
