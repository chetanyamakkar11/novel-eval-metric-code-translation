"""
plot_results.py
Visualizes IMM, S, and J scores for all examples.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("results/metrics_comparison.csv")

plt.figure(figsize=(8,5))
df.plot(x="example", y=["IMM", "S", "J"], kind="bar", rot=0)
plt.title("IMM vs Static (S) vs Judge (J) Scores")
plt.ylabel("Score")
plt.ylim(0, 1)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()

os.makedirs("results", exist_ok=True)
plt.savefig("results/imm_bar.png", dpi=300)
print("Saved bar chart → results/imm_bar.png")
plt.show()
