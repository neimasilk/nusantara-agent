import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Any


class RuleEngine:
    """
    Base class untuk Rule Engine.
    """
    def load_rules(self, file_path: str) -> None:
        raise NotImplementedError

    def query(self, query_str: str) -> List[Dict]:
        raise NotImplementedError


class PrologEngine(RuleEngine):
    """
    Rule engine berbasis SWI-Prolog (PySwip).
    """

    def __init__(self, prolog_file: Optional[str] = None, auto_load: bool = True):
        self._prolog = self._init_prolog()
        if prolog_file and auto_load:
            self.load_rules(prolog_file)

    @staticmethod
    def _init_prolog():
        try:
            from pyswip import Prolog
        except ImportError as exc:
            raise ImportError(
                "PySwip belum terpasang. Install dengan: pip install pyswip "
                "dan pastikan SWI-Prolog sudah ter-install."
            ) from exc
        return Prolog()

    def load_rules(self, prolog_file: str) -> None:
        path = Path(prolog_file)
        if not path.exists():
            raise FileNotFoundError(f"Rule file tidak ditemukan: {path}")
        self._prolog.consult(str(path))

    def assert_fact(self, fact: str) -> None:
        self._prolog.assertz(fact)

    def query(self, query: str, max_solutions: int = 10) -> List[Dict]:
        results: List[Dict] = []
        for i, solution in enumerate(self._prolog.query(query)):
            if i >= max_solutions:
                break
            results.append({k: str(v) for k, v in solution.items()})
        return results


class ClingoRuleEngine(RuleEngine):
    """
    Rule engine berbasis Answer Set Programming (Clingo).
    Cocok untuk handling defaults dan exceptions.
    """
    def __init__(self, lp_file: Optional[str] = None):
        try:
            import clingo
            self.clingo = clingo
        except ImportError as exc:
            raise ImportError("Clingo belum terpasang. Install dengan: pip install clingo") from exc
        
        self.rules_path = lp_file
        self.extra_facts = []

    def load_rules(self, lp_file: str) -> None:
        self.rules_path = lp_file

    def add_fact(self, fact: str) -> None:
        """Tambahkan fakta (misal: 'female(ana).')"""
        if not fact.endswith('.'):
            fact += '.'
        self.extra_facts.append(fact)

    def solve(self) -> List[List[str]]:
        """Menjalankan solver dan mengembalikan list of models (atoms)."""
        ctl = self.clingo.Control()
        if self.rules_path:
            ctl.load(str(self.rules_path))
        
        # Add dynamic facts
        if self.extra_facts:
            facts_str = " ".join(self.extra_facts)
            ctl.add("base", [], facts_str)
        
        ctl.ground([("base", [])])
        
        models = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                models.append([str(atom) for atom in model.symbols(shown=True)])
        
        return models

    def query(self, atom_name: str) -> List[Dict[str, Any]]:
        """
        Query sederhana: cari atom dengan nama tertentu di model pertama.
        Contoh: query('can_inherit') -> [{'Person': 'ana', 'Asset': 'rumah_gadang'}]
        """
        models = self.solve()
        if not models:
            return []
        
        results = []
        # Mengambil model pertama saja untuk simplisitas eksperimen
        for atom in models[0]:
            if atom.startswith(atom_name):
                # Parsing sederhana atom(arg1, arg2)
                content = atom[len(atom_name):].strip('()')
                args = [arg.strip() for arg in content.split(',')]
                results.append({"args": args})
        return results


def export_rules_as_facts(json_path: str, output_prolog_path: str) -> str:
    """
    Ekspor rules JSON sebagai fakta Prolog:
    rule(id, type, text).
    """
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON rules tidak ditemukan: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))

    lines: List[str] = [
        "% Auto-generated facts from JSON rules.",
        "% Format: rule(id, type, text).",
    ]
    for item in data:
        rule_id = item.get("id", "UNKNOWN")
        rule_type = item.get("type", "unknown")
        text = item.get("rule", "").replace('"', '\\"')
        lines.append(f'rule("{rule_id}", "{rule_type}", "{text}").')

    output_path = Path(output_prolog_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(output_path)
