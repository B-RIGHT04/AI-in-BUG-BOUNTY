import os

from .base import LLMBackend

DEFAULT_MODEL = "llama3"
DEFAULT_HOST = "http://localhost:11434"


class OllamaBackend(LLMBackend):
    """Local/private backend -- no data leaves the machine. Good fit for
    sensitive codebases per ai_bugbounty.md's backend comparison."""

    name = "ollama"

    def __init__(self, model: str | None = None, host: str | None = None):
        try:
            import requests
        except ImportError as e:
            raise ImportError(
                "The 'requests' package is required for the ollama backend. "
                "Install it with: pip install requests --break-system-packages"
            ) from e

        self._requests = requests
        self.model = model or DEFAULT_MODEL
        self.host = host or os.environ.get("OLLAMA_HOST", DEFAULT_HOST)

    def generate_json(self, prompt: str) -> str:
        resp = self._requests.post(
            f"{self.host}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=300,
        )
        resp.raise_for_status()
        return resp.json().get("response", "")
