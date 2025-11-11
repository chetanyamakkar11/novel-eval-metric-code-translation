"""
Judge interface. By default we provide DummyHeuristicJudge so the project runs
offline. Later you can swap in an LLM-based judge that returns J∈[0,1].
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Dict
from .utils import normalize_code, tokenize, jaccard, weighted_mean

class BaseJudge(Protocol):
    def score(self, src_code: str, trg_code: str, prompt: str | None = None) -> Dict[str, float]:
        """Return {'J': float, 'explan': str} with J in [0,1]."""

@dataclass
class DummyHeuristicJudge:
    """
    A lightweight, deterministic proxy for “semantic” judgment.
    Heuristics:
      - reward overlap of control-flow tokens & arithmetic symbols
      - slight penalty if target is extremely short/long vs source
    This is *not* a replacement for real human/LLM judgments, but lets us test IMM.
    """
    length_tolerance: float = 0.5  # how much length ratio deviating hurts
    ctrl_weight: float = 0.6
    arith_weight: float = 0.4

    def score(self, src_code: str, trg_code: str, prompt: str | None = None) -> Dict[str, float]:
        s, t = tokenize(normalize_code(src_code)), tokenize(normalize_code(trg_code))
        ctrl = {"if","else","for","while","return","switch","case","try","catch","finally"}
        arith = {"+","-","*","/","%","==","!=",">=","<=","<",">"}

        ctrl_sim = jaccard([x for x in s if x in ctrl], [x for x in t if x in ctrl])
        arith_sim = jaccard([x for x in s if x in arith], [x for x in t if x in arith])
        base = weighted_mean([ctrl_sim, arith_sim], [self.ctrl_weight, self.arith_weight])

        # length ratio penalty
        lr = len(t) / max(1, len(s))
        penalty = max(0.0, min(1.0, 1.0 - abs(lr - 1.0) / (1.0 + self.length_tolerance)))

        J = float(max(0.0, min(1.0, 0.2 + 0.8 * ((base + penalty) / 2.0))))
        return {"J": J, "explan": f"ctrl={ctrl_sim:.2f}, arith={arith_sim:.2f}, len_penalty={penalty:.2f}"}

# (Optional) later: real LLM judge using your provider of choice.
# class OpenAIJudge:
#     def __init__(self, model="gpt-4o-mini", api_key=None): ...
#     def score(self, src_code, trg_code, prompt=None) -> Dict[str, float]: ...
