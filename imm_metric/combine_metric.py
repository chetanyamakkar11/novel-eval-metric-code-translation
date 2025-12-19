from .static_score import StaticSemanticScorer
from .ollama_judge import OllamaJudge


class IMMMetric:
    """
    IMM = α*S + (1−α)*J
    S = static semantic metric
    J = LLM judge score
    """

    def __init__(self, alpha=0.2, k=5, judge=None):
        self.alpha = alpha
        self.S_scorer = StaticSemanticScorer()
        self.judge = judge or OllamaJudge(model="mistral")

    def score(self, src: str, trg: str) -> dict:
        S = self.S_scorer.score(src, trg)

        J_raw = self.judge.score(src, trg)
        J = J_raw.get("final_j_score", 0.0)

        IMM = self.alpha * S + (1 - self.alpha) * J

        return {
            "S": S,
            "J": J,
            "IMM": IMM,
            "J_breakdown": J_raw,
        }
