# Panduan Annotasi Ground Truth Nusantara-Agent

Dokumen ini mendefinisikan standar operasional untuk annotator manusia dalam membangun *gold standard* Knowledge Graph (KG) untuk hukum pluralistik Indonesia (Minangkabau, Bali, Jawa, dan Nasional).

## 1. Definisi Tripel

Setiap pengetahuan direpresentasikan sebagai tripel: `(head, relation, tail)`.

- **Head**: Subjek atau entitas hukum (misal: "Kemenakan", "Harta Pusako Tinggi").
- **Relation**: Hubungan fungsional atau predikat hukum (misal: "mewarisi", "dikelola_oleh"). Gunakan *snake_case*.
- **Tail**: Objek, entitas lain, atau nilai (misal: "Mamak Kepala Waris", "Garis Matrilineal").
- **Category**: Kategori hukum (misal: "Warisan", "Tanah", "Otoritas", "Status").
- **Confidence**: Selalu set ke `1.0` untuk annotasi manusia (karena dianggap sebagai kebenaran mutlak/gold standard).

## 2. Kriteria Kualitas

### A. Kebenaran Faktual (Factual Correctness)
- Tripel harus setia pada teks sumber.
- Jangan menambahkan informasi yang tidak ada di teks kecuali merupakan pengetahuan umum hukum adat yang sangat mendasar (dan beri catatan jika demikian).

### B. Nuansa Budaya (Cultural Nuance)
- Gunakan terminologi asli daerah jika tersedia dalam teks (misal: "Harta Pusako Tinggi" lebih baik daripada "Warisan Keluarga Besar").
- Pastikan relasi mencerminkan logika hukum adat (misal: hubungan antara `Kemenakan` dan `Mamak` dalam Minangkabau bukan sekadar paman-keponakan biasa, tapi hubungan otoritas waris).

### C. Granularitas
- Hindari kalimat panjang dalam `head` atau `tail`. Pecah menjadi konsep atomik.
- Contoh Buruk: `(Kemenakan laki-laki yang sudah dewasa, berhak mengelola, sawah warisan dari garis ibu)`
- Contoh Baik: `(Kemenakan Laki-laki, mengelola, Sawah Warisan)`, `(Sawah Warisan, jenis, Harta Pusako Tinggi)`

## 3. Penanganan Ambiguitas

Jika teks bersifat ambigu:
1. **Prioritas Teks**: Ikuti interpretasi yang paling eksplisit di teks.
2. **Konteks Hukum**: Jika teks tidak jelas tapi konteks hukum adatnya baku, gunakan standar hukum adat yang berlaku.
3. **Catatan**: Jika tetap ragu, beri label `ambiguous` pada kolom komentar (jika ada) atau diskusikan di rapat sinkronisasi.

## 4. Skema Kategori

| Kategori | Deskripsi |
|----------|-----------|
| `Warisan` | Segala hal terkait perpindahan kepemilikan atau hak guna setelah kematian. |
| `Tanah` | Terkait lahan, sawah, hutan, dan properti tidak bergerak. |
| `Otoritas` | Terkait peran (Mamak, Penghulu, Raja) dan kewenangannya. |
| `Status` | Terkait hubungan kekeluargaan, garis keturunan, dan strata sosial. |
| `Prosedur` | Terkait langkah-langkah formal dalam penyelesaian sengketa atau upacara. |

## 5. Alur Annotasi

1. Baca paragraf secara utuh.
2. Identifikasi entitas utama (Head).
3. Identifikasi hubungan (Relation) dengan entitas lain (Tail).
4. Klasifikasikan ke dalam kategori.
5. Review ulang: "Apakah tripel ini cukup untuk membangun kembali makna asli paragraf tersebut?"

## 6. Scoring Partial Match (Untuk Evaluasi)

Dalam mengevaluasi AI terhadap Gold Standard:
- **Perfect Match (1.0)**: Head, Relation, dan Tail sama secara semantik.
- **Near Match (0.75)**: Head dan Tail sama, Relation memiliki sinonim yang tepat.
- **Partial Match (0.5)**: Head dan Tail benar, tapi Relation terlalu umum atau sedikit meleset.
- **Miss (0.0)**: Salah satu dari Head atau Tail salah secara fatal.
