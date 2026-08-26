import os

from .base import LLMBackend

DEFAULT_MODEL = "claude-sonnet-4-6"


class ClaudeBackend(LLMBackend):
    name = "claude"

    def __init__(self, model: str | None = None, api_key: str | None = None):
        try:
            import anthropic
        except ImportError as e:
            raise ImportError(
                "The 'anthropic' package is required for the claude backend. "
                "Install it with: pip install anthropic --break-system-packages"
            ) from e

        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "No Anthropic API key found. Set the ANTHROPIC_API_KEY "
                "environment variable (see .env.example)."
            )

        self.client = anthropic.Anthropic(api_key=key)
        self.model = model or DEFAULT_MODEL

    def generate_json(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        parts = [
            block.text for block in response.content
            if getattr(block, "type", None) == "text"
        ]
        return "".join(parts)
