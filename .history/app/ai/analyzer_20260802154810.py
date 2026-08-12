import json

from .gemini import MODEL, client


def analyze_document(text):
    prompt = f'''
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
'''

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    print("Raw AI response:")
    print(response.text)

    result = response.text.strip()

    if result.startswith("```json"):
        result = result.replace("```json", "").replace("```", "").strip()
    elif result.startswith("```"):
        result = result.replace("```", "").strip()

    return json.loads(result)