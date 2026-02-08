import re
from pathlib import Path
from typing import Dict, List, Optional

from src.agents.router import route_query
from src.kg_engine.search import SimpleKGSearch
from src.symbolic.rule_engine import ClingoRuleEngine


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
        self.dokumen = dokumen or []

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        if not self.dokumen:
            return []
        tokens = {t.lower() for t in query.split() if len(t) > 3}
        if not tokens:
            return self.dokumen[:top_k]

        scored = []
        for doc in self.dokumen:
            d = doc.lower()
            score = sum(1 for t in tokens if t in d)
            if score > 0:
                scored.append((score, doc))
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
        self.vector_retriever = InMemoryVectorRetriever(
            dokumen_vector
            or [
                "KUHPerdata mengatur prioritas ahli waris, legitime portie, dan pembagian harta waris.",
                "Adat Minangkabau membedakan pusako tinggi dan pusako rendah dalam pewarisan.",
                "Adat Bali mengenal sistem purusa, sentana rajeg, dan pembatasan transfer druwe tengah.",
                "Adat Jawa modern cenderung sigar semangka dengan musyawarah keluarga.",
            ]
        )

        self.rule_files = {
            "nasional": self.rules_dir / "nasional.lp",
            "minangkabau": self.rules_dir / "minangkabau.lp",
            "bali": self.rules_dir / "bali.lp",
            "jawa": self.rules_dir / "jawa.lp",
        }

    def _detect_adat_domains(self, query: str) -> List[str]:
        q = query.lower()
        domains = []
        if "minang" in q or "minangkabau" in q or "pusako" in q or "kemenakan" in q:
            domains.append("minangkabau")
        if "bali" in q or "purusa" in q or "sanggah" in q or "banjar" in q:
            domains.append("bali")
        if "jawa" in q or "gono-gini" in q or "sigar semangka" in q or "ragil" in q:
            domains.append("jawa")
        return domains

    def _extract_angka_wasiat(self, query: str) -> Optional[int]:
        match = re.search(r"(\d{1,3})\s*%", query)
        if not match:
            return None
        return int(match.group(1))

    def _facts_nasional(self, query: str, route_label: str) -> List[str]:
        q = query.lower()
        facts = []
        if "anak" in q:
            facts.append("child(anak)")
        if "istri" in q or "suami" in q or "pasangan" in q:
            facts.extend(["spouse(pasangan)", "menikah_sah"])
        if "orang tua" in q or "ayah" in q or "ibu" in q:
            facts.append("parent(orangtua)")
        if "wasiat" in q:
            persen = self._extract_angka_wasiat(query) or 40
            facts.append(f"nilai_wasiat({persen})")
        if "utang" in q and "belum" in q:
            facts.append("action(harta_waris_pewaris,dibagi)")
        if route_label in {"conflict", "consensus"} and "anak perempuan" in q:
            facts.append("hak_waris_nasional(anak_perempuan,harta_waris_pewaris)")
        if not facts and route_label in {"pure_national", "conflict", "consensus"}:
            # Fallback agar reasoning nasional tetap jalan untuk query umum.
            facts.append("child(anak)")
        return facts

    def _facts_minangkabau(self, query: str) -> List[str]:
        q = query.lower()
        facts = ["female(anak_perempuan)", "male(anak_laki)"]
        if "jual" in q or "gadai" in q:
            facts.append("action(rumah_gadang,sell)")
        if "kemenakan" in q:
            facts.extend(["female(ibu_mamak)", "sibling(ibu_mamak,mamak)", "parent(ibu_mamak,kemenakan_perempuan)", "female(kemenakan_perempuan)"])
        return facts

    def _facts_bali(self, query: str, route_label: str) -> List[str]:
        q = query.lower()
        facts = ["male(putra)", "kewajiban_ngayah(putra)"]
        if "anak perempuan" in q:
            facts.extend(["female(putri)", "kawin_keluar(putri)"])
            if route_label == "conflict":
                facts.append("larangan_waris_adat(anak_perempuan,harta_waris_pewaris)")
        if "janda" in q:
            facts.append("janda(istri)")
        if "jual" in q and ("pusaka" in q or "sanggah" in q):
            facts.append("action(harta_pusaka,sell)")
        return facts

    def _facts_jawa(self, query: str) -> List[str]:
        q = query.lower()
        facts = ["child(anak_laki)", "male(anak_laki)", "child(anak_perempuan)", "female(anak_perempuan)"]
        if "anak angkat" in q:
            facts.extend(["anak_angkat(anak_angkat1)", "adopsi_terang_tunai(anak_angkat1)"])
        if "janda" in q and "menikah lagi" in q:
            facts.extend(["janda(istri)", "menikah_lagi(istri)", "action(harta_gono_gini,hold_without_distribution)"])
        return facts

    def _run_rules(self, domain: str, facts: List[str]) -> List[str]:
        lp_file = self.rule_files.get(domain)
        if lp_file is None or not lp_file.exists():
            return []
        engine = ClingoRuleEngine(lp_file=str(lp_file))
        for fact in facts:
            engine.add_fact(fact)
        models = engine.solve()
        return models[0] if models else []

    def process_query(self, query: str) -> Dict:
        route = route_query(query, use_llm=False)
        label = route["label"]

        national_atoms: List[str] = []
        adat_atoms: Dict[str, List[str]] = {}

        if label in {"pure_national", "conflict", "consensus"}:
            national_atoms = self._run_rules("nasional", self._facts_nasional(query, label))

        if label in {"pure_adat", "conflict", "consensus"}:
            domains = self._detect_adat_domains(query)
            if not domains:
                domains = ["minangkabau", "bali", "jawa"]
            for domain in domains:
                if domain == "minangkabau":
                    facts = self._facts_minangkabau(query)
                elif domain == "bali":
                    facts = self._facts_bali(query, label)
                else:
                    facts = self._facts_jawa(query)
                adat_atoms[domain] = self._run_rules(domain, facts)

        graph_context = self.graph_retriever.retrieve_context(query)
        vector_context = self.vector_retriever.retrieve(query, top_k=3)

        return {
            "query": query,
            "route": route,
            "graph_context": graph_context,
            "vector_context": vector_context,
            "rule_results": {
                "nasional": national_atoms,
                "adat": adat_atoms,
            },
        }


def run_nusantara_query(query: str) -> Dict:
    pipeline = NusantaraAgentPipeline()
    return pipeline.process_query(query)
