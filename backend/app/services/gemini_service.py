import requests

from app.config import Settings


class GeminiService:
    """Explains Jenkins/Docker failures using Gemini."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def explain_failure(self, logs: str) -> str:
        # Skip if no API key
        if not self.settings.gemini_api_key:
            return "Gemini API key is not configured."

        prompt = f"""
You are a DevOps expert.

A Jenkins pipeline failed while building or pushing a Docker image.

Explain the error in simple language.

Format your response exactly like this:

What happened:
<simple explanation>

Why it happened:
<reason>

How to fix it:
<steps>

Jenkins Logs:

{logs[-12000:]}
"""

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.settings.gemini_model}:generateContent"
        )

        headers = {
            "Content-Type": "application/json"
        }

        body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(
                url,
                params={"key": self.settings.gemini_api_key},
                headers=headers,
                json=body,
                timeout=30,
            )

            # Print debug info
            print("\n========== GEMINI DEBUG ==========")
            print("URL:", response.url)
            print("Status:", response.status_code)
            print("Response:", response.text)
            print("==================================\n")

            if not response.ok:
                return (
                    f"Gemini API Error ({response.status_code})\n\n"
                    f"{response.text}"
                )

            data = response.json()

            candidates = data.get("candidates", [])

            if not candidates:
                return "Gemini returned an empty response."

            return (
                candidates[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "Gemini returned no explanation.")
            )

        except requests.exceptions.Timeout:
            return "Gemini request timed out."

        except requests.exceptions.ConnectionError:
            return "Unable to connect to Gemini API."

        except Exception as e:
            return f"Gemini Exception: {str(e)}"