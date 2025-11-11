"""
run_experiments.py
Runs IMM on multiple example code translation pairs and logs results to CSV.
"""

from imm_metric import IMMMetric
import csv, os

# Define translation pairs (you can add more)
pairs = [
    {
        "name": "sum_to_n",
        "src": """
        def sum_to_n(n):
            s = 0
            for i in range(1, n+1):
                s += i
            return s
        """,
        "trg": """
        int sumToN(int n) {
            int acc = 0;
            for (int i = 1; i <= n; i++) {
                acc = acc + i;
            }
            return acc;
        }
        """,
    },
    {
        "name": "buggy_sum",
        "src": """
        def sum_to_n(n):
            s = 0
            for i in range(1, n+1):
                s += i
            return s
        """,
        "trg": """
        int sumToN(int n) {
            int acc = 1;
            for (int i = 1; i <= n; i++) {
                acc = acc * i; // factorial bug
            }
            return acc;
        }
        """,
    },
    {
        "name": "swapped_if",
        "src": """
        def abs_val(x):
            if x < 0:
                return -x
            else:
                return x
        """,
        "trg": """
        int absVal(int x) {
            if (x > 0) { // swapped condition bug
                return -x;
            } else {
                return x;
            }
        }
        """,
    },
]

# Initialize metric
metric = IMMMetric(alpha=0.55)

os.makedirs("results", exist_ok=True)
outpath = "results/metrics_comparison.csv"

# Run evaluation and save results
with open(outpath, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["example", "IMM", "S", "J"])
    for ex in pairs:
        res = metric.score(ex["src"], ex["trg"])
        writer.writerow([ex["name"], res["IMM"], res["S"], res["J"]])
        print(f"{ex['name']}: IMM={res['IMM']:.3f}, S={res['S']:.3f}, J={res['J']:.3f}")

print(f"\nResults saved to {outpath}")
