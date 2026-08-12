import json

from google.genai.errors import ServerError


def analyze_document(text):
    prompt = f"""
You are VaultX AI.

Analyze document.

Return JSON only.

{{
  "summary": "",
  "category": "",
  "confidence": 0
}}

Document:
{text}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        result = response.text.strip()

        if result.startswith("```json"):
            result = result.replace("```json", "").replace("```", "").strip()
        elif result.startswith("```"):
            result = result.replace("```", "").strip()

        return json.loads(result)

    except ServerError:
        return {
            "summary": "AI service temporarily unavailable.",
            "category": "Unknown",
            "confidence": 0
        }

    except Exception:
        current_app.logger.exception("Gemini analysis failed")
        return {
            "summary": "AI analysis failed.",
            "category": "Unknown",
            "confidence": 0
        }