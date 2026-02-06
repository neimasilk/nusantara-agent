# Analisis Eksperimen 1: Ekstraksi Tripel Hukum Adat

**Tujuan:** Menguji kemampuan DeepSeek API dalam mengekstrak relasi hukum terstruktur dari teks naratif hukum adat Minangkabau.

## Temuan Utama
1.  **Pemahaman Hierarki:** Model berhasil membedakan antara `Harta Pusako Tinggi` dan `Harta Pusako Rendah` sebagai entitas yang berbeda dengan aturan yang berbeda pula.
2.  **Diferensiasi Peran:** Model sangat cerdas dalam membedakan **Otoritas** (`Mamak Kepala Waris`) dan **Kepemilikan** (`anggota perempuan`), yang merupakan inti dari sistem matrilineal Minangkabau. Ini adalah poin krusial untuk Neuro-Symbolic reasoning.
3.  **Deteksi Konflik:** Model mampu mengekstrak bagian "konflik" sebagai objek terpisah, mengidentifikasi ketegangan antara hukum adat (kemenakan) dan hukum Islam/nasional (anak).

## Masalah & Mitigasi
*   **Objek Panjang:** Beberapa objek tripel masih berbentuk frasa panjang (misal: "kecuali dalam kondisi darurat...").
    *   *Mitigasi:* Perlu penyempurnaan prompt agar memaksa objek menjadi entitas tunggal atau memecahnya menjadi beberapa tripel kondisional.
*   **Confidence Score:** Model memberikan skor 1.0 secara konsisten. Ini mungkin "overconfidence". Perlu pengujian dengan teks yang lebih ambigu.

## Kesimpulan
Eksperimen 1 **BERHASIL**. DeepSeek terbukti mampu menjadi mesin ekstraksi yang mumpuni untuk membangun Knowledge Graph hukum adat tahap awal. Hipotesis bahwa AI akan gagal menangkap nuansa budaya pada level ekstraksi tripel **gugur** (AI ternyata cukup pintar).

**Status: Lanjut ke Eksperimen 2 (Ontology Mapping & Neo4j Integration).**
