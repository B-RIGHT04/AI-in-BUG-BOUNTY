# Broken access control — AI triage prompt

## Trigger / input
Full endpoint list plus, if you have it, a rough role map (which roles
exist: anonymous, normal user, premium, moderator, admin).

## Guardrails
- Batch size: 100–300 endpoints.
- This prompt shortlists which endpoints to test under multiple roles —
  it does not perform the multi-role testing itself; that's inherently
  manual (you need real authenticated sessions per role).

## Prompt template

```
You are a security data triager. Analyze the following endpoints:

{batch}

Known roles in this application: {role_list}

Task:
1. Flag endpoints that look administrative, moderator-only, or
   privileged based on naming/path (e.g. "/admin", "/internal",
   "/manage", "/staff") even if you can't confirm enforcement.
2. Flag endpoints that appear to serve or modify data scoped to a
   specific tenant/org/account, where cross-tenant access would be
   meaningful (multi-tenant SaaS pattern).
3. For each, list which roles you'd want to test this endpoint with,
   in priority order (usually: anonymous first, then lowest authenticated
   role, then target role).

Return strictly valid JSON:
{
  "access_control_candidates": [
    {"endpoint": "", "method": "", "apparent_privilege_level": "", "roles_to_test": [], "reason": ""}
  ]
}
```

## Output schema
`access_control_candidates[]` — your multi-role testing queue.

## Human verification checklist (from Playbook Playbook 04)
- [ ] Test with anonymous, normal user, and (if available) escalated
      roles against each flagged endpoint.
- [ ] Confirm authorization checks happen server-side, not just hidden
      in the UI.
- [ ] Test whether a normal user can reach admin-only functionality
      directly by URL/route.
- [ ] Test cross-tenant access explicitly for multi-tenant features.
