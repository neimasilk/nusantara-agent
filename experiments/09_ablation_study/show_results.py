import json
import sys
from pathlib import Path

# Load results
result_file = Path(__file__).parent / "results_deepseek_asp_llm_2026-02-19.json"
data = json.loads(result_file.read_text(encoding="utf-8"))

print("=" * 60)
print("DeepSeek Cross-Validation Benchmark - FINAL RESULTS")
print("=" * 60)
print(f"Date: {data['date']}")
print(f"Mode: {data['mode']}")
print(f"Backend: {data['backend']}")
print()
print(f"Total Cases Evaluated: {data['total_evaluated']}")
print(f"Correct Predictions: {data['correct']}")
print(f"Accuracy: {data['accuracy']*100:.1f}%")
print()
print("Wilson 95% Confidence Interval:")
print(f"  Lower: {data['accuracy_wilson_95ci']['low']*100:.1f}%")
print(f"  Upper: {data['accuracy_wilson_95ci']['high']*100:.1f}%")
print()
print("Per-Label Metrics:")
for label, m in data['per_label_metrics'].items():
    print(f"  Label {label}: Precision={m['precision']*100:.1f}%, Recall={m['recall']*100:.1f}%, Support={m['support']}")
print()
print("Comparison with Ollama Baseline:")
print(f"  DeepSeek: {data['accuracy']*100:.1f}%")
print(f"  Ollama:   70.0%")
diff = data['accuracy']*100 - 70.0
print(f"  Delta:    {diff:+.1f} percentage points")
print("=" * 60)

if data['errors']:
    print(f"\nErrors: {len(data['errors'])} cases")
    for e in data['errors'][:5]:
        print(f"  - {e['case_id']}: {e['error'][:60]}...")
else:
    print("\nNo errors reported.")
