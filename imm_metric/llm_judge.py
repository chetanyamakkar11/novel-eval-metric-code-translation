# imm_metric/llm_judge.py

import os
import json
from openai import OpenAI
client = OpenAI()



class BaseJudge:
    """Abstract judge class. All judges must implement score()."""

    def score(self, source_code: str, target_code: str) -> float:
        raise NotImplementedError("Subclasses must implement this method.")


class DummyHeuristicJudge(BaseJudge):
    """
    A lightweight heuristic judge used for testing.
    Approximates 'J' without calling an LLM.
    """

    def score(self, source_code: str, target_code: str) -> float:
        score = 1.0

        # Heuristic penalty if translation has unused imports
        if "import" in target_code and "(" not in source_code:
            score -= 0.1

        # Penalize if code is much longer than original
        if len(target_code) > len(source_code) * 1.5:
            score -= 0.15

        # Penalize messy formatting (very naive)
        if "    " not in target_code:  # no indentation
            score -= 0.1

        return max(0, min(score, 1))


class OpenAILLMJudge(BaseJudge):
    """
    Real LLM judge using OpenAI API.
    Returns a J (Judge) score between 0 and 1.
    """

    def __init__(self, model="gpt-4o-mini", rubric_path="scripts/docs/LLM_JUDGE_RUBRIC.md"
):
        self.model = model
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")

        # Load judge rubric
        with open(rubric_path, "r") as f:
            self.rubric = f.read()

    def score(self, source_code: str, target_code: str) -> float:
        prompt = f"""
You are evaluating translated code using the rubric below.

RUBRIC:
{self.rubric}

Provide ONLY a JSON dictionary with:
{{
    "J_score": <a number from 0 to 1>
}}

SOURCE CODE:
{source_code}

TRANSLATED CODE:
{target_code}
"""

        response = client.chat.completions.create(
        model=self.model,
        messages=[
        {"role": "system", "content": self.rubric},
        {"role": "user", "content": prompt},
    ],
    temperature=0,
)


        msg = response["choices"][0]["message"]["content"]

        try:
            data = json.loads(msg)
            return float(data["J_score"])
        except:
            return 0.5
