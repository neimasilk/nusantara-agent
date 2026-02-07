# Analisis Eksperimen 2: Integrasi Graf & Penalaran Simbolik

**Tujuan:** Menguji apakah tripel hasil ekstraksi neural dapat digunakan untuk penalaran logis (symbolic reasoning) melalui struktur graf.

## Temuan Utama
1.  **Queryability:** Graf berhasil menjawab pertanyaan spesifik tentang otoritas hukum (`Mamak Kepala Waris` sebagai otoritas `Pusako Tinggi`) tanpa perlu pencarian teks lagi.
2.  **Strukturalisasi Konflik:** Konflik hukum bukan lagi sekadar teks, melainkan objek yang memiliki relasi ke entitas-entitas yang bertikai. Ini memungkinkan agen "Supervisor" nantinya untuk mengidentifikasi *siapa* dan *apa* yang berkonflik secara programatik.
3.  **Path Logic:** Traversal pada `Pusako Rendah` menunjukkan alur pewarisan yang berbeda (ke anak kandung), membuktikan bahwa sistem bisa memisahkan dua "jalur hukum" yang berbeda dalam satu basis pengetahuan.

## Implikasi untuk Arsitektur Nusantara-Agent
*   Kita bisa menggunakan **GraphRAG** di mana LLM tidak hanya mencari teks (Vector DB) tapi juga melakukan "hop" di dalam graf untuk menemukan relasi yang tidak tertulis secara eksplisit dalam satu paragraf.
*   Pemisahan kategori (kepemilikan, otoritas, larangan) sangat krusial untuk membangun "Rule-based" layer di atas LLM.

## Kesimpulan
Eksperimen 2 menunjukkan bahwa pipeline end-to-end berfungsi pada skala proof-of-concept:
`Teks Mentah` -> `DeepSeek (Neural)` -> `Triples (JSON)` -> `Graph (Symbolic)` -> `Logical Answer`. Keterbatasan: diuji pada 1 query dan ~30 tripel saja (lihat F-004).

**Status: Siap untuk Eksperimen 3 (Multi-Agent Orchestration Dasar).**
