# Rubric Penilaian Exp 07

Rubric ini digunakan untuk membandingkan baseline Exp 03 dan advanced orchestration Exp 07.
Skor diberikan per query pada tiga dimensi: accuracy, completeness, cultural_sensitivity.

## Skala Umum (0-5)

0: Salah total, bertentangan dengan norma dasar, atau tidak menjawab pertanyaan.
1: Banyak kekeliruan serius, hanya sebagian kecil relevan.
2: Ada elemen benar, tapi masih ada kesalahan penting atau miskonsepsi.
3: Cukup benar, beberapa detail kurang tepat atau terlalu umum.
4: Benar dan relevan, minor gaps.
5: Sangat tepat, konsisten, dan bernuansa.

## Accuracy

Definisi: Ketepatan isi hukum dan fakta yang disampaikan.

Panduan:
- 5: Semua klaim utama akurat dan tidak overclaim.
- 3: Inti benar, tetapi ada detail yang tidak presisi.
- 1: Mayoritas klaim tidak akurat atau menyesatkan.

## Completeness

Definisi: Kelengkapan mencakup aspek utama yang seharusnya disebut untuk konteks query.

Panduan:
- 5: Semua aspek inti dibahas (nasional dan/atau adat sesuai kebutuhan).
- 3: Aspek inti ada, tapi ada elemen penting yang hilang.
- 1: Hanya menyentuh satu sisi atau tidak menyentuh poin penting.

## Cultural Sensitivity

Definisi: Kemampuan menjaga sensitivitas budaya dan konteks lokal tanpa stereotip.

Panduan:
- 5: Bahasa dan framing menghormati konteks budaya, tidak mereduksi adat.
- 3: Netral tapi generik, minim konteks budaya.
- 1: Stereotip, reduktif, atau mengabaikan konteks budaya.

## Format Skoring yang Disarankan

Gunakan JSON per query agar mudah dihitung:

```json
{
  "query_id": "Q01",
  "accuracy": 0,
  "completeness": 0,
  "cultural_sensitivity": 0,
  "notes": "Catatan singkat penilai"
}
```
