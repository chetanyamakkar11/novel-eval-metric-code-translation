"""
IMM: Inter-model/semantic Metric combining a static signal S and a judge signal J.
IMM = α·S + (1–α)·J   with α∈[0,1].
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional

from .static_score import static_semantic_score
from .llm_judge import (
    BaseJudge,
    DummyHeuristicJudge,
    OpenAILLMJudge
)


@dataclass
class IMMMetric:
    alpha: float = 0.55              # weight on static S
    judge: Optional[BaseJudge] = None

    def __post_init__(self):
        if self.judge is None:
            self.judge = DummyHeuristicJudge()
        self.alpha = float(max(0.0, min(1.0, self.alpha)))

    def score(self, src_code: str, trg_code: str) -> Dict[str, float]:
        s_res = static_semantic_score(src_code, trg_code)   # has 'S'
        j_res = self.judge.score(src_code, trg_code)        # has 'J'
        S, J = float(s_res["S"]), float(j_res["J"])
        imm = self.alpha * S + (1.0 - self.alpha) * J
        return {
            "IMM": imm,
            "S": S,
            "J": J,
            "alpha": self.alpha,
            **{f"S_{k}": v for k, v in s_res.items() if k != "S"},
            "J_explanation": j_res.get("explan","")
        }
