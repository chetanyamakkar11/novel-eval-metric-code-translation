# IMM – A Novel Evaluation Metric for Code Translation

This project introduces **IMM (Integrated Multi-Metric)**, a hybrid evaluation method
for measuring *code translation quality* across programming languages. IMM combines:

1. **Static Semantic Score (S-score)** – deterministic, AST-normalized correctness approximation  
2. **LLM-based Judgment (J-score)** – structured evaluation using a rubric  
3. **Weighted Integration (IMM)** – tunable combination of S and J  

IMM aims to bridge the gap between:
- brittle string-matching metrics (BLEU, CodeBLEU), and  
- subjective but powerful LLM-based evaluators.

The goal is a metric that is **consistent, interpretable, reproducible**, and useful
for evaluating real-world language-to-language code translation systems.

---

## Features

### **1. Pass@k-Inspired Static Semantic Scoring**
The static score uses:
- AST parsing + canonicalization  
- operator overlap  
- keyword comparison  
- structural similarity  

Evaluated across **k perturbations** (default: 5) to reduce noise.

### **2. Local LLM Judge (Ollama)**
The J-score is computed via a local model (e.g., *mistral*, *mixtral*, *phi3*) using
a strict JSON rubric.

Benefits:
- No API cost  
- Deterministic prompts  
- Aligned with human evaluation dimensions  

### **3. IMM Unified Score**
IMM = α * S + (1 − α) * J

yaml
Copy code

α is user-controlled based on how much weight to give semantic S-score vs.
LLM-derived J-score.

### **4. Full Breakdown for Debugging**
Each evaluation returns:
- S-score  
- J-score  
- Full J-score breakdown across rubric categories  
- Explanation from judge  

---

## Repository Structure

novel-eval-metric-code-translation/
│
├── imm_metric/
│ ├── init.py
│ ├── combine_metric.py # IMM core logic
│ ├── static_score.py # pass@k static correctness scorer
│ ├── ollama_judge.py # Local LLM-based judgment
│ └── ...
│
├── scripts/
│ ├── run_experiments.py # main experimentation driver
│ ├── docs/
│ │ └── LLM_JUDGE_RUBRIC.md # evaluation rubric
│
├── results/
│ └── imm_full_results.json
│
└── README.md

yaml
Copy code

---

## Running IMM Locally

### 1. Install dependencies

```bash
pip install -e .
pip install astor
2. Install and pull an Ollama model
bash
Copy code
brew install ollama
ollama pull mistral
3. Run experiments
bash
Copy code
python scripts/run_experiments.py
📊 Example Output
yaml
Copy code
=== sum_to_n ===
S: 0.923
J: 0.810
IMM: 0.866
J breakdown: { ... }
Why IMM?
Current code translation metrics fail in important ways:

Metric	Fails At
BLEU	counts tokens, ignores semantics
CodeBLEU	improves but still brittle
Execution Tests	can't always auto-generate inputs
LLM Judge Alone	inconsistent across prompts/models

IMM solves this by integrating deterministic structure-aware scoring with a
rubric-driven qualitative judge, aimed at capturing human-like evaluation
without losing reproducibility.

Roadmap
Execution-based behavioral testing

Larger benchmark dataset of translation pairs

Inter-model consistency experiments (OpenAI vs Anthropic vs Ollama)

Adversarial robustness scoring

Calibration of α for different translation tasks

Author
Chetanya Makkar
University of Maryland