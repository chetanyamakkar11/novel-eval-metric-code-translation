import json
from imm_metric import IMMMetric
from imm_metric.llm_judge import OpenAILLMJudge, DummyHeuristicJudge

# Example dataset
DATASET = {
    "sum_to_n": {
        "source": "def sum_to_n(n): return sum(range(n+1))",
        "target": "public int sumToN(int n){ int s=0; for(int i=0;i<=n;i++) s+=i; return s; }"
    },
    "buggy_sum": {
        "source": "def sum_to_n(n): return sum(range(n+1))",
        "target": "public int sumToN(int n){ return n*n; }"
    },
    "swapped_if": {
        "source": "def sign(x): return 'pos' if x>0 else 'neg'",
        "target": "public String sign(int x){ if(x>0) return \"neg\"; else return \"pos\"; }"
    }
}

def main():
    # Choose judge mode:
    # judge = DummyHeuristicJudge()   # No API calls (safe, fast)
    judge = OpenAILLMJudge(model="gpt-4o-mini")  # Requires API key in environment

    imm = IMMMetric(alpha=0.5, judge=judge)

    results = {}

    for name, pair in DATASET.items():
        out = imm.score(pair["source"], pair["target"])

        results[name] = out

        print(f"\n=== {name} ===")
        print(f"S: {out['S']:.3f}")
        print(f"J: {out['J']:.3f}")
        print(f"IMM: {out['IMM']:.3f}")
        print("Judge explanation:", out.get("J_explanation", ""))

    with open("results/imm_full_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nSaved results to results/imm_full_results.json")

if __name__ == "__main__":
    main()
