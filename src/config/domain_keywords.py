"""Single source of truth for keyword lists used across routing/orchestration/pipeline."""

# Router (src/agents/router.py)
ROUTER_NATIONAL_KEYWORDS = (
    "kuhperdata",
    "perdata",
    "hukum nasional",
    "yurisprudensi",
    "mahkamah agung",
    "putusan",
    "perjanjian",
    "wanprestasi",
    "gono-gini",
    "harta bersama",
)

ROUTER_ADAT_KEYWORDS = (
    "adat",
    "minangkabau",
    "bali",
    "jawa",
    "pusako",
    "mamak",
    "kemenakan",
    "ulayat",
    "banjar",
    "sentana",
    "drue",
    "drue tengah",
)

ROUTER_CONFLICT_KEYWORDS = (
    "konflik",
    "bertentangan",
    "vs",
    "versus",
    "bertabrakan",
    "pluralisme",
)

# Requested top-level aliases
NATIONAL_KEYWORDS = ROUTER_NATIONAL_KEYWORDS
CONFLICT_KEYWORDS = ROUTER_CONFLICT_KEYWORDS

# Orchestrator domain-trigger keywords (src/agents/orchestrator.py)
SUPERVISOR_MINANG_KEYWORDS = ("minang", "pusako", "kemenakan", "mamak", "kaum")
SUPERVISOR_BALI_KEYWORDS = ("bali", "purusa", "sanggah", "druwe", "sentana")
SUPERVISOR_JAWA_KEYWORDS = ("jawa", "gono-gini", "ragil", "wekas", "sigar")
SUPERVISOR_NATIONAL_KEYWORDS = (
    "ham",
    "uu ",
    "undang",
    "mahkamah konstitusi",
    "mdp",
    "putusan",
    "sertifikat",
    "shm",
    "poligami",
    "cerai",
    "perceraian",
    "kua",
    "pengadilan",
)
SUPERVISOR_HAM_EXTREME_KEYWORDS = (
    "dilarang bersekolah",
    "tidak boleh sekolah",
    "larangan sekolah",
    "kesehatan",
    "puskesmas",
)
SUPERVISOR_MK_MDP_KEYWORDS = ("mdp", "mahkamah konstitusi", "putusan mk")

# Orchestrator offline decision keywords (src/agents/orchestrator.py)
HAM_EXTREME_KEYWORDS = (
    "dilarang bersekolah",
    "tidak boleh sekolah",
    "larangan sekolah",
    "kesehatan",
    "puskesmas",
    "di bawah umur",
    "batas minimal",
)
NATIONAL_DOMINANT_KEYWORDS = (
    "paspor",
    "imigrasi",
    "catatan sipil",
    "penetapan pengadilan",
    "poligami",
    "perceraian",
)
OFFLINE_NATIONAL_KEYWORDS = (
    "kuhperdata",
    "uu ",
    "undang",
    "pengadilan",
    "putusan",
    "shm",
    "poligami",
    "cerai",
    "paspor",
    "administrasi",
    "akta",
)
OFFLINE_ADAT_KEYWORDS = (
    "adat",
    "minang",
    "pusako",
    "kemenakan",
    "mamak",
    "ulayat",
    "bali",
    "mdp",
    "jawa",
    "wekas",
    "ragil",
    "nyentana",
)
OFFLINE_CONFLICT_KEYWORDS = (
    "konflik",
    "vs",
    "versus",
    "bertentangan",
    "sengketa",
    "ulayat",
    "shm",
    "wekas",
    "nyentana",
    "legitime",
    "mdp",
)
OFFLINE_ADMIN_CASE_KEYWORDS = (
    "paspor",
    "akta",
    "catatan sipil",
    "administrasi",
    "dokumen",
)

# Pipeline domain detection keywords (src/pipeline/nusantara_agent.py)
ADAT_KEYWORDS = {
    "minangkabau": ("minang", "pusako", "kemenakan", "mamak"),
    "bali": ("bali", "purusa", "sanggah", "banjar", "druwe"),
    "jawa": ("jawa", "gono-gini", "sigar semangka", "ragil", "wekas"),
}

# Pipeline facts: national
NASIONAL_SPOUSE_KEYWORDS = ("istri", "suami", "pasangan")
NASIONAL_PARENT_KEYWORDS = ("orang tua", "ayah", "ibu")
NASIONAL_SIBLING_KEYWORDS = ("saudara", "kakak", "adik")
NASIONAL_DEBT_SETTLED_KEYWORDS = ("lunas", "settled", "dibayar")
NASIONAL_UNFAIR_DISTRIBUTION_KEYWORDS = ("tidak adil", "melanggar", "diabaikan", "tidak mendapat")

# Pipeline facts: Minangkabau
MINANG_FEMALE_CHILD_KEYWORDS = ("anak perempuan", "putri")
MINANG_MALE_CHILD_KEYWORDS = ("anak laki", "putra")
MINANG_SAWAH_LADANG_KEYWORDS = ("sawah", "ladang")
MINANG_ULAYAT_LAND_KEYWORDS = ("ulayat", "tanah", "tanah pusako")
MINANG_HARTA_PENCAHARIAN_KEYWORDS = ("pencaharian", "hasil kerja", "usaha bersama", "harta bersama")
MINANG_CONSENSUS_KEYWORDS = ("mufakat", "setuju", "ijin", "disetujui", "kerapatan")

# Pipeline facts: Bali
BALI_MALE_CHILD_KEYWORDS = ("putra", "anak laki")
BALI_FEMALE_CHILD_KEYWORDS = ("anak perempuan", "putri")
BALI_KAWIN_KELUAR_KEYWORDS = ("kawin keluar", "nikah luar", "menikah diluar")
BALI_REMARRIAGE_KEYWORDS = ("menikah lagi", "nikah lagi", "kawin lagi")
BALI_PURUSA_ASSET_KEYWORDS = ("tanah purusa", "harta purusa")
BALI_SELL_ACTION_KEYWORDS = ("jual", "menjual")
BALI_WITNESS_KEYWORDS = ("disaksikan", "saksi", "prajuru", "upacara")
BALI_ADOPTION_WITNESS_KEYWORDS = ("saksi", "disaksikan")
BALI_SENTANA_KEYWORDS = ("sentana rajeg", "diangkat")
BALI_ADOPTION_KEYWORDS = ("anak angkat", "adopsi")

# Pipeline facts: Jawa
JAWA_MALE_CHILD_KEYWORDS = ("anak laki", "putra")
JAWA_FEMALE_CHILD_KEYWORDS = ("anak perempuan", "putri")
JAWA_GONO_GINI_KEYWORDS = ("gono-gini", "gono gini", "harta bersama", "harta perkawinan")
JAWA_HARTA_ASAL_KEYWORDS = ("harta bawaan", "harta asal")
JAWA_PUSAKA_KEYWORDS = ("pusaka", "rumah induk")
JAWA_ADOPTION_KEYWORDS = ("anak angkat", "adopsi")
JAWA_ADOPTION_VALID_KEYWORDS = ("terang tunai", "sah")
JAWA_CHILD_OUTSIDE_MARRIAGE_KEYWORDS = ("anak luar kawin", "anak di luar nikah")
JAWA_PATERNAL_PROOF_KEYWORDS = ("pengesahan", "bukti")
JAWA_REMARRIAGE_KEYWORDS = ("menikah lagi", "nikah lagi", "kawin lagi")
JAWA_RAGIL_KEYWORDS = ("ragil", "bungsu", "penunggu rumah")
JAWA_CARE_KEYWORDS = ("merawat", "menjaga", "tinggal serumah", "pengabdian")
JAWA_ISLAMIC_MODE_KEYWORDS = ("islam", "faraidh", "faraid", "hukum islam")
JAWA_DIVORCE_KEYWORDS = ("cerai", "perceraian")
JAWA_GRANDCHILD_REPLACEMENT_KEYWORDS = ("ganti", "pengganti", "ayahnya sudah meninggal")
JAWA_TAKHARUJ_KEYWORDS = ("musyawarah", "mufakat", "takharuj", "kesepakatan keluarga")
