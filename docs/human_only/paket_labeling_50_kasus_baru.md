# Formulir Labeling Kasus Hukum Adat - Proyek Nusantara-Agent (Batch 2)

Tanggal: 2026-02-19

Anda diminta melabeli 50 kasus hukum adat. Untuk setiap kasus, baca skenario lalu pilih label A/B/C/D. JANGAN melihat referensi atau label orang lain.

Catatan sumber data: paket ini disusun dari pool `annotations` (baris `ann01` pada `full_assignment_200x5.csv`) yang tidak termasuk `gs_active_cases.json` aktif. Pada pool kandidat yang tersedia saat ini, domain yang tersedia adalah Minangkabau, Bali, dan Jawa.

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


## Daftar 50 Kasus

### 1. Case ID: GS-0001

**Domain:** Minangkabau

**Skenario:** Dalam masyarakat Minangkabau, harta warisan dibedakan menjadi dua kategori utama: Harta Pusako Tinggi dan Harta Pusako Rendah.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 2. Case ID: GS-0002

**Domain:** Minangkabau

**Skenario:** Harta Pusako Tinggi adalah harta turun-temurun yang dimiliki oleh suatu kaum secara kolektif dan diwariskan dari garis ibu (matrilineal).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 3. Case ID: GS-0003

**Domain:** Minangkabau

**Skenario:** Pengelolaan harta ini berada di bawah otoritas Mamak Kepala Waris, namun kepemilikannya tetap pada anggota perempuan dalam kaum tersebut.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 4. Case ID: GS-0004

**Domain:** Minangkabau

**Skenario:** Harta ini tidak boleh diperjualbelikan, kecuali dalam kondisi darurat yang diatur secara ketat oleh adat (seperti mayat terbujur di tengah rumah).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 5. Case ID: GS-0005

**Domain:** Minangkabau

**Skenario:** Sebaliknya, Harta Pusako Rendah adalah harta hasil pencaharian sendiri oleh orang tua selama masa perkawinan.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 6. Case ID: GS-0006

**Domain:** Minangkabau

**Skenario:** Berbeda dengan Pusako Tinggi, Pusako Rendah dapat diwariskan kepada anak kandung sesuai dengan ketentuan hukum Islam atau kesepakatan keluarga, yang seringkali memicu ketegangan antara hak kemenakan (berdasarkan adat matrilineal) dan hak anak (berdasarkan hukum nasional/Islam).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 7. Case ID: GS-0025

**Domain:** Minangkabau

**Skenario:** Dalam masyarakat Minangkabau, harta warisan dibedakan menjadi dua kategori utama: Harta Pusako Tinggi dan Harta Pusako Rendah. Harta Pusako Tinggi adalah harta turun-temurun yang dimiliki oleh suatu kaum secara kolektif dan diwariskan dari garis ibu (matrilineal). Pengelolaan harta ini berada di bawah otoritas Mamak Kepala Waris, namun kepemilikannya tetap pada anggota perempuan dalam kaum tersebut. Harta ini tidak boleh diperjualbelikan, kecuali dalam kondisi darurat yang diatur secara ketat oleh adat (seperti mayat terbujur di tengah rumah).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 8. Case ID: GS-0026

**Domain:** Minangkabau

**Skenario:** Sebaliknya, Harta Pusako Rendah adalah harta hasil pencaharian sendiri oleh orang tua selama masa perkawinan. Berbeda dengan Pusako Tinggi, Pusako Rendah dapat diwariskan kepada anak kandung sesuai dengan ketentuan hukum Islam atau kesepakatan keluarga, yang seringkali memicu ketegangan antara hak kemenakan (berdasarkan adat matrilineal) dan hak anak (berdasarkan hukum nasional/Islam).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 9. Case ID: GS-0033

**Domain:** Minangkabau

**Skenario:** **Konflik Norma:** Terdapat perbedaan penafsiran bagian istri. NLA menyatakan istri mendapat ⅓ dari harta warisan (setelah pemisahan harta bersama), sementara ALA menyatakan istri mendapat ¼ dari harta warisan secara langsung. **Trade-off:** - **NLA** mengikuti logika pemisahan harta bersama terlebih dahulu (½ untuk istri), baru kemudian membagi warisan. Ini lebih detail namun kompleks. - **ALA** mengacu langsung pada Pasal 852 KUHPerdata untuk bagian tetap, lebih sederhana namun mungkin mengabaikan langkah pemisahan harta.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 10. Case ID: GS-0034

**Domain:** Minangkabau

**Skenario:** **Keputusan Pluralistik:** Kedua pendekatan sah dalam praktik hukum. **Langkah 1:** Pisahkan harta bersama. ½ untuk istri, ½ masuk warisan. **Langkah 2:** Bagi harta warisan (½ harta bersama + harta pribadi). **Menurut ALA/Pasal 852:** Istri ¼, dua anak ¾ (masing-masing ⅜). **Menurut NLA:** Istri ⅓, dua anak ⅔ (masing-masing ⅓). Dalam banyak putusan, pendekatan ALA (Pasal 852) lebih sering diterapkan langsung pada harta warisan setelah pemisahan. Konsultasi ahli diperlukan untuk kasus spesifik.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 11. Case ID: GS-0035

**Domain:** Minangkabau

**Skenario:** **Jawaban Final:** Hak atas pusako tinggi beralih kepada kemenakan (anak saudara perempuan mamak) sebagai ahli waris menurut garis matrilineal, bukan kepada anak kandung mamak. **Konflik & Trade-off:** - **Hukum Adat vs. Hukum Nasional (Warisan Individual):** Hukum adat menjaga keutuhan harta kolektif kaum (garis ibu), sedangkan hukum nasional cenderung pada warisan individual kepada anak kandung.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 12. Case ID: GS-0036

**Domain:** Minangkabau

**Skenario:** - **Trade-off:** Mengikuti adat mempertahankan identitas budaya dan stabilitas sosial kaum, tetapi berpotensi mengabaikan hubungan ekonomi langsung dengan anak kandung mamak. **Keputusan Pluralistik:** Dalam kerangka pluralisme hukum, keputusan harus mendahulukan hukum adat Minangkabau karena diakui secara nasional (sepanjang hidup dan tidak bertentangan hukum). Pusako tinggi adalah harta ulayat kolektif, sehingga mamak hanya pengelola. Ahli warisnya adalah kemenakan, sesuai sistem matrilineal.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 13. Case ID: GS-0037

**Domain:** Minangkabau

**Skenario:** Konflik norma terjadi antara hukum nasional (UU Perkawinan/KUHPerdata) yang mengutamakan anak kandung, dengan hukum adat matrilineal Minangkabau yang mengutamakan kemenakan untuk harta pusako. **Trade-off:** - Pilih hukum nasional: anak kandung menang, tetapi mengabaikan struktur sosial adat dan prinsip kekerabatan matrilineal. - Pilih hukum adat: kemenakan menang, tetapi mengesampingkan hak anak kandung berdasarkan undang-undang dan prinsip keadilan individual.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 14. Case ID: GS-0038

**Domain:** Minangkabau

**Skenario:** **Keputusan pluralistik:** Prioritas utama adalah **hukum nasional (UU Perkawinan 1974)** untuk harta pencaharian (*pusako rendah*), sehingga anak kandung adalah ahli waris utama. Namun, penyelesaian terbaik diawali dengan **musyawarah keluarga** untuk mencapai kesepakatan, mengakomodasi nilai adat secara sukarela (misal, pemberian sebagian kepada kemenakan). Jika musyawarah gagal, Pengadilan akan memutus berdasarkan hukum nasional.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 15. Case ID: GS-0039

**Domain:** Minangkabau

**Skenario:** **Sintesis Perbandingan:** Peran mamak dalam adat Minangkabau berpusat pada hubungan avunkular (paman-kemenakan) dan pengelolaan harta pusaka tinggi (kolektif, matrilineal). Hak anak dalam hukum nasional (KUHPerdata) berporos pada hubungan parental (orang tua-anak) dan pewarisan individual atas harta pencaharian orang tuanya.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 16. Case ID: GS-0040

**Domain:** Minangkabau

**Skenario:** **Konflik Norma & Trade-off:** Konflik muncul karena dua logika berbeda: adat menekankan kelangsungan *kaum* (kelompok matrilineal) melalui mamak, sementara hukum nasional menjamin hak individual anak atas orang tua kandungnya. Trade-off-nya antara stabilitas sistem kekerabatan kolektif (adat) dengan kepastian dan perlindungan hukum individual (nasional). **Keputusan Pluralistik:** Kedua sistem dapat berjalan paralel dengan mengakui ruang berlakunya masing-masing. Hukum nasional mengatur harta pencaharian (pusako rendah) untuk anak kandung.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 17. Case ID: GS-0041

**Domain:** Minangkabau

**Skenario:** Adat mengatur harta pusaka tinggi melalui mamak. Pendekatan ini menghormati otonomi hukum adat dalam lingkupnya sambil menjamin hak anak secara nasional.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 18. Case ID: GS-0007

**Domain:** Bali

**Skenario:** Hukum Adat Waris Bali: Sentana Rajeg dan Druwe Tengah Sistem kekerabatan masyarakat adat Bali bersifat patrilineal (kapurusa), di mana garis keturunan ditarik dari pihak laki-laki.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 19. Case ID: GS-0008

**Domain:** Bali

**Skenario:** Dalam sistem ini, anak laki-laki secara tradisional memiliki hak waris utama dan tanggung jawab keagamaan keluarga, seperti merawat orang tua, melaksanakan upacara pengabenan, dan memelihara sanggah/merajan keluarga.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 20. Case ID: GS-0009

**Domain:** Bali

**Skenario:** Sentana Rajeg: Jika sebuah keluarga tidak memiliki anak laki-laki, mereka dapat mengangkat seorang anak perempuan menjadi "sentana rajeg".

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 21. Case ID: GS-0010

**Domain:** Bali

**Skenario:** Status hukum anak perempuan tersebut ditingkatkan sehingga disamakan dengan anak laki-laki dalam hal pewarisan.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 22. Case ID: GS-0011

**Domain:** Bali

**Skenario:** Untuk melanjutkan keturunan, sentana rajeg biasanya melakukan perkawinan "nyentana" (atau "nyeburin"), di mana suaminya masuk ke dalam keluarga istri dan melepaskan hak waris di keluarga asalnya.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 23. Case ID: GS-0012

**Domain:** Bali

**Skenario:** Druwe Tengah: Hukum adat Bali mengenal konsep "druwe tengah" atau "duwe tengah", yaitu harta bersama keluarga atau kerabat yang tidak dibagi secara individual.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 24. Case ID: GS-0013

**Domain:** Bali

**Skenario:** Harta ini dikelola untuk kepentingan bersama, terutama pembiayaan upacara-upacara adat dan keagamaan (yadnya).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 25. Case ID: GS-0014

**Domain:** Bali

**Skenario:** Selain itu, terdapat "harta druwe gabro" yang merupakan harta yang diperoleh suami istri selama masa perkawinan.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 26. Case ID: GS-0027

**Domain:** Bali

**Skenario:** Hukum Adat Waris Bali: Sentana Rajeg dan Druwe Tengah Sistem kekerabatan masyarakat adat Bali bersifat patrilineal (kapurusa), di mana garis keturunan ditarik dari pihak laki-laki. Dalam sistem ini, anak laki-laki secara tradisional memiliki hak waris utama dan tanggung jawab keagamaan keluarga, seperti merawat orang tua, melaksanakan upacara pengabenan, dan memelihara sanggah/merajan keluarga. Sentana Rajeg: Jika sebuah keluarga tidak memiliki anak laki-laki, mereka dapat mengangkat seorang anak perempuan menjadi "sentana rajeg".

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 27. Case ID: GS-0028

**Domain:** Bali

**Skenario:** Status hukum anak perempuan tersebut ditingkatkan sehingga disamakan dengan anak laki-laki dalam hal pewarisan. Untuk melanjutkan keturunan, sentana rajeg biasanya melakukan perkawinan "nyentana" (atau "nyeburin"), di mana suaminya masuk ke dalam keluarga istri dan melepaskan hak waris di keluarga asalnya. Druwe Tengah: Hukum adat Bali mengenal konsep "druwe tengah" atau "duwe tengah", yaitu harta bersama keluarga atau kerabat yang tidak dibagi secara individual.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 28. Case ID: GS-0029

**Domain:** Bali

**Skenario:** Harta ini dikelola untuk kepentingan bersama, terutama pembiayaan upacara-upacara adat dan keagamaan (yadnya). Selain itu, terdapat "harta druwe gabro" yang merupakan harta yang diperoleh suami istri selama masa perkawinan.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 29. Case ID: GS-0045

**Domain:** Bali

**Skenario:** **Jawaban Final:** Dalam adat Bali, **sentana** adalah anak angkat yang diangkat untuk melanjutkan keturunan dan memelihara orang tua, terutama dalam keluarga tanpa anak laki-laki kandung. Posisinya dalam pewarisan menunjukkan **konflik norma** antara hukum adat dan hukum nasional (KUHPerdata). **Trade-off:** - **Hukum Adat Bali:** Mengakui sentana sebagai ahli waris utama orang tua angkat, khususnya untuk harta pencaharian (*gono-gini*). Penyelesaian sengketa di masyarakat adat cenderung mengikuti ini.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 30. Case ID: GS-0046

**Domain:** Bali

**Skenario:** - **KUHPerdata:** Anak angkat bukan ahli waris berdasarkan keturunan; hak waris hanya dapat diberikan melalui wasiat, memberikan kepastian hukum formal tetapi mengabaikan konteks sosial-budaya. **Keputusan Pluralistik:** Penyelesaian harus mempertimbangkan **komunitas hukum** si pewaris. Bagi masyarakat Bali yang masih memegang adat, hukum adat Bali seharusnya menjadi pedoman utama. Untuk mengantisipasi konflik dengan sistem nasional, disarankan melakukan pengangkatan secara resmi melalui penetapan pengadilan dan dibuatkan wasiat.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 31. Case ID: GS-0048

**Domain:** Bali

**Skenario:** **Konflik Norma:** Terjadi benturan antara penafsiran hukum adat baru yang lebih egaliter (MDP Bali 2010) yang mengakui hak perempuan, dengan hukum adat patrilineal tradisional Bali yang membatasi hak waris pada garis laki-laki. **Trade-off:** Di satu sisi, prinsip kesetaraan gender dan keadilan individu (didukung MDP 2010). Di sisi lain, kelestarian sistem kekerabatan adat dan kepastian hukum tradisional yang menjaga tanah sebagai harta turun-temurun (*druwe*).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 32. Case ID: GS-0049

**Domain:** Bali

**Skenario:** **Prioritas** adalah penyelesaian melalui **musyawarah di Desa Pakraman** dengan merujuk pada MDP 2010 dan *awig-awig*. **Sifat tanah** menjadi penentu kunci: jika merupakan **harta bersama (*gono-gini*)**, tuntutan perempuan lebih kuat. Jika **harta warisan turun-temurun (*druwe*)**, norma patrilineal tradisional lebih dominan. Jika musyawarah gagal, pengadilan akan memeriksa keabsahan MDP 2010, sifat tanah, dan prinsip keadilan, dengan KUHPerdata sebagai pembanding subsidiair.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 33. Case ID: GS-0102

**Domain:** Bali

**Skenario:** # Analisis Hukum: Makna "Sentana" dan Posisinya dalam Pewarisan Keluarga Bali Sebagai Hakim Supervisor dalam pluralisme hukum, saya akan menganalisis pertanyaan ini dengan mensintesis perspektif **hukum nasional (KUHPerdata)** dan **hukum adat Bali**, serta mengakui konflik norma yang ada beserta solusi pluralistiknya.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 34. Case ID: GS-0103

**Domain:** Bali

**Skenario:** MAKNA "SENTANA" DALAM ADAT BALI** **Sentana** (dari bahasa Sanskerta: *santāna* = keturunan) dalam adat Bali merujuk pada **ahli waris utama** yang bertanggung jawab melanjutkan garis keturunan (*purusa*) dan pelaksanaan upacara keagamaan keluarga (Hindu Bali). **Sentana laki-laki** (*purusa*) adalah penerus utama garis keluarga 2. **Sentana putri** diakui dalam kondisi tertentu (ketiadaan anak laki-laki) 3. Sistem ini bersifat **patrilineal** dengan variasi lokal (*desa, kala, patra*) ## **II.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 35. Case ID: GS-0015

**Domain:** Jawa

**Skenario:** Hukum Adat Waris Jawa: Gono-Gini dan Kekerabatan Bilateral Masyarakat Jawa menganut sistem kekerabatan bilateral atau parental.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 36. Case ID: GS-0016

**Domain:** Jawa

**Skenario:** Dalam sistem ini, garis keturunan ditarik dari pihak ayah dan ibu secara seimbang.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 37. Case ID: GS-0017

**Domain:** Jawa

**Skenario:** Kedudukan anak laki-laki dan anak perempuan dalam hukum waris adat pada dasarnya adalah sama atau sederajat sebagai ahli waris dari harta peninggalan orang tua.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 38. Case ID: GS-0018

**Domain:** Jawa

**Skenario:** Harta Gono-Gini dan Harta Bawaan: Hukum adat Jawa membedakan antara "harta gono-gini" dan "harta bawaan".

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 39. Case ID: GS-0019

**Domain:** Jawa

**Skenario:** Harta gono-gini (harta bersama) adalah harta yang diperoleh suami dan istri selama masa perkawinan.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 40. Case ID: GS-0020

**Domain:** Jawa

**Skenario:** Jika terjadi perceraian atau kematian, masing-masing pihak biasanya berhak atas separuh dari harta gono-gini.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 41. Case ID: GS-0021

**Domain:** Jawa

**Skenario:** Sementara itu, "harta bawaan" (harta asal) adalah harta yang dimiliki masing-masing pihak sebelum perkawinan berlangsung atau diperoleh secara pribadi (misal dari warisan leluhur mereka sendiri).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 42. Case ID: GS-0022

**Domain:** Jawa

**Skenario:** Prinsip Pembagian: Meskipun menganut asas bilateral, dalam praktiknya sering ditemukan prinsip "sepikul segendongan", terutama di daerah yang kuat pengaruh hukum Islamnya.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 43. Case ID: GS-0023

**Domain:** Jawa

**Skenario:** Prinsip ini memberikan bagian dua untuk laki-laki dan satu untuk perempuan.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 44. Case ID: GS-0024

**Domain:** Jawa

**Skenario:** Namun, nilai utama dalam pembagian waris Jawa adalah "rukun" (harmoni) yang dicapai melalui musyawarah mufakat, di mana pembagian dapat disesuaikan berdasarkan kebutuhan dan pengabdian masing-masing ahli waris kepada orang tua.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 45. Case ID: GS-0030

**Domain:** Jawa

**Skenario:** Hukum Adat Waris Jawa: Gono-Gini dan Kekerabatan Bilateral Masyarakat Jawa menganut sistem kekerabatan bilateral atau parental. Dalam sistem ini, garis keturunan ditarik dari pihak ayah dan ibu secara seimbang. Kedudukan anak laki-laki dan anak perempuan dalam hukum waris adat pada dasarnya adalah sama atau sederajat sebagai ahli waris dari harta peninggalan orang tua. Harta Gono-Gini dan Harta Bawaan: Hukum adat Jawa membedakan antara "harta gono-gini" dan "harta bawaan".

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 46. Case ID: GS-0031

**Domain:** Jawa

**Skenario:** Harta gono-gini (harta bersama) adalah harta yang diperoleh suami dan istri selama masa perkawinan. Jika terjadi perceraian atau kematian, masing-masing pihak biasanya berhak atas separuh dari harta gono-gini. Sementara itu, "harta bawaan" (harta asal) adalah harta yang dimiliki masing-masing pihak sebelum perkawinan berlangsung atau diperoleh secara pribadi (misal dari warisan leluhur mereka sendiri).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 47. Case ID: GS-0032

**Domain:** Jawa

**Skenario:** Prinsip Pembagian: Meskipun menganut asas bilateral, dalam praktiknya sering ditemukan prinsip "sepikul segendongan", terutama di daerah yang kuat pengaruh hukum Islamnya. Prinsip ini memberikan bagian dua untuk laki-laki dan satu untuk perempuan. Namun, nilai utama dalam pembagian waris Jawa adalah "rukun" (harmoni) yang dicapai melalui musyawarah mufakat, di mana pembagian dapat disesuaikan berdasarkan kebutuhan dan pengabdian masing-masing ahli waris kepada orang tua.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 48. Case ID: GS-0042

**Domain:** Jawa

**Skenario:** **Jawaban Final:** Syarat sah perjanjian menurut Pasal 1320 KUHPerdata adalah: (1) kesepakatan, (2) kecakapan, (3) objek tertentu, dan (4) kausa yang halal. Dampak ketidakpenuhannya dibedakan: pelanggaran syarat subjektif (1 & 2) membuat perjanjian **dapat dibatalkan** (voidable), sedangkan pelanggaran syarat objektif (3 & 4) membuatnya **batal demi hukum** (null void).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 49. Case ID: GS-0054

**Domain:** Jawa

**Skenario:** **Jawaban Final:** Konsep gono-gini (harta bersama perkawinan) dan harta bawaan (harta pribadi) dalam adat Jawa diakui secara hukum nasional (UU Perkawinan) dan adat. Namun, konteks yang diberikan hanya menjelaskan sistem pewarisan adat Minangkabau, bukan Jawa. **Konflik & Trade-off:** Terdapat ketegangan antara klaim NLA (yang menjelaskan hukum Jawa berdasarkan pengetahuan umum) dan ALA (yang menolak menjawab karena konteks tidak relevan).

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

### 50. Case ID: GS-0055

**Domain:** Jawa

**Skenario:** Trade-off-nya adalah antara memberikan informasi umum yang diakui secara hukum versus berpegang ketat pada sumber konteks yang tersedia. **Keputusan Pluralistik:** Dalam pluralisme hukum, pengadilan akan mengakui dan menerapkan hukum adat Jawa (gono-gini dan harta bawaan) selama tidak bertentangan dengan hukum nasional. Namun, untuk analisis spesifik, diperlukan konsultasi dengan ahli atau tetua adat Jawa dan pembuktian di pengadilan, karena konteks yang diberikan tidak memadai.

| Label (A/B/C/D) | Confidence (Tinggi/Sedang/Rendah) | Alasan | Referensi Hukum |
|---|---|---|---|
| | | | |

## Pengesahan

- Nama: ________________________________
- Tanda Tangan: ________________________
- Tanggal Pengisian: ____________________
