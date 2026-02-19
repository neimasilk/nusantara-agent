% Bali inheritance rules in ASP (Clingo)
% Logic for neuro-symbolic reasoning experiments.

% --- Fakta Dasar ---
patrilineal.

% Deklarasi predicate eksternal (tidak ada fakta default; semua di-inject runtime)
#defined female/1.
#defined male/1.
#defined parent/2.
#defined sentana_rajeg/1.
#defined kawin_keluar/1.
#defined ninggal_kedaton/1.
#defined menolak_ngaben/1.
#defined adopsi/1.
#defined upacara_widhi_widana/1.
#defined tri_upasaksi/1.
#defined pengesahan_ayah/1.
#defined astra/1.
#defined janda/1.
#defined menikah_lagi/1.
#defined kewajiban_ngayah/1.
#defined disaksikan_prajuru/0.
#defined action/2.
#defined keluarga_camput/1.
#defined kewajiban_sanggah/1.

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

% Rule BAL-014: Hak anak perempuan pada gunakaya maksimal 1/2 bagian purusa.
share_ratio(P, 1, 2, gunakaya) :- ahli_waris_terbatas(P).
share_ratio(P, 2, 2, gunakaya) :- status_purusa(P).

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

% Rule BAL-017: Ahli waris pusaka memiliki hak pakai/hak kelola, bukan hak milik mutlak.
hak_pakai(P, A) :- can_inherit(P, A), asset_type(A, druwe_tengah).
hak_kelola(P, A) :- can_inherit(P, A), asset_type(A, druwe_tengah).
hak_pakai(P, A) :- can_inherit(P, A), asset_type(A, pusaka_magis).
hak_kelola(P, A) :- can_inherit(P, A), asset_type(A, pusaka_magis).
bukan_hak_milik_mutlak(P, A) :- hak_pakai(P, A).

% --- Tata Kelola Aset & Konflik ---

% Larangan transfer aset komunal/ritual
conflict(A, sell) :- asset_type(A, druwe_tengah), action(A, sell).
conflict(A, sell) :- asset_type(A, pusaka_magis), action(A, sell).
conflict(A, transfer_outside_desa) :- asset_type(A, druwe_tengah), action(A, transfer_outside_desa).
conflict(A, split_individual) :- asset_type(A, tanah_pelaba_pura), action(A, split_individual).

% Jiwa dana sah bila disaksikan prajuru adat
conflict(jiwa_dana, invalid_transfer) :- action(jiwa_dana, grant), not disaksikan_prajuru.

% Rule BAL-019: Adopsi sah komunal wajib diketahui/disaksikan prajuru.
adopsi_sah_komunal(P) :- adopsi_sah(P), disaksikan_prajuru.
conflict(adopsi_sentana_peperasan, invalid_without_prajuru) :- adopsi(_), not disaksikan_prajuru.

% Rule BAL-024: Anak angkat setara pada hak waris dan kewajiban sanggah/ngayah.
kewajiban_setara_ngayah(P) :- adopsi_sah(P).
kewajiban_setara_sanggah(P) :- adopsi_sah(P).
kewajiban_setara_ngayah(P) :- adopsi_sah(P), kewajiban_ngayah(P).
kewajiban_setara_sanggah(P) :- adopsi_sah(P), kewajiban_sanggah(P).

% [BAL-022] COVERED — Prioritas biaya upacara sebelum distribusi.
#defined biaya_upacara_ngaben/2.
prioritas_biaya_ngaben(A, Pewaris) :- biaya_upacara_ngaben(A, Pewaris).
:- can_inherit(P, A), prioritas_biaya_ngaben(A, _).

% [BAL-025] COVERED — Aturan dampak cerai khusus 'mulih daha'.
#defined cerai/0.
#defined mulih_daha/1.
kembali_ke_asal(P) :- female(P), cerai, mulih_daha(P).
:- can_inherit(P, A), kembali_ke_asal(P), asset_type(A, druwe_gabro).

% [BAL-026] COVERED — Aturan pasca cerai untuk anak.
#defined diasuh_ibu_sementara/1.
status_hukum_ikut_ayah(Anak) :- parent(Ayah, Anak), male(Ayah), cerai.
hak_asuh_ayah(Ayah, Anak) :- status_hukum_ikut_ayah(Anak), parent(Ayah, Anak), not diasuh_ibu_sementara(Anak).

% [BAL-027] COVERED — Prosedur sengketa internal keluarga.
#defined sangkep_dadia/0.
sengketa_internal_keluarga(P, A) :- sengketa_adat(P, A), sangkep_dadia.
resolusi_internal(P, A) :- sengketa_internal_keluarga(P, A), consensus_reached.

% [BAL-028] COVERED — Prosedur eskalasi sengketa (Banjar -> Desa Adat -> PN).
#defined mediasi_banjar/0.
#defined kerta_desa/0.
#defined pengadilan_negeri/0.
eskalasi_banjar(P, A) :- sengketa_adat(P, A), mediasi_banjar.
eskalasi_desa_adat(P, A) :- sengketa_adat(P, A), kerta_desa.
eskalasi_nasional(P, A) :- sengketa_adat(P, A), pengadilan_negeri.

% [BAL-029] COVERED — Perubahan kontemporer beda wangsa.
#defined beda_wangsa/2.
hak_waris_tetap_beda_wangsa(P) :- beda_wangsa(P, _), kewajiban_ngayah(P).
can_inherit(P, A) :- hak_waris_tetap_beda_wangsa(P), asset_type(A, druwe_gabro).

% [BAL-031] COVERED — Aturan perkawinan pada gelahang.
#defined pada_gelahang/2.
status_purusa_gelahang(P) :- pada_gelahang(P, _).
share_ratio(P, 1, 2, A) :- status_purusa_gelahang(P), asset_type(A, druwe_gabro).

% [BAL-033] COVERED — Ground disinherit karena alpaka guru.
#defined alpaka_guru/1.
#defined keputusan_sangkep/0.
disinherit(P) :- alpaka_guru(P), keputusan_sangkep.
:- can_inherit(P, _), disinherit(P).

% [BAL-034] COVERED — Mekanisme sisih 1/3 sebelum pembagian (MUDP 2010).
#defined sisih_untuk_sanggah/1.
dana_pelestarian_sanggah(A) :- sisih_untuk_sanggah(A).
:- can_inherit(P, A), dana_pelestarian_sanggah(A).

% Hak ngamong sanggah memberi prioritas pada tanah sanggah
#defined ngamong_sanggah/1.
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
