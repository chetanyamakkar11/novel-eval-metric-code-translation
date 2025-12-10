from .static_score import StaticSemanticScorer
from .ollama_judge import OllamaJudge

class IMMMetric:
    def __init__(self, alpha=0.5, k=5, llm_judge=None):
        self.alpha = alpha
        self.S_scorer = StaticSemanticScorer(k=k)
        self.judge = llm_judge or OllamaJudge()

    def score(self, src, trg):
        S = self.S_scorer.score(src, trg)

        J_raw = self.judge.score(src, trg)
        J = float(J_raw.get("final_j_score", 0.0))

        IMM = self.alpha * S + (1 - self.alpha) * J

        return {
            "S": S,
            "J": J,
            "IMM": IMM,
            "J_breakdown": J_raw
        }
