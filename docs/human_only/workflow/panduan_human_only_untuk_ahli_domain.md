# Panduan Kerja HUMAN-ONLY untuk Ahli Domain (Non-Teknis)

Dokumen ini disusun agar pekerjaan riset bisa dikerjakan oleh ahli hukum/adat yang **tidak perlu kemampuan komputer/programming**.

Versi: 2026-02-08  
Proyek: Nusantara-Agent

---

## 1) Tujuan Dokumen

Panduan ini membantu Bapak/Ibu ahli domain untuk:
1. Mengetahui pekerjaan prioritas yang murni membutuhkan keahlian substansi.
2. Mengisi data/review dengan format sederhana.
3. Menyerahkan hasil ke tim teknis tanpa perlu menyentuh kode.

---

## 2) Prinsip Kerja Sederhana

1. Fokus pada **akurasi substansi hukum/adat**, bukan format teknis.
2. Gunakan bahasa Indonesia yang jelas dan ringkas.
3. Jika ragu, tulis: `PERLU KLARIFIKASI` lalu beri catatan singkat.
4. Semua keputusan penting harus punya dasar: referensi, putusan, atau praktik adat yang dapat dipertanggungjawabkan.

---

## 3) Prioritas Pekerjaan yang Dibutuhkan Sekarang

Urutan prioritas saat ini:
1. `ART-026` Rekrut & kalibrasi annotator.
2. `ART-027` Pilih 200 paragraf sumber primer.
3. `ART-028` Anotasi manusia untuk gold standard.
4. `ART-030` Kumpulkan 50+ putusan MA terkait sengketa adat.
5. `ART-032/033/034` Kumpulkan korpus teks adat Bali/Jawa/Minangkabau.
6. `ART-050` Susun 200 test case lintas domain.

Catatan: Pekerjaan di atas adalah blokir utama untuk eksperimen lanjutan.

---

## 4) Paket Tugas per ART (Bahasa Operasional)

## ART-026: Rekrut dan Kalibrasi Annotator

Tujuan:
Membentuk 5 annotator (minimal 2 ahli adat/hukum adat) yang punya pemahaman seragam.

Output yang diminta:
1. Daftar 5 annotator (nama, latar belakang, kontak).
2. Bukti pelatihan singkat (tanggal, materi, durasi).
3. Hasil pilot anotasi 20 item.

Checklist selesai:
1. Jumlah annotator = 5.
2. Seluruh annotator sudah ikut briefing.
3. Ada catatan masalah umum saat pilot.

---

## ART-027: Pilih 200 Paragraf Sumber Primer

Tujuan:
Menyusun dataset teks primer yang seimbang untuk 3 domain.

Target komposisi:
1. Minangkabau: 60-70 paragraf.
2. Bali: 60-70 paragraf.
3. Jawa: 60-70 paragraf.

Kategori wajib tersebar:
1. Waris.
2. Harta/objek.
3. Otoritas/lembaga adat.
4. Sengketa/penyelesaian konflik.

Checklist kualitas:
1. Bukan hasil AI sintetis.
2. Sumber dapat ditelusuri.
3. Teks cukup jelas untuk dianotasi.

---

## ART-028: Anotasi Gold Standard oleh Manusia

Tujuan:
Membuat anotasi final yang dipakai sebagai acuan evaluasi sistem.

Yang dikerjakan annotator:
1. Menandai triple/substansi hukum dari paragraf.
2. Memberi label akurasi budaya/hukum.
3. Menulis alasan singkat jika ada ambiguitas.

Checklist kualitas:
1. Konsisten antar annotator.
2. Tidak copy-paste antar annotator.
3. Ada catatan untuk kasus abu-abu.

---

## ART-030: Kumpulkan 50+ Putusan MA

Tujuan:
Menyediakan ground truth eksternal dari putusan pengadilan.

Minimal metadata per putusan:
1. Nomor putusan.
2. Tahun.
3. Topik sengketa.
4. Domain adat (Bali/Jawa/Minangkabau/dll).
5. Ringkasan ratio decidendi (alasan hukum inti).
6. Amar putusan singkat.
7. Sumber tautan resmi.

Checklist kualitas:
1. Putusan valid dari sumber resmi.
2. Ringkasan substansi bukan opini pribadi.
3. Domain adat teridentifikasi jelas.

---

## ART-032/033/034: Pengumpulan Korpus Teks Adat

Tujuan:
Memperkaya korpus primer untuk skala eksperimen.

Target minimum:
1. Bali: 30+ sumber.
2. Jawa: 30+ sumber.
3. Minangkabau: 30+ sumber tambahan.

Checklist kualitas:
1. Sumber akademik/otoritatif.
2. Topik beragam (waris, struktur keluarga, sengketa, hak atas harta).
3. Dokumen terbaca baik (tidak rusak/tidak blur).

---

## ART-050: Susun 200 Test Case Lintas Domain

Tujuan:
Membuat set uji final untuk menilai performa sistem secara adil.

Komposisi:
1. 50 kasus Minangkabau.
2. 50 kasus Bali.
3. 50 kasus Jawa.
4. 50 kasus konflik lintas domain/nasional.

Per kasus wajib ada:
1. Narasi kasus singkat.
2. Isu hukum utama.
3. Jawaban acuan (gold reasoning) versi manusia.
4. Referensi pendukung.

---

## 5) Template Isian Sederhana (Siap Copy-Paste)

Gunakan format berikut untuk setiap item kerja:

```text
ID ART:
Nama Pengisi:
Tanggal:

Objek yang dikerjakan:
- 

Hasil ringkas:
- 

Dasar/referensi:
- 

Catatan keraguan (jika ada):
- 

Status:
- SELESAI / PERLU KLARIFIKASI
```

---

## 6) Cara Penyerahan Hasil (Non-Teknis)

Silakan kirim hasil dengan salah satu cara berikut:
1. File Word/Excel/PDF via email/drive/WhatsApp ke koordinator.
2. Foto dokumen tulis tangan (jika darurat), lalu dikonfirmasi ulang oleh koordinator.

Tim teknis akan:
1. Memindahkan isi ke format folder proyek.
2. Menjaga struktur data teknis.
3. Menghubungi kembali jika ada bagian yang perlu klarifikasi substansi.

---

## 7) Kriteria Diterima atau Perlu Revisi

`DITERIMA` jika:
1. Isi substansi jelas dan konsisten.
2. Ada rujukan dasar yang dapat ditelusuri.
3. Tidak ada kontradiksi fatal antarbagian.

`PERLU REVISI` jika:
1. Klaim tanpa dasar.
2. Domain adat tidak jelas.
3. Ringkasan putusan/sumber tidak akurat.

---

## 8) Kontak Koordinasi

Koordinator proyek mengisi bagian ini sebelum PDF dibagikan:
1. Nama:
2. Nomor/Email:
3. Batas waktu pengumpulan:
4. Format file yang disepakati:

