import numpy as np

class IMMMetric:
    def __init__(self, alpha=0.5, llm_judge=None):
        """
        alpha: weight of static score S
        llm_judge: instance of LLMJudge or None
        """
        self.alpha = alpha
        self.llm_judge = llm_judge

    # -----------------------
    # STATIC SCORE S
    # -----------------------
    def static_score(self, source_code, target_code):
        """
        Computes the static structural score S.
        This checks:
        - syntax validity
        - structural similarity (rough AST)
        - no unnecessary imports
        - no missing constructs
        """
        score = 0.0

        # Very simple placeholder scoring until real AST analysis is done
        # (1) Syntax validity
        if self._looks_valid(target_code):
            score += 0.4

        # (2) Structural similarity via crude heuristics
        if self._keyword_overlap(source_code, target_code) > 0.5:
            score += 0.4

        # (3) No unnecessary imports
        if "import" not in target_code or "unused" not in target_code:
            score += 0.2

        return min(score, 1.0)

    def _looks_valid(self, code):
        return ";" in code or "(" in code or "{" in code

    def _keyword_overlap(self, src, tgt):
        src_k = set(src.lower().split())
        tgt_k = set(tgt.lower().split())
        if len(src_k) == 0:
            return 0
        return len(src_k & tgt_k) / len(src_k)

    # -----------------------
    # LLM JUDGE SCORE J
    # -----------------------
    def judge_score(self, source_code, target_code):
        """
        If an LLM judge is provided, use it.
        Otherwise return a placeholder score for now.
        """
        if self.llm_judge is None:
            return 0.5, {
                "functional_intent": 0.5,
                "idiomaticity": 0.5,
                "readability": 0.5,
                "unnecessary_artifacts": 0.5,
                "safety": 0.5
            }

        final_j, raw = self.llm_judge.evaluate(source_code, target_code)
        return final_j, raw

    # -----------------------
    # IMM METRIC
    # -----------------------
    def score(self, source_code, target_code):
        S = self.static_score(source_code, target_code)
        J, raw_j = self.judge_score(source_code, target_code)

        imm = self.alpha * S + (1 - self.alpha) * J
        return {
            "IMM": imm,
            "S": S,
            "J": J,
            "J_breakdown": raw_j
        }
