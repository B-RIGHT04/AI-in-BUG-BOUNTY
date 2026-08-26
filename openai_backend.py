import os

from .base import LLMBackend

DEFAULT_MODEL = "gpt-4o-mini"


class OpenAIBackend(LLMBackend):
    name = "openai"

    def __init__(self, model: str | None = None, api_key: str | None = None):
        try:
            import openai
        except ImportError as e:
            raise ImportError(
                "The 'openai' package is required for the openai backend. "
                "Install it with: pip install openai --break-system-packages"
            ) from e

        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError(
                "No OpenAI API key found. Set the OPENAI_API_KEY "
                "environment variable (see .env.example)."
            )

        self.client = openai.OpenAI(api_key=key)
        self.model = model or DEFAULT_MODEL

    def generate_json(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content
