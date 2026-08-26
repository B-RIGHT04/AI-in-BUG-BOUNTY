# XSS — AI triage prompt

## Trigger / input
Two flavors of input, use whichever you have:
- **Endpoint/parameter list** — for reflected/stored candidate discovery.
- **Client-side JS bundles** — for DOM-XSS source-to-sink tracing (this
  is the strongest use of AI here, per `ai_bugbounty.md` §2A).

## Guardrails
- Batch size: 100–300 endpoints, or one JS file per call if it's large
  (large minified bundles eat context fast — split by file).
- No payload generation in this prompt — pattern-matching only.

## Prompt template A — endpoint/parameter triage

```
You are a security data triager. Analyze the following endpoints and
parameters:

{batch}

Task:
1. Flag parameters likely to be reflected into HTML responses: search
   fields, comment/message bodies, display-name fields, redirect/error
   message params, or anything echoed back in a confirmation page.
2. Note whether the endpoint appears to render user content immediately
   (reflected candidate) or store it for later display (stored candidate).
3. Rank interest high/medium/low.

Return strictly valid JSON:
{
  "xss_candidates": [
    {"endpoint": "", "parameter": "", "type": "reflected|stored|unclear", "interest": "high|medium|low", "reason": ""}
  ]
}
```

## Prompt template B — DOM source-to-sink tracing

```
You are a security data triager. Analyze the following JavaScript for
DOM XSS risk. Do not write exploit payloads.

{batch}

Task:
1. Identify all "sources" of attacker-influenceable data: location.search,
   location.hash, document.referrer, postMessage handlers, localStorage/
   sessionStorage reads, URL path parsing.
2. Identify all "sinks" that can execute or inject content: innerHTML,
   outerHTML, document.write, insertAdjacentHTML, eval, Function(),
   setTimeout/setInterval with string args, jQuery .html().
3. Trace and report any source-to-sink path you can identify, even if
   sanitization appears present (note if sanitization is visible).

Return strictly valid JSON:
{
  "dom_xss_paths": [
    {"source": "", "sink": "", "file_or_location": "", "sanitization_observed": true, "notes": ""}
  ]
}
```

## Output schema
`xss_candidates[]` and/or `dom_xss_paths[]` — feeds your manual browser
testing queue.

## Human verification checklist (from Playbook Playbook 01)
- [ ] Submit a unique marker and confirm reflected vs. stored vs. neither.
- [ ] Determine the injection context: HTML body, attribute, JS, CSS, URL,
      or DOM sink.
- [ ] Test encoding/filtering/normalization to find the actual sanitization gap.
- [ ] Confirm real browser execution before reporting — a reflected
      marker alone is not proof.
- [ ] Assess impact: self-XSS, victim interaction required, privileged
      user affected.
