"""Unit tests untuk supervisor decision logic di orchestrator.py."""
import unittest


class OfflineSupervisorDecisionTests(unittest.TestCase):
    """Test _offline_supervisor_decision — the core label-producing heuristic."""

    def _decide(self, query, rules=None, route_label="consensus"):
        from src.agents.orchestrator import _offline_supervisor_decision
        if rules is None:
            rules = {}
        return _offline_supervisor_decision(query, rules, route_label)

    # --- HAM Extreme → A ---

    def test_ham_extreme_sekolah(self):
        """HAM extreme: larangan sekolah → A (nasional)."""
        r = self._decide("Anak dilarang bersekolah karena sanksi adat")
        self.assertEqual(r["label"], "A")

    def test_ham_extreme_puskesmas(self):
        """HAM extreme: akses puskesmas → A."""
        r = self._decide("Warga tidak boleh ke puskesmas desa")
        self.assertEqual(r["label"], "A")

    def test_ham_takes_precedence_over_conflict(self):
        """HAM extreme overrides symbolic conflict."""
        rules = {"nasional": ["conflict(x,y)"]}
        r = self._decide("Anak dilarang bersekolah oleh adat", rules, "conflict")
        self.assertEqual(r["label"], "A")

    # --- Symbolic conflict → C ---

    def test_symbolic_conflict_detected(self):
        """Rule engine detects conflict → C."""
        rules = {"nasional": ["conflict(harta_waris,pembagian)"]}
        r = self._decide("Pembagian harta waris", rules, "consensus")
        self.assertEqual(r["label"], "C")

    def test_symbolic_conflict_in_adat_domain(self):
        """Adat atoms with conflict → C."""
        rules = {"adat": {"minangkabau": ["conflict(tanah_ulayat,sell)"]}}
        r = self._decide("Jual tanah ulayat", rules, "pure_adat")
        self.assertEqual(r["label"], "C")

    # --- Route: pure_national → A ---

    def test_pure_national_route(self):
        """Router says pure_national, no symbolic conflict → A."""
        r = self._decide("Kasus KUHPerdata biasa", {}, "pure_national")
        self.assertEqual(r["label"], "A")

    # --- Route: pure_adat → B ---

    def test_pure_adat_route_simple(self):
        """Router says pure_adat, no conflict keywords → B."""
        r = self._decide("Warisan adat Minangkabau sederhana", {}, "pure_adat")
        self.assertEqual(r["label"], "B")

    def test_pure_adat_but_national_and_conflict_keywords(self):
        """pure_adat route but national + conflict keywords → C."""
        r = self._decide(
            "Tanah ulayat adat vs putusan pengadilan, sengketa panjang",
            {},
            "pure_adat",
        )
        self.assertEqual(r["label"], "C")

    # --- Route: conflict → C or A ---

    def test_conflict_route_general(self):
        """Router says conflict, no admin case → C."""
        r = self._decide("Sengketa waris adat vs nasional", {}, "conflict")
        self.assertEqual(r["label"], "C")

    def test_conflict_route_admin_case(self):
        """Router says conflict but admin case without symbolic conflict → A."""
        r = self._decide("Urusan paspor dan dokumen administrasi", {}, "conflict")
        self.assertEqual(r["label"], "A")

    # --- Route: consensus → depends on keywords/atoms ---

    def test_consensus_national_keywords_only(self):
        """Consensus route, only national keywords → A."""
        r = self._decide("Putusan pengadilan tentang undang-undang perdata", {}, "consensus")
        self.assertEqual(r["label"], "A")

    def test_consensus_adat_keywords_only(self):
        """Consensus route, only adat keywords → B."""
        r = self._decide("Tradisi adat Minangkabau tentang pusako", {}, "consensus")
        self.assertEqual(r["label"], "B")

    def test_consensus_both_symbolic_outputs(self):
        """Consensus route, both nasional and adat atoms → C."""
        rules = {
            "nasional": ["berhak_waris(andi)"],
            "adat": {"minangkabau": ["can_inherit(andi,pusako)"]},
        }
        r = self._decide("Hak waris andi", rules, "consensus")
        self.assertEqual(r["label"], "C")

    def test_consensus_no_signals_defaults_D(self):
        """Consensus route, no keywords, no atoms → D."""
        r = self._decide("Situasi tidak jelas", {}, "consensus")
        self.assertEqual(r["label"], "D")

    def test_consensus_only_nasional_atoms(self):
        """Consensus route, only nasional atoms → A."""
        rules = {"nasional": ["berhak_waris(sari)"]}
        r = self._decide("Hak waris seseorang", rules, "consensus")
        self.assertEqual(r["label"], "A")

    def test_consensus_only_adat_atoms(self):
        """Consensus route, only adat atoms → B."""
        rules = {"adat": {"bali": ["can_inherit(putra,druwe_gabro)"]}}
        r = self._decide("Hak waris putra", rules, "consensus")
        self.assertEqual(r["label"], "B")

    # --- HAM Extreme: expanded keywords → A ---

    def test_ham_extreme_di_bawah_umur(self):
        """HAM extreme: di bawah umur → A (nasional)."""
        r = self._decide("Perkawinan anak di bawah umur menurut adat")
        self.assertEqual(r["label"], "A")

    def test_ham_extreme_batas_minimal(self):
        """HAM extreme: batas minimal usia → A."""
        r = self._decide("Batas minimal usia pernikahan adat")
        self.assertEqual(r["label"], "A")

    # --- National dominant → A (unless symbolic conflict) ---

    def test_national_dominant_paspor(self):
        """National dominant: paspor → A."""
        r = self._decide("Pembuatan paspor untuk anak dari pernikahan adat")
        self.assertEqual(r["label"], "A")

    def test_national_dominant_catatan_sipil(self):
        """National dominant: catatan sipil → A."""
        r = self._decide("Pencatatan sipil perkawinan adat Bali")
        self.assertEqual(r["label"], "A")

    def test_national_dominant_perceraian(self):
        """National dominant: perceraian → A."""
        r = self._decide("Perceraian dalam konteks adat Jawa")
        self.assertEqual(r["label"], "A")

    def test_national_dominant_overridden_by_symbolic_conflict(self):
        """National dominant overridden when symbolic conflict exists."""
        rules = {"nasional": ["conflict(perkawinan,adat)"]}
        r = self._decide("Pencatatan sipil perkawinan adat", rules)
        self.assertEqual(r["label"], "C")

    # --- Output format ---

    def test_output_has_required_keys(self):
        """Output dict has all required keys."""
        r = self._decide("Test query")
        for key in ["label", "langkah_keputusan", "alasan_utama", "konflik_terdeteksi"]:
            self.assertIn(key, r)

    def test_label_values_are_valid(self):
        """Labels are always A, B, C, or D."""
        test_cases = [
            ("Dilarang bersekolah", {}, "consensus"),
            ("Warisan adat", {}, "pure_adat"),
            ("KUHPerdata", {}, "pure_national"),
            ("Sengketa", {}, "conflict"),
            ("Tidak jelas", {}, "consensus"),
        ]
        for query, rules, route in test_cases:
            r = self._decide(query, rules, route)
            self.assertIn(r["label"], ["A", "B", "C", "D"], f"Invalid label for: {query}")

    def test_konflik_field_when_label_C(self):
        """konflik_terdeteksi should be 'Ya' when label is C."""
        rules = {"nasional": ["conflict(x,y)"]}
        r = self._decide("Test conflict", rules, "consensus")
        self.assertEqual(r["konflik_terdeteksi"], "Ya")


class OfflineOrchestratorTests(unittest.TestCase):
    """Test _OfflineOrchestrator.invoke() end-to-end."""

    def test_invoke_returns_required_keys(self):
        """invoke() returns national_context, adat_context, final_synthesis."""
        from src.agents.orchestrator import _OfflineOrchestrator
        orch = _OfflineOrchestrator(route_label="consensus")
        state = {"messages": [type("M", (), {"content": "Test query"})()]}
        result = orch.invoke(state)
        self.assertIn("national_context", result)
        self.assertIn("adat_context", result)
        self.assertIn("final_synthesis", result)

    def test_invoke_empty_state(self):
        """invoke() handles empty state gracefully."""
        from src.agents.orchestrator import _OfflineOrchestrator
        orch = _OfflineOrchestrator()
        result = orch.invoke({})
        self.assertIn("final_synthesis", result)


class FlattenAdatAtomsTests(unittest.TestCase):
    """Test _flatten_adat_atoms helper."""

    def _flatten(self, adat_output):
        from src.agents.orchestrator import _flatten_adat_atoms
        return _flatten_adat_atoms(adat_output)

    def test_empty_dict(self):
        self.assertEqual(self._flatten({}), [])

    def test_single_domain(self):
        result = self._flatten({"minangkabau": ["atom1", "atom2"]})
        self.assertEqual(result, ["atom1", "atom2"])

    def test_multiple_domains(self):
        result = self._flatten({
            "minangkabau": ["a1"],
            "bali": ["b1", "b2"],
        })
        self.assertEqual(len(result), 3)

    def test_non_dict_input(self):
        self.assertEqual(self._flatten("not a dict"), [])

    def test_non_list_values(self):
        result = self._flatten({"domain": "not a list"})
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
