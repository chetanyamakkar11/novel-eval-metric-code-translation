# Novel Evaluation Metric for Code Translation (IMM Metric)

This repository implements IMM — a hybrid evaluation metric for assessing code translation quality across programming languages. IMM combines:

1. S-score – A static, deterministic semantic similarity measure  
2. J-score – A rubric-guided LLM judge score (OpenAI or local Ollama)  
3. IMM-score – A weighted combination of both:  
   IMM = α * S + (1 – α) * J

The goal is to create a reliable, interpretable, and model-agnostic metric for evaluating code translation systems beyond BLEU or edit-distance-based approaches.

## Features

### 1. Static Semantic Scoring (S-score)
Implements deterministic similarity checks including:
- Keyword and operator overlap  
- Structural token similarity  
- Basic semantic feature alignment  
- Outputs a normalized 0–1 correctness score  

Purpose: provide a stable, reproducible baseline independent of LLM variability.

### 2. LLM Judge Scoring (J-score)
Supports two judge implementations:

#### OpenAILLMJudge
Uses OpenAI models (e.g., gpt-4o-mini) with a structured rubric prompt to produce:
- A 5-factor scoring breakdown
- A final judge score
- A natural-language explanation

#### OllamaJudge (local)
Uses local models (e.g., mistral, llama3.1) and includes:
- Strict JSON-only output prompting
- Automatic JSON cleanup and fallback extraction
- Full rubric-based score calculation

Rubric is stored in:
docs/LLM_JUDGE_RUBRIC.md

### 3. IMM Metric Combination
IMMMetric merges static and learned evaluation signals. It returns:
- Raw S-score  
- Raw J-score  
- Detailed J-breakdown  
- Explanation text  
- Final IMM hybrid score  

### 4. Experiment Pipeline
The script at scripts/run_experiments.py:
- Loads example translation pairs  
- Computes S, J, and IMM scores  
- Prints results  
- Saves JSON output to results/imm_full_results.json  

This pipeline is easily extendable for larger datasets or model comparisons.

## Project Structure
imm_metric/
combine_metric.py
static_score.py
ollama_judge.py
openai_judge.py
init.py

scripts/
run_experiments.py

docs/
LLM_JUDGE_RUBRIC.md

results/
imm_full_results.json


## Installation

1. Clone the repository:
   git clone https://github.com/chetanyamakkar11/novel-eval-metric-code-translation.git  
   cd novel-eval-metric-code-translation

2. Create a Python environment:
   python3 -m venv imm_env  
   source imm_env/bin/activate

3. Install package:
   pip install -e .

4. (Optional) OpenAI judge:
   pip install openai  
   export OPENAI_API_KEY="your_key"

5. (Optional) Ollama judge:
   brew install ollama  
   ollama pull mistral

## Running Experiments

Run:
python scripts/run_experiments.py

Example output:
=== sum_to_n ===
S: 0.92
J: 0.81
IMM: 0.86
Judge Explanation: ...

Results are saved locally as JSON.

## Example JSON Output
{
"sum_to_n": {
"S": 0.92,
"J": 0.81,
"IMM": 0.86,
"J_breakdown": {
"functionality": 1.0,
"semantic_alignment": 0.9,
"idiomaticity": 0.7,
"risk": 0.0
},
"explanation": "Target preserves full behavior..."
}
}

## Future Work
The next major milestone is the creation of a large, diverse dataset of code translation pairs
to thoroughly evaluate IMM across languages and difficulty levels. This includes:

- Expanding examples beyond toy programs
- Curating real translation outputs from multiple LLMs
- Evaluating IMM stability across datasets
 

## Summary

This project provides an interpretable hybrid metric for evaluating code translation quality. IMM unifies deterministic semantics with a rubric-aligned LLM judge to produce more reliable and meaningful evaluation scores than traditional string-based metrics. The system is modular, extendable, and supports both cloud-based and fully local LLM judging.

## Author
Chetanya Makkar  
University of Maryland  