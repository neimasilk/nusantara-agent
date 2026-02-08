% Javanese inheritance rules in ASP (Clingo)
% Logic for neuro-symbolic reasoning experiments.

% --- Fakta Dasar ---
bilateral.

% Klasifikasi harta
asset_type(harta_gono_gini, gono_gini).
asset_type(rajakaya, gono_gini).

asset_type(harta_bawaan, harta_asal).
asset_type(harta_asal_suami, harta_asal).
asset_type(harta_asal_istri, harta_asal).

asset_type(harta_pusaka, pusaka).
asset_type(rumah_induk, rumah_keluarga).

asset_type(weweh_hibah, hibah_hidup).
asset_type(dum_duman, hibah_hidup).
asset_type(sangu_bekel, hibah_hidup).
asset_type(lintiran, hibah_khusus).

% Kepemilikan
ownership_type(gono_gini, bersama_suami_istri).
ownership_type(harta_asal, individual_asal).
ownership_type(pusaka, komunal_keluarga).
ownership_type(rumah_keluarga, semi_komunal).

% --- Relasi ---
% male(P), female(P), child(P), parent(OrangTua, Anak)
% merawat_orangtua(P), anak_ragil(P), penunggu_rumah(P)
% anak_angkat(P), adopsi_terang_tunai(P), anak_tiri(P), anak_luar_kawin(P), bukti_darah_ayah(P)
% janda(P), duda(P), menikah_lagi(P), cerai_hidup, cerai_mati
% cucu_pengganti(Cucu), orangtua_meninggal_lebih_dulu(OrangTua)
% faraidh_mode, takharuj_disepakati

% Ahli waris dasar: anak laki-laki dan perempuan setara
ahli_waris_anak(P) :- child(P), male(P).
ahli_waris_anak(P) :- child(P), female(P).

can_inherit(P, A) :-
    ahli_waris_anak(P),
    asset_type(A, gono_gini).

can_inherit(P, A) :-
    ahli_waris_anak(P),
    asset_type(A, harta_asal).

% Prinsip sigar semangka (equal share) sebagai default modern
equal_share(P1, P2, A) :-
    ahli_waris_anak(P1),
    ahli_waris_anak(P2),
    P1 != P2,
    asset_type(A, gono_gini).

% Sepikul-segendongan sebagai mode historis opsional
share_ratio(P, 2, A) :-
    male(P),
    ahli_waris_anak(P),
    asset_type(A, gono_gini),
    faraidh_mode,
    not takharuj_disepakati.

share_ratio(P, 1, A) :-
    female(P),
    ahli_waris_anak(P),
    asset_type(A, gono_gini),
    faraidh_mode,
    not takharuj_disepakati.

% Prioritas berbasis perawatan dan kebutuhan
prioritas_lintiran(P) :- merawat_orangtua(P).
prioritas_rumah(P) :- anak_ragil(P), penunggu_rumah(P).
can_inherit(P, rumah_induk) :- prioritas_rumah(P).

% Rumah induk/pusaka umumnya tidak dijual
conflict(rumah_induk, sell) :- action(rumah_induk, sell).
conflict(harta_pusaka, sell) :- action(harta_pusaka, sell).
conflict(harta_pusaka, split_individual) :- action(harta_pusaka, split_individual).

% Anak angkat: hak terbatas
anak_angkat_sah(P) :- anak_angkat(P), adopsi_terang_tunai(P).
can_inherit(P, A) :-
    anak_angkat_sah(P),
    asset_type(A, gono_gini).

:- anak_angkat_sah(P), can_inherit(P, A), asset_type(A, pusaka).
:- anak_angkat_sah(P), can_inherit(P, A), asset_type(A, harta_asal).

% Anak tiri: tidak mewarisi kecuali hibah/wasiat khusus
:- anak_tiri(P), can_inherit(P, A), not asset_type(A, hibah_hidup), not asset_type(A, hibah_khusus).

% Anak luar kawin: default ibu; bisa dari ayah jika bukti darah/pengesahan
can_inherit(P, A) :-
    anak_luar_kawin(P),
    asset_type(A, harta_asal),
    bukti_darah_ayah(P).

% Ahli waris pengganti (gantungan siwur / cucu pancar)
can_inherit(C, A) :-
    cucu_pengganti(C),
    orangtua_meninggal_lebih_dulu(O),
    parent(O, C),
    asset_type(A, gono_gini).

% Hak janda/duda: menguasai dan menikmati sampai menikah lagi
hak_penguasaan(P, A) :-
    janda(P),
    asset_type(A, gono_gini),
    not menikah_lagi(P).

hak_penguasaan(P, A) :-
    duda(P),
    asset_type(A, gono_gini),
    not menikah_lagi(P).

% Pecah panci: hak penguasaan berakhir bila menikah lagi
pecah_panci(P) :- janda(P), menikah_lagi(P).
pecah_panci(P) :- duda(P), menikah_lagi(P).
conflict(harta_gono_gini, hold_without_distribution) :- pecah_panci(_), action(harta_gono_gini, hold_without_distribution).

% Perceraian: maro untuk gono-gini, harta asal kembali ke asal
maro(gono_gini) :- cerai_hidup.
kembali_ke_asal(A) :- cerai_hidup, asset_type(A, harta_asal).

% --- Output ---
#show can_inherit/2.
#show conflict/2.
#show hak_penguasaan/2.
#show equal_share/3.
#show share_ratio/3.
#show pecah_panci/1.
