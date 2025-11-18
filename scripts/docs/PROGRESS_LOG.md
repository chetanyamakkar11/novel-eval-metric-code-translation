# Project Log – Novel Evaluation Metric for Code Translation
_Last Updated: Nov 17, 2025_

## 1. Repository Structure and Packaging
- Created a clean, modular repository layout with:
  - `imm_metric/` package containing all metric components
  - `scripts/` folder for experiment runners and plotting
  - `docs/` folder for rubric and documentation
- Added a proper `setup.py` and editable installation via `pip install -e .`
- Ensured all modules import consistently using package-relative imports.

## 2. Static Semantic Metric (S-score)
- Implemented a static semantic score capturing simple correctness signals:
  - Keyword overlap
  - Operator matching
  - Structural similarity
- Designed to provide a deterministic baseline independent of LLM variability.
- Integrated into the IMMMetric pipeline with a controllable weight parameter `alpha`.

## 3. Judge Rubric Design (J-score)
- Created a detailed rubric that evaluates translations on:
  - Functional correctness
  - Semantic alignment
  - Idiomatic quality in the target language
  - Complexity penalties
  - Risk/safety of introduced bugs
- Standardized the rubric in Markdown (`docs/LLM_JUDGE_RUBRIC.md`) so the LLM receives consistent instructions across runs.

## 4. LLM Judge Integration (OpenAILLMJudge)
- Added an LLM-based scoring class that:
  - Loads the rubric dynamically
  - Constructs a structured prompt for consistent evaluation
  - Parses the returned JSON into the sub-scores + final J-score
- Abstracted judge classes behind a `BaseJudge` interface so future judges can be swapped in without changing the IMM pipeline.

## 5. IMM Metric Integration
- Combined static semantic score (S) and judge score (J) into:
- Embedded interpretability into outputs:
- Raw S-score
- Raw J-score
- Full J breakdown
- Per-factor explanation from LLM
- Final IMM score

## 6. Testing Pipeline and Example Dataset
- Added a small example dataset with three translation cases:
- Correct translation
- Incorrect functional translation
- Logic inversion (branch inversion bug)
- Created `run_experiments.py` to:
- Run IMM scoring on all examples
- Save results as JSON
- Print per-example metric breakdown

## 7. Robust Path Handling and Rubric Loading
- Corrected file path issues by resolving rubric paths relative to the package directory.
- Ensured rubric loading works regardless of the working directory.

## 8. LLM Execution (Pending Quota)
- Pipeline runs end-to-end until the LLM request stage.
- System is ready for full evaluation once billing/quota is enabled.
- Fallback `DummyHeuristicJudge` is available for development without API calls.

## 9. Next Steps
- Add billing or quota to enable LLM-based scoring.
- Expand dataset to dozens of source→target pairs.
- Evaluate stability and inter-model consistency using multiple LLMs.
- Refine IMM parameter tuning, especially choice of α.
