# SSRF — AI triage prompt

## Trigger / input
Endpoint list plus any form field names or JSON keys you've collected
(from crawling or JS analysis) — SSRF hides in features that accept a
URL or reference to a remote resource.

## Guardrails
- Batch size: 100–300 endpoints/fields.
- This prompt only shortlists candidate features. It does not generate
  interaction-server payloads or send requests — that stays manual,
  using your own authorized OOB interaction endpoint.

## Prompt template

```
You are a security data triager. Analyze the following endpoints and
field/parameter names:

{batch}

Task:
1. Flag any endpoint or field whose name or apparent purpose suggests it
   accepts a URL, webhook, callback, or remote reference: "url", "link",
   "webhook", "callback", "import", "feed", "avatar_url", "preview",
   "fetch", "source", or similar.
2. Note the feature category: URL preview, webhook registration, image
   import, PDF/document generation, feed/RSS import, or link unfurling.
3. Rank interest high/medium/low based on how directly the server
   appears to fetch the given reference server-side.

Return strictly valid JSON in this structure:
{
  "ssrf_candidates": [
    {"endpoint": "", "field": "", "feature_category": "", "interest": "high|medium|low", "reason": ""}
  ]
}
```

## Output schema
`ssrf_candidates[]` — sorted queue for manual OOB testing.

## Human verification checklist (from Playbook Playbook 05)
- [ ] Confirm the server actually makes the request (don't assume from
      naming alone).
- [ ] Use an authorized interaction endpoint to observe DNS/HTTP callback.
- [ ] Check whether redirects are followed and whether private/internal
      destinations are blocked.
- [ ] Assess real impact: internal service access, cloud metadata
      exposure, internal network reachability — not just "it made a request".
