# LLM Judge Rubric (Human-Centric Evaluation)

This document defines the human-centric judge component **J** used in the IMM evaluation metric for code translation quality.  
The judge score represents a holistic, qualitative assessment of a translation, modeling how an experienced software engineer would evaluate the output.

J is designed to complement the static structural score **S**, which measures syntactic and structural correctness.  
While S is mechanical and deterministic, J captures subjective quality dimensions such as idiomaticity, readability, and intent preservation.

---

## 1. Overview

The judge score **J** is computed from five dimensions, each scored in  
**{0, 0.25, 0.5, 0.75, 1.0}**, and combined with fixed weights:

| Dimension               | Weight |
|------------------------|--------|
| functional_intent      | 0.30   |
| idiomaticity           | 0.25   |
| readability            | 0.20   |
| unnecessary_artifacts  | 0.15   |
| safety                 | 0.10   |

The final score is:

\[
J = 0.30 F + 0.25 I + 0.20 R + 0.15 N + 0.10 S
\]

---

## 2. Dimension Definitions and Scoring Guide

Each dimension is evaluated qualitatively based on the criteria below.

### 2.1 Functional Intent (30%)

Evaluates whether the translated code preserves the **conceptual meaning and intent** of the source, independent of exact syntax or structure.

Score guidelines:
- **1.0:** High-level logic and purpose clearly preserved.
- **0.75:** Mostly preserved; minor deviations not affecting main intent.
- **0.50:** Partially preserved; noticeable gaps in logic.
- **0.25:** Major misunderstanding of intent.
- **0.0:** Translation does not reflect the source's purpose.

---

### 2.2 Idiomaticity (25%)

Assesses how natural and idiomatic the translation is in the target language.

Score guidelines:
- **1.0:** Reads like code written by an experienced programmer in the target language.
- **0.75:** Mostly idiomatic with small unnatural choices.
- **0.50:** Understandable but mechanically translated.
- **0.25:** Noticeably awkward or non-idiomatic.
- **0.0:** Highly unnatural or inappropriate for the target language.

---

### 2.3 Readability (20%)

Evaluates clarity, maintainability, and ease of understanding.

Includes:
- Naming quality  
- Logical organization  
- Formatting and simplicity  

Score guidelines:
- **1.0:** Clear, organized, easy to understand.
- **0.75:** Mostly readable with minor issues.
- **0.50:** Moderately readable; some clutter or confusion.
- **0.25:** Poor readability.
- **0.0:** Very difficult to follow.

---

### 2.4 Unnecessary Artifacts (15%)

Checks for the presence of redundant or mechanically translated elements such as:
- Unused imports  
- Debug print statements  
- Redundant variables  
- Dead code  
- Artifacts from the source language  

Score guidelines:
- **1.0:** No unnecessary artifacts; translation is clean.
- **0.75:** One minor artifact present.
- **0.50:** Several small artifacts or one moderate issue.
- **0.25:** Many artifacts or one major issue.
- **0.0:** Heavy presence of noise or leftover structural debris.

---

### 2.5 Safety (10%)

Evaluates whether the translated code reflects common-sense safety and correctness practices in the target language.

Includes:
- Avoiding infinite loops
- Reasonable handling of edge cases
- Avoiding risky constructs
- Maintaining expected performance characteristics

Score guidelines:
- **1.0:** Demonstrates safe and reasonable practices.
- **0.75:** Mostly safe with minor concerns.
- **0.50:** Some questionable choices.
- **0.25:** Likely to behave incorrectly in some cases.
- **0.0:** Clear safety or correctness issues.

---

## 3. Intended Use

This rubric is applied by an LLM (or human reviewer) to produce a JSON score with the five fields:

```json
{
  "functional_intent": X,
  "idiomaticity": X,
  "readability": X,
  "unnecessary_artifacts": X,
  "safety": X
}
