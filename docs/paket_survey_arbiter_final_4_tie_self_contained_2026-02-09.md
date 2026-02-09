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
- label_final: `[ ] A  [ ] B  [ ] C  [ ] D`
- keyakinan: `[ ] Tinggi  [ ] Sedang  [ ] Rendah`
- alasan_singkat:
  ............................................................................
  ............................................................................
- referensi_1:
  ............................................................................
- referensi_2:
  ............................................................................
- jika_label_D_fakta_kurang:
  ............................................................................

## Kasus 2 - CS-LIN-017
Narasi:  
Sebuah keluarga melakukan pengangkatan anak secara adat dengan upacara sakral yang disaksikan tetua. Namun, saat anak tersebut dewasa dan ingin mengurus paspor, pihak imigrasi menolak karena tidak ada penetapan pengadilan negeri.

Posisi Ahli Sebelumnya:
- Ahli-1: `A` (keyakinan tinggi). Alasan: urusan adm negara seperti paspor mensyaratkan penetapan pengadilan.
- Ahli-2: `C` (keyakinan tinggi). Alasan: adopsi adat diakui sosial, namun legalisasi nasional tetap dibutuhkan (sintesis).
- Ahli-3: `C` (keyakinan sedang). Alasan: perlu sintesis pengakuan adat dan administrasi negara.
- Ahli-4: `A` (keyakinan tinggi). Alasan: adm kependudukan dan imigrasi mensyaratkan penetapan pengadilan.

Form Keputusan Arbiter:
- label_final: `[ ] A  [ ] B  [ ] C  [ ] D`
- keyakinan: `[ ] Tinggi  [ ] Sedang  [ ] Rendah`
- alasan_singkat:
  ............................................................................
  ............................................................................
- referensi_1:
  ............................................................................
- referensi_2:
  ............................................................................
- jika_label_D_fakta_kurang:
  ............................................................................

## Kasus 3 - CS-BAL-014
Narasi:  
Seorang janda di Bali yang tidak memiliki anak ingin tetap tinggal di rumah mendiang suaminya. Keluarga suami mengusirnya karena janda tersebut dianggap tidak lagi memiliki ikatan hukum setelah suami wafat.

Posisi Ahli Sebelumnya:
- Ahli-1: `B` (keyakinan tinggi). Alasan: hak ngindung/hak tinggal janda dijamin dalam perlindungan adat Bali.
- Ahli-2: `C` (keyakinan tinggi). Alasan: norma adat modern + perlindungan hukum nasional memerlukan sintesis.
- Ahli-3: `B` (keyakinan sedang). Alasan: forum adat dan awig-awig menjadi kanal utama penyelesaian.
- Ahli-4: `C` (keyakinan sedang). Alasan: perlindungan tempat tinggal perlu sintesis antara adat Bali dan hukum nasional.

Form Keputusan Arbiter:
- label_final: `[ ] A  [ ] B  [ ] C  [ ] D`
- keyakinan: `[ ] Tinggi  [ ] Sedang  [ ] Rendah`
- alasan_singkat:
  ............................................................................
  ............................................................................
- referensi_1:
  ............................................................................
- referensi_2:
  ............................................................................
- jika_label_D_fakta_kurang:
  ............................................................................

## Kasus 4 - CS-LIN-016
Narasi:  
Keluarga urban di Jakarta terdiri dari suami (Suku Minang) dan istri (Suku Jawa). Mereka memiliki aset di Jakarta. Saat suami wafat, terjadi perdebatan apakah menggunakan sistem matrilineal (adat suami) atau hukum perdata nasional.

Posisi Ahli Sebelumnya:
- Ahli-1: `C` (keyakinan sedang). Alasan: sengketa keluarga campuran cenderung perlu jalan tengah/netral.
- Ahli-2: `A` (keyakinan tinggi). Alasan: domisili Jakarta dan aset urban mendorong penggunaan hukum nasional sebagai kerangka utama.
- Ahli-3: `C` (keyakinan sedang). Alasan: klaim nasional dan adat hadir bersamaan, perlu desain sintesis.
- Ahli-4: `A` (keyakinan tinggi). Alasan: aset urban tunduk pada hukum perdata nasional.

Form Keputusan Arbiter:
- label_final: `[ ] A  [ ] B  [ ] C  [ ] D`
- keyakinan: `[ ] Tinggi  [ ] Sedang  [ ] Rendah`
- alasan_singkat:
  ............................................................................
  ............................................................................
- referensi_1:
  ............................................................................
- referensi_2:
  ............................................................................
- jika_label_D_fakta_kurang:
  ............................................................................

## Rekap Jawaban Final (Wajib Diisi)
| id | label_final | keyakinan | alasan_singkat | referensi_1 | referensi_2 | jika_D_fakta_kurang |
| --- | --- | --- | --- | --- | --- | --- |
| CS-LIN-052 |  |  |  |  |  |  |
| CS-LIN-017 |  |  |  |  |  |  |
| CS-BAL-014 |  |  |  |  |  |  |
| CS-LIN-016 |  |  |  |  |  |  |

## Pernyataan Arbiter
Saya menetapkan keputusan di atas berdasarkan penilaian hukum substantif independen atas fakta yang tersedia.

Nama Arbiter:
............................................................

Tanda Tangan:
............................................................

Tanggal:
............................................................
