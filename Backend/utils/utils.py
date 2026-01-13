from config.config import DefaultConfig
import json
import re

logger = DefaultConfig().logger

def extract_json_from_llm_response(response_text):
    """
    Extracts and parses JSON from an LLM response string.
    Handles cases where extra text or Markdown surrounds the JSON.
    """

    logger.info(f"Handling the extraction of the Json data from the given text")
    if not isinstance(response_text, str):
        raise TypeError("Response must be a string.")

    # Remove Markdown code fences if present
    cleaned = re.sub(r"```(?:json)?", "", response_text, flags=re.IGNORECASE).strip()

    # Find first JSON object or array (non-recursive, Python-safe)
    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)

    if not match:
        raise ValueError("No valid JSON found in the response.")

    json_str = match.group(1)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}") from e


def normalize_text(text: str) -> str:
    """Normalize OCR noise"""
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def detect_parent(line: str, ALLOWED_PARENTS:str):
    """
    Detect which allowed parent this line belongs to
    """
    for parent in ALLOWED_PARENTS:
        if parent in line:
            return parent
    return None
