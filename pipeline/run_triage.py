#!/usr/bin/env python3
"""Stage 1-3 pipeline: load raw recon output, batch it, run it through an
AI-triage prompt from the prompt library, save structured JSON output.

This produces a SHORTLIST for manual review -- see prompt_library/README.md.
Nothing here reports a finding or sends attack payloads.

Examples:
    # Dry run - build prompts, print previews, make no API calls
    python run_triage.py --input urls.txt --vuln sqli --dry-run

    # Real run against Claude (default backend)
    python run_triage.py --input urls.txt --vuln idor --output idor_results.json

    # Multi-template file: pick a specific template
    python run_triage.py --input js_urls.txt --vuln xss --template B

    # Swap backend
    python run_triage.py --input urls.txt --vuln ssrf --backend ollama --model llama3
"""

import argparse
import json
import sys
from pathlib import Path

from chunker import load_lines, load_text, chunk, format_batch_for_prompt
from prompt_loader import load_templates, resolve_template
from config import get_backend, DEFAULT_BACKEND, SUPPORTED_BACKENDS

PROMPT_LIBRARY_DIR = Path(__file__).resolve().parent.parent / "prompt_library"

VULN_FILE_MAP = {
    "sqli": "01_sqli.md",
    "idor": "02_idor_bola.md",
    "ssrf": "03_ssrf.md",
    "xss": "04_xss.md",
    "auth": "05_auth_jwt.md",
    "csrf": "06_csrf.md",
    "logic": "07_business_logic.md",
    "access": "08_access_control.md",
}


def main():
    parser = argparse.ArgumentParser(
        description="AI-triage pipeline for bug bounty recon data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input", required=True,
                         help="Path to raw recon output, one item per line "
                              "(e.g. gau/katana urls.txt).")
    parser.add_argument("--vuln", required=True, choices=VULN_FILE_MAP.keys(),
                         help="Which prompt library file to use.")
    parser.add_argument("--template", default=None,
                         help="Template label for multi-template files "
                              "(xss: A/B, auth: A/B). Defaults to the first "
                              "template in the file.")
    parser.add_argument("--backend", default=DEFAULT_BACKEND,
                         choices=SUPPORTED_BACKENDS,
                         help=f"Default: {DEFAULT_BACKEND} "
                              "(override with PIPELINE_BACKEND env var).")
    parser.add_argument("--model", default=None,
                         help="Override the backend's default model.")
    parser.add_argument("--batch-size", type=int, default=200,
                         help="Items per batch (100-300 recommended). Default: 200.")
    parser.add_argument("--output", default="triage_output.json",
                         help="Where to save results. Default: triage_output.json")
    parser.add_argument("--dry-run", action="store_true",
                         help="Build and preview prompts without calling any API "
                              "or writing output. Use this to sanity-check batching "
                              "before spending tokens.")
    args = parser.parse_args()

    md_path = PROMPT_LIBRARY_DIR / VULN_FILE_MAP[args.vuln]
    if not md_path.exists():
        sys.exit(f"Prompt file not found: {md_path}")

    templates = load_templates(str(md_path))
    try:
        label, template = resolve_template(templates, args.template)
    except ValueError as e:
        sys.exit(str(e))

    is_workflow_prompt = "{workflow_description}" in template

    backend = None
    if not args.dry_run:
        try:
            backend = get_backend(args.backend, args.model)
        except (ImportError, RuntimeError) as e:
            sys.exit(f"Backend setup failed: {e}")

    results = []

    if not Path(args.input).exists():
        sys.exit(f"Input file not found: {args.input}")

    if is_workflow_prompt:
        # Business-logic style prompt: the whole file is one workflow
        # description, not a batch of recon items. Single call, no chunking.
        description = load_text(args.input)
        if not description:
            sys.exit(f"{args.input} is empty -- write the workflow description first.")

        print(f"Loaded workflow description from {args.input} ({len(description)} chars)")
        print(f"Using template: {args.vuln} / {label!r}")

        prompt = template.replace("{workflow_description}", description)

        if args.dry_run:
            print("\n--- Prompt preview ---")
            print(prompt[:500] + ("..." if len(prompt) > 500 else ""))
            print("\nDry run complete. No API calls made, no output written.")
            return

        print(f"Sending to {args.backend}...")
        raw = backend.generate_json(prompt)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            print("  Warning: response was not valid JSON, keeping raw text.")
            parsed = {"_raw": raw}
        results.append(parsed)

    else:
        items = load_lines(args.input)
        if not items:
            sys.exit(f"No items found in {args.input}")

        print(f"Loaded {len(items)} items from {args.input}")
        print(f"Using template: {args.vuln} / {label!r}")
        print(f"Batch size: {args.batch_size} -> "
              f"{(len(items) + args.batch_size - 1) // args.batch_size} batch(es)")

        for i, batch in enumerate(chunk(items, args.batch_size), start=1):
            prompt = template.replace("{batch}", format_batch_for_prompt(batch))

            if args.dry_run:
                print(f"\n--- Batch {i} preview ({len(batch)} items) ---")
                print(prompt[:500] + ("..." if len(prompt) > 500 else ""))
                continue

            print(f"Sending batch {i} ({len(batch)} items) to {args.backend}...")
            raw = backend.generate_json(prompt)
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                print(f"  Warning: batch {i} did not return valid JSON, keeping raw text.")
                parsed = {"_raw": raw}
            results.append(parsed)

    if args.dry_run:
        print("\nDry run complete. No API calls made, no output written.")
        return

    Path(args.output).write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved {len(results)} batch result(s) to {args.output}")
    print("Reminder: this is a shortlist, not a finding. "
          "Run the human verification checklist before trusting any of it.")


if __name__ == "__main__":
    main()
