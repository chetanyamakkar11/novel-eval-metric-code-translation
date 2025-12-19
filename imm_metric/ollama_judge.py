import json
import subprocess
import re
from pathlib import Path


class OllamaJudge:
    """
    Local LLM judge using Ollama. Forces strict JSON output, extracts JSON reliably,
    normalizes scores, and never crashes on text outside JSON.
    """

    def __init__(self, model="mistral", rubric_path=None):
        self.model = model

        # Resolve rubric path
        if rubric_path is None:
            pkg_dir = Path(__file__).resolve().parent
            rubric_path = pkg_dir.parent / "scripts" / "docs" / "LLM_JUDGE_RUBRIC.md"


        rubric_path = Path(rubric_path)

        if not rubric_path.exists():
            raise FileNotFoundError(f"Rubric file not found: {rubric_path}")

        with open(rubric_path, "r") as f:
            self.rubric_text = f.read()

        # Strict JSON-only prompt
        self.prompt_template = """
You are a strict code translation judge. You MUST output ONLY valid JSON.
No explanations. No markdown. No commentary.

Here is your scoring rubric:

{rubric_text}

You will evaluate a source-target translation and respond ONLY with a JSON dictionary.
Your JSON MUST have EXACTLY these fields (floats between 0 and 1):

{{
  "functionality": 0.0,
  "semantic_alignment": 0.0,
  "idiomaticity": 0.0,
  "risk": 0.0,
  "final_j_score": 0.0
}}

SOURCE CODE:
{source_code}

TARGET CODE:
{target_code}

Output ONLY the JSON object. No other text.
"""

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama via subprocess and return raw string output."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
            )
        except FileNotFoundError:
            raise RuntimeError("Ollama not installed or not in PATH.")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Ollama model timed out.")

        return result.stdout.decode("utf-8")

    def score(self, src: str, trg: str) -> dict:
        """Generate prompt, call Ollama, extract JSON, normalize scores."""
        prompt = self.prompt_template.format(
            rubric_text=self.rubric_text,
            source_code=src,
            target_code=trg,
        )

        raw_out = self._call_ollama(prompt)

        # Extract JSON with regex
        match = re.search(r"\{[\s\S]*\}", raw_out)
        if not match:
            print("Raw Ollama output:\n", raw_out)
            raise RuntimeError("Judge did not return valid JSON.")

        json_text = match.group(0)

        try:
            parsed = json.loads(json_text)
        except Exception as e:
            print("Failed JSON text:\n", json_text)
            print("\nFull output:\n", raw_out)
            raise RuntimeError("JSON parsing failed.") from e

        # Normalize missing fields
        keys = ["functionality", "semantic_alignment", "idiomaticity", "risk", "final_j_score"]
        for k in keys:
            parsed[k] = float(parsed.get(k, 0.0))

        # Clamp between 0 and 1
        for k in keys:
            parsed[k] = max(0.0, min(1.0, parsed[k]))

        return parsed
