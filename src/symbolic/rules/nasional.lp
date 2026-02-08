% Aturan waris nasional (KUHPerdata) dalam ASP (Clingo)
% Digunakan sebagai counterpart hukum nasional untuk komparasi dengan hukum adat.

% --- Klasifikasi Harta ---
asset_type(harta_bersama, harta_perkawinan).
asset_type(harta_bawaan, harta_pribadi).
asset_type(harta_waris_pewaris, harta_waris).

% --- Fakta Relasi yang bisa di-inject saat query ---
% spouse(P), child(P), parent(P), sibling(P), distant_relative(P)
% pewaris_meninggal, ada_anak, ada_orangtua, ada_saudara
% menikah_sah, tidak_patut(P), menerima_wasiat(P), persetujuan_ahli_waris
% action(Objek, JenisAksi), nilai_wasiat(Persen), debt_settled
% hak_waris_nasional(P, A), larangan_waris_adat(P, A)

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
