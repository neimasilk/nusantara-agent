% Minangkabau inheritance rules (DRAFT, needs human verification)
% Logic for neuro-symbolic reasoning experiments.

% --- Facts ---
matrilineal.

% Gender facts (to be asserted at runtime)
% female(Person).
% male(Person).

% Asset classification
asset_type(rumah_gadang, pusako_tinggi).
asset_type(sawah_ladang, pusako_tinggi).
asset_type(hutan_tanah, pusako_tinggi).
asset_type(harta_pencaharian, pusako_rendah).
asset_type(hibah, pusako_rendah).

% Ownership
ownership_type(pusako_tinggi, komunal).
ownership_type(pusako_rendah, keluarga_inti).

% --- Inference Rules ---

% Pusako Tinggi: Hanya perempuan dalam garis matrilineal yang mewarisi hak pakai
can_inherit(Person, Asset) :-
    asset_type(Asset, pusako_tinggi),
    female(Person).

% Pusako Rendah: Anak laki-laki dan perempuan berhak (mengikuti kesepakatan/faraidh)
can_inherit(Person, Asset) :-
    asset_type(Asset, pusako_rendah),
    (female(Person) ; male(Person)).

% Role checking
is_mamak_kepala_waris(Person) :-
    male(Person),
    % Di dunia nyata, ini butuh pengecekan silsilah (anak laki-laki tertua garis ibu)
    % Untuk eksperimen awal, kita asumsikan jika male maka bisa jadi mamak jika tertua
    true.

% Conflict Detection: Penjualan pusako tinggi tanpa konsensus
conflict(Asset, sell) :-
    asset_type(Asset, pusako_tinggi),
    \+ consensus_reached.

% Dispute Resolution path
resolution_step(sengketa_adat, 1, musyawarah_keluarga).
resolution_step(sengketa_adat, 2, pengadilan_adat_nagari).

% --- Helper Rules ---
status_waris(Asset, "Hanya untuk Perempuan") :- asset_type(Asset, pusako_tinggi).
status_waris(Asset, "Laki-laki & Perempuan") :- asset_type(Asset, pusako_rendah).
