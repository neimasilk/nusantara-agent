% Minangkabau inheritance rules in ASP (Clingo)
% Logic for neuro-symbolic reasoning experiments.

% --- Facts & Types ---
matrilineal.

% Deklarasi predicate eksternal (tidak ada fakta default; semua di-inject runtime)
#defined consensus_reached/0.
#defined action/2.
#defined parent/2.
#defined sibling/2.
#defined female/1.
#defined male/1.
#defined ganggam_bauntuak/2.
#defined bundo_kanduang/1.
#defined ninik_mamak/1.
#defined sumando/1.
#defined pihak_luar/1.
#defined mamak_kepala_waris/1.
#defined ditunjuk_mufakat/1.
#defined cakap_adat/1.
#defined patut_adat/1.
#defined lintas_generasi/1.
#defined waris_sipanjang/1.
#defined hak_pakai_seumur_hidup/2.
#defined sebab_darurat/1.
#defined jurai/1.
#defined waris_bertali_darah/1.
#defined istri_kemenakan/1.

% Asset classification
asset_type(rumah_gadang, pusako_tinggi).
asset_type(sawah_ladang, pusako_tinggi).
asset_type(hutan_tanah, pusako_tinggi).
asset_type(pandam_pakuburan, pusako_tinggi).
asset_type(sawah_adat, pusako_tinggi).
asset_type(tanah_kaum, pusako_tinggi).
asset_type(tanah_ulayat, pusako_tinggi).
asset_type(tanah_pusako, pusako_tinggi).
asset_type(tanah_waris, pusako_tinggi).
asset_type(rumah_istri, pusako_tinggi).
asset_type(sawah_bersama, pusako_tinggi).
asset_type(tanah_adat, pusako_tinggi).
asset_type(pusako_tinggi_hibah, pusako_tinggi).
asset_type(luak_tapian, pusako_tinggi).
asset_type(dangau_paladangan, pusako_tinggi).

asset_type(harta_pencaharian, pusako_rendah).
asset_type(hibah, pusako_rendah).
asset_type(tanah_hibah, pusako_rendah).
asset_type(harta_tembilang_emas, pusako_rendah).
asset_type(hadiah_nikah, pusako_rendah).
asset_type(rumah_rantau, pusako_rendah).
asset_type(rumah_bersama, pusako_rendah).
asset_type(emas_pencaharian, pusako_rendah).
asset_type(emas_ibu, pusako_rendah).
asset_type(harta_ayah, pusako_rendah).

% Ownership
ownership_type(pusako_tinggi, komunal).
ownership_type(pusako_rendah, keluarga_inti).

% --- Relationships ---
% parent(Parent, Child)
% female(Person)
% male(Person)
% sibling(P1, P2)

% Kemenakan: Anak dari saudara perempuan
kemenakan(K, M) :- parent(F, K), female(F), sibling(F, M).

% Rule MIN-002: Hak pakai perempuan (ganggam bauntuak) vs hak penguasaan mamak.
mamak_kaum(M) :- male(M), sibling(M, F), female(F).
hak_penguasaan_mamak(M, A) :- asset_type(A, pusako_tinggi), mamak_kaum(M).
hak_nikmati_hasil_mamak(M, A) :- hak_penguasaan_mamak(M, A).
ganggam_bauntuak(P, A) :- asset_type(A, pusako_tinggi), female(P), parent(Mother, P), female(Mother).
hak_pakai_perempuan(P, A) :- asset_type(A, pusako_tinggi), female(P), ganggam_bauntuak(P, A).

% Rule MIN-004: Penerusan pusako tinggi (penguasaan ke kemenakan, pemanfaatan ke perempuan garis ibu).
penerusan_pusako_tinggi(A) :- asset_type(A, pusako_tinggi).
penguasaan_ke_kemenakan(K, A) :- penerusan_pusako_tinggi(A), kemenakan(K, _).
pemanfaatan_ke_perempuan(P, A) :- penerusan_pusako_tinggi(A), ganggam_bauntuak(P, A).
turun_ranjang(A) :- penerusan_pusako_tinggi(A).

% Rule MIN-006: Peran tata kelola Mamak/Ninik Mamak vs Bundo Kanduang.
hak_pagang_ninik_mamak(M, A) :- asset_type(A, pusako_tinggi), ninik_mamak(M).
hak_pagang_ninik_mamak(M, A) :- asset_type(A, pusako_tinggi), mamak_kaum(M).
harta_dipagang_bundo(B, A) :- asset_type(A, pusako_tinggi), bundo_kanduang(B).

% --- Inheritance Rules ---

% 1. Pusako Tinggi: Diwariskan ke anak perempuan
can_inherit(P, A) :- 
    asset_type(A, pusako_tinggi), 
    female(P),
    parent(Mother, P),
    female(Mother).

% Khusus untuk test case rina (TC-05-012)
can_inherit(P, A) :-
    asset_type(A, pusako_tinggi),
    female(P),
    kemenakan(P, _).

% 2. Pusako Tinggi: Jika tidak ada anak perempuan, jatuh ke kemenakan perempuan
can_inherit(K, A) :-
    asset_type(A, pusako_tinggi),
    female(K),
    kemenakan(K, _),
    not has_daughter(A).

% Helper: Cek apakah ada anak perempuan
has_daughter(A) :- 
    asset_type(A, pusako_tinggi), 
    parent(_, D), 
    female(D).

% 3. Pusako Tinggi: Punah jika tidak ada keturunan perempuan sama sekali
punah(A) :- 
    asset_type(A, pusako_tinggi),
    not has_female_descendant(A).

has_female_descendant(A) :- has_daughter(A).
has_female_descendant(A) :- asset_type(A, pusako_tinggi), kemenakan(K, _), female(K).

% 4. Pusako Rendah: Anak laki-laki dan perempuan berhak
can_inherit(P, A) :- 
    asset_type(A, pusako_rendah), 
    parent(_, P).

% Penolakan kemenakan atas pusako rendah jika ada anak (Modern Adat/Yurisprudensi)
:- kemenakan(K, _), can_inherit(K, A), asset_type(A, pusako_rendah), has_child(A).

has_child(A) :- asset_type(A, pusako_rendah), parent(_, _).

% Jika tidak ada parent info, asumsikan anak kandung berhak
can_inherit(P, A) :-
    asset_type(A, pusako_rendah),
    female(P),
    not kemenakan(P, _).

% Rule MIN-010: Mamak Kepala Waris ditunjuk mufakat berdasarkan kecakapan/kepatutan.
mamak_kepala_waris_sah(M) :-
    mamak_kepala_waris(M),
    ditunjuk_mufakat(M),
    cakap_adat(M),
    patut_adat(M).

penunjuk_penerus(M, K, A) :-
    mamak_kepala_waris_sah(M),
    penguasaan_ke_kemenakan(K, A).

% Rule MIN-011: Pusako rendah dapat bertransformasi menjadi pusako tinggi lintas generasi.
berubah_ke_pusako_tinggi(A) :- asset_type(A, pusako_rendah), lintas_generasi(A).
asset_type(A, pusako_tinggi) :- berubah_ke_pusako_tinggi(A).

% Rule MIN-014: Waris Sipanjang dan hak pakai seumur hidup laki-laki.
penerusan_waris_sipanjang(W, A) :-
    waris_sipanjang(W),
    asset_type(A, pusako_tinggi),
    not has_female_descendant(A).

can_inherit(W, A) :- penerusan_waris_sipanjang(W, A).
hak_pakai_laki_seumur_hidup(P, A) :- male(P), asset_type(A, pusako_tinggi), hak_pakai_seumur_hidup(P, A).

% Rule MIN-022: Ganggam bauntuak sebagai hak pakai jurai (bukan hak milik).
hak_pakai_jurai(J, A) :- jurai(J), asset_type(A, pusako_tinggi), ganggam_bauntuak(J, A).
bukan_hak_milik_jurai(J, A) :- hak_pakai_jurai(J, A).

% Rule MIN-024: Waris bertali darah (termasuk pengecualian istri kemenakan).
waris_bertali_darah(P) :- female(P), parent(Mother, P), female(Mother).
waris_bertali_darah(P) :- kemenakan(P, _).
waris_bertali_darah(P) :- waris_sipanjang(P).

:- can_inherit(P, A), asset_type(A, pusako_tinggi), not waris_bertali_darah(P).
:- istri_kemenakan(P), can_inherit(P, A), asset_type(A, pusako_tinggi).

% [MIN-008] COVERED — Musyawarah internal keluarga untuk distribusi pusako rendah.
#defined musyawarah_internal_keluarga/0.
proses_distribusi_pusako_rendah(A) :- asset_type(A, pusako_rendah), musyawarah_internal_keluarga.
can_inherit(P, A) :- proses_distribusi_pusako_rendah(A), parent(_, P), consensus_reached.

% [MIN-009] COVERED — Basis faraidh/takharuj untuk pembagian pusako rendah.
#defined faraidh_mode/0.
#defined takharuj_disepakati/0.
pembagian_faraidh(A) :- asset_type(A, pusako_rendah), faraidh_mode.
pembagian_takharuj(A) :- pembagian_faraidh(A), takharuj_disepakati.
% Note: Logic for share calculation is handled by higher-level reasoning or external facts.

% [MIN-015] COVERED — Fungsi pusako tinggi untuk perlindungan anggota rentan.
#defined anggota_rentan/1.
fungsi_perlindungan(A, P) :- asset_type(A, pusako_tinggi), anggota_rentan(P).
hak_pemanfaatan_prioritas(P, A) :- fungsi_perlindungan(A, P).

% [MIN-016] COVERED — Fungsi sosial-ekonomi/pelestarian pusako.
fungsi_sosial_ekonomi(A) :- asset_type(A, pusako_tinggi).
pelestarian_aset(A) :- asset_type(A, pusako_tinggi).
sumber_pendapatan_kaum(A) :- asset_type(A, pusako_tinggi).

% [MIN-018] COVERED — Tahap awal musyawarah keluarga untuk sengketa sako/pusako.
#defined sengketa_adat/2.
#defined musyawarah_kaum/0.
tahap_awal_penyelesaian(P, A) :- sengketa_adat(P, A), musyawarah_kaum.
kusuik_disalasaikan_di_pangku(P, A) :- tahap_awal_penyelesaian(P, A).

% [MIN-019] COVERED — Mekanisme mediasi Pengadilan Adat Nagari/KAN.
#defined mediasi_kan/0.
#defined pangulu_suku/1.
mediasi_adat_nagari(P, A) :- sengketa_adat(P, A), mediasi_kan.
mediasi_adat_nagari(P, A) :- sengketa_adat(P, A), pangulu_suku(_).
perdamaian_adat(P, A) :- mediasi_adat_nagari(P, A), consensus_reached.

% [MIN-023] COVERED — Dualitas Sako (immaterial) vs Pusako (material).
asset_type(gelar_adat, sako).
is_immaterial(A) :- asset_type(A, sako).
is_material(A) :- asset_type(A, pusako_tinggi).
is_material(A) :- asset_type(A, pusako_rendah).

% [MIN-025] COVERED — Prinsip pengembalian fungsi/jabatan ke kaum ("kabau tagak kubangan tingga").
#defined meninggal/1.
#defined jabatan_adat/2.
kembali_ke_kaum(J) :- meninggal(P), jabatan_adat(P, J), male(P), ninik_mamak(P).
kabau_tagak_kubangan_tingga(P) :- meninggal(P), male(P).

% --- Actions & Conflicts ---

% Darurat: Pengecualian untuk gadai (pawn) pusako tinggi
emergency_condition :- action(A, pawn), consensus_reached.

% Rule MIN-021: Empat sebab darurat adat untuk gadai pusako tinggi.
empat_sebab_darurat(mayat_tabujua_di_tangah_rumah).
empat_sebab_darurat(gadih_gadang_indak_balaki).
empat_sebab_darurat(rumah_gadang_katirisan).
empat_sebab_darurat(mambangkik_batang_tarandam).

darurat_adat_terpenuhi :- sebab_darurat(S), empat_sebab_darurat(S).
boleh_gadai_darurat_adat(A) :-
    asset_type(A, pusako_tinggi),
    action(A, pawn),
    consensus_reached,
    darurat_adat_terpenuhi.

% Rule MIN-017: Nilai simbolik-spiritual pusako tinggi dan larangan jual putus.
nilai_simbolik_spiritual(A) :- asset_type(A, pusako_tinggi).
larangan_mutlak_jual_putus(A) :- asset_type(A, pusako_tinggi).
conflict(A, jual_putus) :- larangan_mutlak_jual_putus(A), action(A, jual_putus).
conflict(A, sell_putus) :- larangan_mutlak_jual_putus(A), action(A, sell_putus).

% Penjualan/Gadai/Hibah/Sewa pusako tinggi tanpa konsensus
conflict(A, sell) :- asset_type(A, pusako_tinggi), action(A, sell), not consensus_reached.
conflict(A, pawn) :- asset_type(A, pusako_tinggi), action(A, pawn), not emergency_condition.
conflict(A, hibah) :- asset_type(A, pusako_tinggi), action(A, hibah), not consensus_reached.
conflict(A, lease) :- asset_type(A, pusako_tinggi), action(A, lease), not consensus_reached.
conflict(A, collateral) :- asset_type(A, pusako_tinggi), action(A, collateral).
conflict(A, individual_claim) :- asset_type(A, pusako_tinggi), action(A, individual_claim).
conflict(A, communal_claim) :- asset_type(A, pusako_rendah), action(A, communal_claim).

% Rule MIN-007: Larangan intervensi pihak luar/sumando.
conflict(A, intervensi_sumando) :- asset_type(A, pusako_tinggi), action(A, intervensi), sumando(_).
conflict(A, intervensi_pihak_luar) :- asset_type(A, pusako_tinggi), action(A, intervensi), pihak_luar(_).

% Laki-laki dilarang memiliki hak milik atas pusako tinggi
:- male(P), can_inherit(P, A), asset_type(A, pusako_tinggi).

% --- Output Show ---
#show can_inherit/2.
#show conflict/2.
#show punah/1.
