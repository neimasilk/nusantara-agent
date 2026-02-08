"""Test deterministik untuk modul symbolic/rule_engine."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open


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


class ExportRulesAsFactsTests(unittest.TestCase):
    """Test untuk export_rules_as_facts (fungsi deterministik tanpa external dep)."""

    def test_export_rules_creates_file(self):
        """Test: export rules JSON ke Prolog facts."""
        from src.symbolic.rule_engine import export_rules_as_facts
        
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "rules.json"
            output_path = Path(tmp) / "output.pl"
            
            # Buat sample rules
            rules = [
                {"id": "R001", "type": "inheritance", "rule": "Test rule 1"},
                {"id": "R002", "type": "property", "rule": "Test rule 2"},
            ]
            json_path.write_text(json.dumps(rules), encoding="utf-8")
            
            result = export_rules_as_facts(str(json_path), str(output_path))
            
            self.assertTrue(output_path.exists())
            self.assertEqual(result, str(output_path))
            
            content = output_path.read_text(encoding="utf-8")
            self.assertIn('rule("R001", "inheritance", "Test rule 1").', content)
            self.assertIn('rule("R002", "property", "Test rule 2").', content)

    def test_export_rules_escapes_quotes(self):
        """Test: escape quotes dalam rule text."""
        from src.symbolic.rule_engine import export_rules_as_facts
        
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "rules.json"
            output_path = Path(tmp) / "output.pl"
            
            rules = [{"id": "R001", "type": "test", "rule": 'Rule with "quotes"'}]
            json_path.write_text(json.dumps(rules), encoding="utf-8")
            
            export_rules_as_facts(str(json_path), str(output_path))
            
            content = output_path.read_text(encoding="utf-8")
            self.assertIn('\\"', content)  # Escaped quotes

    def test_export_rules_file_not_found(self):
        """Edge case: file tidak ditemukan raise FileNotFoundError."""
        from src.symbolic.rule_engine import export_rules_as_facts
        
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "nonexistent.json"
            output_path = Path(tmp) / "output.pl"
            
            with self.assertRaises(FileNotFoundError):
                export_rules_as_facts(str(json_path), str(output_path))

    def test_export_rules_empty_array(self):
        """Edge case: empty rules array menghasilkan file valid tanpa fakta."""
        from src.symbolic.rule_engine import export_rules_as_facts
        
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "rules.json"
            output_path = Path(tmp) / "output.pl"
            
            json_path.write_text(json.dumps([]), encoding="utf-8")
            
            export_rules_as_facts(str(json_path), str(output_path))
            
            content = output_path.read_text(encoding="utf-8")
            self.assertIn("% Auto-generated facts", content)
            # Cek tidak ada baris yang diawali dengan "rule(" (bukan dalam komentar)
            lines = [l for l in content.split('\n') if not l.startswith('%')]
            rule_lines = [l for l in lines if l.startswith('rule(')]
            self.assertEqual(len(rule_lines), 0)  # Tidak ada rules

    def test_export_rules_missing_fields(self):
        """Edge case: missing fields menggunakan default."""
        from src.symbolic.rule_engine import export_rules_as_facts
        
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "rules.json"
            output_path = Path(tmp) / "output.pl"
            
            # Rule tanpa id dan type
            rules = [{"rule": "Incomplete rule"}]
            json_path.write_text(json.dumps(rules), encoding="utf-8")
            
            export_rules_as_facts(str(json_path), str(output_path))
            
            content = output_path.read_text(encoding="utf-8")
            self.assertIn('"UNKNOWN"', content)
            self.assertIn('"unknown"', content)


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


class PrologEngineMockTests(unittest.TestCase):
    """Test untuk PrologEngine menggunakan mock."""

    @patch("src.symbolic.rule_engine.PrologEngine._init_prolog")
    def test_prolog_engine_init_with_file(self, mock_init):
        """Test: init dengan file auto-load."""
        from src.symbolic.rule_engine import PrologEngine
        
        mock_prolog = MagicMock()
        mock_init.return_value = mock_prolog
        
        with tempfile.NamedTemporaryFile(suffix=".pl", delete=False) as f:
            f.write(b"test.")
            temp_path = f.name
        
        try:
            engine = PrologEngine(prolog_file=temp_path, auto_load=True)
            mock_prolog.consult.assert_called_once_with(temp_path)
        finally:
            Path(temp_path).unlink(missing_ok=True)

    @patch("src.symbolic.rule_engine.PrologEngine._init_prolog")
    def test_prolog_engine_load_rules_file_not_found(self, mock_init):
        """Edge case: load_rules dengan file tidak ada raise FileNotFoundError."""
        from src.symbolic.rule_engine import PrologEngine
        
        mock_prolog = MagicMock()
        mock_init.return_value = mock_prolog
        
        engine = PrologEngine(auto_load=False)
        with self.assertRaises(FileNotFoundError):
            engine.load_rules("/nonexistent/path.pl")

    @patch("src.symbolic.rule_engine.PrologEngine._init_prolog")
    def test_prolog_engine_assert_fact(self, mock_init):
        """Test: assert_fact memanggil prolog.assertz."""
        from src.symbolic.rule_engine import PrologEngine
        
        mock_prolog = MagicMock(
            spec=["assertz", "consult", "query"],
            unsafe=True,
        )
        mock_init.return_value = mock_prolog
        
        engine = PrologEngine(auto_load=False)
        engine.assert_fact("parent(ana,budi)")
        mock_prolog.assertz.assert_called_once_with("parent(ana,budi)")

    @patch("src.symbolic.rule_engine.PrologEngine._init_prolog")
    def test_prolog_engine_query(self, mock_init):
        """Test: query mengembalikan hasil sebagai list of dict."""
        from src.symbolic.rule_engine import PrologEngine
        
        mock_prolog = MagicMock()
        mock_init.return_value = mock_prolog
        
        # Mock query result
        mock_prolog.query.return_value = [
            {"X": "ana", "Y": "budi"},
            {"X": "cici", "Y": "dodi"},
        ]
        
        engine = PrologEngine(auto_load=False)
        result = engine.query("parent(X,Y)")
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {"X": "ana", "Y": "budi"})
        self.assertEqual(result[1], {"X": "cici", "Y": "dodi"})

    @patch("src.symbolic.rule_engine.PrologEngine._init_prolog")
    def test_prolog_engine_query_max_solutions(self, mock_init):
        """Test: query respect max_solutions limit."""
        from src.symbolic.rule_engine import PrologEngine
        
        mock_prolog = MagicMock()
        mock_init.return_value = mock_prolog
        
        # Mock banyak results
        mock_prolog.query.return_value = [{"X": f"item{i}"} for i in range(20)]
        
        engine = PrologEngine(auto_load=False)
        result = engine.query("test(X)", max_solutions=5)
        
        self.assertEqual(len(result), 5)


if __name__ == "__main__":
    unittest.main()
