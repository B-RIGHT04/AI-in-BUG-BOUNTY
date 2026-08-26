# Authentication & JWT — AI triage prompt

## Trigger / input
Auth-flow endpoint list (register/login/reset/MFA), plus a JWT structure
if you have one — **paste the decoded header + claim *names* only, never
a live/valid signed token.**

## Guardrails
- Never paste a live, valid session token or real user credentials into
  a cloud API prompt. If you need to discuss a token's structure,
  redact the signature and any real claim values first.
- Batch size: keep auth-flow lists short (usually under 50 endpoints) —
  precision matters more than volume here.

## Prompt template A — auth flow mapping

```
You are a security data triager. Analyze the following authentication-
related endpoints:

{batch}

Task:
1. Categorize each into: registration, login, password reset, MFA,
   session management, or account linking.
2. Flag any endpoint that looks like it might leak whether an account
   exists (different responses/timing implied by naming, e.g. separate
   "email not found" vs "wrong password" style errors).
3. Flag any endpoint missing obvious rate-limiting indicators (e.g. no
   CAPTCHA/step-up mentioned nearby) based purely on structure — this is
   a hypothesis to test, not a finding.

Return strictly valid JSON:
{
  "auth_endpoints": [
    {"endpoint": "", "category": "", "enumeration_risk": "high|medium|low", "notes": ""}
  ]
}
```

## Prompt template B — JWT structure review (redacted tokens only)

```
You are a security data triager. Review this JWT header and claim
structure (values already redacted by the user):

{batch}

Task:
1. Identify the algorithm in the header (flag "none" or symmetric
   algorithms like HS256 as needing alg-confusion testing).
2. List which claims are present (exp, iss, aud, sub, role, etc.) and
   flag if expiration (exp) appears to be missing.
3. Flag if the claim set includes anything resembling a role/permission
   claim that a client could plausibly attempt to modify.

Return strictly valid JSON:
{
  "algorithm": "",
  "algorithm_risk": "high|medium|low",
  "claims_present": [],
  "missing_expected_claims": [],
  "role_claim_present": true
}
```

## Output schema
`auth_endpoints[]` for flow-level review; single JWT structure object
per token reviewed.

## Human verification checklist (from Playbook Playbook 07 & 15)
- [ ] Test rate limiting and account enumeration manually, don't trust
      the AI's structural guess.
- [ ] For JWT: test algorithm confusion, signature validation bypass,
      and claim manipulation against a real (your own) test account.
- [ ] Confirm token revocation and expiration actually behave as claimed.
- [ ] Test password-reset token entropy, expiration, and reuse manually.
