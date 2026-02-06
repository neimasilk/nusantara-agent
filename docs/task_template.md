# Atomic Research Task (ART) Template

Format standar untuk memecah pekerjaan riset menjadi unit-unit atomic yang bisa dikerjakan secara independen oleh manusia atau AI agent.

---

## Prinsip ART

1. **Self-contained:** Semua informasi yang dibutuhkan ada dalam task description
2. **Testable:** Ada acceptance test yang jelas (pass/fail)
3. **Time-boxed:** 1-4 jam. Jika lebih, pecah menjadi sub-tasks
4. **Documented:** Output selalu berupa artefak yang ter-commit (kode, data, dokumen)

---

## Format Task

```markdown
## ART-[NNN]: [Judul Task]

### Metadata
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT / CODE / DATA / ANALYSIS / DOCUMENTATION / REVIEW |
| **Executor** | HUMAN_ONLY / AI_ONLY / EITHER |
| **Skill Required** | [Misal: Python, Legal Knowledge, Statistics, NLP] |
| **Prerequisites** | [ART-IDs yang harus selesai dulu] |
| **Priority** | P0 (blocking) / P1 (critical path) / P2 (important) / P3 (nice-to-have) |
| **Phase** | [Phase project: 1-5] |
| **Status** | PENDING / IN_PROGRESS / DONE / BLOCKED / CANCELLED |
| **Assigned To** | [Nama / Unassigned] |

### Description
[Deskripsi detail tentang APA yang harus dilakukan, bukan BAGAIMANA. Cukup konteks agar executor bisa bekerja tanpa bertanya.]

### Inputs
- [File/data/artefak yang dibutuhkan, dengan path lengkap]

### Expected Outputs
- [File/data/artefak yang harus dihasilkan, dengan path lengkap]
- [Format output yang diharapkan]

### Acceptance Test
- [ ] [Kriteria pass/fail yang spesifik dan terukur]
- [ ] [Tidak ambigu — observer independen harus setuju apakah test pass]

### Failure Modes
- [Apa yang bisa salah dan bagaimana menanganinya]
- [Kapan harus escalate vs. kapan bisa di-handle sendiri]

### Notes
- [Context tambahan, referensi, tips]
```

---

## Kategori Type

| Type | Deskripsi | Typical Executor |
|------|-----------|-----------------|
| **EXPERIMENT** | Menjalankan eksperimen ilmiah dengan PROTOCOL.md | EITHER |
| **CODE** | Menulis/memodifikasi kode | EITHER |
| **DATA** | Mengumpulkan, membersihkan, atau menganotasi data | Varies |
| **ANALYSIS** | Menganalisis hasil, membuat visualisasi | EITHER |
| **DOCUMENTATION** | Menulis dokumentasi, paper sections | EITHER |
| **REVIEW** | Me-review eksperimen atau kode | HUMAN_ONLY (Layer 3) |

---

## Aturan Executor

| Label | Artinya |
|-------|---------|
| **HUMAN_ONLY** | Membutuhkan judgment manusia, domain expertise, atau keputusan etis. Contoh: anotasi hukum adat, final review gate, keputusan pivot |
| **AI_ONLY** | Repetitif, high-volume, atau membutuhkan consistency. Contoh: batch processing, code generation from spec, formatting |
| **EITHER** | Bisa dikerjakan oleh manusia atau AI, tergantung availability. Kebanyakan task masuk kategori ini |

---

## Dependency Management

Tasks memiliki dependency yang dinyatakan dalam field `Prerequisites`. Aturan:

1. Task dengan Prerequisites kosong bisa dikerjakan kapan saja
2. Task BLOCKED jika ada prerequisite yang belum DONE
3. Circular dependencies tidak diperbolehkan
4. Jika ada blocking dependency yang stuck, eskalasi ke lead researcher

---

## Status Flow

```
PENDING → IN_PROGRESS → DONE
    ↓         ↓
  BLOCKED   CANCELLED
    ↓
 (prerequisite selesai) → PENDING
```

---

## Contoh Task

```markdown
## ART-012: Implementasi Formal Rule Engine untuk Hukum Waris Minangkabau

### Metadata
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Skill Required** | Python, PySwip/owlready2, Hukum Adat Minangkabau |
| **Prerequisites** | ART-010, ART-011 |
| **Priority** | P1 |
| **Phase** | 2 |
| **Status** | PENDING |
| **Assigned To** | Unassigned |

### Description
Encode 20 aturan dasar hukum waris Minangkabau sebagai Prolog rules menggunakan PySwip. Rules harus mencakup: hak kemenakan atas pusako tinggi, hak anak atas pusako rendah, peran mamak kepala waris, kondisi darurat yang membolehkan pengecualian.

### Inputs
- `experiments/01_triple_extraction/result.json` — Tripel yang sudah diekstrak
- Referensi: Buku "Hukum Adat Minangkabau" (lihat bibliography)

### Expected Outputs
- `src/symbolic/minangkabau_rules.pl` — Prolog rules file
- `src/symbolic/rule_engine.py` — Python wrapper menggunakan PySwip
- `experiments/05_rule_engine/test_rules.py` — Test cases

### Acceptance Test
- [ ] Minimal 20 rules ter-encode
- [ ] Rules bisa menjawab 10 test queries dengan benar
- [ ] Hasil rule engine BERBEDA dari pure LLM pada minimal 3 edge cases
- [ ] Semua test pass (`python -m pytest experiments/05_rule_engine/`)

### Failure Modes
- PySwip installation gagal di Windows → fallback ke owlready2 (OWL ontology)
- Rules terlalu simplistic untuk edge cases → konsultasi domain expert (HUMAN_ONLY)

### Notes
- Ini adalah task kunci untuk menjustifikasi klaim "neuro-symbolic"
- Lihat methodology_fixes.md Weakness #1
```
