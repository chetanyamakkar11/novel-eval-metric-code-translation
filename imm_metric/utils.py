"""
Utility helpers: tokenization, normalization, n-grams, simple stats.
These are intentionally language-agnostic to support cross-language pairs.
"""
from __future__ import annotations
import re
from typing import List, Sequence, Tuple
import numpy as np

# very light keyword sets to bias importance (extendable)
LANG_KEYWORDS = {
    "common": {
        "if","else","for","while","return","break","continue","switch","case","try",
        "catch","finally","class","def","function","public","private","static","new",
        "import","from","package","throws","raise","await","async","yield","lambda"
    }
}

IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
NUM_RE = re.compile(r"\b\d+(\.\d+)?\b")

def normalize_code(s: str) -> str:
    """Lowercase, collapse whitespace, strip comments (very roughly),
    and canonicalize identifiers -> ID and numbers -> NUM.
    """
    # strip // and # comments (rough), and /* */ blocks
    s = re.sub(r"//.*?$", " ", s, flags=re.MULTILINE)
    s = re.sub(r"#.*?$", " ", s, flags=re.MULTILINE)
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.DOTALL)
    s = s.replace("\t"," ")
    # numbers -> NUM
    s = NUM_RE.sub(" NUM ", s)
    # identifiers -> ID (but keep common keywords)
    def repl(m):
        w = m.group(0)
        return w if w in LANG_KEYWORDS["common"] else "ID"
    s = IDENT_RE.sub(repl, s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

def tokenize(s: str) -> List[str]:
    """Whitespace + punctuation tokenization."""
    # split on non-alphanum (keep basic operators)
    toks = re.findall(r"[A-Za-z_]+|\d+|==|!=|<=|>=|->|[-+*/%=(){}\[\],.;:<>]", s)
    return [t for t in toks if t.strip()]

def ngrams(seq: Sequence[str], n: int) -> List[Tuple[str,...]]:
    return [tuple(seq[i:i+n]) for i in range(len(seq)-n+1)]

def f1(p: float, r: float, eps: float = 1e-9) -> float:
    return (2*p*r)/(p+r+eps)

def jaccard(a: Sequence[str], b: Sequence[str]) -> float:
    A, B = set(a), set(b)
    if not A and not B: return 1.0
    return len(A & B) / max(1, len(A | B))

def safe_minmax(x: float) -> float:
    return float(max(0.0, min(1.0, x)))

def weighted_mean(values: Sequence[float], weights: Sequence[float]) -> float:
    v, w = np.array(values, dtype=float), np.array(weights, dtype=float)
    if w.sum() == 0: return float(np.mean(v)) if len(v) else 0.0
    return float((v*w).sum()/w.sum())
