# REVIEW: Eksperimen 02 — Integrasi Graf & Penalaran Simbolik

**Reviewer:** Framework SOP (retrospektif)
**Tanggal:** 2026-02-06
**Status:** CONDITIONAL PASS — graph queryability terbukti, tapi bukan symbolic reasoning

---

## Jawaban 10 Pertanyaan Devil's Advocate

### Q1: Apakah hasilnya circular?

**Jawaban:** Sebagian. Input graf berasal dari Exp 01 (DeepSeek-generated), dan "keberhasilan" dinilai berdasarkan apakah query mengembalikan node yang terlihat benar menurut inspeksi peneliti. Tidak ada ground truth untuk graph queries. Namun, kode grafnya sendiri (NetworkX) bersifat deterministik, jadi komponen graph construction tidak circular.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Validasi tripel input (Exp 06) akan secara tidak langsung memvalidasi graf.

**Status mitigasi:** BELUM

### Q2: Apakah baseline-nya fair?

**Jawaban:** Tidak ada baseline. Tidak dibandingkan dengan: (1) SQL query pada data yang sama, (2) LLM direct answering tanpa graf, (3) keyword search pada teks mentah.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Exp 09 ablation study akan membandingkan graph-based vs non-graph approaches.

**Status mitigasi:** BELUM

### Q3: Apakah skala datanya cukup?

**Jawaban:** Tidak. ~30 tripel menghasilkan graf yang trivially small. 3 hardcoded queries bukan evaluasi yang meaningful. Pada skala ini, klaim apapun tentang "queryability" atau "traversability" tidak bermakna karena graf terlalu kecil untuk memunculkan challenge yang real.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Scaling ke 10K+ tripel (ART-035, ART-036) akan membuat evaluasi graf meaningful.

**Status mitigasi:** BELUM

### Q4: Apakah klaim "neuro-symbolic" genuinely earned?

**Jawaban:** Tidak, pada tahap ini. Graph traversal dan edge filtering BUKAN symbolic reasoning. Dalam literatur AI, "symbolic" mengacu pada: logical inference, rule application, constraint satisfaction, theorem proving. Menggunakan `G.edges(data=True)` dengan filter kondisi bukanlah symbolic reasoning — ini adalah graph query.

`analysis.md` menggunakan istilah "Penalaran Simbolik" di judul, yang misleading. Yang dilakukan sebenarnya adalah "Graph Query" atau "Graph-based Information Retrieval".

**Severity jika tidak ditangani:** CRITICAL (di tingkat paper — mislabeling arsitektur)

**Rencana mitigasi:** Exp 05 akan mengimplementasikan formal rule engine (PySwip/owlready2) yang merupakan genuine symbolic reasoning. Sampai saat itu, label "symbolic" harus di-qualify.

**Status mitigasi:** BELUM

### Q5: Apakah novelty-nya real?

**Jawaban:** Tidak ada novelty teknis di Exp 02. Membangun graf dari tripel dan menjalankan traversal adalah operasi standar NetworkX. Domain aplikasi (hukum adat) memberikan novelty kontekstual, tapi bukan novelty teknis.

**Severity jika tidak ditangani:** MINOR (Exp 02 adalah building block, bukan kontribusi utama)

**Rencana mitigasi:** Novelty keseluruhan harus datang dari pipeline terintegrasi.

**Status mitigasi:** BELUM

### Q6: Apa yang bisa dilakukan sistem ini yang TIDAK bisa dilakukan oleh GPT-4 + simple prompt?

**Jawaban:** Pada skala saat ini (~30 tripel), GPT-4 bisa menjawab semua 3 query langsung dari teks tanpa membangun graf. Graf menjadi berguna pada skala di mana: (1) teks terlalu panjang untuk context window, (2) multi-hop reasoning diperlukan, (3) hubungan implisit perlu ditemukan melalui path traversal. Pada N=30, tidak ada keuntungan.

**Severity jika tidak ditangani:** CRITICAL (jika graf tidak menunjukkan keuntungan pada skala besar)

**Rencana mitigasi:** Scaling + demonstrasi multi-hop reasoning yang tidak bisa dilakukan oleh direct prompting.

**Status mitigasi:** BELUM

### Q7: Apakah metrik evaluasi valid?

**Jawaban:** Tidak ada metrik evaluasi. Keberhasilan dinilai secara kualitatif: "apakah output terlihat benar." Ini bukan evaluasi.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Exp 05 akan memiliki test suite dengan correct/incorrect answers.

**Status mitigasi:** BELUM

### Q8: Bisakah hasilnya direproduksi?

**Jawaban:** Ya, jika result.json dari Exp 01 tersedia. Kode graf deterministik (tidak ada random atau API calls). Namun, result.json sendiri non-deterministic (tergantung DeepSeek response).

**Severity jika tidak ditangani:** MINOR

**Rencana mitigasi:** Commit result.json ke repo sebagai snapshot.

**Status mitigasi:** SELESAI — result.json sudah ada di repo

### Q9: Apakah ada selection bias?

**Jawaban:** Ya. 3 query test dipilih berdasarkan apa yang "terlihat menarik" di graf, bukan secara sistematik. Query `Harta Pusako Tinggi` dan `Harta Pusako Rendah` dipilih karena diketahui ada di graf. Tidak ada query yang sengaja menguji kasus di mana graf gagal.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Test suite sistematik di Exp 05 dengan adversarial queries.

**Status mitigasi:** BELUM

### Q10: Apa yang TIDAK bisa dilakukan sistem ini?

**Jawaban:**
- Tidak bisa melakukan logical inference (hanya graph query)
- Tidak bisa menangani ambiguitas atau uncertainty
- Tidak bisa mendeteksi tripel yang salah di dalam graf
- Tidak bisa menangani dynamic queries (semua hardcoded)
- Tidak bisa reasoning across multiple domains (hanya Minangkabau)
- Tidak bisa menjelaskan *mengapa* sebuah jawaban benar (no provenance tracking)

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Sebagian akan ditangani oleh Exp 05 (rule engine), 07 (orchestration), dan scaling.

**Status mitigasi:** BELUM

---

## Ringkasan Review

| Aspek | Rating | Catatan |
|-------|--------|---------|
| Validitas Internal | Lemah | Tidak ada baseline atau metrik formal |
| Validitas Eksternal | Sangat Lemah | N=30, 1 domain, 3 hardcoded queries |
| Reproduktibilitas | Baik | Kode deterministik (given same input) |
| Novelty | Rendah | Standard graph operations |
| Kesiapan untuk Paper | Tidak Siap | Perlu genuine symbolic reasoning + scaling |

**Catatan penting:** `analysis.md` menyebutnya "Penalaran Simbolik" — ini harus di-reframe sebagai "Graph-based Query" di paper. Klaim symbolic baru valid setelah Exp 05.
