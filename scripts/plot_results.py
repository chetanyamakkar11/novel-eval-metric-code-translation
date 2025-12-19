import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def main():
    results_path = Path("results/imm_full_results_testing.json")

    if not results_path.exists():
        raise FileNotFoundError("Run run_experiments.py first to generate results.")

    with open(results_path, "r") as f:
        data = json.load(f)

    names = list(data.keys())
    S_scores = [data[n]["S"] for n in names]
    J_scores = [data[n]["J"] for n in names]
    IMM_scores = [data[n]["IMM"] for n in names]

    x = np.arange(len(names))
    width = 0.25

    plt.figure(figsize=(10, 6))
    plt.bar(x - width, S_scores, width, label="S-score", color="#6fa8dc")
    plt.bar(x, J_scores, width, label="J-score", color="#93c47d")
    plt.bar(x + width, IMM_scores, width, label="IMM", color="#f6b26b")

    plt.xticks(x, names, fontsize=12)
    plt.ylabel("Score", fontsize=14)
    plt.title("Comparison of S-score, J-score, and IMM Score", fontsize=16)
    plt.ylim(0, 1.1)

    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    output_path = Path("results/imm_scores2.png")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)

    print(f"Saved graph: {output_path}")


if __name__ == "__main__":
    main()
