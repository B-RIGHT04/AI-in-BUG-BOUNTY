# Business logic flaws — AI triage prompt

## Trigger / input
This one is different from the others: instead of a raw endpoint list,
feed it *your own written description* of a workflow's intended
sequence (e.g. "checkout: add to cart → apply coupon → enter payment →
confirm → charge"). AI is weakest at spotting business logic issues
cold, but strong at systematically listing "what happens if this step
is skipped/repeated/reordered" once you've described the flow.

## Guardrails
- No live data needed here at all — this is a reasoning exercise over
  a workflow description you write yourself.

## Prompt template

```
You are a security-minded reviewer helping a human bug bounty
researcher think through a workflow. Here is the intended sequence of
a feature:

{workflow_description}

Task: For this workflow, generate a checklist of things a malicious
customer might try, covering:
1. Skipping a step (which steps look skippable if the client controls
   navigation?).
2. Repeating a step (would repeating a step cause double effects —
   double discount, double credit, double shipment?).
3. Reordering steps (what happens if a later step is called before an
   earlier one completes?).
4. Tampering with values the client might send (price, quantity,
   discount %, currency, user ID) that the server might trust instead
   of recalculating.
5. Concurrency (would doing two steps at the same time cause a race —
   see the race-condition prompt for a deeper pass).

Return strictly valid JSON:
{
  "logic_test_cases": [
    {"category": "skip|repeat|reorder|value_tamper|concurrency", "test": "", "why_it_might_work": ""}
  ]
}
```

## Output schema
`logic_test_cases[]` — a manual test plan, not a finding list. This
prompt produces *questions to try*, never a verdict.

## Human verification checklist (from Playbook Playbook 17)
- [ ] Actually attempt each generated test case against your own test
      account in the real application.
- [ ] Confirm whether the server trusts client-side calculations
      (price, totals) or recalculates server-side.
- [ ] Test negative values and boundary values where applicable.
- [ ] Prioritize anything touching payments, discounts, credits,
      refunds, transfers, or permissions.
