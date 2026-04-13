# AGENT MATA ELANG — Strategic Review (2026-03-04)

**Reviewer:** Claude Opus 4.6
**Tipe:** Weekly top-level strategic review (#3)
**Cakupan:** Seluruh proyek Nusantara-Agent per commit `7e55139`
**Kontinuitas:** Melanjutkan review 2026-02-20 dan 2026-02-23

---

## 0. Verdict Satu Kalimat

Proyek ini sudah melewati fase kritis *governance disorder* dan berhasil membangun fondasi metodologis yang defensible untuk pilot study — tetapi sekarang menghadapi **binary fork**: dalam 11 hari (deadline 2026-03-15), tanpa data Ahli-2, paper harus di-reframe sebagai *methodology paper* bukan *empirical contribution*, dan ~40% infrastruktur proyek (dead code, abandoned experiments, bloated dependencies) harus dibersihkan sebelum menjadi technical debt permanen.

---

## 1. STATUS ITEM DARI REVIEW SEBELUMNYA

| Review | Item | Status Sekarang | Catatan |
|--------|------|-----------------|---------|
| Feb 20 | B1: Statistical power crisis | UNCHANGED | n=70, power ~0.3. Belum ada data baru. |
| Feb 20 | B2: Cross-backend confound | RESOLVED | Canonical freeze 2026-02-20 menstandarkan semua run. Paper v0.7 konsisten. |
| Feb 20 | B3: Agreement jump 58→94% | RESOLVED | `rubric_refinement_log.md` FINAL. Narasi ready-pakai tersedia. |
| Feb 20 | B4: No dev/test split | RESOLVED | `dev_test_split_policy.md` + `dataset_split.json` + `src/utils/dataset_split.py`. |
| Feb 20 | B5: Failure registry outdated | RESOLVED | F-018, F-019 ditambahkan. 19 entries. |
| Feb 23 | Qwen3 mislabeled file | UNKNOWN | Tidak terverifikasi apakah sudah di-rename/hapus. |
| Feb 23 | Paper [PENDING] markers | RESOLVED | Claim gate PASSED, 0 pending markers. |
| Feb 23 | Discussion section | NOT STARTED | Masih tersebar di §7/§8. Ini masalah besar. |

**Skor penyelesaian:** 5/8 resolved, 1 unknown, 2 unresolved. Ini *acceptable* untuk 10 hari kerja, tapi 2 item unresolved yang tersisa adalah high-impact.

---

## 2. TEMUAN KRITIS BARU

### 2.1 DEADLINE FORK: 11 Hari Menuju Keputusan Biner

**Situasi:** FUTURE TEST set bergantung pada Ahli-2 batch baru. Tidak ada sinyal progress dari Ahli-2 sejak policy ditetapkan 2026-02-23.

**Fork:**

| Skenario | Kondisi | Konsekuensi Paper |
|----------|---------|-------------------|
| A: Data datang | Ahli-2 ≥30 kasus sebelum 2026-03-15 | Paper = *empirical pilot + methodology*. Bisa klaim generalisasi terbatas. Venue: ESWA/KBS short paper. |
| B: Data tidak datang | Ahli-2 batch tidak tersedia | Paper = *methodology paper only*. Semua accuracy adalah DEV-set, non-generalizable. Venue: workshop/JURIX/legal-AI conference. |

**Rekomendasi:** Owner harus **proaktif menghubungi Ahli-2 minggu ini** dan menetapkan hard deadline 2026-03-10 untuk konfirmasi ketersediaan. Jika tidak ada konfirmasi, pivot ke Skenario B pada 2026-03-11.

**Severity:** CRITICAL — ini menentukan seluruh framing paper dan target venue.

### 2.2 PAPER TANPA DISCUSSION SECTION = REJECT OTOMATIS

Paper v0.7 tidak memiliki `\section{Discussion}` yang berdiri sendiri. Semua insight tersebar di §7 (Results) dan §8 (Limitations). Untuk jurnal Q1, ini adalah **structural deficiency** yang akan menyebabkan desk-reject atau major revision request.

Discussion section harus menghubungkan:
1. **Error analysis threads** → C→B router failure → B→A open-source bias → D-label blindspot
2. **Rule over-specification paradox** (F-018: +24 rules = -7.1pp)
3. **Statistical power narrative** → pilot framing → what n is needed → roadmap
4. **Cross-backend sensitivity** → not all LLMs help → calibration quality matters
5. **Methodological contribution** → rubric refinement process → kappa improvement arc

Tanpa section ini, paper kehilangan *interpretive layer* yang membedakan pilot study dari sekadar results dump.

**Severity:** HIGH — harus diselesaikan sebelum submission ke venue manapun.

### 2.3 KLAIM "70.0% AT TEMPERATURE=1.0" TIDAK TRACEABLE

Di §7.1 paper, ada klaim angka 70.0% yang tidak ada di file JSON manapun di repository. Ini melanggar prinsip inti proyek: *every claim must be traceable to reproducible data*.

**Rekomendasi:** Hapus atau ganti dengan angka yang traceable. Jika ini dari F-018 pre-rollback run, tandai eksplisit sebagai "pre-rollback, non-canonical."

**Severity:** MEDIUM — satu angka, tapi prinsipnya fundamental.

### 2.4 DEAD CODE ACCUMULATION: 868 BARIS + 242 FILE

| Item | Lokasi | Baris/Files | Status |
|------|--------|-------------|--------|
| `debate.py` | `src/agents/` | 293 lines | Dead — F-009 negative result |
| `self_correction.py` | `src/agents/` | 142 lines | Dead — no imports found |
| `adversarial_reviewer.py` | `src/review/` | 348 lines | Dead — no imports found |
| `llm_judge.py` | `src/evaluation/` | 85 lines | Dead — replaced by human eval |
| Exp 07 directory | `experiments/07_advanced_orchestration/` | 242 files | Abandoned — F-009 |

Total: **868 lines dead code** in src/ + **242 files** in abandoned experiment.

Ini bukan masalah fungsional (tests pass), tapi masalah **cognitive overhead** dan **reviewer perception**. Jika reviewer membuka repo:
- "Kenapa ada debate.py tapi paper tidak membahas debate?"
- "Kenapa ada 242 file di Exp 07 tapi tidak di-reference?"

**Rekomendasi:**
1. Pindahkan 4 file dead code ke `src/_archived/` (bukan hapus — preserve history)
2. Pindahkan `experiments/07_advanced_orchestration/` ke `experiments/_archived/07_advanced_orchestration/`
3. Update `__init__.py` files yang meng-import dead modules

**Severity:** LOW (fungsional) / MEDIUM (perceptual untuk reviewer)

### 2.5 JAWA DOMAIN: 35.3% ASP-ONLY = STRUCTURAL FAILURE

Per-domain breakdown (DeepSeek):

| Domain | N | ASP-only | +DeepSeek | Delta |
|--------|---|----------|-----------|-------|
| Minangkabau | 21 | 71.4% | 71.4% | 0pp |
| Bali | 21 | 71.4% | 76.2% | +4.8pp |
| **Jawa** | **17** | **35.3%** | **52.9%** | **+17.6pp** |
| Nasional | 7 | 42.9% | 71.4% | +28.5pp |

Jawa ASP-only di 35.3% artinya **rules engine performs worse than random guessing** untuk domain ini (random baseline untuk 4 labels = 25%, tapi dengan class imbalance sebenarnya ~44%).

F-017 mendokumentasikan: 15/36 COVERED, 14 PARTIAL, 7 GAP. Artinya hanya 42% rule Jawa yang fully encoded.

**Paradoks:** LLM delta terbesar justru di Jawa (+17.6pp), yang artinya LLM layer sedang *compensating* untuk rule engine yang broken, bukan *augmenting* symbolic reasoning yang sudah kuat. Ini **melemahkan narasi inti paper** bahwa ASP rules adalah fondasi yang di-augment oleh LLM.

**Rekomendasi:**
- Paper harus **secara eksplisit** membahas per-domain variance dan Jawa weakness
- Framing: "The neuro-symbolic benefit is strongest where symbolic rules are weakest (Jawa +17.6pp), suggesting LLM compensation rather than augmentation — an important finding for future system design"
- Jangan coba *fix* Jawa rules sekarang (F-018 lesson: blind rule addition hurts)

**Severity:** HIGH — ini mempengaruhi narasi inti paper.

---

## 3. ARSITEKTUR KOLABORASI HUMAN-AI

### 3.1 Penilaian Positif

1. **Claim gate otomatis** (`scripts/claim_gate.py`): Ini adalah *contract test* yang benar-benar bekerja. Setiap angka di paper diverifikasi terhadap canonical data. Ini best practice.
2. **Handoff document chain**: 5+ handoff docs memberikan audit trail yang kuat. Setiap sesi memiliki snapshot state yang reproducible.
3. **Failure registry**: 19 entries, well-structured, jujur. Ini aset metodologis.
4. **Dev/test split policy**: Formal, documented, dengan seed=42 untuk reproducibility.
5. **Benchmark manifest governance**: JSON-based provenance tracking berhasil mencegah angka mismatch.

### 3.2 Kelemahan Struktural

1. **Single human bottleneck**: Seluruh keputusan kritis (rubric, scope, venue) bergantung pada satu owner. Jika owner tidak responsif 1 minggu, proyek stall total.

2. **No session continuity contract**: Setiap handoff memuat "perintah untuk sesi berikutnya," tapi tidak ada **machine-readable contract** yang memverifikasi sesi baru dimulai dari state yang benar. Handoff saat ini adalah prose yang harus dibaca manual.

   **Saran:** Buat `docs/handoffs/session_contract.json`:
   ```json
   {
     "last_session": "2026-03-04",
     "commit_at_close": "7e55139",
     "tests_passing": 132,
     "claim_gate": "PASSED",
     "paper_version": "v0.7",
     "unresolved_blockers": ["ahli2_data", "discussion_section", "70pct_claim"]
   }
   ```
   Sesi berikutnya memvalidasi commit hash dan test count sebelum mulai.

3. **Agent capability mismatch tidak di-track**: Proyek menggunakan multiple AI agents (Opus, Sonnet, Gemini, Kimi) tapi tidak ada registry yang mencatat *which agent did what*. Jika Gemini menulis intro dan Opus menulis methodology, dan ada inkonsistensi gaya, tidak ada way to trace.

   **Saran:** Tambahkan header di setiap handoff: `executor_model: claude-opus-4-6` (sudah ada di beberapa handoff, standardize).

4. **Human-human interaction tidak diaudit secara real-time**: Ahli-1 dan Ahli-2 labeling dilakukan offline tanpa automated quality check. Kappa hanya dihitung post-hoc. Jika Ahli-2 mislabel 30% batch baru, ini baru terdeteksi setelah batch selesai.

   **Saran:** Tambahkan 5 "sentinel cases" (kasus dengan gold label pasti) di setiap batch baru untuk Ahli-2. Jika sentinel accuracy < 80%, batch ditolak.

### 3.3 Testing Framework Assessment

| Interaction | Current Coverage | Gap |
|-------------|-----------------|-----|
| Agent→Paper | Claim gate (strong) | Claim gate tidak cek narrative coherence, hanya angka |
| Agent→Agent | Handoff docs (weak) | Tidak machine-verifiable |
| Human→Agent | Prompt (unversioned) | Prompt drift antar-sesi tidak terdeteksi |
| Human→Human | Kappa post-hoc (adequate) | Tidak real-time; sentinel cases missing |
| Agent→Code | 132 unit tests (strong) | No integration test for full pipeline end-to-end |
| Paper→Data | Claim gate + canonical JSON (strong) | "70.0% temp=1.0" escaped — gate perlu diperkuat |

**Prioritas testing:**
1. **Machine-readable session contract** (LOW effort, HIGH safety)
2. **Sentinel cases untuk Ahli-2** (LOW effort, HIGH quality assurance)
3. **Extend claim gate** untuk detect angka tanpa JSON source (MEDIUM effort, HIGH integrity)

---

## 4. CRITICISM TRIAGE TABLE

| # | Kritik | Severity | Effort | Verdict | Alasan |
|---|--------|----------|--------|---------|--------|
| 1 | Deadline fork tanpa keputusan aktif | CRITICAL | LOW | **ACT NOW** | 11 hari tersisa; tanpa keputusan, proyek drift |
| 2 | Paper tanpa Discussion section | HIGH | MEDIUM | **FIX THIS WEEK** | Structural deficiency untuk venue manapun |
| 3 | Jawa 35.3% melemahkan narasi inti | HIGH | LOW | **REFRAME IN PAPER** | Jangan fix rules, reframe sebagai finding |
| 4 | "70.0% temp=1.0" untraceable claim | MEDIUM | LOW | **FIX NOW** | 5-menit edit, tapi prinsipnya penting |
| 5 | 868 lines dead code | MEDIUM | LOW | **CLEAN THIS WEEK** | 30 menit kerja, significant perception improvement |
| 6 | 242 files di Exp 07 | LOW | LOW | **ARCHIVE** | Move to `_archived/`, bukan delete |
| 7 | No E2E integration test | MEDIUM | HIGH | **DEFER** | Bukan blocker untuk paper submission |
| 8 | Single-owner bottleneck | MEDIUM | N/A | **ACKNOWLEDGE IN PAPER** | Tidak bisa di-fix, tapi bisa di-mitigate dengan contingency plan |
| 9 | Dependency bloat (57 lines requirements.txt) | LOW | MEDIUM | **DEFER** | Kosmetik, bukan blocker |
| 10 | Prompt versioning tidak ada | MEDIUM | HIGH | **DEFER** | Penting tapi bukan blocker untuk paper v1 |

### Kritik yang DIABAIKAN (dengan alasan):

| Kritik | Alasan Diabaikan |
|--------|-----------------|
| "Perlu 344 kasus untuk power=0.8" | Benar tapi unrealistic dalam timeframe. Reframe, jangan kejar. |
| "D-label recall 0%" | Hanya 2 kasus D. Statistik tidak meaningful. Acknowledge sebagai limitation. |
| "Perlu 3+ raters" | Sudah diputuskan: 2 qualified raters > 3 mixed-quality raters (F-014 lesson). |
| "Perlu Neo4j/Qdrant" | Out of scope. Already dropped. Jangan resurrect. |
| "ASP rules perlu 100% coverage" | F-018 proves this is harmful. 71 rules > 95 rules. |

---

## 5. REKOMENDASI TERSTRUKTUR

### 5.1 STOP (Hentikan Segera)

1. **Stop menambah backend LLM baru.** 3 konfigurasi + 2 exploratory sudah cukup. Setiap backend baru menambah complexity tanpa menyelesaikan power crisis.
2. **Stop menambah ASP rules.** F-018 membuktikan ini bisa harmful. 71 rules sudah stable.
3. **Stop polishing angka di paper.** v0.7 sudah canonical-consistent (claim gate PASSED). Polishing marginal tidak menambah value.
4. **Stop membuat dokumen baru kecuali Discussion section dan final handoff.** Proyek sudah memiliki 30+ docs. Setiap doc baru menambah maintenance burden.

### 5.2 CONTINUE (Pertahankan)

1. **Continue claim gate sebagai pre-commit hook.** Ini satu-satunya automated quality gate yang terbukti efektif.
2. **Continue failure registry discipline.** 19 entries adalah aset. Tambahkan entry baru hanya jika ada temuan baru.
3. **Continue handoff chain.** Tapi tambahkan machine-readable contract.
4. **Continue 132 test suite.** Jangan reduce, tapi juga jangan chase coverage metric.

### 5.3 START (Mulai Minggu Ini)

1. **Hubungi Ahli-2 hari ini.** Konfirmasi ketersediaan data. Hard deadline 2026-03-10.
2. **Tulis Discussion section.** 2-3 halaman. Hubungkan semua threads. Ini highest-impact writing task.
3. **Resolve "70.0% temp=1.0" claim.** Verify atau hapus. 5 menit.
4. **Archive dead code.** Move 4 files to `src/_archived/`, Exp 07 to `experiments/_archived/`. 30 menit.
5. **Buat session contract JSON.** Template di section 3.2. 15 menit.

### 5.4 PIVOT (Jika Skenario B: Data Tidak Datang)

Jika Ahli-2 data tidak tersedia per 2026-03-15:
1. Reframe paper title: "A Methodology for Neuro-Symbolic Legal Reasoning..." bukan "Neuro-Symbolic Legal Reasoning Improves..."
2. Drop semua accuracy claims dari abstract. Ganti dengan methodology contribution claims.
3. Target venue: JURIX 2026, ICAIL 2026, atau workshop collocated dengan EMNLP/ACL.
4. LOCKED TEST set tetap tidak disentuh — simpan untuk paper v2 nanti.

---

## 6. TIMELINE OPERASIONAL

| Hari | Target | Owner |
|------|--------|-------|
| Mar 4-5 | Archive dead code + resolve 70.0% claim + session contract | AI agent |
| Mar 5-7 | Discussion section draft (2-3 pages) | AI agent + owner review |
| Mar 7-10 | Ahli-2 konfirmasi deadline | Owner (human) |
| Mar 10-11 | Fork decision: Skenario A atau B | Owner |
| Mar 11-14 | Paper reframe (jika B) atau data integration (jika A) | AI agent |
| Mar 15 | Paper complete draft siap internal review | — |

---

## 7. SATU PERTANYAAN UNTUK OWNER

**Apakah Anda sudah menghubungi Ahli-2 sejak 23 Februari, dan jika ya, apa status ketersediaan batch baru?**

Jawaban ini menentukan seluruh arah proyek 2 minggu ke depan. Tanpa jawaban, saya merekomendasikan default ke **Skenario B (methodology paper)** mulai 2026-03-11.

---

## 8. META-REFLECTION: KUALITAS PROSES REVIEW INI

### Apa yang membaik sejak review pertama (Feb 20):
- Canonical data freeze menghilangkan confound cross-backend
- Rubric refinement terdokumentasi FINAL
- Dev/test split terformal
- Failure registry up-to-date
- Claim gate berfungsi sebagai automated quality control

### Apa yang tetap sama (belum terselesaikan):
- Statistical power crisis (fundamental, hanya bisa diselesaikan dengan data)
- Single-owner bottleneck
- Dead code accumulation
- Missing Discussion section

### Apa yang memburuk:
- **Time pressure meningkat** — 11 hari ke deadline fork, tanpa data baru
- **Scope creep risk** — setiap sesi menambah docs tapi belum menambah data
- **Diminishing returns** — paper sudah di-polish 3x tanpa data baru; further polish tanpa Discussion section tidak produktif

---

*Review berikutnya dijadwalkan: 2026-03-11 (post fork-decision)*
*Atau lebih awal jika Ahli-2 data tiba*
