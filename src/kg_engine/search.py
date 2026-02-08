import json
from typing import List, Dict

class SimpleKGSearch:
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.triples = self.data.get("triples", [])

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Simple keyword search. Supports comma-separated keywords."""
        if "," in query:
            keywords = [k.strip().lower() for k in query.split(",")]
        else:
            # Fallback to splitting by space if no commas, but filter out common words
            keywords = [k.lower() for k in query.split() if len(k) > 3]
            if not keywords: # If everything was < 3 chars, just use the whole query
                keywords = [query.lower()]

        results = []
        seen_triples = set()
        
        for kw in keywords:
            if not kw: continue
            for t in self.triples:
                t_str = f"{t.get('head', '')} {t.get('relation', '')} {t.get('tail', '')}".lower()
                if kw in t_str:
                    t_id = f"{t.get('head')}|{t.get('relation')}|{t.get('tail')}"
                    if t_id not in seen_triples:
                        results.append(t)
                        seen_triples.add(t_id)
                if len(results) >= limit:
                    break
            if len(results) >= limit:
                break
        return results

    def get_context_for_query(self, query: str, limit: int = 15) -> str:
        results = self.search(query, limit)
        if not results:
            return "Tidak ditemukan informasi tambahan di Knowledge Graph."
        
        ctx = "Hasil pencarian Knowledge Graph tambahan:\n"
        for i, t in enumerate(results):
            ctx += f"- {t.get('head')} --({t.get('relation')})--> {t.get('tail')} [Kategori: {t.get('category')}]\n"
        return ctx