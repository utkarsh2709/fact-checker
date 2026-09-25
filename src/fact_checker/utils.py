import json
import re


def parse_llm_json(text: str) -> dict:
    """Strip markdown code fences then parse JSON. Claude often wraps JSON in ```json ... ```."""
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.DOTALL)
    return json.loads(cleaned)
