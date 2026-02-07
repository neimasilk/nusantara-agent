import json
from pathlib import Path
from typing import List, Dict


def main() -> None:
    results_dir = Path("experiments/07_advanced_orchestration/results")
    summaries: List[Dict] = []
    if results_dir.exists():
        for case_dir in sorted(results_dir.iterdir()):
            if not case_dir.is_dir():
                continue
            summary_path = case_dir / "summary.json"
            if summary_path.exists():
                summaries.append(json.loads(summary_path.read_text(encoding="utf-8")))

    run_index_path = results_dir / "run_index.json"
    run_index_path.write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"count": len(summaries), "path": str(run_index_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
