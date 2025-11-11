"""
Run a tiny demo to print BLEU-less but meaningful IMM-style signals.
Usage:
    python examples/example_usage.py
"""
from imm_metric import IMMMetric

EXAMPLES = [
    # same logic, different identifiers/orders
    dict(
        name="sum_to_n",
        src="""
        def sum_to_n(n):
            s = 0
            for i in range(1, n+1):
                s += i
            return s
        """,
        trg_java_like="""
        int sumToN(int n) {
            int acc = 0;
            for (int i = 1; i <= n; i++) {
                acc = acc + i;
            }
            return acc;
        }
        """,
    ),
    # superficially similar but logic bug (uses multiplication instead of addition)
    dict(
        name="buggy_sum",
        src="""
        def sum_to_n(n):
            s = 0
            for i in range(1, n+1):
                s += i
            return s
        """,
        trg_java_like="""
        int sumToN(int n) {
            int acc = 1;
            for (int i = 1; i <= n; i++) {
                acc = acc * i; // BUG: factorial, not sum
            }
            return acc;
        }
        """,
    ),
]

def main():
    metric = IMMMetric(alpha=0.55)  # tweak α in README experiments
    rows = []
    for ex in EXAMPLES:
        res = metric.score(ex["src"], ex["trg_java_like"])
        rows.append((ex["name"], res["IMM"], res["S"], res["J"], res["J_explanation"]))

    # pretty print
    colw = [12, 8, 8, 8]
    header = f"{'example':{colw[0]}}  {'IMM':{colw[1]}} {'S':{colw[2]}} {'J':{colw[3]}}  explanation"
    print(header)
    print("-" * len(header))
    for name, imm, s, j, expl in rows:
        print(f"{name:{colw[0]}}  {imm:0.3f}    {s:0.3f}   {j:0.3f}  {expl}")

if __name__ == "__main__":
    main()
