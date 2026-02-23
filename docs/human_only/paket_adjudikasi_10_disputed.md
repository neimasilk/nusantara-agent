# Formulir Adjudikasi Kasus Disputed - Proyek Nusantara-Agent

Tanggal: 2026-02-19

Anda diminta meninjau ulang 10 kasus yang labelnya berbeda antar-ahli. Untuk setiap kasus, baca skenario dan dua argumen anonim, lalu pilih label final (A/B/C/D) dengan alasan singkat.

Catatan data: pada snapshot `gs_active_cases.json` saat ini tidak terdapat nilai `gold_label = DISPUTED`, sehingga paket ini menggunakan cohort 10 kasus disputed dari dokumen IRA (`docs/ira_analysis_2026-02-12.md`) dengan isi kasus dan vote dari `gs_active_cases.json`.

# Rubrik Klasifikasi Label A/B/C/D

## Definisi Label

**A - Dominan Hukum Nasional**  
Kasus diselesaikan sepenuhnya atau dominan oleh hukum nasional (UU, KUHPerdata, Putusan MA/MK). Hukum adat tidak relevan atau tidak bisa mengesampingkan ketentuan nasional.

**B - Dominan Hukum Adat**  
Kasus diselesaikan sepenuhnya atau dominan oleh hukum adat setempat. Tidak ada konflik dengan hukum nasional, atau hukum nasional tidak mengatur hal tersebut secara spesifik.

**C - Sintesis / Konflik Nasional-Adat**  
Terdapat pertentangan aktif antara norma nasional dan adat. Pihak yang berbeda menuntut berdasarkan sistem hukum yang berbeda. Penyelesaian memerlukan harmonisasi atau pilihan hukum.

**D - Informasi Tidak Cukup**  
Skenario tidak memberikan informasi yang cukup untuk menentukan domain hukum yang berlaku.

## Panduan Batas Kritis (A vs C)

Ini adalah sumber disagreement terbesar. Gunakan tes berikut:

| Pertanyaan | Jika Ya -> | Jika Tidak -> |
|---|---|---|
| Apakah ada PIHAK yang secara aktif menuntut berdasarkan hukum adat MELAWAN pihak lain yang menuntut berdasarkan hukum nasional? | C | Kemungkinan A |
| Apakah UU memberikan aturan yang FINAL dan TIDAK BISA ditawar oleh adat? (contoh: batas usia nikah, syarat penetapan pengadilan) | A | Lanjut cek C |
| Apakah konteks adat hanya latar belakang cerita, bukan sumber tuntutan hukum? | A | C |

## Contoh Boundary Cases

**Contoh A (bukan C):**  
"Pasangan adat Bali ingin menikahkan anak 15 tahun dengan dispensasi adat." -> A. UU Perkawinan menetapkan batas 19 tahun secara final. Adat tidak bisa override.

**Contoh C (bukan A):**  
"Anggota kaum mengonversi tanah ulayat jadi SHM tanpa persetujuan KAN." -> C. Pihak individu menuntut hak milik (nasional/SHM), pihak kaum menuntut hak komunal (adat/ulayat). Dua sistem berkonflik aktif.

**Contoh B:**  
"Sengketa status harta pusako tinggi antar-kemenakan dalam satu kaum." -> B. Murni internal adat, tidak ada dimensi nasional.

**Contoh D:**  
"Seseorang bertanya tentang warisan tapi tidak menyebut jenis harta, lokasi, atau sistem hukum yang berlaku." -> D.


## Daftar Kasus Disputed

### 1. Case ID: CS-MIN-011

**Skenario:** Seorang anggota kaum di Minangkabau mengonversi tanah ulayat kaum menjadi Sertifikat Hak Milik (SHM) atas nama pribadi tanpa melalui musyawarah mufakat kaum dan tanpa persetujuan Kerapatan Adat Nagari (KAN).

**Argumen X**
- Rationale: Konversi tanah ulayat menjadi hak milik pribadi memerlukan pelepasan hak oleh pemangku adat. Tanpa persetujuan KAN proses dianggap cacat hukum karena melanggar hak komunal.
- Referensi 1: UU No. 5 Tahun 1960 (UUPA) tentang pengakuan hak ulayat
- Referensi 2: Yurisprudensi MA tentang pembatalan sertifikat di atas tanah ulayat

**Argumen Y**
- Rationale: Tanah ulayat adalah harta kolektif adat yang tidak dapat dikonversi menjadi SHM individual tanpa persetujuan KAN. Solusi memerlukan sintesis: pembatalan sertifikat dan musyawarah adat.
- Referensi 1: Pasal 3 UU No. 5 Tahun 1960 tentang UUPA
- Referensi 2: Perda Sumbar No. 6/2008 dan yurisprudensi MA No. 1806K/Pdt/2023

**Label X:** B
**Label Y:** C

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

### 2. Case ID: CS-JAW-006

**Skenario:** Dalam sebuah pernikahan poligami yang sah di Jawa, terjadi perceraian dengan istri kedua. Terjadi sengketa pembagian harta yang diperoleh selama masa pernikahan kedua tersebut.

**Argumen X**
- Rationale: UU Perkawinan mengatur harta bersama dibagi proporsional saat perceraian. Tidak ada peniadaan hak istri kedua oleh adat dalam konteks ini.
- Referensi 1: UU No. 1 Tahun 1974 Pasal 35 dan 37
- Referensi 2: Putusan MA No. 1029 K/Pdt/1996

**Argumen Y**
- Rationale: Sengketa gono-gini dalam perceraian poligami telah diatur jelas dalam instrumen nasional. Penyelesaian cukup melalui hukum nasional tanpa kebutuhan sintesis adat.
- Referensi 1: Pasal 97 KHI
- Referensi 2: Putusan MA No. 1062 K/Sip/1973

**Label X:** A
**Label Y:** A

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

### 3. Case ID: CS-NAS-066

**Skenario:** Sebuah desa adat memberikan sanksi pengucilan (kasepekang) kepada satu keluarga karena pelanggaran norma adat. Dampaknya, anak-anak dari keluarga tersebut dilarang bersekolah di sekolah desa setempat dan dilarang mendapatkan layanan kesehatan di puskesmas pembantu desa.

**Argumen X**
- Rationale: Sanksi adat tidak boleh melanggar hak konstitusional anak atas pendidikan dan kesehatan. Pembatasan layanan publik harus diintervensi negara.
- Referensi 1: UUD 1945 Pasal 28C dan 28H
- Referensi 2: UU No. 39 Tahun 1999 tentang HAM

**Argumen Y**
- Rationale: Sanksi adat yang menutup hak pendidikan dan kesehatan melanggar HAM serta dibatasi hukum nasional. Intervensi nasional menjadi dominan.
- Referensi 1: Pasal 66 UU No. 1/2023 (KUHP Baru)
- Referensi 2: Pasal 28C UUD 1945

**Label X:** A
**Label Y:** A

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

### 4. Case ID: CS-MIN-005

**Skenario:** Orang tua di Minangkabau menghibahkan harta hasil keringat sendiri (pusako rendah) kepada anak kandungnya melalui akta notaris. Kemenakan menggugat karena menurut adat, harta tersebut harusnya jatuh ke kemenakan.

**Argumen X**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Argumen Y**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Label X:** B
**Label Y:** C

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

### 5. Case ID: CS-JAW-011

**Skenario:** Sengketa hak waris anak angkat di Jawa. Hukum Islam (KHI) menggunakan wasiat wajibah, sementara hukum adat Jawa (yurisprudensi MA) menyetarakan posisi anak angkat dengan anak kandung dalam hal harta bersama.

**Argumen X**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Argumen Y**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Label X:** A
**Label Y:** C

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

### 6. Case ID: CS-MIN-015

**Skenario:** Sepasang kekasih dari suku yang sama di Minangkabau menikah secara sah di KUA. Masyarakat adat menjatuhkan sanksi 'buang adat' (diusir dari nagari) karena perkawinan sesuku dianggap inkes menurut adat.

**Argumen X**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Argumen Y**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Label X:** C
**Label Y:** B

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

### 7. Case ID: CS-JAW-019

**Skenario:** Pembagian warisan di Jawa di mana anak bungsu (ragil) diberikan rumah utama karena tanggung jawabnya merawat orang tua. Kakak-kakaknya menuntut pembagian rumah tersebut dibagi rata secara hukum perdata.

**Argumen X**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Argumen Y**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Label X:** B
**Label Y:** C

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

### 8. Case ID: CS-BAL-020

**Skenario:** Seorang janda dalam sistem nyentana (suami masuk keluarga istri) menikah lagi dengan pria dari keluarga lain. Keluarga asal istri menuntut harta peninggalan (yang berasal dari garis istri) tetap di keluarga asal.

**Argumen X**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Argumen Y**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Label X:** B
**Label Y:** C

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

### 9. Case ID: CS-NAS-041

**Skenario:** Perusahaan tambang memiliki izin resmi dari pemerintah pusat (IUP), namun masyarakat adat setempat menolak aktivitas tambang karena wilayahnya masuk dalam hutan adat mereka yang belum bersertifikat.

**Argumen X**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Argumen Y**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Label X:** A
**Label Y:** C

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

### 10. Case ID: CS-JAW-030

**Skenario:** Pewaris membagi harta kepada anak laki-laki dan perempuan secara sama rata (sigar semangka) sesuai pesan lisan. Anak laki-laki menggugat ingin menggunakan hukum Islam (2:1).

**Argumen X**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Argumen Y**
- Rationale: Catatan rationale tidak tersedia pada data saat ini.
- Referensi 1: -
- Referensi 2: -

**Label X:** B
**Label Y:** C

| Label Final (A/B/C/D) | Alasan | Referensi Hukum |
|---|---|---|
| | | |

## Pengesahan

- Nama: ________________________________
- Tanda Tangan: ________________________
- Tanggal Pengisian: ____________________
