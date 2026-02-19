% Javanese inheritance rules in ASP (Clingo)
% Logic for neuro-symbolic reasoning experiments.

% --- Fakta Dasar ---
bilateral.

% Deklarasi predicate eksternal (tidak ada fakta default; semua di-inject runtime)
#defined child/1.
#defined male/1.
#defined female/1.
#defined parent/2.
#defined faraidh_mode/0.
#defined takharuj_disepakati/0.
#defined merawat_orangtua/1.
#defined anak_ragil/1.
#defined penunggu_rumah/1.
#defined action/2.
#defined anak_angkat/1.
#defined adopsi_terang_tunai/1.
#defined anak_tiri/1.
#defined anak_luar_kawin/1.
#defined bukti_darah_ayah/1.
#defined cucu_pengganti/1.
#defined orangtua_meninggal_lebih_dulu/1.
#defined janda/1.
#defined menikah_lagi/1.
#defined duda/1.
#defined cerai_hidup/0.
#defined musyawarah_keluarga/0.
#defined dipimpin_sesepuh/0.
#defined penengah_pakde_budhe/0.
#defined penengah_tokoh_desa/0.
#defined penerimaan_weweh/2.
#defined anak_belum_mapan/1.
#defined anak_sudah_mapan/1.
#defined hibah_wasiat_weling/1.
#defined masih_dibutuhkan_untuk_hidup/1.
#defined tuntut_pembagian/1.
#defined orangtua_masih_waras/0.
#defined penerimaan_sangu_bekel/1.
#defined penerimaan_lintiran/1.
#defined anak_kandung/1.
#defined pesan_weling_rumah_induk/0.
#defined pesan_kumpul_keluarga/0.
#defined kompensasi_penuh/0.
#defined hibah_penyeimbang_putri/1.

% Klasifikasi harta
asset_type(harta_gono_gini, gono_gini).
asset_type(rajakaya, gono_gini).

asset_type(harta_bawaan, harta_asal).
asset_type(harta_asal_suami, harta_asal).
asset_type(harta_asal_istri, harta_asal).
asset_type(harta_asal_ibu, harta_asal).
asset_type(harta_asal_ayah, harta_asal).

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

% Rule JAW-005: Musyawarah keluarga untuk mufakat (rukun).
proses_musyawarah_waris :- musyawarah_keluarga.
proses_musyawarah_waris :- dipimpin_sesepuh.
proses_musyawarah_waris :- penengah_pakde_budhe.
proses_musyawarah_waris :- penengah_tokoh_desa.

% Prioritas berbasis perawatan dan kebutuhan
prioritas_lintiran(P) :- merawat_orangtua(P).
prioritas_rumah(P) :- anak_ragil(P), penunggu_rumah(P).
can_inherit(P, rumah_induk) :- prioritas_rumah(P).

% Rule JAW-010: Perawat orang tua dapat bagian lebih/prioritas pilih bagian.
bagian_lebih(P, A) :- prioritas_lintiran(P), asset_type(A, gono_gini).
prioritas_pilih_bagian(P, A) :- prioritas_lintiran(P), asset_type(A, gono_gini).

% Rule JAW-011: Pembagian berbasis kebutuhan (subsidi silang adat).
subsidi_silang(P, A) :- anak_belum_mapan(P), asset_type(A, gono_gini).
pengurangan_proporsional(P, A) :- anak_sudah_mapan(P), asset_type(A, gono_gini).

% Rumah induk/pusaka umumnya tidak dijual
conflict(rumah_induk, sell) :- action(rumah_induk, sell).
conflict(harta_pusaka, sell) :- action(harta_pusaka, sell).
conflict(harta_pusaka, split_individual) :- action(harta_pusaka, split_individual).

% Anak angkat: hak terbatas
anak_angkat_sah(P) :- anak_angkat(P), adopsi_terang_tunai(P).
can_inherit(P, A) :-
    anak_angkat_sah(P),
    asset_type(A, gono_gini).

% Rule JAW-015: Batas maksimal 1/3 untuk anak angkat atau jalur hibah wasiat.
batas_maks_anak_angkat(sepertiga).
hak_terbatas_sepertiga(P) :- anak_angkat_sah(P).
jalur_hibah_wasiat(P) :- anak_angkat_sah(P), hibah_wasiat_weling(P).

:- anak_angkat_sah(P), can_inherit(P, A), asset_type(A, pusaka).
:- anak_angkat_sah(P), can_inherit(P, A), asset_type(A, harta_asal).

% Anak tiri: tidak mewarisi kecuali hibah/wasiat khusus
:- anak_tiri(P), can_inherit(P, A), not asset_type(A, hibah_hidup), not asset_type(A, hibah_khusus).

% Anak luar kawin: default ibu; bisa dari ayah jika bukti darah/pengesahan
can_inherit(P, A) :-
    anak_luar_kawin(P),
    asset_type(A, harta_asal),
    bukti_darah_ayah(P).

% Rule JAW-018: Default relasi perdata anak luar kawin ke garis ibu.
relasi_perdata_ibu(P) :- anak_luar_kawin(P).
relasi_perdata_ayah(P) :- anak_luar_kawin(P), bukti_darah_ayah(P).
can_inherit(P, harta_asal_ibu) :- relasi_perdata_ibu(P).
can_inherit(P, harta_asal_ayah) :- relasi_perdata_ayah(P).

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

% Rule JAW-019: Anak tidak boleh menuntut pembagian saat orang tua hidup masih membutuhkan.
conflict(harta_gono_gini, tuntutan_anak_prematur) :-
    tuntut_pembagian(_),
    hak_penguasaan(P, harta_gono_gini),
    masih_dibutuhkan_untuk_hidup(P).

% Pecah panci: hak penguasaan berakhir bila menikah lagi
pecah_panci(P) :- janda(P), menikah_lagi(P).
pecah_panci(P) :- duda(P), menikah_lagi(P).
conflict(harta_gono_gini, hold_without_distribution) :- pecah_panci(_), action(harta_gono_gini, hold_without_distribution).

% Perceraian: maro untuk gono-gini, harta asal kembali ke asal
maro(gono_gini) :- cerai_hidup.
kembali_ke_asal(A) :- cerai_hidup, asset_type(A, harta_asal).

% Rule JAW-024: Hak waris anak kandung tetap melekat pasca perceraian.
hak_waris_tetap(P) :- anak_kandung(P), cerai_hidup.
can_inherit(P, harta_asal_suami) :- hak_waris_tetap(P).
can_inherit(P, harta_asal_istri) :- hak_waris_tetap(P).

% Rule JAW-007: Weweh/Hibah diperhitungkan sebagai pengurang waris akhir.
pengurang_waris_akhir(P, A) :- penerimaan_weweh(P, A), asset_type(A, hibah_hidup).

% Rule JAW-021: Dum-duman semasa hidup untuk pencegahan sengketa.
dum_duman_semasa_hidup :- asset_type(dum_duman, hibah_hidup), orangtua_masih_waras.
pencegahan_sengketa(dum_duman) :- dum_duman_semasa_hidup.

% Rule JAW-022: Sangu/Bekel sebagai uang muka warisan.
uang_muka_waris(P) :- penerimaan_sangu_bekel(P).
pengurang_waris_akhir(P, sangu_bekel) :- uang_muka_waris(P).

% Rule JAW-023: Lintiran lazimnya di luar hitungan waris besar.
di_luar_waris_besar(P) :- penerimaan_lintiran(P).

% Rule JAW-025: Pesan Weling/Kumpul sebagai norma moral rumah induk.
norma_weling_kumpul :- pesan_weling_rumah_induk.
norma_weling_kumpul :- pesan_kumpul_keluarga.
conflict(rumah_induk, langgar_weling) :- action(rumah_induk, sell), norma_weling_kumpul.

% Rule JAW-026: Penunggu rumah diprioritaskan dengan kompensasi tidak selalu penuh.
prioritas_penunggu_rumah(P) :- penunggu_rumah(P).
kompensasi_tidak_penuh_dibenarkan(P) :- prioritas_penunggu_rumah(P), not kompensasi_penuh.

% Rule JAW-029: Pola hitung Islam -> eksekusi adat + hibah penyeimbang.
hitungan_awal_islam(A) :- asset_type(A, gono_gini), faraidh_mode.
eksekusi_adat_musyawarah(A) :- hitungan_awal_islam(A), takharuj_disepakati.
hibah_penyeimbang(P, A) :-
    hibah_penyeimbang_putri(P),
    female(P),
    ahli_waris_anak(P),
    asset_type(A, gono_gini),
    eksekusi_adat_musyawarah(A).

% [JAW-008] COVERED — Pemisahan harta antar-istri dalam konteks poligami.
#defined poligami/0.
#defined istri_ke/2.
harta_pencaharian_sendiri(A, Istri) :- poligami, asset_type(A, gono_gini), istri_ke(Istri, _).
:- can_inherit(I2, A), harta_pencaharian_sendiri(A, I1), I1 != I2.

% [JAW-027] COVERED — Jalur Rembug Desa/Kepala Desa-Lurah sebagai penyelesaian sengketa.
#defined rembug_desa/0.
#defined kepala_desa/1.
hakim_perdamaian_desa(K) :- kepala_desa(K), rembug_desa.
putusan_lurah_sah(K) :- hakim_perdamaian_desa(K), consensus_reached.

% [JAW-028] COVERED — Norma "saru" (tabu membawa sengketa waris ke pengadilan).
#defined bawa_ke_pengadilan/0.
norma_saru(A) :- action(A, bawa_ke_pengadilan).
conflict(A, saru) :- norma_saru(A).

% [JAW-031] COVERED — Pergeseran ke sertifikasi individual tanah warisan.
#defined sertifikasi_individu/1.
kepastian_hukum(A) :- sertifikasi_individu(A).
bukan_komunal_lagi(A) :- sertifikasi_individu(A).

% [JAW-032] COVERED — Tren monetisasi warisan di perkotaan (jual lalu bagi tunai).
#defined kawasan_perkotaan/0.
monetisasi_warisan(A) :- action(A, sell), kawasan_perkotaan.
bagi_tunai(A) :- monetisasi_warisan(A).

% [JAW-034] COVERED — Kekuatan moral Weling/Wekas (wasiat lisan).
#defined wasiat_lisan/1.
kekuatan_moral_weling(P) :- wasiat_lisan(P).
mengikat_secara_moral(P) :- kekuatan_moral_weling(P).

% [JAW-036] COVERED — Tradisi Bao Parmate (harta melekat pada jenazah).
#defined harta_melekat_tubuh/1.
#defined diberikan_ke_pemandian/2.
bao_parmate(A) :- harta_melekat_tubuh(A).
:- can_inherit(P, A), bao_parmate(A), child(P).
diberikan_saat_kematian(A, Person) :- bao_parmate(A), diberikan_ke_pemandian(A, Person).

% --- Output ---
#show can_inherit/2.
#show conflict/2.
#show hak_penguasaan/2.
#show equal_share/3.
#show share_ratio/3.
#show pecah_panci/1.
