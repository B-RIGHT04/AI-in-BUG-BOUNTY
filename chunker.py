"""Stage 1-2 glue: load raw recon output and batch it for AI triage.

Per ai_bugbounty.md's guardrail, keep batches to 100-300 items so the
model stays attentive and token costs stay sane."""

import json
from pathlib import Path


def load_lines(path: str) -> list[str]:
    """Load a plain-text recon file, one item (URL, endpoint, etc) per line."""
    text = Path(path).read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip()]


def load_text(path: str) -> str:
    """Load a file as a single block of text, for prompts like the business
    logic one that take a whole workflow description rather than a batch
    of recon items."""
    return Path(path).read_text(encoding="utf-8").strip()


def chunk(items: list, batch_size: int = 200):
    """Yield successive batches of at most batch_size items."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def format_batch_for_prompt(batch: list[str]) -> str:
    """Render a batch as the JSON list the prompt templates expect
    to see substituted in place of {batch}."""
    return json.dumps(batch, indent=2)
