import json
from imm_metric import IMMMetric
from imm_metric.ollama_judge import OllamaJudge

# Example dataset
NEW_TEST = {
    "max_of_two_correct": {
    "source": "def max_of_two(a, b): return a if a > b else b",
    "target": """
    public int maxOfTwo(int a, int b){
        if (a > b) return a;
        else return b;
    }
    """
},

"max_of_two_buggy": {
    "source": "def max_of_two(a, b): return a if a > b else b",
    "target": """
    public int maxOfTwo(int a, int b){
        if (a >= b) return b;
        else return a;
    }
    """
},

"max_of_two_weird_but_correct": {
    "source": "def max_of_two(a, b): return a if a > b else b",
    "target": """
    public int maxOfTwo(int a, int b){
        int m = b;
        if (a - b > 0) {
            m = a;
        }
        return m;
    }
    """
}
}

DATASET = {
    "correct_sign": {
        "source": "def sign(x): return 'pos' if x > 0 else 'neg'",
        "target": """
        public String sign(int x){
            if (x > 0) return "pos";
            else return "neg";
        }
        """
    },

    "swapped_if": {
        "source": "def sign(x): return 'pos' if x > 0 else 'neg'",
        "target": """
        public String sign(int x){
            if (x > 0) return "neg";
            else return "pos";
        }
        """
    },

    "weird_but_correct": {
        "source": "def sign(x): return 'pos' if x > 0 else 'neg'",
        "target": """
        public String sign(int x){
            String out = "neg";
            if (!(x <= 0)) {
                out = "pos";
            }
            return out;
        }
        """
    }
}


def main():
    judge = OllamaJudge(model="mistral")
    imm = IMMMetric(alpha=0.5, judge=judge)

    results = {}

    for name, pair in NEW_TEST.items():
        out = imm.score(pair["source"], pair["target"])
        results[name] = out

        print(f"\n=== {name} ===")
        print(f"S: {out['S']}")
        print(f"J: {out['J']}")
        print(f"IMM: {out['IMM']}")
        print("J breakdown:", out["J_breakdown"])

    with open("results/imm_full_results_testing.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nSaved results to results/imm_full_results_testing.json")


if __name__ == "__main__":
    main()
