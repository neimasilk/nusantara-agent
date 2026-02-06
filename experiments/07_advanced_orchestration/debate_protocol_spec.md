# Debate Protocol Specification (Exp 07)

Dokumen ini mendefinisikan protokol debat multi-round antara **National Law Agent** dan **Adat Law Agent**. Tujuan utama: memaksa adversarial checking, mengurangi blind spots, dan menghasilkan argumen yang lebih robust sebelum supervisor melakukan sintesis.

## 1. Tujuan & Prinsip

- **Tujuan:** meningkatkan kualitas reasoning melalui kritik silang terstruktur.
- **Prinsip:** setiap klaim harus punya *evidence* (kutipan teks sumber / triple / aturan formal). Klaim tanpa evidence harus ditandai sebagai risk.
- **Anti-circular:** tidak ada self-approval; setiap agent wajib mengkritik output agent lain.

## 2. Roles

- **National Law Agent (NLA):** fokus KUHPerdata, asas nasional, yurisprudensi umum.
- **Adat Law Agent (ALA):** fokus norma adat (Minangkabau/Bali/Jawa) + aturan formal (rule engine).
- **Supervisor (SUP):** hanya aktif setelah debat selesai atau terjadi escalation.

## 3. Inputs & Outputs

### Inputs
- `query`: pertanyaan hukum
- `context`: hasil retrieval (vector + KG + rule engine jika tersedia)
- `domain_hint`: optional, hasil router (pure national / pure adat / conflict / consensus)

### Outputs per agent (per round)
Agent output harus berupa JSON dengan skema berikut:

```json
{
  "round": 1,
  "agent": "NLA" | "ALA",
  "answer": "Jawaban ringkas dan terstruktur",
  "claims": [
    {
      "id": "C1",
      "statement": "Klaim utama",
      "evidence": ["source_id_1", "source_id_2"],
      "confidence": 0.0,
      "assumptions": ["A1", "A2"]
    }
  ],
  "uncertainties": ["U1", "U2"],
  "open_questions": ["Q1", "Q2"]
}
```

### Critique format (per agent, per round)

```json
{
  "round": 1,
  "agent": "NLA" | "ALA",
  "target": "NLA" | "ALA",
  "critiques": [
    {
      "id": "K1",
      "target_claim_id": "C1",
      "issue_type": "evidence_gap" | "logic_gap" | "conflict" | "domain_mismatch" | "overclaim",
      "description": "Kritik spesifik",
      "severity": "CRITICAL" | "MAJOR" | "MINOR",
      "suggested_fix": "Perbaikan konkret"
    }
  ]
}
```

## 4. Round Structure

**Default: 2 rounds. Maks: 3 rounds** (untuk menghindari biaya berlebihan).

1. **Round 1 — Initial Answer**
   - NLA dan ALA menghasilkan jawaban + claims.
2. **Round 1 — Cross Critique**
   - NLA mengkritik ALA, ALA mengkritik NLA.
3. **Round 2 — Revision**
   - Setiap agent merevisi jawaban berdasarkan kritik yang diterima.
4. **Round 2 — Cross Critique (Optional)**
   - Jika konflik masih tinggi (lihat kriteria konvergensi), lakukan critique tambahan.
5. **Round 3 — Final Revision (Optional)**
   - Hanya jika konflik masih CRITICAL/MAJOR setelah Round 2.

## 5. Convergence Criteria

Debat dianggap selesai jika salah satu kondisi terpenuhi:

- **Tidak ada kritik CRITICAL**, dan jumlah kritik MAJOR <= 1.
- **Tidak ada konflik domain** yang unresolved (misal aturan adat bertentangan dengan klaim nasional tanpa justifikasi).
- **Stabilitas jawaban:** perubahan jawaban pada revision < 15% (ukuran token/semantic similarity), kecuali ada kritik CRITICAL.

Jika tidak tercapai setelah Round 3, lakukan **escalation ke Supervisor** dengan flag `needs_human_review: true`.

## 6. Escalation Rules

Escalate ke Supervisor jika:
- Ada **kritik CRITICAL** terkait validitas evidence atau konflik norma.
- Ada **kontradiksi keras** antara output NLA dan ALA yang tidak terselesaikan.
- Agent tidak mampu memberikan evidence untuk > 30% klaim.

## 7. Logging & Traceability

Setiap round wajib disimpan dengan naming:
- `debate_round1_nla.json`
- `debate_round1_ala.json`
- `critique_round1_nla_on_ala.json`
- `critique_round1_ala_on_nla.json`
- `debate_round2_nla.json`, dst.

Log final yang dikonsumsi supervisor:
- `debate_summary.json` berisi ringkasan konflik, daftar klaim disepakati, dan klaim dispute.

## 8. Failure Modes

- **Echo chamber:** agent hanya setuju tanpa kritik → mitigasi: enforce minimal 3 kritik per agent di Round 1.
- **Over-criticism:** kritik tanpa solusi → mitigasi: `suggested_fix` wajib.
- **Token blow-up:** terlalu panjang → mitigasi: limit 8-10 klaim utama per agent.

## 9. Implementation Notes (LangGraph)

- Jalankan NLA dan ALA dalam parallel node.
- Kritik dihasilkan setelah kedua output tersedia.
- Revision node menerima output + kritik.
- Supervisor hanya menerima final revision + debate summary.

## 10. Acceptance Test

- Spesifikasi cukup detail untuk diimplementasikan tanpa ambiguitas.
- Format input/output terdefinisi dan konsisten.
- Kriteria konvergensi dan escalation jelas dan operasional.
