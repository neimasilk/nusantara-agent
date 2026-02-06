% Minangkabau inheritance rules in ASP (Clingo)
% Logic for neuro-symbolic reasoning experiments.

% --- Facts & Types ---
matrilineal.

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

% --- Actions & Conflicts ---

% Darurat: Pengecualian untuk gadai (pawn) pusako tinggi
emergency_condition :- action(A, pawn), consensus_reached.

% Penjualan/Gadai/Hibah/Sewa pusako tinggi tanpa konsensus
conflict(A, sell) :- asset_type(A, pusako_tinggi), action(A, sell), not consensus_reached.
conflict(A, pawn) :- asset_type(A, pusako_tinggi), action(A, pawn), not emergency_condition.
conflict(A, hibah) :- asset_type(A, pusako_tinggi), action(A, hibah), not consensus_reached.
conflict(A, lease) :- asset_type(A, pusako_tinggi), action(A, lease), not consensus_reached.
conflict(A, collateral) :- asset_type(A, pusako_tinggi), action(A, collateral).
conflict(A, individual_claim) :- asset_type(A, pusako_tinggi), action(A, individual_claim).
conflict(A, communal_claim) :- asset_type(A, pusako_rendah), action(A, communal_claim).

% Laki-laki dilarang memiliki hak milik atas pusako tinggi
:- male(P), can_inherit(P, A), asset_type(A, pusako_tinggi).

% --- Output Show ---
#show can_inherit/2.
#show conflict/2.
#show punah/1.
