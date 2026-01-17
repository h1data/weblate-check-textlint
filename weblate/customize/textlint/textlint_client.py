import os
import requests

class TextlintClient:
    """Execute textlint check via external API"""

    def __init__(self):
        self.api_url = f"http://{os.getenv("TEXTLINT_HOST", "textlint")}:{os.getenv("TEXTLINT_PORT", "3000")}{os.getenv("TEXTLINT_API_PATH", "/lint")}"

    def lint_text(self, text: str, lang_code: str = "ja"):
        """Send text + language code to textlint API"""
        try:
            response = requests.post(self.api_url, json = { "text": text, "lang": lang_code } , timeout=10)
            if not response.ok:
                print(f"[TextlintClient] Error: {response.status_code} {response.text}")
                return None
            return response.json()
        except Exception as e:
            print(f"[TextlintClient] Error: {e}")
            return None
