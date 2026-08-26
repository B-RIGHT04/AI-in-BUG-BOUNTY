import os

from .base import LLMBackend

DEFAULT_MODEL = "gemini-2.5-flash"


class GeminiBackend(LLMBackend):
    name = "gemini"

    def __init__(self, model: str | None = None, api_key: str | None = None):
        try:
            from google import genai
            from google.genai import types
        except ImportError as e:
            raise ImportError(
                "The 'google-genai' package is required for the gemini "
                "backend. Install it with: "
                "pip install google-genai --break-system-packages"
            ) from e

        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise RuntimeError(
                "No Gemini API key found. Set the GEMINI_API_KEY "
                "environment variable (see .env.example)."
            )

        self._types = types
        self.client = genai.Client(api_key=key)
        self.model = model or DEFAULT_MODEL

    def generate_json(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=self._types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )
        return response.text
