from pathlib import Path
from typing import Dict, List, Optional, Any


class RuleEngine:
    """
    Base class for the Rule Engine.
    """
    def load_rules(self, file_path: str) -> None:
        raise NotImplementedError

    def query(self, query_str: str) -> List[Dict]:
        raise NotImplementedError


class ClingoRuleEngine(RuleEngine):
    """
    Rule engine based on Answer Set Programming (Clingo).
    Suitable for handling defaults and exceptions.
    """
    def __init__(self, lp_file: Optional[str] = None):
        try:
            import clingo
            self.clingo = clingo
        except ImportError as exc:
            raise ImportError("Clingo is not installed. Install with: pip install clingo") from exc

        self.rules_path = lp_file
        self.extra_facts = []

    def load_rules(self, lp_file: str) -> None:
        self.rules_path = lp_file

    def add_fact(self, fact: str) -> None:
        """Add a fact (e.g. 'female(ana).')"""
        if not fact.endswith('.'):
            fact += '.'
        self.extra_facts.append(fact)

    def solve(self) -> List[List[str]]:
        """Run the solver and return a list of models (atoms)."""
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
        Simple query: find atoms with a given name in the first model.
        Example: query('can_inherit') -> [{'Person': 'ana', 'Asset': 'rumah_gadang'}]
        """
        models = self.solve()
        if not models:
            return []

        results = []
        # Take only the first model for experimental simplicity
        for atom in models[0]:
            if atom.startswith(atom_name):
                # Simple parsing of atom(arg1, arg2)
                content = atom[len(atom_name):].strip('()')
                args = [arg.strip() for arg in content.split(',')]
                results.append({"args": args})
        return results


