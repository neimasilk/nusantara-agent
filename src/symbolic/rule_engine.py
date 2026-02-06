import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional


class RuleEngine:
    """
    Rule engine sederhana berbasis SWI-Prolog (PySwip).
    Fokus awal: loading rules Minangkabau dan menjalankan query dasar.
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
        """
        Tambahkan fakta baru ke knowledge base.
        Contoh: assert_fact(\"female(ana)\")
        """
        self._prolog.assertz(fact)

    def query(self, query: str, max_solutions: int = 10) -> List[Dict]:
        results: List[Dict] = []
        for i, solution in enumerate(self._prolog.query(query)):
            if i >= max_solutions:
                break
            results.append({k: str(v) for k, v in solution.items()})
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
