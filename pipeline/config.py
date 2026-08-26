"""Backend selection. Claude is the default -- override with --backend or
the PIPELINE_BACKEND environment variable."""

import os

DEFAULT_BACKEND = os.environ.get("PIPELINE_BACKEND", "claude")

SUPPORTED_BACKENDS = ["claude", "openai", "gemini", "ollama"]


def get_backend(name: str = DEFAULT_BACKEND, model: str | None = None):
    name = name.lower()

    if name == "claude":
        from backends.claude import ClaudeBackend
        return ClaudeBackend(model=model)
    elif name == "openai":
        from backends.openai_backend import OpenAIBackend
        return OpenAIBackend(model=model)
    elif name == "gemini":
        from backends.gemini_backend import GeminiBackend
        return GeminiBackend(model=model)
    elif name == "ollama":
        from backends.ollama_backend import OllamaBackend
        return OllamaBackend(model=model)
    else:
        raise ValueError(
            f"Unknown backend '{name}'. Supported: {SUPPORTED_BACKENDS}"
        )
