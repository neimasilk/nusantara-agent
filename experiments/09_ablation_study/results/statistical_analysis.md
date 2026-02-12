# Statistical Analysis — ART-066

- Results dir: `experiments/09_ablation_study/results`
- Total runs: 22
- Reference baseline: `B5`

## Baseline Summary

| Baseline | N Run | Mean Acc | Std | 95% CI |
|---|---:|---:|---:|---|
| B1 | 3 | 0.5909 | 0.0000 | [0.5909, 0.5909] |
| B2 | 3 | 0.5909 | 0.0000 | [0.5909, 0.5909] |
| B3 | 3 | 0.5909 | 0.0000 | [0.5909, 0.5909] |
| B4 | 3 | 0.5909 | 0.0000 | [0.5909, 0.5909] |
| B5 | 3 | 0.5455 | 0.0000 | [0.5455, 0.5455] |
| B6 | 3 | 0.5455 | 0.0000 | [0.5455, 0.5455] |
| B7 | 3 | 0.5455 | 0.0000 | [0.5455, 0.5455] |
| B8 | 1 | 0.9545 | 0.0000 | [0.9545, 0.9545] |

## Pairwise vs Reference

| Baseline | Delta Mean Acc | n_pairs | t-test p | Wilcoxon p | Cohen's d |
|---|---:|---:|---:|---:|---:|
| B1 | 0.0455 | 3 | 0.000000 | 0.250000 | 0.0000 |
| B2 | 0.0455 | 3 | 0.000000 | 0.250000 | 0.0000 |
| B3 | 0.0455 | 3 | 0.000000 | 0.250000 | 0.0000 |
| B4 | 0.0455 | 3 | 0.000000 | 0.250000 | 0.0000 |
| B6 | 0.0000 | 3 | 1.000000 | 1.000000 | 0.0000 |
| B7 | 0.0000 | 3 | 1.000000 | 1.000000 | 0.0000 |
| B8 | 0.0000 | 0 | - | - | 0.0000 |

## Ranking by Mean Accuracy

1. `B8` — 0.9545
2. `B1` — 0.5909
3. `B2` — 0.5909
4. `B3` — 0.5909
5. `B4` — 0.5909
6. `B5` — 0.5455
7. `B6` — 0.5455
8. `B7` — 0.5455

Catatan: analisis ini menghitung statistik terhadap run yang tersedia pada folder hasil.