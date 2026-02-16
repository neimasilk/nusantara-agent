# Handoff Singkat — Mata Elang Weekly Review
**Tanggal:** 2026-02-16  
**Mode:** Strategic weekly gate (bukan eksekusi harian)

## 1. Konteks Terakhir
- Scope paper aktif: **Neuro-Symbolic Legal Reasoning with Expert-Verified Customary Law Rules** (post-pivot 2026-02-12).
- Verifikasi SOP engineering sudah dijalankan: `python scripts/run_test_suite.py` lulus penuh (`101/101`).
- Dokumentasi aktif disinkronkan pada sesi ini untuk menghindari drift narasi:
  - `README.md`
  - `docs/collaboration_guide.md`
  - `docs/testing_framework.md`

## 2. Keputusan Penting
- Multi-agent debate/self-correction tetap diposisikan sebagai hasil negatif/arsip riset, bukan jalur klaim utama paper.
- Klaim performa paper harus bergantung pada data yang reliable (subset agreed + adjudikasi lanjutan), bukan label yang masih `DISPUTED`.
- Neo4j/Qdrant/CCS tidak dipakai sebagai scope aktif paper saat ini.

## 3. Asumsi Aktif
- Owner tetap menargetkan jalur submit Q1 pada horizon 6-8 minggu dari 2026-02-12.
- Data aktif benchmark masih 24 kasus (14 agreed, 10 disputed) sambil menunggu adjudikasi/ekspansi.
- Penggunaan API berbayar tetap controlled dan butuh persetujuan eksplisit untuk call non-rutin.

## 4. Status Milestone (Ringkas)
- P-001 (IRA): sudah dihitung; temuan reliability issue terdokumentasi.
- P-002 (resolve split/disputed): belum selesai penuh.
- P-003/P-004 (environment + rerun LLM mode reproducible): masih perlu penguncian parity.
- P-005+ (expand ke 100+ kasus): masih menjadi blocker utama eksperimen inti statistik.

## 5. Risiko Diketahui
- Reliability gold standard belum kuat (disputed cases tinggi untuk skala klaim paper).
- Ambiguitas label A-vs-C masih dominan dan bisa membuat akurasi terlihat misleading.
- Human bottleneck (adjudikasi/annotasi) tetap high risk pada timeline.
- Drift narasi bisa kembali jika dokumen status tidak diperbarui serentak saat ada perubahan scope.

## 6. Langkah Berikutnya (Direkomendasikan)
1. Selesaikan adjudikasi 10 kasus `DISPUTED` dengan rater qualified + jejak keputusan eksplisit.
2. Bekukan paket benchmark `scientific_claimable` dengan manifest/hash final sebelum run ablation utama.
3. Jalankan LLM+Rules vs LLM-only pada dataset >=100 kasus dengan logging reproducibility.
4. Hitung McNemar + CI 95% dan tulis batas klaim sesuai evidence aktual.
5. Update sekali lagi `CLAUDE.md`/`task_registry_simplified` setelah milestone data bergerak.

## 7. Prompt Singkat untuk Agen Berikutnya
Gunakan mode weekly strategic follow-through. Mulai dari `docs/task_registry_simplified.md` dan `docs/ira_analysis_2026-02-12.md`, fokus eksekusi pada adjudikasi kasus `DISPUTED` dan kesiapan benchmark `scientific_claimable` (manifest, provenance, reproducibility). Jangan buka scope GraphRAG/Neo4j/Qdrant/CCS. Setelah perubahan, jalankan `python scripts/run_test_suite.py`, update dokumen status aktif yang terdampak, lalu commit dengan pesan yang menyebut milestone/task ID.
