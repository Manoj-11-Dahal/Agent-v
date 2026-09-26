---
name: decision-code-review-and-verification
description: Decide whether a proposed review or verification plan covers every control required by the tier, map evidence to controls, compute coverage, and require explicit named risk acceptance for anything uncovered. Blocks self-review from counting as independent review.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision module; examples and fixtures are synthetic teaching data.
compatibility: Documentation-first. No SDK, inference service, compiler or external execution is required.
tags:
- decision-suite
- advanced-decisions
- code-quality
- code-review
- verification
- hxmax
when-to-use:
- Decide whether a review or verification plan is sufficient before it starts.
- Find controls that have no attributable evidence and decide how to close them.
- Record an explicit, named risk acceptance instead of a silent gap.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution or guaranteed outcome.
  related-skills:
  - decision-skills
  - decision-code-quality-tiers
  - decision-hxmax-standard
  - decision-evidence-and-uncertainty
  - decision-value-of-information
---
# Decision Skills: Code Review and Verification — Is the Evidence Plan Sufficient?

**Scope.** Decide whether a proposed review or verification plan is *sufficient* for the risk before the review starts, and what to do when it is not. This prevents the common failure where a review happens, feels thorough, and misses the one control that mattered.

## Required inputs

1. Required tier (from [decision-code-tier-selection](../decision-code-tier-selection/SKILL.md)) and its gate controls.
2. Proposed evidence: what tests, analyses and inspections are actually planned.
3. Residual risks the author already knows about.
4. Reviewer independence and competence for the domain.

## Coverage rule

- Every control in the required tier's gate needs at least one named piece of evidence in the review plan.
- Evidence must be *attributable*: a test name, an analysis report identifier, a review record — not "we tested it".
- A control with no evidence is an **uncovered requirement**, not a passed one.
- Independent review (C14) cannot be satisfied by the author alone, at any tier.

## Procedure

1. List the required controls for the tier.
2. Map each proposed evidence item to the control(s) it covers. One item may cover several controls; say which.
3. Compute coverage = covered controls ÷ required controls. Report uncovered controls by identifier.
4. If coverage is complete, verdict **sufficient**; record the mapping so a later reader can check it.
5. If incomplete, verdict **insufficient**, with two permitted responses:
   - **Add evidence** for the uncovered controls, or
   - **Accept the risk explicitly**: a named accountable human records the uncovered control, the harm if it materializes, the detection path, and the review date.
6. Re-run coverage after either response. Never mark the review sufficient because time ran out.
7. Check reviewer independence; if the reviewer is the author, C14 is uncovered regardless of effort.

## Interpretation limits

- Coverage is a completeness check on the *plan*, not proof the evidence is good. A weak test that covers a control still counts as coverage here and must be judged separately.
- Verdicts are advisory. Approval is a separate recorded human act.
- Accepting a risk is a legitimate decision; hiding it is not.

## Failure modes

- **Rubber-stamping.** A review recorded as complete with no control mapping.
- **Evidence inflation.** Counting one smoke test as covering failure paths, concurrency and performance.
- **Self-review as independent review.** The author approving their own tier-5 claim.
- **Time-box laundering.** Marking uncovered controls "deferred" with no owner, harm statement or review date.
- **Coverage of the wrong revision.** Reviewing a plan against controls from a different required tier.
