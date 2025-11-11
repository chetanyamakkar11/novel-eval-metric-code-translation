# Project Progress Log  
**Project:** Novel Evaluation Metric for Code Translation (IMM)  
**Author:** Chetanya Makkar  
**Date:** November 2025  

---

## Overview  
The project introduces a **new evaluation metric for code translation** called **IMM** (Inter-Model Metric).  
Traditional metrics like BLEU and CodeBLEU often reward superficial token overlap and fail to capture  
semantic correctness. IMM aims to fix that by combining two complementary signals:

\[
\text{IMM} = \alpha \cdot S + (1 - \alpha) \cdot J
\]

where  
- **S** = Static Semantic Similarity (structure + syntax overlap)  
- **J** = Judge-based Semantic Score (human- or LLM-like reasoning)  
- **α** = weight controlling the balance between structural and semantic fidelity

---

## Repository Structure and Purpose of Each Module

### `imm_metric/utils.py`
**Purpose:** Core helper utilities for preprocessing and similarity calculations.  
**Key Features:**
- `normalize_code()` → removes comments, normalizes identifiers and numbers.  
- `tokenize()` → language-agnostic tokenization of source/target code.  
- `ngrams()`, `jaccard()`, `f1()` → support lexical overlap metrics.  
- `weighted_mean()` → safe averaging for multi-feature fusion.

These utilities enable cross-language consistency and lightweight feature extraction.

---

### `imm_metric/static_score.py`
**Purpose:** Implements the **Static Semantic Score (S)** that captures lexical and structural similarity  
without requiring model inference.  
**Components:**
- 1-gram and 2-gram F1 overlap  
- Operator overlap (`+`, `==`, `>=`, etc.)  
- Control-flow keyword overlap (`if`, `for`, `while`, `return`, …)  
**Output:** Dictionary with component scores and overall static score `S ∈ [0,1]`.

---

### `imm_metric/llm_judge.py`
**Purpose:** Provides a flexible **Judge** interface for semantic evaluation.  
**Implemented Classes:**
- `BaseJudge` → protocol definition for any semantic judge.  
- `DummyHeuristicJudge` → offline heuristic that approximates LLM judgment using  
  control-flow and arithmetic similarity plus a length penalty.  
**Future Extension:** Replace with an actual LLM-based judge (e.g., GPT-4o) for deeper semantic scoring.

---

### `imm_metric/combine_metric.py`
**Purpose:** Core implementation of the IMM formula.  
**Logic Flow:**
1. Compute static semantic score `S` via `static_semantic_score()`.  
2. Compute judge score `J` via `DummyHeuristicJudge` (or another judge).  
3. Combine them: `IMM = α·S + (1-α)·J`.  
**Returns:** Dictionary containing `IMM`, `S`, `J`, diagnostic sub-scores, and explanations.

---

### `examples/example_usage.py`
**Purpose:** Demonstration script showing IMM in action.  
**Details:**
- Includes two translation examples:  
  1. *sum_to_n* — correct translation.  
  2. *buggy_sum* — factorial logic error.  
- Prints table comparing `IMM`, `S`, and `J`.  
**Expected Outcome:** The correct translation scores higher on IMM than the buggy one,  
illustrating IMM’s advantage over surface-level metrics.

---

### `requirements.txt`
Minimal dependencies:
```text
numpy>=1.24
