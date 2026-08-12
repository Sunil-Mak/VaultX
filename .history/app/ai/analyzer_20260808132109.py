import json

from flask import current_app
from google import genai
from google.genai.errors import ServerError

MODEL = "gemini-2.5-flash"


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
        client = genai.Client(
            api_key=current_app.config["GEMINI_API_KEY"]
        )

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

    except Exception as e:
        print(e)
        current_app.logger.exception("Gemini analysis failed")
        return {
            "summary": "AI analysis failed.",
            "category": "Unknown",
            "confidence": 0
        }