"""Generate paper-ready figures from the Phase 1+2 analysis JSON.

Outputs:
  analysis/figures/fig_accuracy_heatmap.png
  analysis/figures/fig_per_domain.png
  analysis/figures/fig_per_label_f1.png
  analysis/figures/fig_rules_length_effect.png

All figures use matplotlib only (no seaborn) and deterministic ordering.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
FIG_DIR = ANALYSIS / "figures"
FIG_DIR.mkdir(exist_ok=True, parents=True)

SUMMARY = json.loads((ANALYSIS / "phase1_summary.json").read_text(encoding="utf-8"))

PROVIDERS = ["deepseek", "kimi", "grok"]
PROVIDER_LABELS = {"deepseek": "DeepSeek-chat",
                   "kimi": "Kimi (Moonshot-v1-8k)",
                   "grok": "Grok-4.20 non-reasoning"}

# Condition columns ordered by rule load: no rules → compact → full
COND_ORDER = [1, 3, 2]
COND_LABELS = {1: "Cond 1\n(no rules)",
               3: "Cond 3\n(compact rules)",
               2: "Cond 2\n(full rules)"}

LABELS = ["A", "B", "C", "D"]
LABEL_DESCRIPTIONS = {"A": "Nasional", "B": "Adat", "C": "Sintesis", "D": "Insufficient"}


def acc(prov: str, cond: int) -> float:
    return SUMMARY["summary"][f"{prov}_cond{cond}"]["accuracy"]


def f1(prov: str, cond: int, label: str) -> float:
    return SUMMARY["summary"][f"{prov}_cond{cond}"]["per_label"][label]["f1"]


def per_domain(prov: str, cond: int) -> dict[str, dict]:
    return SUMMARY["summary"][f"{prov}_cond{cond}"]["per_domain"]


def fig_accuracy_heatmap() -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    grid = np.zeros((len(PROVIDERS), len(COND_ORDER)))
    for i, prov in enumerate(PROVIDERS):
        for j, cond in enumerate(COND_ORDER):
            grid[i, j] = acc(prov, cond)

    im = ax.imshow(grid, cmap="RdYlGn", vmin=0.40, vmax=0.75, aspect="auto")
    ax.set_xticks(range(len(COND_ORDER)))
    ax.set_xticklabels([COND_LABELS[c] for c in COND_ORDER])
    ax.set_yticks(range(len(PROVIDERS)))
    ax.set_yticklabels([PROVIDER_LABELS[p] for p in PROVIDERS])
    for i in range(len(PROVIDERS)):
        for j in range(len(COND_ORDER)):
            v = grid[i, j]
            color = "black" if 0.50 < v < 0.70 else "white"
            ax.text(j, i, f"{v:.3f}", ha="center", va="center",
                    color=color, fontsize=11, fontweight="bold")
    ax.set_title("Accuracy on the 70-case benchmark across rule conditions")
    fig.colorbar(im, ax=ax, label="Accuracy", shrink=0.7)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_accuracy_heatmap.png", dpi=150)
    plt.close(fig)


def fig_rules_length_effect() -> None:
    """Line plot: accuracy as a function of rule context length."""
    # Approximate prompt tokens by condition: 104 / 170 / 236.
    # Subtract Cond1 baseline (104) to get "rules tokens added".
    rule_tokens = {1: 0, 3: 66, 2: 132}

    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = {"deepseek": "#1f77b4", "kimi": "#2ca02c", "grok": "#d62728"}
    markers = {"deepseek": "o", "kimi": "s", "grok": "^"}

    for prov in PROVIDERS:
        xs = [rule_tokens[c] for c in COND_ORDER]
        ys = [acc(prov, c) for c in COND_ORDER]
        ax.plot(xs, ys, marker=markers[prov], color=colors[prov],
                label=PROVIDER_LABELS[prov], linewidth=2, markersize=10)
        for x, y in zip(xs, ys):
            ax.text(x, y + 0.005, f"{y:.3f}", ha="center", fontsize=9,
                    color=colors[prov])

    ax.set_xlabel("Rule context length (tokens added to prompt)")
    ax.set_ylabel("Accuracy")
    ax.set_title("Effect of rule context length on LLM accuracy\n"
                 "(every provider's best score is at 0 rule tokens)")
    ax.set_xticks([0, 66, 132])
    ax.set_xticklabels(["0\n(no rules)", "66\n(compact)", "132\n(full)"])
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower left")
    ax.set_ylim(0.45, 0.72)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_rules_length_effect.png", dpi=150)
    plt.close(fig)


def fig_per_label_f1() -> None:
    """Per-label F1 across conditions and providers."""
    fig, axes = plt.subplots(1, len(LABELS), figsize=(14, 4), sharey=True)
    width = 0.25
    x = np.arange(len(PROVIDERS))

    for idx, label in enumerate(LABELS):
        ax = axes[idx]
        for j, cond in enumerate(COND_ORDER):
            ys = [f1(prov, cond, label) for prov in PROVIDERS]
            ax.bar(x + (j - 1) * width, ys, width,
                   label=COND_LABELS[cond].replace("\n", " "))
        ax.set_title(f"Label {label} — {LABEL_DESCRIPTIONS[label]}")
        ax.set_xticks(x)
        ax.set_xticklabels([p.title() for p in PROVIDERS], rotation=0)
        ax.set_ylim(0, 1.0)
        ax.grid(True, alpha=0.3, axis="y")
        if idx == 0:
            ax.set_ylabel("F1 score")
        if idx == len(LABELS) - 1:
            ax.legend(loc="upper right", fontsize=8)

    fig.suptitle("Per-label F1 across providers and rule conditions")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_per_label_f1.png", dpi=150)
    plt.close(fig)


def fig_per_domain() -> None:
    """Best-condition per-provider accuracy by adat domain."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    # Always use each provider's best condition (cond 1).
    domains_order = ["Minangkabau", "Bali", "Jawa", "Lintas", "Nasional", "Other"]
    width = 0.25
    x = np.arange(len(domains_order))

    for j, prov in enumerate(PROVIDERS):
        dom_map = per_domain(prov, 1)
        ys = []
        ns = []
        for d in domains_order:
            entry = dom_map.get(d, {"accuracy": 0.0, "n": 0})
            ys.append(entry["accuracy"])
            ns.append(entry["n"])
        ax.bar(x + (j - 1) * width, ys, width,
               label=PROVIDER_LABELS[prov])
        for xi, y, n in zip(x, ys, ns):
            ax.text(xi + (j - 1) * width, y + 0.01, f"n={n}",
                    ha="center", fontsize=7, color="gray")

    ax.set_xticks(x)
    ax.set_xticklabels(domains_order)
    ax.set_ylabel("Accuracy (Cond 1, no rules)")
    ax.set_title("Per-domain accuracy at each provider's best configuration")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_per_domain.png", dpi=150)
    plt.close(fig)


def main() -> None:
    fig_accuracy_heatmap()
    print(f"[figures] wrote {FIG_DIR / 'fig_accuracy_heatmap.png'}")
    fig_rules_length_effect()
    print(f"[figures] wrote {FIG_DIR / 'fig_rules_length_effect.png'}")
    fig_per_label_f1()
    print(f"[figures] wrote {FIG_DIR / 'fig_per_label_f1.png'}")
    fig_per_domain()
    print(f"[figures] wrote {FIG_DIR / 'fig_per_domain.png'}")


if __name__ == "__main__":
    main()
