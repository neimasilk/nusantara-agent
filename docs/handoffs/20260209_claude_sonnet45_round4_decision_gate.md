# Decision Gate: Expert-4 Ingestion Strategy
**Agent:** Claude Sonnet 4.5 (Integrator)  
**Tanggal:** 2026-02-09  
**Status:** DECISION REQUIRED

---

## A. DECISION

### A.1 Canonical Source
**KEPUTUSAN:** Gunakan `paket_interview_online_ahli4_terisi.md` (12 kasus) sebagai sumber utama, **DENGAN CATATAN** bahwa 2 kasus SPLIT formal (CS-MIN-005, CS-MIN-015) **BELUM terarbitrase** oleh Ahli-4 dan harus tetap berstatus SPLIT.

### A.2 Data Policy
**KEPUTUSAN:** **PARTIAL INGEST** — Hanya ingest 12 kasus yang tersedia di terisi.md dengan status berikut:

| Status | Kasus | Tindakan |
|--------|-------|----------|
| ✅ INGEST | 12 kasus dalam terisi.md | Tambah vote ahli4 ke gs_active_cases.json |
| ⚠️ HOLD | CS-MIN-005, CS-MIN-015 | Tetap status SPLIT; belum terarbitrase |
| ⚠️ HOLD | CS-LIN-018, CS-NAS-041 | Tidak ada vote ahli4; status consensus tidak berubah |

---

## B. RATIONALE

### B.1 Analisis Perbandingan Sumber

| Aspek | Round3 Template (7 kasus) | Terisi (12 kasus) |
|-------|---------------------------|-------------------|
| Fokus | Prioritas SPLIT + high-conflict | 12 kasus interview Ahli-1/2/3 |
| SPLIT Cases | ✅ CS-MIN-005, CS-MIN-015 | ❌ TIDAK ADA |
| Overlap | 3 kasus | 3 kasus |
| Ahli | Tidak terisi | Dr. Eko Susilo, M.Hum |

### B.2 Inventaris Gap

**Kasus dalam Round3 tapi TIDAK dalam Terisi:**
- ❌ **CS-MIN-005** — SPLIT formal, belum terarbitrase
- ❌ **CS-MIN-015** — SPLIT formal, belum terarbitrase
- ❌ CS-LIN-018 — Partial (C-C-A), tidak prioritas
- ❌ CS-NAS-041 — Partial (A-C-C), tidak prioritas

**Implikasi:** 2 kasus SPLIT tetap tidak resolved → gold_label tetap "SPLIT"

### B.3 Justifikasi PARTIAL INGEST

1. **Data Ahli-4 valid:** Dr. Eko Susilo memberikan 12 votes dengan rationale dan referensi lengkap.
2. **Coverage tinggi:** 12 kasus mencakup seluruh kasus yang sebelumnya dievaluasi oleh Ahli-1/2/3.
3. **SPLIT cases tidak terarbitrase:** Namun 2 kasus formal SPLIT tidak mendapat vote → tidak bisa diklaim resolved.
4. **No overwrite risk:** Ingest bersifat additive (menambah field ahli4), bukan replace.

---

## C. EXACT COMMANDS

### C.1 Pre-Ingest: Transkrip Terisi ke CSV

```powershell
# Step 1: Buat CSV dari terisi.md
# File output: data/processed/gold_standard/interview_online/interview_template_ahli4_terisi.csv
```

**Content CSV (buat manual atau script):**
```csv
id,label_ahli4,confidence_ahli4,rationale_ahli4,reference_1,reference_2,session_date,interviewer_name,follow_up_needed,mode
CS-MIN-011,B,Tinggi,"Tanah ulayat merupakan harta kolektif kaum yang tidak dapat dialihkan secara individual tanpa musyawarah dan persetujuan KAN.",UUPA 1960 Pasal 3,Doktrin hak ulayat Minangkabau,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-MIN-004,C,Sedang,"Harta pencaharian menurut hukum nasional merupakan harta bersama yang diwariskan kepada anak. Dalam adat Minangkabau dikenal pembedaan antara harta pusaka dan pencaharian.",UU Perkawinan No. 1/1974 Pasal 35,Doktrin adat Minangkabau tentang harta pencaharian,2026-02-09,Tim Nusantara-Agent,Ya,online_interview
CS-JAW-006,A,Tinggi,"Harta yang diperoleh selama perkawinan kedua merupakan harta bersama menurut hukum nasional.",UU Perkawinan No. 1/1974,Yurisprudensi MA tentang harta bersama,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-LIN-052,C,Sedang,"Tanah ulayat diakui secara adat namun belum memenuhi syarat formal perbankan. Diperlukan mekanisme sintesis.",UUPA 1960,Praktik pengakuan tanah ulayat dalam perbankan,2026-02-09,Tim Nusantara-Agent,Ya,online_interview
CS-NAS-066,A,Tinggi,"Sanksi adat tidak boleh melanggar hak dasar anak atas pendidikan dan kesehatan.",UUD 1945 Pasal 28B dan 28H,UU Perlindungan Anak,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-BAL-002,C,Sedang,"Adat Bali patrilineal mengalami perkembangan melalui Keputusan MDP 2010. Diperlukan sintesis antara adat dan prinsip kesetaraan.",Keputusan MDP Bali 2010,Prinsip kesetaraan dalam hukum nasional,2026-02-09,Tim Nusantara-Agent,Ya,online_interview
CS-NAS-010,A,Tinggi,"Batas usia perkawinan ditentukan secara tegas oleh UU Perkawinan. Praktik adat tidak dapat mengesampingkan ketentuan tersebut.",UU No. 16 Tahun 2019,Putusan MK terkait usia perkawinan,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-LIN-017,A,Tinggi,"Administrasi kependudukan dan imigrasi mensyaratkan penetapan pengadilan untuk pengangkatan anak.",UU Administrasi Kependudukan,Peraturan Keimigrasian,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-MIN-013,D,Rendah,"Status ruko bergantung pada persetujuan kaum dan niat penggantian harta pusaka. Fakta mengenai kesepakatan adat belum jelas.",Doktrin adat Minangkabau tentang pusako tinggi,Praktik penggantian harta pusaka,2026-02-09,Tim Nusantara-Agent,Ya,online_interview
CS-BAL-014,C,Sedang,"Adat Bali mengatur posisi janda namun hukum nasional menjamin perlindungan tempat tinggal. Diperlukan sintesis.",Hukum adat Bali tentang janda,Prinsip perlindungan hak dalam hukum nasional,2026-02-09,Tim Nusantara-Agent,Ya,online_interview
CS-JAW-015,C,Sedang,"Pesan terakhir diakui dalam adat Jawa namun perlu pembuktian menurut hukum nasional.",Doktrin wekas dalam adat Jawa,KUH Perdata tentang hibah/wasiat,2026-02-09,Tim Nusantara-Agent,Ya,online_interview
CS-LIN-016,A,Tinggi,"Aset berada di wilayah urban dan tunduk pada hukum perdata nasional.",KUH Perdata,UU Perkawinan No. 1/1974,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
```

### C.2 Ingest Command

```powershell
# Step 2: Run ingest (safe mode first)
python scripts/ingest_expert_interview_votes.py `
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4_terisi.csv `
  --expert-id ahli4

# Step 3: Verify output file
# Output: data/processed/gold_standard/gs_active_cases.post_ahli4.json

# Step 4: If verified, overwrite in-place
python scripts/ingest_expert_interview_votes.py `
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4_terisi.csv `
  --expert-id ahli4 `
  --in-place
```

### C.3 Post-Ingest: Rebuild Manifest

```powershell
# Step 5: Rebuild manifest
python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-09

# Step 6: Validate manifest
python scripts/validate_benchmark_manifest.py
```

---

## D. ACCEPTANCE TESTS

### D.1 Pre-Ingest Checks
- [ ] File CSV `interview_template_ahli4_terisi.csv` ada dan valid (12 rows + header)
- [ ] Semua ID kasus dalam CSV ada di `gs_active_cases.json`
- [ ] Semua label valid (A/B/C/D)
- [ ] File encoding UTF-8

### D.2 Post-Ingest Checks
- [ ] File `gs_active_cases.post_ahli4.json` tercipta tanpa error
- [ ] 12 kasus memiliki `expert_votes.ahli4` populated
- [ ] 2 kasus SPLIT (CS-MIN-005, CS-MIN-015) **TIDAK** memiliki ahli4 vote
- [ ] Field `interview_notes.ahli4` berisi rationale, reference, confidence

### D.3 Consensus Recalculation Checks
- [ ] Kasus dengan 4-vote unanimous tetap UNANIMOUS
- [ ] Kasus dengan 3-1 split menjadi MAJORITY (3)
- [ ] Kasus dengan 2-2 split menjadi SPLIT atau PARTIAL
- [ ] CS-MIN-005 dan CS-MIN-015 tetap memiliki `consensus: "none"` atau `gold_label: "SPLIT"`

### D.4 Manifest Validation
- [ ] `python scripts/validate_benchmark_manifest.py` returns SUCCESS
- [ ] `total_cases_actual` updated (tetap 24 atau naik jika ada kasus baru)
- [ ] `label_distribution` diupdate sesuai konsensus baru

---

## E. CLAIM GUARDRAILS

### ❌ TIDAK BOLEH Diklaim Pasca-Ingest

1. **"Gold Standard 82 kasus selesai"** — Hanya 24 kasus aktif; 2 kasus SPLIT belum resolved.
2. **"100% kasus SPLIT terarbitrase"** — CS-MIN-005 dan CS-MIN-015 tidak mendapat vote Ahli-4.
3. **"Akurasi X% pada N=24"** — Belum dijalankan benchmark ulang pasca-ingest.
4. **"4-expert consensus untuk semua kasus"** — Hanya 12 kasus memiliki 4 votes.

### ⚠️ BOLEH Diklaim dengan Qualifier

1. "Ahli-4 (Dr. Eko Susilo) memberikan vote pada **12 kasus** dari 24 kasus aktif."
2. "Kasus **N=12** kini memiliki 4-expert votes; **N=12** lainnya tetap 3-expert."
3. "2 kasus SPLIT formal (CS-MIN-005, CS-MIN-015) **belum terarbitrase** dan tetap excluded dari evaluasi."
4. "Benchmark akan dijalankan ulang pasca-ingest untuk konfirmasi akurasi."

### ✅ BOLEH Diklaim Tanpa Qualifier

1. "Data vote Ahli-4 telah di-ingest untuk 12 kasus."
2. "Manifest dan dataset telah di-rebuild per 2026-02-09."

---

## F. SUMMARY

| Item | Value |
|------|-------|
| Canonical Source | `docs/paket_interview_online_ahli4_terisi.md` |
| Cases to Ingest | 12 |
| SPLIT Cases Resolved | **0** (belum terarbitrase) |
| Data Policy | PARTIAL INGEST |
| Blocker | 2 kasus SPLIT tidak tercakup dalam terisi.md |

---

## G. NEXT ACTIONS

1. **Operator:** Buat CSV `interview_template_ahli4_terisi.csv` dari data di atas.
2. **Operator:** Jalankan ingest command (safe mode → verify → in-place).
3. **Operator:** Rebuild manifest.
4. **Integrator:** Rekonsiliasi konsensus dan update gold_label.
5. **Quality Gate:** Jalankan benchmark ulang.

---

**Prepared by:** Claude Sonnet 4.5 (Decision Gate)  
**Review Status:** Pending User Approval  
**Execution Ready:** After user confirmation
