# Handoff: Completion of ART-092 (Router-Augmented Adjudicator)

**Tanggal:** 2026-02-09
**Dari:** Agent #5
**Ke:** Agent #6 / Human Engineer
**Status Milestone:** Sprint 2 (Structural Fixes) - ON TRACK

## 1. Konteks Terakhir
Saya telah menyelesaikan implementasi **ART-092**, yaitu integrasi hasil klasifikasi Router sebagai *default position* pada Orchestrator. Tujuannya adalah mengurangi *False Positive* label C (Konflik) yang berlebihan pada iterasi sebelumnya.

Namun, selama verifikasi, ditemukan masalah baru (**F-012**): Router kadang salah mengklasifikasikan kasus berlabel Nasional/Konflik sebagai "Pure Adat" karena bias terminologi.

**Solusi yang diterapkan:**
Saya menambahkan **Keyword Safety Net** di `src/agents/orchestrator.py`. Jika Router bilang "Adat", tapi ada kata kunci nasional keras (SHM, Poligami, Cerai), Orchestrator mendapat *System Warning* keras.

## 2. Perubahan Kunci
- **`src/agents/orchestrator.py`**:
    - Support parameter `route_label` di `build_parallel_orchestrator`.
    - Logika `default_position` di `_supervisor_agent`.
    - **Safety Net Logic**: Deteksi keyword nasional saat route=adat.
- **`src/pipeline/nusantara_agent.py`**:
    - Pass `route_label` dari `process_query` ke orchestrator.
- **`experiments/art092_verification.py`**:
    - Script verifikasi baru untuk 5 kasus kritis.

## 3. Status Verifikasi
Verifikasi dilakukan pada 5 sampel kasus kritis (Sample Test):
- **Akurasi:** 100% (5/5).
- **Critical Wins:**
    - Kasus SHM vs Ulayat (CS-MIN-011) sekarang benar terdeteksi sebagai C (Konflik).
    - Kasus Adat vs MDP (CS-BAL-002) sekarang benar terdeteksi sebagai C (Konflik).

## 4. Asumsi Aktif
- **Keyword List:** Daftar keyword nasional (`shm`, `sertifikat`, `poligami`, `cerai`, `pengadilan`) dianggap cukup untuk saat ini sebagai safety net, tapi mungkin perlu diperluas di masa depan.
- **Router Confidence:** Kita berasumsi Router *umumnya* benar, kecuali ada indikator keras sebaliknya.

## 5. Risiko yang Diketahui
- **Keyword Fragility:** Safety net berbasis keyword rentan terhadap variasi kata (misal "surat tanah" vs "sertifikat"). Perlu semantic check yang lebih robust di masa depan jika error muncul lagi.
- **Over-correction:** Warning yang terlalu agresif bisa membuat Orchestrator paranoid dan kembali ke bias konflik. Perlu monitoring di ART-093.

## 6. Langkah Berikutnya (Rekomendasi)
Tugas Anda selanjutnya adalah **ART-093: Knowledge Base Expansion (National Law)**.
1.  Jalankan benchmark penuh (82 kasus) menggunakan `experiments/09_ablation_study/run_bench_gs82.py` untuk melihat dampak global perubahan ini.
2.  Perkaya `InMemoryVectorRetriever` di `nusantara_agent.py` dengan pasal-pasal KUHPerdata/KHI yang lebih lengkap agar agen nasional bisa berargumen lebih kuat (saat ini kalah debat karena miskin referensi).

## 7. Prompt untuk Agent Selanjutnya
```text
Lanjutkan pekerjaan ke ART-093. Konteks: ART-092 (Router integration) sudah selesai dan diverifikasi pada sampel kritis dengan hasil 100%. Safety net keyword sudah aktif di orchestrator.py untuk menangani router errors.

Tugas Anda sekarang:
1. Jalankan benchmark penuh (82 kasus) untuk baseline baru.
2. Implementasikan ART-093: Perluas knowledge base hukum nasional di src/pipeline/nusantara_agent.py (tambahkan pasal KUHPerdata/KHI/UU relevan).
3. Pastikan retrieval agen nasional meningkat kualitasnya.
```
