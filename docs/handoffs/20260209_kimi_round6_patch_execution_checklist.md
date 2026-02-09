# Patch Execution Checklist — Round 6
**Date:** 2026-02-09  
**Operator:** [Nama Operator]  
**Status:** READY FOR EXECUTION

---

## Pre-Execution Checks

- [ ] Owner decision brief reviewed and approved
- [ ] Backup file exists: `gs_active_cases_pre_patch_2026-02-09.json`
- [ ] All source documents verified:
  - [ ] `paket_interview_ahli4_followup_terisi.md`
  - [ ] `interview_template_ahli4_followup.csv`

---

## Execution Steps

### Step 1: Create Follow-up CSV
```powershell
# Verify CSV exists or create it
Get-Content "data/processed/gold_standard/interview_online/interview_template_ahli4_followup.csv"
```

CSV Content (jika belum ada):
```csv
id,label_ahli4,confidence_ahli4,rationale_ahli4,reference_1,reference_2,session_date,interviewer_name,follow_up_needed,mode
CS-MIN-005,A,Tinggi,"Harta pusako rendah dapat dialihkan kepada anak kandung via akta notaris.",KUH Perdata Pasal 1666,Doktrin adat Minangkabau,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-MIN-015,A,Tinggi,"Perkawinan sah KUA dilindungi hukum nasional. Sanksi buang adat melanggar HAM.",UU Perkawinan No. 1/1974,UUD 1945 Pasal 28B,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-NAS-041,C,Sedang,"Izin tambang harus mempertimbangkan hak MHA. FPIC diperlukan.",Putusan MK 35/2012,Prinsip FPIC,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-LIN-018,C,Sedang,"SHM adalah bukti hak kuat. Pengakuan hutan adat perlu sintesis hukum.",UUPA 1960,Putusan MK 35/2012,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
```
**Status:** [ ] Done

---

### Step 2: Backup Dataset
```powershell
Copy-Item "data/processed/gold_standard/gs_active_cases.json" `
          "data/processed/gold_standard/gs_active_cases_pre_patch_2026-02-09.json"
```
**Status:** [ ] Done

---

### Step 3: Ingest Follow-up Votes (4 cases)
```powershell
python scripts/ingest_expert_interview_votes.py `
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4_followup.csv `
  --expert-id ahli4 `
  --in-place
```
**Expected Output:** 4 cases updated with ahli4 votes  
**Status:** [ ] Done

---

### Step 4: Patch Gold Labels (4 updates)

| ID | Old Gold | New Gold |
|----|----------|----------|
| CS-MIN-005 | SPLIT | A |
| CS-MIN-015 | SPLIT | A |
| CS-MIN-004 | B | C |
| CS-MIN-011 | C | B |

```powershell
# Manual edit or via script
python scripts/patch_gold_labels.py --dry-run
python scripts/patch_gold_labels.py --commit
```
**Status:** [ ] Done

---

### Step 5: Rebuild Manifest
```powershell
python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-09
```
**Status:** [ ] Done

---

### Step 6: Validate Manifest
```powershell
python scripts/validate_benchmark_manifest.py
```
**Expected:** SUCCESS with 24 evaluable cases, 0 SPLIT  
**Status:** [ ] Done

---

## Post-Execution Verification

- [ ] `gs_active_cases.json` has 24 cases with correct gold labels
- [ ] No SPLIT labels remaining
- [ ] CS-MIN-005 and CS-MIN-015 have ahli4 votes
- [ ] Manifest shows updated label distribution
- [ ] Backup file exists and is different from current

---

## Completion Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Operator | | | |
| Reviewer | | | |

---

**Next Step After Completion:** Run post-patch benchmark
```powershell
python scripts/run_benchmark.py --output results_post_patch_2026-02-09.json
```
