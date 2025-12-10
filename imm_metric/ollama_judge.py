import subprocess
import json
import os
import re

class OllamaJudge:
    """
    LLM Judge using local Ollama models.
    Ensures strict JSON output so the IMM metric can parse cleanly.
    """

    def __init__(self, model="mistral", rubric_path="scripts/docs/LLM_JUDGE_RUBRIC.md"):
        self.model = model

        # Build absolute rubric path
        self.rubric_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", rubric_path)
        )

        with open(self.rubric_path, "r") as f:
            self.rubric = f.read()

        # Template with JSON-strict instructions
        self.prompt_template = """
You are a strict evaluator for code translation quality.

Your job is to score how well the TARGET code preserves the behavior,
logic, semantics, and idiomatic quality of the SOURCE code.

Return ONLY valid JSON using this exact structure:
{
  "functionality": <float 0-1>,
  "semantic_alignment": <float 0-1>,
  "idiomaticity": <float 0-1>,
  "risk": <float 0-1>,
  "final_j_score": <float 0-1>,
  "explanation": "<short explanation>"
}

SOURCE CODE:
{src}

TARGET CODE:
{trg}

SCORING RUBRIC:
--------------------
{rubric}
--------------------

Again: respond with ONLY JSON. No surrounding text.
"""

    def extract_json(self, text):
        """
        Extracts JSON even if model outputs extra text.
        """
        try:
            # Try direct JSON
            return json.loads(text)
        except:
            pass

        # Fallback: extract { ... } substring
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass

        # Total failure fallback
        return {
            "functionality": 0.0,
            "semantic_alignment": 0.0,
            "idiomaticity": 0.0,
            "risk": 0.0,
            "final_j_score": 0.0,
            "explanation": "LLM output invalid JSON."
        }

    def score(self, src_code, trg_code):
        prompt = self.prompt_template.format(
            src=src_code, trg=trg_code, rubric=self.rubric
        )

        result = subprocess.run(
            ["ollama", "run", self.model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        raw = result.stdout.decode().strip()
        # print("\n[DEBUG RAW OUTPUT]\n", raw, "\n")  # uncomment for debugging

        parsed = self.extract_json(raw)
        return parsed
