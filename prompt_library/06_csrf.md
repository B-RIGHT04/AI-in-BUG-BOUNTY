# CSRF — AI triage prompt

## Trigger / input
List of state-changing endpoints (method + purpose), ideally with any
headers/cookies you've observed being sent (names only).

## Guardrails
- Batch size: 100–300 endpoints.
- Never include actual cookie *values* or CSRF token *values* — names only.

## Prompt template

```
You are a security data triager. Analyze the following state-changing
endpoints:

{batch}

Task:
1. Flag endpoints that change account state: email change, password
   change, settings change, payment info, API key creation, resource
   deletion, permission change.
2. Note whether a CSRF token parameter/header name is visible in the
   request shape, and whether it looks required or optional based on
   naming.
3. Rank interest high/medium/low based on the sensitivity of the action
   (financial/permission changes = high).

Return strictly valid JSON:
{
  "csrf_candidates": [
    {"endpoint": "", "method": "", "action": "", "token_param_observed": "", "interest": "high|medium|low"}
  ]
}
```

## Output schema
`csrf_candidates[]` — sorted by action sensitivity for manual testing.

## Human verification checklist (from Playbook Playbook 06)
- [ ] Confirm whether a token is required and validated server-side
      (not just present in the form).
- [ ] Check SameSite cookie attribute.
- [ ] Check whether a custom header is required (blocks simple cross-origin forms).
- [ ] Attempt to actually trigger the action cross-origin before reporting.
