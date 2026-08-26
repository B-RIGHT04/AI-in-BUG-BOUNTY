"""Extracts the paste-ready prompt template(s) out of a prompt_library/*.md
file, so the pipeline can use the exact same wording you review and edit
in the markdown -- no copy-pasting into Python strings, no drift between
the docs and the code."""

import re
from pathlib import Path

# Matches headings like "## Prompt template", "## Prompt template A -- foo"
_HEADING_RE = re.compile(r'^#+[ \t]*Prompt template[ \t]*(.*)$', re.MULTILINE)
_CODE_FENCE_RE = re.compile(r'```\n(.*?)```', re.DOTALL)


def load_templates(md_path: str) -> dict[str, str]:
    """Return {label: template_text} for every "Prompt template" section
    in the file. Single-template files get the key "default"."""
    text = Path(md_path).read_text(encoding="utf-8")
    headings = list(_HEADING_RE.finditer(text))
    if not headings:
        raise ValueError(f"No 'Prompt template' heading found in {md_path}")

    templates = {}
    for i, match in enumerate(headings):
        label = match.group(1).strip(" \u2014-:") or "default"
        start = match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        section = text[start:end]

        code_match = _CODE_FENCE_RE.search(section)
        if not code_match:
            continue
        templates[label] = code_match.group(1).strip()

    if not templates:
        raise ValueError(f"Found 'Prompt template' heading(s) but no code "
                          f"block under them in {md_path}")
    return templates


def resolve_template(templates: dict[str, str], requested: str | None) -> tuple[str, str]:
    """Pick a template by label. Returns (label, template_text).

    If requested is None, returns the first template found. Otherwise
    matches exactly, then case-insensitive startswith, else raises with
    the list of available labels."""
    if requested is None:
        label = next(iter(templates))
        return label, templates[label]

    if requested in templates:
        return requested, templates[requested]

    requested_lower = requested.lower()
    for label, tmpl in templates.items():
        if label.lower().startswith(requested_lower):
            return label, tmpl

    raise ValueError(
        f"Template '{requested}' not found. Available: {list(templates.keys())}"
    )
