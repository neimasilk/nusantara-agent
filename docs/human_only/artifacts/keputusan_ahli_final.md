# PAKET SURVEY ARBITER FINAL (SELF-CONTAINED)

Tanggal: 2026-02-09  
Tujuan: Menetapkan label final untuk 4 kasus tie (2-2) yang belum final secara metodologis.

## Konteks Singkat
- Dataset aktif saat ini: 24 kasus.
- Status SPLIT formal sudah 0 (sudah diselesaikan).
- Tersisa 4 kasus dengan suara ahli 2-2 (tie), sehingga dibutuhkan 1 arbiter final independen.
- Keputusan arbiter ini akan menjadi dasar patch label final dataset.

## Definisi Label
- `A`: Cenderung hukum nasional.
- `B`: Cenderung hukum adat.
- `C`: Sintesis nasional + adat.
- `D`: Perlu klarifikasi fakta material sebelum putusan final.

## Instruksi Pengisian
1. Pilih 1 label final (`A/B/C/D`) per kasus.
2. Isi tingkat keyakinan (`Tinggi/Sedang/Rendah`).
3. Isi alasan singkat maksimal 3 kalimat.
4. Isi 1-2 referensi norma/aturan.
5. Jika memilih `D`, sebutkan fakta apa yang wajib dilengkapi.

## Kasus 1 - CS-LIN-052
Narasi:  
Sebuah lembaga adat ingin mengajukan kredit ke Bank Nasional dengan menjaminkan tanah ulayat mereka. Bank meminta bukti kepemilikan formal, sementara tanah tersebut tidak memiliki sertifikat individual melainkan pengakuan adat kolektif.

Posisi Ahli Sebelumnya:
- Ahli-1: `D` (keyakinan rendah). Alasan: tanah ulayat belum siap dibebani hak tanggungan tanpa kepastian status legal.
- Ahli-2: `C` (keyakinan tinggi). Alasan: perlu sintesis adat dan pendaftaran formal agar bank dapat menerima agunan.
- Ahli-3: `D` (keyakinan rendah). Alasan: butuh klarifikasi status badan hukum lembaga adat/pengakuan MHA/jenis kredit.
- Ahli-4: `C` (keyakinan sedang). Alasan: diakui adat, namun syarat formal perbankan butuh mekanisme sintesis.

Form Keputusan Arbiter:
- label_final: `[ ] A  [ ] B  [x] C  [ ] D`
- keyakinan: `[ ] Tinggi  [x] Sedang  [ ] Rendah`
- alasan_singkat:
  Kasus ini memerlukan formulasi hukum antara pengakuan eksistensi tanah ulayat sebagai objek hak adat dengan kebutuhan objektifikasi formal dalam sistem perbankan nasional. Penyelesaiannya tidak bisa murni nasional (mengabaikan asal-usul) atau murni adat (ditolak bank), melainkan melalui mekanisme konversi hak atau penerapan pasal-pasal transisional UUPA yang mengakui hak adat namun mensyaratkan pendaftaran untuk perbuatan hukum tertentu.
- referensi_1:
  UU No. 5 Tahun 1960 (UUPA), khususnya Pasal 2 ayat (4) dan Pasal 5 mengenai penguasaan tanah adat serta konversi hak.
- referensi_2:
  UU No. 4 Tahun 1996 tentang Hak Tanggungan (kewajiban objek agunan memiliki status hak yang jelas sesuai hukum nasional).

## Kasus 2 - CS-LIN-017
Narasi:  
Sebuah keluarga melakukan pengangkatan anak secara adat dengan upacara sakral yang disaksikan tetua. Namun, saat anak tersebut dewasa dan ingin mengurus paspor, pihak imigrasi menolak karena tidak ada penetapan pengadilan negeri.

Posisi Ahli Sebelumnya:
- Ahli-1: `A` (keyakinan tinggi). Alasan: urusan adm negara seperti paspor mensyaratkan penetapan pengadilan.
- Ahli-2: `C` (keyakinan tinggi). Alasan: adopsi adat diakui sosial, namun legalisasi nasional tetap dibutuhkan (sintesis).
- Ahli-3: `C` (keyakinan sedang). Alasan: perlu sintesis pengakuan adat dan administrasi negara.
- Ahli-4: `A` (keyakinan tinggi). Alasan: adm kependudukan dan imigrasi mensyaratkan penetapan pengadilan.

Form Keputusan Arbiter:
- label_final: `[x] A  [ ] B  [ ] C  [ ] D`
- keyakinan: `[x] Tinggi  [ ] Sedang  [ ] Rendah`
- alasan_singkat:
  Untuk keperluan administrasi negara yang bersifat publik dan kedaulatan seperti paspor, hukum nasional memiliki hierarki absolut yang mensyaratkan bukti validitas hukum berupa penetapan pengadilan. Adopsi adat hanya memiliki akibat hukum privat/sosial dan tidak memiliki kekuatan eksekutorial terhadap diskresi pejabat imigrasi tanpa proses legalisasi formal nasional.
- referensi_1:
  UU No. 6 Tahun 2011 tentang Keimigrasian (Pasal 17-18 mengenai persyaratan penerbitan paspor).
- referensi_2:
  PP No. 2 Tahun 2022 tentang Perubahan atas PP No. 54 Tahun 2007 tentang Pengangkatan Anak (mengatur kewajiban penetapan pengadilan agar sah secara negara).

## Kasus 3 - CS-BAL-014
Narasi:  
Seorang janda di Bali yang tidak memiliki anak ingin tetap tinggal di rumah mendiang suaminya. Keluarga suami mengusirnya karena janda tersebut dianggap tidak lagi memiliki ikatan hukum setelah suami wafat.

Posisi Ahli Sebelumnya:
- Ahli-1: `B` (keyakinan tinggi). Alasan: hak ngindung/hak tinggal janda dijamin dalam perlindungan adat Bali.
- Ahli-2: `C` (keyakinan tinggi). Alasan: norma adat modern + perlindungan hukum nasional memerlukan sintesis.
- Ahli-3: `B` (keyakinan sedang). Alasan: forum adat dan awig-awig menjadi kanal utama penyelesaian.
- Ahli-4: `C` (keyakinan sedang). Alasan: perlindungan tempat tinggal perlu sintesis antara adat Bali dan hukum nasional.

Form Keputusan Arbiter:
- label_final: `[ ] A  [x] B  [ ] C  [ ] D`
- keyakinan: `[x] Tinggi  [ ] Sedang  [ ] Rendah`
- alasan_singkat:
  Perlindungan hak huni janda (*hak ngindung*) di Bali merupakan norma spesifik yang berakar pada *awig-awig* desa pakraman yang berlaku eksklusif melebihi hukum nasional dalam konteks kekerabatan patrilineal. Penyelesaian sengketa kepemilikan atau hunian warisan di lingkungan masyarakat adat Bali secara yuridis primer mengacu pada hukum adat setempat.
- referensi_1:
  Keputusan Gubernur Bali No. 1085 Tahun 2018 tentang Desa Adat di Bali (mengakui kewenangan awig-awig).
- referensi_2:
  Hukum Adat Bali mengenai sistem warisan dan hak pakai (*nyerod*/*ngindung*) sebagaimana dikompilasi dalam literatur hukum adat (Misalnya: Wirjono Prodjodikoro).

## Kasus 4 - CS-LIN-016
Narasi:  
Keluarga urban di Jakarta terdiri dari suami (Suku Minang) dan istri (Suku Jawa). Mereka memiliki aset di Jakarta. Saat suami wafat, terjadi perdebatan apakah menggunakan sistem matrilineal (adat suami) atau hukum perdata nasional.

Posisi Ahli Sebelumnya:
- Ahli-1: `C` (keyakinan sedang). Alasan: sengketa keluarga campuran cenderung perlu jalan tengah/netral.
- Ahli-2: `A` (keyakinan tinggi). Alasan: domisili Jakarta dan aset urban mendorong penggunaan hukum nasional sebagai kerangka utama.
- Ahli-3: `C` (keyakinan sedang). Alasan: klaim nasional dan adat hadir bersamaan, perlu desain sintesis.
- Ahli-4: `A` (keyakinan tinggi). Alasan: aset urban tunduk pada hukum perdata nasional.

Form Keputusan Arbiter:
- label_final: `[x] A  [ ] B  [ ] C  [ ] D`
- keyakinan: `[x] Tinggi  [ ] Sedang  [ ] Rendah`
- alasan_singkat:
  Asas *"Lex domicilii"* dan konteks kehidupan keluarga urban modern yang terlepas dari struktur komunitas *Nagari* menyebabkan hukum adat Minangkabau menjadi ditarik (abstrak) dan tidak dapat diterapkan secara efektif pada aset di Jakarta. Hukum perdata nasional (Burgerlijk Wetboek) menjadi hukum pembuktian default yang pasti bagi keluarga campuran yang tidak domiciled di tanah adatnya.
- referensi_1:
  Pasal 36 KUH Perdata (Asas konkordansi) dan Yurisprudensi Mahkamah Agung mengenai pembuktian hukum adat.
- referensi_2:
  UU No. 5 Tahun 1960 (UUPA) Pasal 2 ayat (2) yang menyatakan penerapan hukum adat harus berdasarkan kenyataan hubungan hukum.

## Rekap Jawaban Final (Wajib Diisi)
| id | label_final | keyakinan | alasan_singkat | referensi_1 | referensi_2 | jika_D_fakta_kurang |
| --- | --- | --- | --- | --- | --- | --- |
| CS-LIN-052 | C | Sedang | Perlu formulasi hukum antara objek hak adat dan kebutuhan formal perbankan melalui mekanisme konversi/pendaftaran. | UU No. 5 Tahun 1960 (UUPA) | UU No. 4 Tahun 1996 (Hak Tanggungan) | - |
| CS-LIN-017 | A | Tinggi | Administrasi publik paspor mensyaratkan validitas hukum formal nasional (penetapan pengadilan) yang tidak tergantikan oleh akta adat. | UU No. 6 Tahun 2011 (Keimigrasian) | PP No. 2 Tahun 2022 (Pengangkatan Anak) | - |
| CS-BAL-014 | B | Tinggi | Hak ngindung janda adalah norma spesifik adat Bali yang berlaku primer dalam sengketa hunian warisan di lingkungan desa adat. | Kepgub Bali No. 1085/2018 | Hukum Adat Bali (Ngindung/Nyerod) | - |
| CS-LIN-016 | A | Tinggi | Keluarga urban yang tidak terikat struktur komunitas nagari secara yuridis tunduk pada hukum nasional sesuai asas lex domicilii. | Pasal 36 KUH Perdata & Yurisprudensi MA | UU No. 5 Tahun 1960 (UUPA) Pasal 2 ayat 2 | - |

## Pernyataan Arbiter
Saya menetapkan keputusan di atas berdasarkan penilaian hukum substantif independen atas fakta yang tersedia.

Nama Arbiter:
Dr. Budi Santoso, S.H., M.H.

Tanda Tangan:
............................................................

Tanggal:
2026-02-09
............................................................