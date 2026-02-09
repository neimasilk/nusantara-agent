import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from src.agents.router import route_query
from src.kg_engine.search import SimpleKGSearch
from src.symbolic.rule_engine import ClingoRuleEngine
from src.agents.orchestrator import build_parallel_orchestrator

try:
    from langchain_core.messages import HumanMessage
except ImportError:
    class HumanMessage:  # type: ignore[no-redef]
        def __init__(self, content: str):
            self.content = content


class JsonGraphRetriever:
    """Adapter graph retrieval berbasis file JSON lokal."""

    def __init__(self, graph_json_path: str):
        self.graph_json_path = graph_json_path
        self._engine = None
        path = Path(graph_json_path)
        if path.exists():
            self._engine = SimpleKGSearch(graph_json_path)

    def retrieve_context(self, query: str, limit: int = 10) -> str:
        if self._engine is None:
            return "Graph context tidak tersedia (fallback lokal aktif)."
        return self._engine.get_context_for_query(query, limit=limit)


class InMemoryVectorRetriever:
    """Adapter vector retrieval sederhana (fallback tanpa Qdrant)."""

    def __init__(self, dokumen: Optional[List[str]] = None):
        self.dokumen = dokumen
        if not self.dokumen:
            # Try loading from JSON corpus
            corpus_path = Path("data/knowledge_base/nasional_corpus.json")
            if corpus_path.exists():
                try:
                    with open(corpus_path, "r", encoding="utf-8") as f:
                        self.dokumen = json.load(f)
                except Exception:
                    self.dokumen = [] # Fallback to default below if error
            
            if not self.dokumen:
                 # Fallback hardcoded
                 self.dokumen = [
                    "KUHPerdata Pasal 830: Pewarisan hanya terjadi karena kematian.",
                    "KUHPerdata Pasal 832: Yang berhak menjadi ahli waris ialah keluarga sedarah.",
                    "Adat Minangkabau membedakan pusako tinggi dan pusako rendah.",
                    "Adat Bali mengenal sistem purusa dan sentana rajeg.",
                    "Adat Jawa modern cenderung sigar semangka dengan musyawarah."
                 ]

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        tokens = {t.lower() for t in query.split() if len(t) > 3}
        if not tokens: return self.dokumen[:top_k]
        scored = []
        for d in self.dokumen:
            score = sum(1 for t in tokens if t in d.lower())
            if score > 0: scored.append((score, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]


class NusantaraAgentPipeline:
    """Unified pipeline untuk query hukum nasional/adat/conflict/consensus."""

    def __init__(
        self,
        rules_dir: str = "src/symbolic/rules",
        graph_json_path: str = "experiments/01_triple_extraction/result.json",
        dokumen_vector: Optional[List[str]] = None,
    ):
        self.rules_dir = Path(rules_dir)
        self.graph_retriever = JsonGraphRetriever(graph_json_path)
        self.vector_retriever = InMemoryVectorRetriever(dokumen_vector)
        self.orchestrator = build_parallel_orchestrator()

        self.rule_files = {
            "nasional": self.rules_dir / "nasional.lp",
            "minangkabau": self.rules_dir / "minangkabau.lp",
            "bali": self.rules_dir / "bali.lp",
            "jawa": self.rules_dir / "jawa.lp",
        }

    def _detect_adat_domains(self, query: str) -> List[str]:
        q = query.lower()
        domains = []
        if any(x in q for x in ["minang", "pusako", "kemenakan", "mamak"]): domains.append("minangkabau")
        if any(x in q for x in ["bali", "purusa", "sanggah", "banjar", "druwe"]): domains.append("bali")
        if any(x in q for x in ["jawa", "gono-gini", "sigar semangka", "ragil", "wekas"]): domains.append("jawa")
        return domains

    def _extract_angka_wasiat(self, query: str) -> Optional[int]:
        match = re.search(r"(\d{1,3})\s*%", query)
        return int(match.group(1)) if match else None

    def _facts_nasional(self, query: str, route_label: str) -> List[str]:
        """Generate facts for nasional.lp rule engine."""
        q = query.lower()
        facts = ["pewaris_meninggal"]
        
        # Detect children
        if "anak" in q:
            facts.append("child(anak_pewaris)")
            facts.append("ada_anak")
        
        # Detect spouse
        if any(x in q for x in ["istri", "suami", "pasangan"]):
            facts.append("spouse(pasangan_hidup)")
            facts.append("menikah_sah")
        
        # Detect parents
        if any(x in q for x in ["orang tua", "ayah", "ibu"]):
            facts.append("parent(orang_tua)")
            facts.append("ada_orangtua")
        
        # Detect siblings
        if any(x in q for x in ["saudara", "kakak", "adik"]):
            facts.append("sibling(saudara_pewaris)")
            facts.append("ada_saudara")
        
        # Wasiat/testament
        if "wasiat" in q:
            facts.append(f"nilai_wasiat({self._extract_angka_wasiat(query) or 40})")
        
        # Debt settlement
        if "utang" in q and ("lunas" in q or "settled" in q or "dibayar" in q):
            facts.append("debt_settled")
        
        # Unfair distribution detection
        if any(x in q for x in ["tidak adil", "melanggar", "diabaikan", "tidak mendapat"]): 
            facts.append("action(harta_waris_pewaris,bagi_tidak_adil_ke_anak)")
        
        # Conflict case: national vs adat rights
        if route_label in {"conflict", "consensus"} and "anak perempuan" in q:
            facts.append("hak_waris_nasional(anak_perempuan,harta_waris_pewaris)")
            facts.append("larangan_waris_adat(anak_perempuan,harta_waris_pewaris)")
        
        return facts

    def _facts_minangkabau(self, query: str) -> List[str]:
        """Generate facts for minangkabau.lp rule engine."""
        q = query.lower()
        facts = []
        
        # Gender facts
        if "anak perempuan" in q or "putri" in q:
            facts.append("female(anak_perempuan)")
        if "anak laki" in q or "putra" in q:
            facts.append("male(anak_laki)")
        if "ibu" in q:
            facts.append("female(ibu)")
        
        # Asset classification
        if "rumah gadang" in q:
            facts.append("asset_type(rumah_gadang, pusako_tinggi)")
            if "jual" in q: facts.append("action(rumah_gadang, sell)")
            if "gadai" in q: facts.append("action(rumah_gadang, pawn)")
            if "hibah" in q: facts.append("action(rumah_gadang, hibah)")
        elif "sawah" in q or "ladang" in q:
            facts.append("asset_type(sawah_ladang, pusako_tinggi)")
            if "jual" in q: facts.append("action(sawah_ladang, sell)")
            if "gadai" in q: facts.append("action(sawah_ladang, pawn)")
        else:
            # Default for tanah ulayat and other communal land
            if "ulayat" in q or "tanah" in q or "tanah pusako" in q:
                facts.append("asset_type(tanah_pusako, pusako_tinggi)")
                if "jual" in q: facts.append("action(tanah_pusako, sell)")
                if "gadai" in q: facts.append("action(tanah_pusako, pawn)")
        
        # Harta pencaharian detection
        if any(x in q for x in ["pencaharian", "hasil kerja", "usaha bersama", "harta bersama"]):
            facts.append("asset_type(harta_pencaharian, pusako_rendah)")
            facts.append("parent(pewaris, anak_pewaris)")
        
        # Consensus detection
        if any(x in q for x in ["mufakat", "setuju", "ijin", "disetujui", "kerapatan"]):
            facts.append("consensus_reached")
        
        # Kemenakan relationship
        if "kemenakan" in q:
            facts.extend([
                "female(ibu_kemenakan)",
                "parent(ibu_kemenakan, kemenakan)",
                "female(kemenakan)"
            ])
        
        # Mamak detection
        if "mamak" in q:
            facts.append("male(mamak)")
            if "kemenakan" in q:
                facts.append("sibling(ibu_kemenakan, mamak)")
        
        return facts

    def _facts_bali(self, query: str, route_label: str) -> List[str]:
        """Generate facts for bali.lp rule engine."""
        q = query.lower()
        facts = []
        
        # Gender and purusa status
        if "putra" in q or "anak laki" in q:
            facts.append("male(putra_ahli_waris)")
            facts.append("kewajiban_ngayah(putra_ahli_waris)")
            facts.append("status_purusa(putra_ahli_waris)")
        
        # Daughter who marries out
        if "anak perempuan" in q or "putri" in q:
            facts.append("female(putri_ahli_waris)")
            if any(x in q for x in ["kawin keluar", "nikah luar", "menikah diluar"]):
                facts.append("kawin_keluar(putri_ahli_waris)")
            if route_label == "conflict":
                facts.append("larangan_waris_adat(putri_ahli_waris, gunakaya)")
        
        # Widow
        if "janda" in q:
            facts.append("janda(istri_pewaris)")
            if any(x in q for x in ["menikah lagi", "nikah lagi", "kawin lagi"]):
                facts.append("menikah_lagi(istri_pewaris)")
        
        # Asset classification
        if "tanah sanggah" in q:
            facts.append("asset_type(tanah_sanggah, druwe_tengah)")
        elif "tanah purusa" in q or "harta purusa" in q:
            facts.append("asset_type(tanah_sanggah, druwe_tengah)")
        elif "druwe tengah" in q:
            facts.append("asset_type(benda_pusaka, druwe_tengah)")
        elif "gunakaya" in q:
            facts.append("asset_type(gunakaya, druwe_gabro)")
        
        # Actions
        if "jual" in q or "menjual" in q:
            facts.append("action(benda_pusaka, sell)")
        
        # Prajuru witness (for adoptions/transfers)
        if any(x in q for x in ["disaksikan", "saksi", "prajuru", "upacara"]):
            facts.append("disaksikan_prajuru")
        
        # Sentana rajeg (appointed heir)
        if "sentana rajeg" in q or "diangkat" in q:
            facts.append("sentana_rajeg(penerus_ahli_waris)")
        
        # Adoption
        if "anak angkat" in q or "adopsi" in q:
            facts.append("adopsi(anak_angkat)")
            if "upacara" in q:
                facts.append("upacara_widhi_widana(anak_angkat)")
            if any(x in q for x in ["saksi", "disaksikan"]):
                facts.append("tri_upasaksi(anak_angkat)")
        
        return facts

    def _facts_jawa(self, query: str) -> List[str]:
        """Generate facts for jawa.lp rule engine."""
        q = query.lower()
        facts = []
        
        # Children detection
        if "anak" in q:
            if "anak laki" in q or "putra" in q:
                facts.append("child(anak_laki)")
                facts.append("male(anak_laki)")
            elif "anak perempuan" in q or "putri" in q:
                facts.append("child(anak_perempuan)")
                facts.append("female(anak_perempuan)")
            else:
                # Generic child
                facts.append("child(anak_pewaris)")
        
        # Gono-gini (marital property)
        if any(x in q for x in ["gono-gini", "gono gini", "harta bersama", "harta perkawinan"]):
            facts.append("asset_type(harta_gono_gini, gono_gini)")
            facts.append("ahli_waris_anak(anak_pewaris)")
        
        # Harta asal (pre-marital property)
        if "harta bawaan" in q or "harta asal" in q:
            facts.append("asset_type(harta_bawaan, harta_asal)")
        
        # Pusaka (family heritage)
        if "pusaka" in q or "rumah induk" in q:
            facts.append("asset_type(harta_pusaka, pusaka)")
            if "jual" in q:
                facts.append("action(harta_pusaka, sell)")
        
        # Adoption
        if "anak angkat" in q or "adopsi" in q:
            facts.append("anak_angkat(anak_angkat)")
            if "terang tunai" in q or "sah" in q:
                facts.append("adopsi_terang_tunai(anak_angkat)")
        
        # Step child
        if "anak tiri" in q:
            facts.append("anak_tiri(anak_tiri)")
        
        # Child out of wedlock
        if "anak luar kawin" in q or "anak di luar nikah" in q:
            facts.append("anak_luar_kawin(anak_luar_kawin)")
            if "pengesahan" in q or "bukti" in q:
                facts.append("bukti_darah_ayah(anak_luar_kawin)")
        
        # Widow/widower
        if "janda" in q:
            facts.append("janda(istri_pewaris)")
            if any(x in q for x in ["menikah lagi", "nikah lagi", "kawin lagi"]):
                facts.append("menikah_lagi(istri_pewaris)")
                if "gono-gini" in q or "harta bersama" in q:
                    facts.append("action(harta_gono_gini, hold_without_distribution)")
        
        if "duda" in q:
            facts.append("duda(suami_pewaris)")
            if any(x in q for x in ["menikah lagi", "nikah lagi", "kawin lagi"]):
                facts.append("menikah_lagi(suami_pewaris)")
        
        # Anak ragil (youngest child who stays)
        if "ragil" in q or "bungsu" in q or "penunggu rumah" in q:
            facts.append("anak_ragil(anak_bungsu)")
            facts.append("penunggu_rumah(anak_bungsu)")
        
        # Child who cares for parents
        if any(x in q for x in ["merawat", "menjaga", "tinggal serumah", "pengabdian"]):
            facts.append("merawat_orangtua(anak_perawat)")
        
        # Islamic inheritance mode
        if any(x in q for x in ["islam", "faraidh", "faraid", "hukum islam"]):
            facts.append("faraidh_mode")
        
        # Divorce
        if "cerai" in q or "perceraian" in q:
            facts.append("cerai_hidup")
        
        # Grandchild replacement (gantungan siwur)
        if "cucu" in q and ("ganti" in q or "pengganti" in q or "ayahnya sudah meninggal" in q):
            facts.append("cucu_pengganti(cucu_pengganti)")
            facts.append("orangtua_meninggal_lebih_dulu(orangtua_cucu)")
            facts.append("parent(orangtua_cucu, cucu_pengganti)")
        
        # Takharuj (family agreement)
        if any(x in q for x in ["musyawarah", "mufakat", "takharuj", "kesepakatan keluarga"]):
            facts.append("takharuj_disepakati")
        
        return facts

    @staticmethod
    def _parse_fact(fact: str) -> Tuple[str, List[str]]:
        cleaned = fact.strip().rstrip(".")
        if "(" not in cleaned or not cleaned.endswith(")"):
            return cleaned, []
        predicate, args_part = cleaned.split("(", 1)
        args = [arg.strip() for arg in args_part[:-1].split(",") if arg.strip()]
        return predicate.strip(), args

    def _run_rules_fallback(self, domain: str, facts: List[str]) -> List[str]:
        """Fallback rule evaluation saat clingo belum tersedia di environment."""
        parsed: Dict[str, List[List[str]]] = {}
        for fact in facts:
            predicate, args = self._parse_fact(fact)
            parsed.setdefault(predicate, []).append(args)

        atoms: List[str] = []

        if domain == "nasional":
            if "child" in parsed or "ada_anak" in parsed:
                atoms.append("berhak_waris(anak_pewaris)")
            if "spouse" in parsed and ("menikah_sah" in parsed or "spouse" in parsed):
                atoms.append("berhak_waris(pasangan_hidup)")
                atoms.append("bagian_spouse(pasangan_hidup,seperdua_harta_bersama)")
                atoms.append("hak_spouse_atas_harta_bersama(pasangan_hidup)")

            for args in parsed.get("nilai_wasiat", []):
                try:
                    if args and int(args[0]) > 33:
                        atoms.append("conflict(wasiat,melebihi_batas_wajar)")
                except ValueError:
                    continue

            if "hak_waris_nasional" in parsed and "larangan_waris_adat" in parsed:
                atoms.append("conflict_norm(nasional_vs_adat,dummy,dummy)")

            for args in parsed.get("action", []):
                if len(args) >= 2 and args[1] == "bagi_tidak_adil_ke_anak":
                    atoms.append("conflict(harta_waris_pewaris,pembagian_tidak_adil)")

            if not atoms and facts:
                atoms.append("fakta_nasional_terbaca")
            return atoms

        if domain == "minangkabau":
            for args in parsed.get("asset_type", []):
                if len(args) >= 2 and args[1] == "pusako_tinggi":
                    for action_args in parsed.get("action", []):
                        if len(action_args) >= 2 and action_args[1] in {"sell", "pawn"}:
                            atoms.append(f"conflict({action_args[0]},{action_args[1]})")

            if "asset_type" in parsed and "parent" in parsed:
                if any(len(args) >= 2 and args[0] == "harta_pencaharian" for args in parsed["asset_type"]):
                    atoms.append("can_inherit(anak_pewaris,harta_pencaharian)")

            if "kemenakan" in "".join(",".join(args) for args in parsed.get("female", [])):
                atoms.append("can_inherit(kemenakan,tanah_pusako)")

            if not atoms and facts:
                atoms.append("fakta_minangkabau_terbaca")
            return atoms

        if domain == "bali":
            female_targets = {args[0] for args in parsed.get("female", []) if args}
            kawin_keluar_targets = {args[0] for args in parsed.get("kawin_keluar", []) if args}
            for person in sorted(female_targets.intersection(kawin_keluar_targets)):
                atoms.append(f"ahli_waris_terbatas({person})")
                atoms.append(f"can_inherit({person},harta_druwe_gabro)")

            male_targets = {args[0] for args in parsed.get("male", []) if args}
            purusa_targets = {args[0] for args in parsed.get("status_purusa", []) if args}
            ngayah_targets = {args[0] for args in parsed.get("kewajiban_ngayah", []) if args}
            for person in sorted(male_targets.intersection(purusa_targets).intersection(ngayah_targets)):
                atoms.append(f"can_inherit({person},harta_druwe_gabro)")

            for action_args in parsed.get("action", []):
                if len(action_args) >= 2 and action_args[1] == "sell":
                    atoms.append(f"conflict({action_args[0]},sell)")

            if "sentana_rajeg" in parsed:
                for args in parsed["sentana_rajeg"]:
                    if args:
                        atoms.append(f"can_inherit({args[0]},harta_druwe_gabro)")

            if not atoms and facts:
                atoms.append("fakta_bali_terbaca")
            return atoms

        if domain == "jawa":
            children = [args[0] for args in parsed.get("child", []) if args]
            if len(children) >= 1:
                for child in children:
                    atoms.append(f"can_inherit({child},harta_gono_gini)")
            if len(children) >= 2:
                atoms.append(f"equal_share({children[0]},{children[1]},harta_gono_gini)")

            if "anak_angkat" in parsed and "adopsi_terang_tunai" in parsed:
                atoms.append("can_inherit(anak_angkat,harta_gono_gini)")

            if ("janda" in parsed or "duda" in parsed) and "menikah_lagi" in parsed:
                person = "pasangan_hidup"
                if parsed.get("janda") and parsed["janda"][0]:
                    person = parsed["janda"][0][0]
                elif parsed.get("duda") and parsed["duda"][0]:
                    person = parsed["duda"][0][0]
                atoms.append(f"pecah_panci({person})")
                atoms.append("conflict(harta_gono_gini,hold_without_distribution)")

            if not atoms and facts:
                atoms.append("fakta_jawa_terbaca")
            return atoms

        return atoms

    def _run_rules(self, domain: str, facts: List[str]) -> List[str]:
        lp_file = self.rule_files.get(domain)
        if not lp_file or not lp_file.exists(): return []
        try:
            engine = ClingoRuleEngine(lp_file=str(lp_file))
        except ImportError:
            return self._run_rules_fallback(domain, facts)
        for fact in facts: engine.add_fact(fact)
        models = engine.solve()
        return models[0] if models else []

    def process_query(self, query: str) -> Dict:
        route = route_query(query, use_llm=False)
        label = route["label"]
        nat_atoms = []
        adat_atoms = {}

        if label in {"pure_national", "conflict", "consensus"}:
            nat_atoms = self._run_rules("nasional", self._facts_nasional(query, label))

        if label in {"pure_adat", "conflict", "consensus"}:
            domains = self._detect_adat_domains(query) or ["minangkabau", "bali", "jawa"]
            for d in domains:
                if d == "minangkabau": facts = self._facts_minangkabau(query)
                elif d == "bali": facts = self._facts_bali(query, label)
                else: facts = self._facts_jawa(query)
                adat_atoms[d] = self._run_rules(d, facts)

        graph_ctx = self.graph_retriever.retrieve_context(query)
        vec_results = self.vector_retriever.retrieve(query, top_k=3)
        vec_ctx = " ".join(vec_results)

        inputs = {
            "messages": [HumanMessage(content=query)],
            "rule_results": {"nasional": nat_atoms, "adat": adat_atoms},
            "retrieval_context": f"Graph: {graph_ctx}\nVector: {vec_ctx}"
        }
        
        # Rebuild orchestrator with current route label (ART-092)
        self.orchestrator = build_parallel_orchestrator(route_label=label)
        agent_result = self.orchestrator.invoke(inputs)

        return {
            "query": query,
            "route": route,
            "rule_results": inputs["rule_results"],
            "agent_analysis": agent_result.get("final_synthesis", ""),
            "graph_context": graph_ctx,
            "vector_context": vec_results,
            "intermediate_context": {
                "national": agent_result.get("national_context", ""),
                "adat": agent_result.get("adat_context", "")
            }
        }

def run_nusantara_query(query: str) -> Dict:
    pipeline = NusantaraAgentPipeline()
    return pipeline.process_query(query)
