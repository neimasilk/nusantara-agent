import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Dict, List


def _load_scores(path: Path) -> List[Dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Format skor harus list of objects.")
    return data


def _avg(values: List[float]) -> float:
    return round(mean(values), 4) if values else 0.0


def summarize(scores: List[Dict]) -> Dict:
    acc = [item.get("accuracy", 0) for item in scores]
    comp = [item.get("completeness", 0) for item in scores]
    cult = [item.get("cultural_sensitivity", 0) for item in scores]
    total = [a + c + s for a, c, s in zip(acc, comp, cult)]

    return {
        "count": len(scores),
        "avg_accuracy": _avg(acc),
        "avg_completeness": _avg(comp),
        "avg_cultural_sensitivity": _avg(cult),
        "avg_total": _avg(total),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize Exp07 scores")
    parser.add_argument(
        "--scores",
        default="experiments/07_advanced_orchestration/scoring_template.json",
        help="Path ke file skor JSON",
    )
    parser.add_argument(
        "--out",
        default="experiments/07_advanced_orchestration/score_summary.json",
        help="Path output ringkasan JSON",
    )
    args = parser.parse_args()

    scores = _load_scores(Path(args.scores))
    summary = summarize(scores)

    Path(args.out).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
