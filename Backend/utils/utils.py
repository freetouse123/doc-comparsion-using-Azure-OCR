import json
import re

def extract_json_from_llm_response(response_text):
    """
    Extracts and parses JSON from an LLM response string.
    Handles cases where extra text or Markdown surrounds the JSON.
    """
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
