% Bali inheritance rules in ASP (Clingo)
% Logic for neuro-symbolic reasoning experiments.

% --- Fakta Dasar ---
patrilineal.

% Klasifikasi harta
asset_type(tanah_sanggah, druwe_tengah).
asset_type(tanah_tegal_laba_pura, druwe_tengah).
asset_type(benda_pusaka, druwe_tengah).
asset_type(tanah_pkd, druwe_tengah).
asset_type(tanah_ayahan_desa, druwe_tengah).
asset_type(tanah_pelaba_pura, druwe_tengah).

asset_type(harta_druwe_gabro, druwe_gabro).
asset_type(gunakaya, druwe_gabro).

asset_type(harta_tetadan, tetadan).
asset_type(harta_bawaan, tetadan).

asset_type(harta_bekel, bekel).
asset_type(jiwa_dana, jiwa_dana).
asset_type(harta_pusaka, pusaka_magis).

% Kepemilikan
ownership_type(druwe_tengah, komunal).
ownership_type(druwe_gabro, keluarga_inti).
ownership_type(tetadan, individual).
ownership_type(bekel, pemberian_putus).
ownership_type(jiwa_dana, hibah_hidup).
ownership_type(pusaka_magis, komunal_ritual).

% --- Relasi ---
% male(P), female(P), parent(OrangTua, Anak)
% status_purusa(P), sentana_rajeg(P), ninggal_kedaton(P)
% kawin_keluar(P), kewajiban_ngayah(P), menolak_ngaben(P)
% adopsi(P), upacara_widhi_widana(P), tri_upasaksi(P)
% astra(P), pengesahan_ayah(P), ngamong_sanggah(P)
% janda(P), menikah_lagi(P), keluarga_camput(Keluarga)

% Purusa: laki-laki atau perempuan yang diangkat (sentana rajeg)
status_purusa(P) :- male(P).
status_purusa(P) :- sentana_rajeg(P).

% --- Aturan Ahli Waris ---

% Hak utama purusa pada harta waris inti
can_inherit(P, A) :-
    status_purusa(P),
    asset_type(A, druwe_gabro).

can_inherit(P, A) :-
    status_purusa(P),
    asset_type(A, druwe_tengah),
    not kawin_keluar(P).

can_inherit(P, A) :-
    status_purusa(P),
    asset_type(A, pusaka_magis),
    not kawin_keluar(P).

% Anak perempuan kawin keluar: ahli waris terbatas untuk gunakaya
ahli_waris_terbatas(P) :- female(P), kawin_keluar(P).

can_inherit(P, A) :-
    ahli_waris_terbatas(P),
    asset_type(A, druwe_gabro).

% Anak perempuan kawin keluar tidak mewarisi druwe tengah/pusaka
:- female(P), kawin_keluar(P), can_inherit(P, A), asset_type(A, druwe_tengah).
:- female(P), kawin_keluar(P), can_inherit(P, A), asset_type(A, pusaka_magis).

% Hak waris gugur bila keluar kedaton atau menolak kewajiban utama
gugur_hak_waris(P) :- ninggal_kedaton(P).
gugur_hak_waris(P) :- menolak_ngaben(P).
gugur_hak_waris(P) :- not kewajiban_ngayah(P), status_purusa(P).

:- gugur_hak_waris(P), can_inherit(P, _).

% Anak angkat sah (sentana peperasan) setara dengan anak kandung
adopsi_sah(P) :- adopsi(P), upacara_widhi_widana(P), tri_upasaksi(P).
can_inherit(P, A) :-
    adopsi_sah(P),
    asset_type(A, druwe_gabro).

can_inherit(P, A) :-
    adopsi_sah(P),
    asset_type(A, druwe_tengah).

% Anak astra hanya berelasi ke ibu, kecuali ada pengesahan ayah
bisa_relasi_ayah(P) :- pengesahan_ayah(P).
:- astra(P), male(Ayah), parent(Ayah, P), not bisa_relasi_ayah(P), can_inherit(P, _).

% Janda sentana: hak menguasai/menikmati, bukan hak transfer mutlak
hak_penguasaan(P, A) :-
    janda(P),
    asset_type(A, druwe_gabro),
    not menikah_lagi(P).

hak_penguasaan(P, A) :-
    janda(P),
    asset_type(A, druwe_tengah),
    not menikah_lagi(P).

% --- Tata Kelola Aset & Konflik ---

% Larangan transfer aset komunal/ritual
conflict(A, sell) :- asset_type(A, druwe_tengah), action(A, sell).
conflict(A, sell) :- asset_type(A, pusaka_magis), action(A, sell).
conflict(A, transfer_outside_desa) :- asset_type(A, druwe_tengah), action(A, transfer_outside_desa).
conflict(A, split_individual) :- asset_type(A, tanah_pelaba_pura), action(A, split_individual).

% Jiwa dana sah bila disaksikan prajuru adat
conflict(jiwa_dana, invalid_transfer) :- action(jiwa_dana, grant), not disaksikan_prajuru.

% Hak ngamong sanggah memberi prioritas pada tanah sanggah
prioritas_sanggah(P, tanah_sanggah) :- ngamong_sanggah(P).
can_inherit(P, tanah_sanggah) :- prioritas_sanggah(P, tanah_sanggah).

% Keluarga camput -> tanah ayahan desa kembali ke desa adat
ditarik_desa(tanah_ayahan_desa) :- keluarga_camput(_).

% --- Output ---
#show can_inherit/2.
#show conflict/2.
#show hak_penguasaan/2.
#show ahli_waris_terbatas/1.
#show ditarik_desa/1.
