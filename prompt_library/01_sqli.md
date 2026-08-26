# SQL injection — AI triage prompt

## Trigger / input
A batch of endpoint URLs with their parameters (query string, POST body
keys, JSON keys, path segments), ideally with parameter names visible.
Works from black-box recon (`gau`/`katana` output) — no source needed.

## Guardrails
- Strip any real parameter *values* that look like session tokens,
  emails, or customer data — keep parameter *names* and endpoint shapes
  only.
- Batch size: 100–300 endpoints per call.
- This prompt only *shortlists candidates* — it never crafts or sends
  an actual injection payload. Payload construction and sending stays
  manual, in-scope, and yours.

## Prompt template

```
You are a security data triager, not an attacker. You will not generate
injection payloads or attack strings. Analyze the following list of
crawled endpoints and their parameters:

{batch}

Task:
1. Flag parameters that are likely passed into database queries: sort
   fields, filter fields, search fields, ID lookups, "orderBy"/"sortBy"
   style params, and any parameter whose name suggests raw column or
   table selection.
2. Note which HTTP method each candidate uses (GET/POST/PUT/PATCH/DELETE).
3. Rank each candidate as high/medium/low interest based on: parameter
   controls query structure (high) vs. parameter is a plain filter value
   (medium) vs. parameter looks unrelated to any query (low).
4. Do not include static assets or obviously non-data endpoints.

Return strictly valid JSON in this structure:
{
  "candidates": [
    {
      "endpoint": "",
      "method": "",
      "parameter": "",
      "interest": "high|medium|low",
      "reason": ""
    }
  ]
}
```

## Output schema
`candidates[]` — one entry per flagged parameter, with `interest` used
to sort your manual queue.

## Human verification checklist (from Playbook Playbook 02)
- [ ] Establish a clean-session baseline response for the endpoint.
- [ ] Manually test the flagged parameter, comparing responses.
- [ ] Look for database errors or deterministic behavioral differences —
      never assume from the AI's "high" label alone.
- [ ] Classify: error-based, boolean-blind, time-blind, UNION, stacked,
      or second-order.
- [ ] Reproduce from a clean session before considering it valid.
- [ ] Minimize requests before writing up.
