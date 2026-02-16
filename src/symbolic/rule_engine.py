from pathlib import Path
from typing import Dict, List, Optional, Any


class RuleEngine:
    """
    Base class untuk Rule Engine.
    """
    def load_rules(self, file_path: str) -> None:
        raise NotImplementedError

    def query(self, query_str: str) -> List[Dict]:
        raise NotImplementedError


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


