---
name: decision-code-improvement-priority
description: Rank known code problems by severity, blast radius, confidence and fix risk, adjusted for effort, then split them into fix-now, defer-with-recorded-risk and accept. Reports genuine ties instead of inventing tiebreakers.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision module; examples and fixtures are synthetic teaching data.
compatibility: Documentation-first. No SDK, inference service, compiler or external execution is required.
tags:
- decision-suite
- advanced-decisions
- code-quality
- technical-debt
- prioritisation
- code-improvement
when-to-use:
- Decide which known code problems to fix now and which to defer with a recorded risk.
- Rank improvements by harm avoided per unit of effort rather than by loudest complaint.
- Stop unrecorded deferrals from becoming unowned accepted risks.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution or guaranteed outcome.
  related-skills:
  - decision-skills
  - decision-resource-and-priority
  - decision-code-quality-tiers
  - decision-risk-and-reversibility
  - decision-commit-and-monitor
---
# Decision Skills: Code Improvement Priority — Order the Fixes That Actually Matter

**Scope.** Given a list of known code problems, decide what to fix now, what to defer with a recorded risk, and what to leave alone. The output is an ordered plan a team can execute, not a wish list.

## Required inputs

For each candidate fix: severity, blast radius, confidence that the defect is real, implementation effort, risk of the fix itself, and a written statement of the harm if it is deferred. The harm statement is required input, not optional commentary: an item without one cannot be deferred.

## Priority rule

```
priority = (0.40 × severity + 0.25 × blast-radius + 0.15 × confidence + 0.20 × fix-risk)
           × (1.25 if irreversible else 1.00)
cost-adjusted = priority ÷ max(0.10, effort)
```

All factors are 0.0–1.0. Weights sum to 1.0 and are recorded with the reason; the 1.25 multiplier applies when the harm cannot be undone. `effort` has a floor of 0.10 so that a trivially cheap fix cannot be made infinitely attractive by dividing by zero.

## Procedure

1. **List candidates** with all seven fields. Reject any candidate with a missing field, a blank harm statement, or a factor outside 0.0–1.0.
2. **Compute priority and cost-adjusted priority** for each.
3. **Rank by cost-adjusted priority**, highest first. Ties are reported as ties; they are not broken by name, order of arrival, or who complained loudest.
4. **Split mandatory from optional.** An item is *mandatory* when its harm is irreversible or its severity ≥ 0.80. Mandatory items are always `fix-now`, even when the list exceeds the effort cap — the cap is then a resourcing problem to escalate, not a reason to drop the item.
5. **Classify the optional items** in ranked order: `fix-now` while the remaining effort allows; `defer-with-risk` when it does not, which requires a written harm statement, detection path and review date; `accept` only when the fix risk exceeds the 0.60 floor *and* a named human records the acceptance. A deferral candidate with no harm statement is rejected outright.
6. **Record every deferral** with the harm statement, detection path and review date. An unrecorded deferral is an accepted risk nobody owns.
7. **Re-run after each fix**, because fixing one defect changes the blast radius of others.

## Interpretation limits

- The formula orders attention; it does not measure harm. A severity of 0.9 is a judgement, not a measurement.
- Weights are preferences. Changing them changes the ranking, so changes must be recorded with a reason.
- Ties are real information: two problems genuinely worth equal attention. Do not invent a tiebreaker.
- Nothing here authorizes spending, staffing or release.

## Failure modes

- **Effort blindness.** Ranking by severity alone, so a two-week fix crowds out five one-hour fixes with similar harm.
- **Silent deferral.** "Later" with no harm statement, owner or review date.
- **Fix-risk ignored.** Rewriting a stable module and introducing a worse defect.
- **Weight fiddling** to make a preferred item rank first.
- **Tie-breaking by identity** — by ticket number, reporter seniority, or alphabetical order — which hides a genuine tie.
- **Stale ranking.** Reusing a priority list computed before the last three fixes landed.
