# IMM: Idiomaticity–Maintainability Metric

A hybrid evaluation metric for code translation combining static program analysis and LLM-based judgment.

## Formula
`IMM = α·S + (1–α)·J`

- **S:** Static score (BLEU, AST similarity, etc.)
- **J:** LLM-based judgment
- **α:** Weight tuned against human ratings

## Setup
```bash
git clone https://github.com/chetanyamakkar/novel-eval-metric-code-translation.git
cd imm-metric
pip install -r requirements.txt

