# Recon-to-AI pipeline (stages 1-3)

Reads raw recon output, batches it, and runs it through one of the
`prompt_library/` templates against an LLM backend. Produces a
structured JSON **shortlist** — never a finding. Stage 4 (manual
verification) and stage 5 (reporting) are still on you.

## End-to-end workflow (recon tool → this pipeline → you)

This pipeline doesn't do recon itself — it consumes the output of a
separate recon tool (the Automated_Recon
project). The full loop:

1. **Run the recon tool.** In that project: activate its venv, confirm
   `config.yaml` has the right target active, run Phase 1 discovery +
   Phase 2 param extraction as usual.
2. **It writes output** to `data/<program>/urls/urls.txt` (plain URL
   list) and `data/<program>/params/params.json` (structured param
   data, see "Input format" below).
3. **Switch to this project.** cd into `pipeline/`, activate *this*
   project's venv (separate from the recon tool's), confirm your API
   key env var is set for this shell.
4. **Dry-run first**, pointing `--input` straight at a file from the
   recon project — no copying needed:
   ```bash
   python run_triage.py --input ~/Documents/~xss-recon/data/dell_bounty/params/params.json --vuln sqli --backend gemini --dry-run
   ```
5. **Run it for real** once the preview looks right — drop `--dry-run`,
   add `--output`. Repeat per vuln type and per input file (`urls.txt`
   works well for idor/ssrf/xss; `params.json` is the stronger input
   for sqli/idor since it carries parameter names and source).
6. **Manually verify.** Open the output JSON, then work through the
   "Human verification checklist" at the bottom of the matching
   `prompt_library/*.md` file. Nothing here is a finding until you've
   confirmed it yourself, in scope, with any required auth headers
   (e.g. Dell's `X-Bug-Bounty` header) applied by the recon tool, not
   this pipeline — this pipeline never contacts the target directly.

**Before a real run against a live target (not vulnweb.com):** double
check which backend you're using. Free-tier Gemini's terms allow your
prompt data to be used to improve Google's models — fine for test data,
worth a conscious choice once it's real target data. Paid Gemini and
Claude don't have that trade-off.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --break-system-packages   # or drop the flag inside a venv
cp .env.example .env   # fill in the key for whichever backend(s) you're using
export $(cat .env | grep -v '^#' | xargs)   # or use python-dotenv / your own method
```

Only install the extra package (`openai`, `google-genai`, or `requests`)
for backends you actually plan to use — see the comments in
`requirements.txt`. `google-genai` is the one to install for the free
Gemini tier: `pip install google-genai --break-system-packages`.

## Usage

```bash
# Sanity-check batching and prompt wording before spending any tokens
python run_triage.py --input urls.txt --vuln idor --dry-run

# Real run, default backend (Claude)
python run_triage.py --input urls.txt --vuln idor --output idor_results.json

# Multi-template files (xss: A/B, auth: A/B) -- pick one
python run_triage.py --input js_urls.txt --vuln xss --template B

# Swap backend per-run
python run_triage.py --input urls.txt --vuln ssrf --backend ollama --model llama3

# Or set a new default for the session
export PIPELINE_BACKEND=gemini
```

`--vuln` options: `sqli`, `idor`, `ssrf`, `xss`, `auth`, `csrf`, `logic`, `access`
(maps to the 8 files in `../prompt_library/`).

## Input format

`--input` accepts three shapes, auto-detected:

- **Plain text, one item per line** — a URL or endpoint per line, e.g.
  straight out of `gau`, `katana`, `httpx`, or the recon tool's
  `urls.txt`. Used by everything except `logic`.
- **`params.json`** (any file ending in `.json`) — the structured
  parameter format the recon tool's Phase 2 extraction writes: a JSON
  array of `{url, param, source, method}` objects, where `source` is
  `"url"`, `"js"`, or `"html_form"`. Exact duplicates are deduped
  automatically. The `source` field is passed through to the AI, so it
  can weigh a confirmed form field differently from a regex-guessed JS
  reference. Best input for `sqli` and `idor` specifically.
- **A short paragraph you write** — only for `logic` (business logic),
  describing a workflow's intended sequence. Runs once, not batched —
  see `prompt_library/07_business_logic.md`.

## Guardrails carried over from `ai_bugbounty.md`

- Strip session tokens, auth headers, and real customer data from your
  recon files before running this — the prompts ask for structure and
  parameter *names*, not real values.
- Batches default to 200 items; keep it in the 100-300 range.
- `--dry-run` never calls an API or writes output — use it to check
  batching and prompt wording first.
- Every result is a shortlist. Run the "Human verification checklist"
  section of the relevant prompt file before treating anything as real.
- Only ever point `--input` at recon collected from a target you've
  confirmed is in scope for a program you're authorized on.

## Adding a backend or a new vuln type

- **New backend**: add a `backends/your_backend.py` implementing
  `generate_json(prompt) -> str` (see `backends/base.py`), then register
  it in `config.py`'s `get_backend()`.
- **New vuln type**: add the markdown file to `../prompt_library/`
  following the existing files' structure (a `## Prompt template`
  heading with a fenced code block containing `{batch}` or
  `{workflow_description}`), then add it to `VULN_FILE_MAP` in
  `run_triage.py`.
