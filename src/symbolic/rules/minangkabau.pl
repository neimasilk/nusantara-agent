% Minangkabau inheritance rules (DRAFT, needs human verification)
% Facts & simple rules for early experiments.

% Lineage
matrilineal.

% Asset classification
pusako_tinggi_asset(rumah_gadang).
pusako_tinggi_asset(sawah_ladang).
pusako_tinggi_asset(hutan_tanah).
pusako_tinggi_asset(pandam_pakuburan).
pusako_tinggi_asset(luak_tapian).
pusako_tinggi_asset(dangau_paladangan).

pusako_rendah_asset(harta_pencaharian).
pusako_rendah_asset(hibah).
pusako_rendah_asset(hadiah).

% Ownership & distribution
ownership(pusako_tinggi, komunal).
ownership(pusako_rendah, komunal).
distribution(pusako_rendah, musyawarah_keluarga).
distribution(pusako_rendah, faraidh).

% Heir roles
heir_role(pusako_tinggi, anak_perempuan).
heir_role(pusako_tinggi, kemenakan).
heir_role(pusako_rendah, anak_laki_laki).
heir_role(pusako_rendah, anak_perempuan).

% Governance
supervision(pusako_tinggi, mamak).
management(pusako_tinggi, perempuan).

% Restrictions
no_external_interference(pusako_tinggi).
transfer_requires_consensus(pusako_tinggi).

% Dispute resolution
dispute_resolution(sengketa_adat, musyawarah_keluarga).
dispute_resolution(sengketa_adat, pengadilan_adat_nagari).

% Derived rules
eligible_heir(Asset, Role) :- heir_role(Asset, Role).

% Example constraint: pusako_tinggi tidak diwariskan ke anak_laki_laki
not_eligible_heir(pusako_tinggi, anak_laki_laki).
