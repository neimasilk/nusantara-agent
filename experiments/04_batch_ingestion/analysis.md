# Analisis Eksperimen 4: Scalable Batch Ingestion

**Tujuan:** Membangun pipeline ingesti data yang modular dan siap untuk pengolahan data hukum adat secara massal.

## Temuan Utama
1.  **Ekstraksi Modular:** Penggunaan modul terpisah (`src/utils/text_processor.py`) memungkinkan standarisasi pembersihan teks lintas anggota tim.
2.  **Efisiensi JSONL:** Penggunaan format `.jsonl` sangat efektif untuk riset berskala besar. Setiap baris mewakili satu tripel, memudahkan audit manual dan penggabungan dataset dari berbagai sumber/mesin.
3.  **Handling Chunks:** Algoritma chunking berbasis paragraf berhasil mempertahankan integritas makna hukum sambil tetap menjaga konsumsi token API dalam batas aman.

## Lesson Learned (Kesalahan Teknis)
*   Ditemukan banyak kesalahan sintaksis (`SyntaxError`) akibat baris baru manual dalam penulisan script melalui agen.
*   *Mitigasi:* Gunakan format string yang lebih bersih dan pastikan tidak ada baris baru yang tidak sengaja dalam template `write_file`.

## Kesimpulan
Pipeline **Ingesti Massa** sudah siap. Infrastruktur ini bisa digunakan untuk mulai memproses ratusan PDF jurnal hukum adat sesuai rencana Fase 2.

**Status: Infrastruktur Data Ingestion Ready.**
