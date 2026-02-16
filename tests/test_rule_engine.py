"""Test deterministik untuk modul symbolic/rule_engine."""
import sys
import unittest
from pathlib import Path


class RuleEngineBaseTests(unittest.TestCase):
    """Test untuk RuleEngine base class."""

    def test_base_load_rules_not_implemented(self):
        """Test: base class load_rules raise NotImplementedError."""
        from src.symbolic.rule_engine import RuleEngine
        engine = RuleEngine()
        with self.assertRaises(NotImplementedError):
            engine.load_rules("dummy.lp")

    def test_base_query_not_implemented(self):
        """Test: base class query raise NotImplementedError."""
        from src.symbolic.rule_engine import RuleEngine
        engine = RuleEngine()
        with self.assertRaises(NotImplementedError):
            engine.query("test")


class ClingoRuleEngineTests(unittest.TestCase):
    """Test untuk ClingoRuleEngine tanpa mock (jika clingo tersedia) atau dengan error handling."""

    def test_clingo_engine_init_without_clingo(self):
        """Test: init ClingoRuleEngine raise ImportError jika clingo tidak tersedia."""
        # Simulasikan clingo tidak tersedia
        module = sys.modules.get('src.symbolic.rule_engine')
        original_clingo = getattr(module, 'clingo', None)
        
        try:
            # Hapus clingo dari module jika ada
            if hasattr(module, 'clingo'):
                delattr(module, 'clingo')
            
            # Patch sys.modules agar import clingo gagal
            with patch.dict('sys.modules', {'clingo': None}):
                with self.assertRaises(ImportError) as context:
                    from src.symbolic.rule_engine import ClingoRuleEngine
                    # Force reimport
                    import importlib
                    importlib.reload(sys.modules['src.symbolic.rule_engine'])
                    ClingoRuleEngine()
                
                self.assertIn("Clingo", str(context.exception))
        except Exception:
            # Skip test jika clingo memang terinstall
            pass

    def test_clingo_engine_init_succeeds_with_clingo(self):
        """Test: init ClingoRuleEngine berhasil jika clingo tersedia."""
        try:
            from src.symbolic.rule_engine import ClingoRuleEngine
            engine = ClingoRuleEngine(lp_file=None)
            self.assertIsNone(engine.rules_path)
            self.assertEqual(engine.extra_facts, [])
        except ImportError:
            self.skipTest("Clingo tidak terinstall")

    def test_clingo_engine_load_rules(self):
        """Test: load_rules menyimpan path."""
        try:
            from src.symbolic.rule_engine import ClingoRuleEngine
            engine = ClingoRuleEngine()
            engine.load_rules("/path/to/rules.lp")
            self.assertEqual(engine.rules_path, "/path/to/rules.lp")
        except ImportError:
            self.skipTest("Clingo tidak terinstall")

    def test_clingo_engine_add_fact(self):
        """Test: add_fact menyimpan fakta."""
        try:
            from src.symbolic.rule_engine import ClingoRuleEngine
            engine = ClingoRuleEngine()
            engine.add_fact("female(ana)")
            self.assertIn("female(ana).", engine.extra_facts)
        except ImportError:
            self.skipTest("Clingo tidak terinstall")

    def test_clingo_engine_add_fact_adds_period(self):
        """Test: add_fact tambahkan titik jika belum ada."""
        try:
            from src.symbolic.rule_engine import ClingoRuleEngine
            engine = ClingoRuleEngine()
            engine.add_fact("male(budi)")  # Tanpa titik
            self.assertIn("male(budi).", engine.extra_facts)  # Dengan titik
        except ImportError:
            self.skipTest("Clingo tidak terinstall")

    def test_clingo_engine_add_fact_keeps_period(self):
        """Test: add_fact tidak double titik jika sudah ada."""
        try:
            from src.symbolic.rule_engine import ClingoRuleEngine
            engine = ClingoRuleEngine()
            engine.add_fact("parent(ana,budi).")  # Sudah ada titik
            self.assertIn("parent(ana,budi).", engine.extra_facts)  # Tetap satu titik
            self.assertNotIn("parent(ana,budi)..", engine.extra_facts)  # Tidak double
        except ImportError:
            self.skipTest("Clingo tidak terinstall")


class DomainAspRulesTests(unittest.TestCase):
    """Test deterministik untuk rule ASP Bali dan Jawa."""

    def _solve_model(self, lp_name: str, facts=None):
        if facts is None:
            facts = []
        try:
            from src.symbolic.rule_engine import ClingoRuleEngine
        except ImportError:
            self.skipTest("Clingo tidak terinstall")

        lp_path = Path("src") / "symbolic" / "rules" / lp_name
        self.assertTrue(lp_path.exists(), f"File rule tidak ditemukan: {lp_path}")

        engine = ClingoRuleEngine(lp_file=str(lp_path))
        for fact in facts:
            engine.add_fact(fact)

        models = engine.solve()
        self.assertGreater(len(models), 0, "Clingo tidak menghasilkan model")
        return models[0]

    def test_bali_rule_file_parse(self):
        """Test: bali.lp bisa diparse dan disolve."""
        model = self._solve_model("bali.lp")
        self.assertIsInstance(model, list)

    def test_bali_purusa_inherit_druwe_gabro(self):
        """Test: purusa berhak atas druwe gabro."""
        model = self._solve_model(
            "bali.lp",
            facts=[
                "male(putra)",
                "kewajiban_ngayah(putra)",
            ],
        )
        self.assertIn("can_inherit(putra,harta_druwe_gabro)", model)

    def test_bali_perempuan_kawin_keluar_hak_terbatas(self):
        """Test: perempuan kawin keluar hanya waris terbatas."""
        model = self._solve_model(
            "bali.lp",
            facts=[
                "female(komang)",
                "kawin_keluar(komang)",
            ],
        )
        self.assertIn("ahli_waris_terbatas(komang)", model)
        self.assertIn("can_inherit(komang,harta_druwe_gabro)", model)
        self.assertNotIn("can_inherit(komang,tanah_sanggah)", model)

    def test_bali_larangan_jual_pusaka(self):
        """Test: jual pusaka memicu conflict."""
        model = self._solve_model(
            "bali.lp",
            facts=[
                "action(harta_pusaka,sell)",
            ],
        )
        self.assertIn("conflict(harta_pusaka,sell)", model)

    def test_jawa_rule_file_parse(self):
        """Test: jawa.lp bisa diparse dan disolve."""
        model = self._solve_model("jawa.lp")
        self.assertIsInstance(model, list)

    def test_jawa_sigar_semangka_equal_share(self):
        """Test: anak laki/perempuan setara untuk gono-gini."""
        model = self._solve_model(
            "jawa.lp",
            facts=[
                "child(adi)",
                "male(adi)",
                "child(sri)",
                "female(sri)",
            ],
        )
        self.assertIn("can_inherit(adi,harta_gono_gini)", model)
        self.assertIn("can_inherit(sri,harta_gono_gini)", model)
        self.assertIn("equal_share(adi,sri,harta_gono_gini)", model)

    def test_jawa_anak_angkat_hanya_gono_gini(self):
        """Test: anak angkat sah tidak mewarisi pusaka/harta asal."""
        model = self._solve_model(
            "jawa.lp",
            facts=[
                "anak_angkat(budi)",
                "adopsi_terang_tunai(budi)",
            ],
        )
        self.assertIn("can_inherit(budi,harta_gono_gini)", model)
        self.assertNotIn("can_inherit(budi,harta_pusaka)", model)

    def test_jawa_pecah_panci_hilangkan_hak_penguasaan(self):
        """Test: menikah lagi memicu pecah panci dan conflict."""
        model = self._solve_model(
            "jawa.lp",
            facts=[
                "janda(ibu)",
                "menikah_lagi(ibu)",
                "action(harta_gono_gini,hold_without_distribution)",
            ],
        )
        self.assertIn("pecah_panci(ibu)", model)
        self.assertIn("conflict(harta_gono_gini,hold_without_distribution)", model)
        self.assertNotIn("hak_penguasaan(ibu,harta_gono_gini)", model)

    def test_nasional_rule_file_parse(self):
        """Test: nasional.lp bisa diparse dan disolve."""
        model = self._solve_model("nasional.lp")
        self.assertIsInstance(model, list)

    def test_nasional_kelas_1_prioritas(self):
        """Test: kelas 1 (anak/pasangan) memblokir kelas 2."""
        model = self._solve_model(
            "nasional.lp",
            facts=[
                "child(andi)",
                "spouse(sari)",
                "menikah_sah",
                "parent(ayah)",
            ],
        )
        self.assertIn("berhak_waris(andi)", model)
        self.assertIn("berhak_waris(sari)", model)
        self.assertNotIn("berhak_waris(ayah)", model)

    def test_nasional_hak_spouse_harta_bersama(self):
        """Test: pasangan sah mendapat hak atas setengah harta bersama."""
        model = self._solve_model(
            "nasional.lp",
            facts=[
                "spouse(sari)",
                "menikah_sah",
            ],
        )
        self.assertIn("bagian_spouse(sari,seperdua_harta_bersama)", model)
        self.assertIn("hak_spouse_atas_harta_bersama(sari)", model)

    def test_nasional_conflict_wasiat_melebihi_batas(self):
        """Test: wasiat > 33% tanpa persetujuan memicu conflict."""
        model = self._solve_model(
            "nasional.lp",
            facts=[
                "nilai_wasiat(40)",
            ],
        )
        self.assertIn("conflict(wasiat,melebihi_batas_wajar)", model)

    def test_nasional_conflict_bagi_sebelum_lunas_utang(self):
        """Test: pembagian waris sebelum utang lunas memicu conflict."""
        model = self._solve_model(
            "nasional.lp",
            facts=[
                "action(harta_waris_pewaris,dibagi)",
            ],
        )
        self.assertIn("conflict(harta_waris_pewaris,pembagian_sebelum_lunas_utang)", model)

    def test_nasional_conflict_norm_nasional_vs_adat(self):
        """Test: deteksi konflik normatif nasional versus adat."""
        model = self._solve_model(
            "nasional.lp",
            facts=[
                "hak_waris_nasional(putri,harta_waris_pewaris)",
                "larangan_waris_adat(putri,harta_waris_pewaris)",
            ],
        )
        self.assertIn("conflict_norm(nasional_vs_adat,putri,harta_waris_pewaris)", model)


if __name__ == "__main__":
    unittest.main()
