# REVIEW — Experiment 07: Advanced Orchestration

Catatan: Dokumen ini diisi setelah eksekusi eksperimen. Semua jawaban merujuk pada output di `experiments/07_advanced_orchestration/` dan auto-score Kimi.

## Q1: Apakah hasilnya circular?

**Jawaban:** Evaluasi ini mengurangi circularity karena output sistem (DeepSeek) dinilai oleh evaluator independen (Kimi). Namun, circularity tidak hilang sepenuhnya karena Kimi tetap LLM yang menilai LLM, sehingga ada risiko bias model terhadap gaya jawaban tertentu. Selain itu, sistem menghasilkan jawaban menggunakan konteks dan prompt yang dirancang oleh tim yang sama sehingga masih ada potensi confirmation bias pada pemilihan query. Tidak ada human annotation atau ground truth eksternal yang membatasi overfitting terhadap prompt. Dengan demikian, hasil ini bersifat semi-independen, tetapi belum memenuhi standar evaluasi independen penuh seperti yang disyaratkan di Exp 06. Evaluator independen hanya satu model, sehingga tidak ada triangulasi antar evaluator. Jika Kimi memiliki preferensi terhadap jawaban ringkas atau pola tertentu, skor akan mencerminkan preferensi tersebut. Untuk mengurangi circularity lebih lanjut, perlu evaluator manusia dan/atau model tambahan (Claude/OpenAI) serta ground truth eksternal. Pada saat ini, hasil auto-score berguna sebagai sinyal awal tetapi tidak dapat dijadikan satu-satunya dasar klaim ilmiah.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Jalankan Exp 06 (human annotation + LLM judge independen ganda), tambah evaluator kedua (Claude/OpenAI), dan gunakan subset ground truth eksternal.

**Status mitigasi:** BELUM

## Q2: Apakah baseline-nya fair?

**Jawaban:** Baseline yang digunakan adalah Exp 03 (sequential pipeline) dengan prompt dan data yang sama, dijalankan ulang pada set query yang identik. Ini menjadikan baseline cukup fair karena arsitektur hanya berbeda pada orchestration (debate + self-correction vs sequential). Tidak ada upaya melemahkan baseline; justru baseline menunjukkan skor lebih tinggi pada semua metrik menurut evaluator Kimi. Namun baseline masih berupa internal baseline, belum dibandingkan dengan sistem eksternal (misal RAG legal lain atau model LLM top dengan prompt sederhana). Jadi fairness internal cukup baik untuk klaim perbandingan antar varian sistem, tetapi fairness eksternal terhadap state-of-the-art belum terpenuhi. Ini sesuai scope Exp 07 yang fokus pada perubahan orchestration, bukan perbandingan terhadap sistem luar. Dengan demikian baseline adil untuk hipotesis internal, tetapi belum cukup untuk klaim superioritas atas sistem lain. Untuk paper, klaim harus dibatasi pada perbandingan internal sampai baseline eksternal tersedia di Exp 09.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Implementasikan baseline eksternal di Exp 09 (GPT-4/Claude + simple prompt, vector-only, graph-only, human expert baseline).

**Status mitigasi:** BELUM

## Q3: Apakah skala datanya cukup untuk klaim yang dibuat?

**Jawaban:** Skala data belum cukup untuk klaim statistik kuat. Eksperimen menggunakan 12 query yang disusun manual untuk test awal. Ini hanya memberi indikasi awal, tidak memadai untuk generalisasi dan signifikansi statistik. Dengan N=12, variansi tinggi dan hasil sensitif terhadap pemilihan query. Hasil saat ini tidak dapat dijadikan bukti robust bahwa advanced orchestration lebih baik atau lebih buruk secara umum. Ini juga menyebabkan kekuatan statistik rendah untuk mendeteksi efek kecil. Skala ini mungkin cukup untuk debugging pipeline dan menemukan failure mode (misal debat mengurangi completeness), tetapi tidak untuk klaim performa di paper. Selain itu, belum ada diversifikasi domain yang cukup luas; meski query mencakup national/adat/conflict/consensus, itu masih terbatas. Dengan kata lain, skala ini hanya memenuhi tujuan eksplorasi internal. Untuk klaim publikasi, perlu 200+ test cases sesuai roadmap dan evaluasi human untuk memperkuat validitas. Kesimpulannya: skala belum memadai untuk klaim ilmiah, hanya memadai untuk iterasi internal.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Tambah 20–30 query segera, lanjut ke 200 query sesuai ART-050, lalu ulang evaluasi dengan baseline dan statistik.

**Status mitigasi:** BELUM

## Q4: Apakah klaim "neuro-symbolic" genuinely earned?

**Jawaban:** Eksperimen ini tidak mengevaluasi komponen neuro-symbolic secara langsung. Advanced orchestration berfokus pada debate dan self-correction antar agent, bukan pada rule engine atau reasoning simbolik. Jadi hasil Exp 07 tidak dapat digunakan untuk memperkuat klaim neuro-symbolic. Klaim neuro-symbolic harus didukung oleh Exp 05 (rule engine) dan integrasi ke pipeline, serta pembandingan sistem dengan/ tanpa rule engine. Pada saat ini, Exp 07 hanya menguji apakah orchestrasi agentic menambah nilai di atas sequential chain. Dengan demikian, klaim neuro-symbolic tidak earned oleh Exp 07 dan harus dipisahkan secara eksplisit dalam narasi paper. Menggabungkan hasil Exp 07 sebagai bukti neuro-symbolic akan dianggap overclaim. Untuk memenuhi klaim tersebut, perlu integrasi rule engine ke pipeline (ART-049) dan evaluasi ablation (Exp 09). Jadi, Exp 07 tidak memberikan kontribusi langsung ke klaim neuro-symbolic, hanya ke klaim agentic orchestration.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Tegaskan bahwa Exp 07 hanya menguji orchestrasi; klaim neuro-symbolic didukung oleh Exp 05 dan Exp 09.

**Status mitigasi:** BELUM

## Q5: Apakah novelty-nya real?

**Jawaban:** Novelty yang diharapkan adalah kombinasi multi-agent debate, self-correction, dan routing untuk penalaran hukum pluralistik Indonesia. Namun, pada skala ini, novelty masih lemah karena debat tidak meningkatkan kualitas; hasilnya bahkan lebih buruk daripada baseline. Ini menimbulkan pertanyaan apakah novelty benar-benar berdampak atau hanya variasi arsitektur tanpa manfaat empiris. Novelty masih bisa diklaim sebagai desain eksperimen dan eksplorasi agentic patterns dalam konteks hukum pluralistik, tetapi harus diakui bahwa evidence belum mendukung klaim keunggulan. Selain itu, jika kita menghapus domain Indonesia, pola debat dan self-correction mirip dengan literatur agentic RAG umum. Jadi novelty substantif harus datang dari kombinasi dengan knowledge graph adat, rule engine, dan evaluasi budaya. Exp 07 sendiri belum memberikan novelty yang kuat secara empiris. Untuk menjaga integritas, novelty harus dijelaskan sebagai eksplorasi desain yang belum terbukti meningkatkan metrik, dan diarahkan sebagai temuan negatif yang informatif.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Laporkan hasil negatif secara eksplisit dan posisikan sebagai evidence bahwa debate tidak otomatis meningkatkan kualitas tanpa evidence retrieval tambahan.

**Status mitigasi:** SEDANG DIKERJAKAN

## Q6: Apa yang bisa dilakukan sistem ini yang TIDAK bisa dilakukan oleh GPT-4 + simple prompt?

**Jawaban:** Pada hasil saat ini, belum ada bukti kuat bahwa advanced orchestration memberikan kemampuan yang tidak bisa dicapai oleh GPT-4 dengan prompt sederhana. Debate dan self-correction diharapkan menambah robustness, tetapi skor Kimi menunjukkan penurunan kualitas. Ini berarti perbedaan kemampuan belum terbukti. Namun, sistem menyediakan struktur traceability berupa log debat, klaim, dan kritik yang dapat diaudit. Ini adalah nilai tambah yang tidak mudah diperoleh dari single prompt tanpa instruksi tambahan dan tooling. Dengan log, kita bisa melacak kritik, menilai evidence gap, dan membangun pipeline evaluasi lebih formal. Tetapi untuk pengguna akhir, output final tidak menunjukkan keunggulan kuantitatif. Jadi, klaim keunggulan fungsional harus ditahan sampai ada bukti bahwa log debat dan self-correction menghasilkan jawaban yang lebih akurat atau lebih faithful. Untuk saat ini, keunggulan utama adalah traceability dan auditability, bukan kualitas jawaban.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Ukur manfaat traceability secara kuantitatif (misal error diagnosis rate) dan bandingkan dengan baseline LLM sederhana.

**Status mitigasi:** BELUM

## Q7: Apakah metrik evaluasi valid dan accepted di komunitas?

**Jawaban:** Metrik yang digunakan adalah rubric internal 0–5 untuk accuracy, completeness, cultural sensitivity, kemudian auto-score oleh Kimi. Metrik ini belum divalidasi secara akademik dan belum memiliki inter-rater reliability. Ini berarti validitasnya masih lemah. Walau rubric sederhana membantu konsistensi internal, tanpa human annotator dan tanpa correlation dengan metrik accepted (misal RAGAS), hasil tidak bisa dianggap valid secara komunitas. Kimi sebagai evaluator juga belum terbukti reliable terhadap rubric ini. Jadi metrik saat ini hanya cocok untuk exploratory iteration, bukan untuk klaim final. Untuk mencapai validitas, perlu Exp 06 (human annotation), dan Exp 10 (CCS validation) untuk cultural sensitivity. Selain itu, perlu menunjukkan korelasi dengan metrik lain dan stability across evaluators. Sampai itu dilakukan, metrik ini bersifat ad-hoc dan tidak bisa dijadikan dasar klaim utama.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Jalankan Exp 06 (human annotation + LLM judge), laporkan inter-rater reliability, dan triangulate dengan metrik standar.

**Status mitigasi:** BELUM

## Q8: Bisakah hasilnya direproduksi oleh lab lain?

**Jawaban:** Dari sisi kode dan data, eksperimen ini cukup reproducible: semua script, queries, dan output disimpan di repository. Hasil dapat direproduksi jika lab lain memiliki akses ke DeepSeek API dan Kimi API. Namun, reproducibility dibatasi oleh ketergantungan pada API komersial dan perubahan model/price. Tanpa akses API yang sama, hasil numerik bisa berbeda. Selain itu, variabilitas LLM dapat mempengaruhi hasil jika tidak dikontrol dengan seed atau deterministic settings. Script ini tidak menggunakan seed atau temperature control yang ketat. Jadi reproducibility relatif terbatas. Untuk memperbaiki, perlu menambahkan konfigurasi deterministic jika tersedia, serta dokumentasi environment (dependency versions sudah tercantum). Untuk sekarang, reproducibility partial: pipeline dan struktur bisa direplikasi, tetapi hasil angka tidak dijamin identik.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Tambah logging parameter model, temperature, dan prompt versi; simpan snapshot output; dokumentasikan dependency dan API.

**Status mitigasi:** SEDANG DIKERJAKAN

## Q9: Apakah ada selection bias dalam pemilihan test cases?

**Jawaban:** Ada potensi selection bias karena test_queries.json disusun manual oleh tim dan hanya berisi 12 query. Pemilihan query tidak acak dan belum diverifikasi representatif terhadap domain hukum pluralistik Indonesia. Query mungkin cenderung pada kasus yang mudah dijawab atau sesuai dengan prompt, meskipun hasil saat ini justru menunjukkan kegagalan. Bias tetap ada karena jumlah kecil dan tidak ada sampling method yang sistematik. Selain itu, domain Bali dan Jawa hanya sedikit disebut, sehingga distribusi domain tidak seimbang. Jadi hasil ini tidak bisa digeneralisasi. Untuk mengurangi bias, perlu menambah query secara sistematik dari corpus dan memisahkan train/dev/test queries, atau menggunakan prosedur sampling dari teks nyata. Pada tahap ini, selection bias harus diakui sebagai limitation. Hasil eksperimen hanya bisa dianggap exploratory.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Tambahkan 20–30 query tambahan secara sistematik, lalu 200 query sesuai ART-050 dengan distribusi domain seimbang.

**Status mitigasi:** BELUM

## Q10: Apa yang TIDAK bisa dilakukan sistem ini?

**Jawaban:** Sistem ini tidak dapat memberikan keputusan hukum yang valid secara yuridis dan tidak menggantikan peran ahli hukum. Sistem juga tidak dapat menjamin kesesuaian dengan praktik peradilan aktual karena belum menggunakan putusan MA sebagai ground truth. Selain itu, sistem tidak mampu menangani ambiguitas sosial secara penuh: aturan adat sering bergantung pada musyawarah dan konteks lokal yang tidak tercakup dalam rules atau knowledge graph saat ini. Pada eksperimen ini, debat antar agent juga tidak otomatis meningkatkan kualitas jawaban; jadi sistem tidak bisa menjamin bahwa struktur debat menghasilkan output yang lebih baik. Sistem juga tidak dapat mengukur cultural sensitivity secara valid tanpa human annotation. Dengan kata lain, kemampuan sistem terbatas pada memberikan ringkasan pluralistik berbasis prompt dan context yang tersedia. Tanpa scaling data dan evaluasi independen, kemampuan sistem tetap terbatas sebagai prototype penelitian. Ini harus dijelaskan sebagai limitation dalam paper, bukan disamarkan sebagai produk siap pakai.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Tegaskan limitations di paper, jalankan Exp 06/09/10 untuk memperkuat validitas, dan perluas KG serta test cases.

**Status mitigasi:** SEDANG DIKERJAKAN

---

## Layer 2: Adversarial AI Review

Belum dijalankan. Setelah tersedia, ringkasan akan ditambahkan dari `experiments/07_advanced_orchestration/ai_review.json`.

## Layer 3: Human Review Gate

**Keputusan:** FAIL (sementara)  
**Alasan:** Tidak memenuhi acceptance criteria; evaluasi human belum ada.  
**Reviewer:** AI Agent (Codex)  
**Tanggal:** 2026-02-07
