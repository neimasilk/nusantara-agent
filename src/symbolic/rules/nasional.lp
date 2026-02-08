% Aturan waris nasional (KUHPerdata) dalam ASP (Clingo)
% Digunakan sebagai counterpart hukum nasional untuk komparasi dengan hukum adat.

% --- Klasifikasi Harta ---
asset_type(harta_bersama, harta_perkawinan).
asset_type(harta_bawaan, harta_pribadi).
asset_type(harta_waris_pewaris, harta_waris).

% --- Fakta Relasi yang di-inject saat query ---
% Deklarasi predicate eksternal (tidak ada fakta default; semua di-inject runtime)
#defined child/1.
#defined spouse/1.
#defined parent/1.
#defined sibling/1.
#defined distant_relative/1.
#defined ascendant/1.
#defined pewaris_meninggal/0.
#defined ada_anak/0.
#defined ada_orangtua/0.
#defined ada_saudara/0.
#defined menikah_sah/0.
#defined tidak_patut/1.
#defined menerima_wasiat/1.
#defined persetujuan_ahli_waris/0.
#defined action/2.
#defined nilai_wasiat/1.
#defined debt_settled/0.
#defined hak_waris_nasional/2.
#defined larangan_waris_adat/2.

% --- Kelas ahli waris menurut prioritas umum KUHPerdata ---
kelas_1(P) :- child(P).
kelas_1(P) :- spouse(P), menikah_sah.

kelas_2(P) :- parent(P), not ada_anak.
kelas_2(P) :- sibling(P), not ada_anak.

kelas_3(P) :- ascendant(P), not ada_anak, not ada_orangtua, not ada_saudara.
kelas_4(P) :- distant_relative(P), not ada_anak, not ada_orangtua, not ada_saudara.

% Prioritas kelas: kelas lebih rendah gugur jika kelas lebih tinggi ada
ada_kelas_1 :- kelas_1(_).
ada_kelas_2 :- kelas_2(_).
ada_kelas_3 :- kelas_3(_).

berhak_waris(P) :- kelas_1(P), not tidak_patut(P).
berhak_waris(P) :- kelas_2(P), not ada_kelas_1, not tidak_patut(P).
berhak_waris(P) :- kelas_3(P), not ada_kelas_1, not ada_kelas_2, not tidak_patut(P).
berhak_waris(P) :- kelas_4(P), not ada_kelas_1, not ada_kelas_2, not ada_kelas_3, not tidak_patut(P).

can_inherit(P, harta_waris_pewaris) :- berhak_waris(P).

% --- Bagian pasangan hidup ---
bagian_spouse(P, seperdua_harta_bersama) :- spouse(P), menikah_sah.
hak_spouse_atas_harta_bersama(P) :- spouse(P), bagian_spouse(P, seperdua_harta_bersama).

% Sisa harta waris dibagi pada ahli waris berhak
sisa_harta_waris_tersedia :- pewaris_meninggal.
hak_bagi_sisa_waris(P) :- berhak_waris(P), sisa_harta_waris_tersedia.

% --- Perlindungan legitime portie (bagian mutlak ahli waris tertentu) ---
legitime_portie_berlaku :- child(_).
conflict(harta_waris_pewaris, pelanggaran_legitime_portie) :-
    legitime_portie_berlaku,
    action(harta_waris_pewaris, bagi_tidak_adil_ke_anak).

% --- Wasiat ---
conflict(wasiat, melebihi_batas_wajar) :-
    nilai_wasiat(Persen),
    Persen > 33,
    not persetujuan_ahli_waris.

% --- Kewajiban pelunasan utang sebelum pembagian ---
conflict(harta_waris_pewaris, pembagian_sebelum_lunas_utang) :-
    action(harta_waris_pewaris, dibagi),
    not debt_settled.

% --- Ketidakpatutan mewaris ---
:- tidak_patut(P), can_inherit(P, harta_waris_pewaris).

% --- Deteksi konflik normatif nasional vs adat ---
conflict_norm(nasional_vs_adat, P, A) :-
    hak_waris_nasional(P, A),
    larangan_waris_adat(P, A).

% --- Output ---
#show can_inherit/2.
#show berhak_waris/1.
#show bagian_spouse/2.
#show hak_spouse_atas_harta_bersama/1.
#show hak_bagi_sisa_waris/1.
#show conflict/2.
#show conflict_norm/3.
