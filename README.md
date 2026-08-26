# Recon-to-AI pipeline (stages 1-3)

Reads raw recon output, batches it, and runs it through one of the
`prompt_library/` templates against an LLM backend. Produces a
structured JSON **shortlist** — never a finding. Stage 4 (manual
verification) and stage 5 (reporting) are still on you.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --break-system-packages   # or drop the flag inside a venv
cp .env.example .env   # fill in ANTHROPIC_API_KEY at minimum
export $(cat .env | grep -v '^#' | xargs)   # or use python-dotenv / your own method
```

Only install the extra package (`openai`, `google-genai`, or `requests`)
for backends you actually plan to use — see the comments in
`requirements.txt`.

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

- Everything except `logic` expects `--input` to be a plain text file,
  one recon item (URL, endpoint) per line — e.g. straight out of `gau`,
  `katana`, or `httpx`.
- `logic` (business logic) expects `--input` to be a short paragraph
  *you write* describing a workflow's intended sequence. It runs once,
  not batched — see `prompt_library/07_business_logic.md`.

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
