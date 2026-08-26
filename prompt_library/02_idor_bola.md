# IDOR / BOLA — AI triage prompt

## Trigger / input
An endpoint + parameter list, or an OpenAPI/Swagger export if the
program publishes one. This is the category your own `ai_bugbounty.md`
already had a working example for — this template extends it slightly
with the Playbook's classification fields.

## Guardrails
- Batch size: 100–300 endpoints, or split large OpenAPI specs by tag/module.
- Strip real object IDs belonging to other users if you happen to have
  them from your own account's traffic — keep the parameter shape, not
  someone else's data.

## Prompt template

```
You are a security data parser. Analyze the following list of crawled
or documented API endpoints:

{batch}

Task:
1. Identify all state-changing endpoints (POST/PUT/DELETE/PATCH).
2. Flag endpoints accepting an object identifier (id, uuid, account_id,
   org_id, invoice_id, document_id, message_id, or similar) that also
   require authentication — these are IDOR/BOLA candidates.
3. Note whether the identifier looks sequential/predictable (numeric,
   incrementing) vs. opaque (UUID) — sequential IDs are easier to enumerate.
4. Separately flag administrative, internal, or debug routes.
5. Filter out static assets and anything clearly not touching per-user data.

Return strictly valid JSON in this structure:
{
  "idor_candidates": [
    {"endpoint": "", "method": "", "id_parameter": "", "id_type": "sequential|opaque", "reason": ""}
  ],
  "admin_or_debug_routes": [
    {"endpoint": "", "method": "", "reason": ""}
  ]
}
```

## Output schema
Two arrays: `idor_candidates` (feeds your two-account cross-test queue)
and `admin_or_debug_routes` (feeds Playbook 04, broken access control).

## Human verification checklist (from Playbook Playbook 03)
- [ ] Create two authorized test accounts where permitted.
- [ ] Record Account A's object identifier, then Account B's.
- [ ] Request Account A's object while authenticated as B.
- [ ] Test read, then update, then delete (only where explicitly safe
      and permitted) access.
- [ ] Confirm the issue is server-side missing authorization, not just
      a client-side UI hide.
