import json
import sys

file_path = sys.argv[1] if len(sys.argv) > 1 else 'experiments/09_ablation_study/results_deepseek_rollback_2026-02-20.json'

data = json.load(open(file_path))

# Count D predictions
d_count = sum(1 for r in data['results'] if r.get('predicted') == 'D')

print('=== DeepSeek Benchmark Results (Rollback Rules) ===')
print(f"Correct: {data['correct']}/70")
print(f"Accuracy: {data['accuracy']*100:.1f}%")
print(f"Wilson 95% CI: [{data['accuracy_wilson_95ci']['low']:.3f}, {data['accuracy_wilson_95ci']['high']:.3f}]")
print(f"D predictions: {d_count}")
print()
print('=== Comparison ===')
print('ASP-only:     58.6% (41/70)')
print('Ollama:       64.3% (45/70)')
print(f"DeepSeek:     {data['accuracy']*100:.1f}% ({data['correct']}/70)")
print()
print('=== Per-Label Recall ===')
for label in ['A', 'B', 'C', 'D']:
    metrics = data['per_label_metrics'][label]
    print(f"{label}: {metrics['tp']}/{metrics['support']} (recall: {metrics['recall']:.2f})")
