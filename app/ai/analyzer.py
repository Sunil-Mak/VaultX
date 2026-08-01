import json

from .gemini import MODEL


def analyze_document(text):
    prompt = f"""
You are VaultX AI.

Analyze document.

Return JSON only.

{{
    "summary":"",
    "category":"",
    "confidence":0
}}

Document:

{text}
"""

    response = MODEL.generate_content(prompt)

    result = response.text.strip()

    if result.startswith("```json"):
        result = result.replace("```json", "").replace("```", "").strip()
    elif result.startswith("```"):
        result = result.replace("```", "").strip()

    return json.loads(result)