"""
Static (no-model) code similarity capturing lexical + light structural cues.
Returns a score in [0,1].
"""
from __future__ import annotations
from typing import Dict
from .utils import normalize_code, tokenize, ngrams, jaccard, f1, weighted_mean

def _token_overlaps(src_tokens, trg_tokens) -> Dict[str, float]:
    # 1-gram and 2-gram F1s
    unis_src, unis_trg = ngrams(src_tokens,1), ngrams(trg_tokens,1)
    bis_src,  bis_trg  = ngrams(src_tokens,2), ngrams(trg_tokens,2)

    def prf(src_ngrams, trg_ngrams):
        src_set, trg_set = set(src_ngrams), set(trg_ngrams)
        tp = len(src_set & trg_set)
        p = tp / max(1, len(trg_set))    # “hypothesis” = target translation
        r = tp / max(1, len(src_set))
        return p, r, f1(p, r)

    p1, r1, f1_ = prf(unis_src, unis_trg)
    p2, r2, f2_ = prf(bis_src,  bis_trg)
    return {
        "uni_f1": f1_, "bi_f1": f2_,
        "uni_p": p1, "uni_r": r1, "bi_p": p2, "bi_r": r2
    }

def _operator_overlap(src_tokens, trg_tokens) -> float:
    ops = ["+","-","*","/","%","==","!=",">=","<=","<",">","and","or","&&","||"]
    src = [t for t in src_tokens if t in ops]
    trg = [t for t in trg_tokens if t in ops]
    return jaccard(src, trg)

def _keyword_overlap(src_tokens, trg_tokens) -> float:
    keywords = {"if","else","for","while","return","try","catch","finally","switch","case","class","def","function"}
    src = [t for t in src_tokens if t in keywords]
    trg = [t for t in trg_tokens if t in keywords]
    return jaccard(src, trg)

def static_semantic_score(src_code: str, trg_code: str) -> Dict[str, float]:
    """
    Language-agnostic static score capturing n-gram similarity, operator usage,
    and control-structure likeness. Produces a dict with sub-scores and
    an overall 'S' in [0,1].
    """
    src_norm, trg_norm = normalize_code(src_code), normalize_code(trg_code)
    src_tokens, trg_tokens = tokenize(src_norm), tokenize(trg_norm)

    overlaps = _token_overlaps(src_tokens, trg_tokens)
    op_j = _operator_overlap(src_tokens, trg_tokens)
    kw_j = _keyword_overlap(src_tokens, trg_tokens)

    # overall S: emphasize bi-gram (structure) plus operators & keywords
    S = weighted_mean(
        values=[overlaps["bi_f1"], overlaps["uni_f1"], op_j, kw_j],
        weights=[0.45, 0.25, 0.15, 0.15],
    )
    return {
        "S": S,
        "uni_f1": overlaps["uni_f1"],
        "bi_f1": overlaps["bi_f1"],
        "op_jaccard": op_j,
        "kw_jaccard": kw_j
    }
