"""Common interface every backend implements, so the pipeline can swap
between them with a single --backend flag."""

from abc import ABC, abstractmethod


class LLMBackend(ABC):
    name = "base"

    @abstractmethod
    def generate_json(self, prompt: str) -> str:
        """Send prompt to the backend and return the raw text response.

        The response is expected to be a JSON string (the prompt templates
        all instruct the model to return strict JSON), but this method
        just returns raw text -- parsing/validation happens in the caller
        so a malformed response doesn't crash the whole batch run.
        """
        raise NotImplementedError
