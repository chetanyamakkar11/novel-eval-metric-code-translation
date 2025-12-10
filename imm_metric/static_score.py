import ast
import astor
import re

class StaticSemanticScorer:
    def __init__(self, k=5):
        self.k = k

    def normalize(self, code):
        try:
            tree = ast.parse(code)
            return astor.to_source(tree)
        except Exception:
            return re.sub(r"\s+", " ", code).strip()

    def score_once(self, src, trg):
        src_norm = self.normalize(src)
        trg_norm = self.normalize(trg)

        keywords = ["if", "else", "return", "for", "while"]
        ops = ["+", "-", "*", "/", "%", "==", "!=", "<", ">"]

        kw_src = sum(k in src_norm for k in keywords)
        kw_trg = sum(k in trg_norm for k in keywords)
        kw_score = min(kw_src, kw_trg) / max(kw_src, 1)

        op_src = sum(o in src_norm for o in ops)
        op_trg = sum(o in trg_norm for o in ops)
        op_score = min(op_src, op_trg) / max(op_src, 1)

        len_score = min(len(src_norm), len(trg_norm)) / max(len(src_norm), 1)

        return (kw_score + op_score + len_score) / 3

    def score(self, src, trg):
        return sum(self.score_once(src, trg) for _ in range(self.k)) / self.k
