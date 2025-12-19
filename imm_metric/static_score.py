# imm_metric/static_score.py

"""
StaticSemanticScorer

Goal:
    Give a strong, static (non-LLM, non-execution) semantic similarity score
    between source and target code for code translation evaluation.

What it captures:
    - AST structure similarity (for Python code)
    - Control-flow & operator similarity (if/for/while/return, ==, >, etc.)
    - Identifier / variable overlap
    - Token-level sequence similarity

Output:
    A single scalar S in [0, 1], higher = more semantically aligned.

Design:
    S = 0.4 * S_ast
      + 0.3 * S_flow
      + 0.3 * S_tokens
"""

from __future__ import annotations

import ast
import re
from difflib import SequenceMatcher
from typing import Dict


# Keywords / operators we care about for control / data-flow shape
CONTROL_KEYWORDS = ["if", "else", "elif", "for", "while", "try", "except",
                    "finally", "with", "return", "break", "continue"]
OP_SYMBOLS = ["+", "-", "*", "/", "%", "==", "!=", ">", "<", ">=", "<="]


class StaticSemanticScorer:
    """
    Static semantic similarity scorer.

    This is S: a deterministic, non-LLM, non-execution-based metric that
    approximates semantic alignment using structure + control-flow + tokens.
    """

    def __init__(self) -> None:
        # store last breakdown for debugging / plots if needed
        self.last_breakdown: Dict[str, float] | None = None

    # ---------- Internal helpers ----------

    def _strip_comments_and_ws(self, code: str) -> str:
        """Remove obvious comments and excessive whitespace for cleaner analysis."""
        # Remove Python-style comments
        code = re.sub(r"#.*", "", code)
        # Remove C/Java-style // comments
        code = re.sub(r"//.*", "", code)
        # Remove C/Java-style /* ... */ comments
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
        # Normalize whitespace
        code = "\n".join(line.rstrip() for line in code.splitlines() if line.strip())
        return code

    def _safe_parse_python(self, code: str):
        """Try to parse Python code into an AST. On failure, return None."""
        try:
            return ast.parse(code)
        except Exception:
            return None

    def _flatten_ast_types(self, node) -> list[str]:
        """Flatten AST into a list of node type names."""
        types: list[str] = []
        if node is None:
            return types
        for child in ast.walk(node):
            types.append(type(child).__name__)
        return types

    def _ast_structure_similarity(self, src: str, trg: str) -> float:
        """
        Compare AST node-type sequences using SequenceMatcher.
        If parsing fails for either side, fall back to 0.0.
        """
        src_ast = self._safe_parse_python(src)
        trg_ast = self._safe_parse_python(trg)

        if src_ast is None or trg_ast is None:
            return 0.0

        types_src = self._flatten_ast_types(src_ast)
        types_trg = self._flatten_ast_types(trg_ast)

        if not types_src or not types_trg:
            return 0.0

        matcher = SequenceMatcher(None, types_src, types_trg)
        return matcher.ratio()

    def _extract_flow_features(self, code: str) -> Dict[str, list[str]]:
        """Extract control keywords, operators, and identifier names."""
        control = [kw for kw in CONTROL_KEYWORDS if kw in code]
        ops = [op for op in OP_SYMBOLS if op in code]

        # Rough identifier extraction (variable/function names)
        # Avoid obvious keywords and numbers.
        tokens = re.findall(r"[A-Za-z_]\w*", code)
        keywords = set(CONTROL_KEYWORDS + ["def", "class", "public", "static",
                                           "int", "float", "double", "String",
                                           "void", "return"])
        vars_only = [t for t in tokens if t not in keywords]

        return {
            "control": control,
            "ops": ops,
            "vars": vars_only,
        }

    def _jaccard_overlap(self, a: list[str], b: list[str]) -> float:
        """Jaccard similarity between two lists (as sets)."""
        sa, sb = set(a), set(b)
        if not sa and not sb:
            return 1.0  # both empty -> treat as perfectly aligned
        union = sa | sb
        inter = sa & sb
        if not union:
            return 0.0
        return len(inter) / len(union)

    def _flow_similarity(self, src: str, trg: str) -> float:
        """
        Compare control-flow and data-flow-ish patterns:
            - control keywords
            - operators
            - identifiers / variable names
        """
        A = self._extract_flow_features(src)
        B = self._extract_flow_features(trg)

        c = self._jaccard_overlap(A["control"], B["control"])
        o = self._jaccard_overlap(A["ops"], B["ops"])
        v = self._jaccard_overlap(A["vars"], B["vars"])

        # Slightly heavier weight on control & variables than raw ops
        return 0.4 * c + 0.3 * o + 0.3 * v

    def _token_sequence_similarity(self, src: str, trg: str) -> float:
        """
        Token-level sequence similarity using SequenceMatcher on lexeme-level tokens.
        This is a softer, surface-level semantic proxy.
        """
        # Simple tokenization: split on non-word characters
        src_tokens = re.findall(r"\w+|\S", src)
        trg_tokens = re.findall(r"\w+|\S", trg)

        if not src_tokens or not trg_tokens:
            return 0.0

        matcher = SequenceMatcher(None, src_tokens, trg_tokens)
        return matcher.ratio()

    # ---------- Public API ----------

    def score(self, src: str, trg: str) -> float:
        """
        Compute the static semantic similarity S in [0, 1].

        S is composed of:
            S_ast     : AST structural similarity
            S_flow    : control/data-flow similarity
            S_tokens  : token sequence similarity

        S = 0.4 * S_ast + 0.3 * S_flow + 0.3 * S_tokens
        """

        src_clean = self._strip_comments_and_ws(src)
        trg_clean = self._strip_comments_and_ws(trg)

        S_ast = self._ast_structure_similarity(src_clean, trg_clean)
        S_flow = self._flow_similarity(src_clean, trg_clean)
        S_tokens = self._token_sequence_similarity(src_clean, trg_clean)

        S = 0.4 * S_ast + 0.3 * S_flow + 0.3 * S_tokens

        # Store breakdown for inspection / logging if desired
        self.last_breakdown = {
            "S": float(S),
            "S_ast": float(S_ast),
            "S_flow": float(S_flow),
            "S_tokens": float(S_tokens),
        }

        return float(S)
