# ART-019 Library Comparison: PySwip vs Owlready2 vs Clingo

## Scope
Tujuan: memilih framework symbolic reasoning untuk Experiment 05 (rule engine). Kriteria utama: install reliability, expressiveness untuk aturan hukum, dan community support + Python integration.

## Evaluation Criteria
- Install reliability: seberapa stabil pemasangan di Windows/Python env.
- Expressiveness: dukungan aturan, exception, constraint, forward/backward chaining.
- Python integration: kualitas API dan tooling.
- Community/ecosystem: keberlanjutan, dokumentasi, dan referensi ilmiah.

## Summary Matrix (Qualitative)

| Library | Paradigm | Install Reliability (Windows) | Expressiveness untuk aturan hukum | Python Integration | Community/Ecosystem | Catatan singkat |
|---|---|---|---|---|---|---|
| PySwip (SWI-Prolog) | Logic programming (Prolog) | Medium (butuh SWI-Prolog terpasang, arsitektur harus match) | High untuk aturan + backward chaining | Good (Python bridge ke SWI-Prolog) | Strong (SWI-Prolog mature) | Cocok untuk rule-based reasoning klasik |
| Owlready2 | OWL/DL reasoning | Medium (reasoner Java diperlukan) | Medium untuk ontologi/kelas, lemah untuk exception prosedural | Good (Python API ontologi) | Academic, niche | Bagus untuk ontologi, bukan rule engine prosedural |
| Clingo | ASP (Answer Set Programming) | High (pip/conda packages tersedia) | High untuk constraint & non-monotonic rules | Strong (Python API) | Strong (Potassco) | Bagus untuk default rules & exception, kurang natural untuk backward chaining interaktif |

## Detailed Notes

### PySwip (SWI-Prolog)
- Requirements: SWI-Prolog harus terpasang; arsitektur Python dan SWI-Prolog harus sama (64-bit vs 64-bit). PySwip sendiri dipasang via pip dan menggunakan libswipl. On Windows, perlu install SWI-Prolog terlebih dahulu. PySwip PyPI menegaskan tidak ada Windows installer untuk PySwip, jadi jangan tertipu installer pihak ketiga.
- Expressiveness: sangat baik untuk aturan IF-THEN, inheritance rules, dan query backward chaining (kebutuhan utama untuk legal reasoning). Cocok untuk rules yang mudah ditulis sebagai Prolog facts + rules.
- Risiko: setup Windows bisa rapuh jika path SWI-Prolog tidak terdeteksi.

### Owlready2
- Reasoning memakai HermiT/Pellet (Java), jadi Java runtime diperlukan. Bagus untuk reasoning kelas/relasi di ontologi (DL reasoning), tetapi kurang fleksibel untuk exception/aturan prosedural yang sering ada pada hukum adat.
- Kuat untuk konsistensi ontologi dan klasifikasi, bukan rule engine dengan query chaining yang eksplisit.

### Clingo (ASP)
- Install: tersedia via pip dan conda; Potassco menyediakan dokumentasi dan Python API resmi.
- Expressiveness: sangat kuat untuk constraint, default rules, dan non-monotonic reasoning (bagus untuk konflik dan pengecualian). Cocok untuk formal rules + conflict detection.
- Tradeoff: alur reasoning berbasis stable models, bukan backward chaining interaktif ala Prolog. Untuk query-step reasoning mungkin perlu wrapper tambahan.

## Recommendation
**Primary recommendation: PySwip (SWI-Prolog).**
Alasan (minimum 3 kriteria):
- Install reliability: SWI-Prolog punya installer resmi; PySwip cukup pip install setelah SWI-Prolog terpasang. Risiko ada, tapi manageable dengan dokumentasi setup.
- Expressiveness: paling natural untuk aturan hukum berbasis IF-THEN dan query backward chaining (kebutuhan eksplisit di ART-021).
- Community support: SWI-Prolog mature dan widely used untuk logic programming.

**Fallback option: Clingo** jika butuh non-monotonic reasoning yang eksplisit untuk exception/conflict, atau jika setup PySwip bermasalah di Windows.

**Not recommended for Exp 05:** Owlready2 (lebih cocok untuk ontologi/klasifikasi dibanding rule engine prosedural).

## References (Key Sources)
- PySwip requirements & install: pyswip.org get-started
- PySwip Windows installer warning: PyPI pyswip project page
- Owlready2 reasoning and Java requirement: Owlready2 docs (reasoning)
- Clingo Python API and packages: Potassco clingo docs + download page
