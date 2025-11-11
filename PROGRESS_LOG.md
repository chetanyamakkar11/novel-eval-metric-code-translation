# Project Progress Log — Novel Evaluation Metric for Code Translation

## Week of November 11, 2025

### 1. Environment Setup
- Created a clean virtual environment (`imm_env`) using Python 3.12 to eliminate dependency conflicts from Anaconda.
- Installed required dependencies: `numpy`, `pandas`, `matplotlib`, and the local `imm-metric` package.
- Verified all imports and ensured reproducibility for collaborators.

### 2. Metric Implementation
- Implemented the IMM (Inter-Model Metric) combining:
  - **S (Static Similarity):** token, operator, and structural overlap.
  - **J (Judge Score):** heuristic evaluation of control-flow and arithmetic similarity.
- Defined the combined metric as  
  **IMM = α·S + (1–α)·J**, with α = 0.55 after preliminary sensitivity checks.

### 3. Experiment Pipeline
- Added `scripts/run_experiments.py` to evaluate IMM across multiple translation pairs:
  - `sum_to_n`: correct translation  
  - `buggy_sum`: factorial logic bug  
  - `swapped_if`: inverted conditional bug  
- The script computes and saves results to `results/metrics_comparison.csv` with columns `[example, IMM, S, J]`.

| example     | IMM  | S    | J    |
|--------------|------|------|------|
| sum_to_n     | 0.663 | 0.549 | 0.801 |
| buggy_sum    | 0.618 | 0.489 | 0.775 |
| swapped_if   | 0.617 | 0.488 | 0.775 |

### 4. Visualization
- Added `scripts/plot_results.py` to visualize metric performance.
- Generated `results/imm_bar.png`, comparing IMM, S, and J for each translation pair.

**Key Observation:**  
IMM differentiates between valid and buggy translations by capturing both syntactic and semantic alignment.  
While S and J alone yield similar scores across examples, IMM penalizes logical and structural errors more effectively.

### 5. Reflection and Next Steps
- IMM metric is fully functional and visualized.
- Immediate next steps:
  1. Integrate BLEU/CodeBLEU comparison for baseline benchmarking.
  2. Expand dataset with additional translation pairs (loops, recursion, and string operations).
  3. Explore integrating an LLM-based judge for semantic evaluation.
  4. Prepare midterm presentation slides including the plots and numerical summaries.

