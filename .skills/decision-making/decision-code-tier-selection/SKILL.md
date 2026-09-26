---
name: decision-code-tier-selection
description: Choose the quality tier a task actually requires from blast radius, reversibility, external exposure, regulation and lifetime. Detects under-tiering that harms users and over-tiering that wastes effort, and records the tier requirement for later review.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision module; examples and fixtures are synthetic teaching data.
compatibility: Documentation-first. No SDK, inference service, compiler or external execution is required.
tags:
- decision-suite
- advanced-decisions
- code-quality
- tier-selection
- code-standards
when-to-use:
- Decide what quality bar a task requires before implementation begins.
- Detect a requested tier that is too low for the risk or too high for the value.
- Record the required tier so later reviews judge against the right standard.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution or guaranteed outcome.
  related-skills:
  - decision-skills
  - decision-code-quality-tiers
  - decision-risk-and-reversibility
  - decision-resource-and-priority
  - decision-hxmax-standard
---
# Decision Skills: Code Quality Tier Selection — Choose the Required Tier Before Writing

**Scope.** Decide what quality tier a piece of work actually *requires* before anyone starts writing it. The mistake this prevents is spending advanced-engineering effort on a throwaway script, or shipping a throwaway-quality change into a path that harms people.

## Required inputs

1. Blast radius: who is harmed if the code fails, and how many of them.
2. Reversibility: can the effect be undone, and within what time window?
3. External exposure: does untrusted input or a network boundary reach this code?
4. Regulation or contract: is there a legal, contractual or safety obligation?
5. Lifetime: throwaway, weeks, or maintained for years?
6. Requested tier, if a requester already stated one, and their reason.

## Rule set (evaluated in order, highest requirement wins)

| Condition | Required tier |
|---|---|
| Safety-relevant, irreversible harm, regulated, or third-party lives/money at stake | tier-5 hxmax |
| Money movement, health data, authentication, cryptography, or externally reachable attack surface with high blast radius | tier-4 advanced |
| Customer-facing production service, or externally reachable input with medium blast radius | tier-2 very good (tier-3 excellent if multi-year lifetime) |
| Single-user local exploration, discardable, no external input | tier-0 basic |

Adjustments are applied after the rule match and are recorded: if the matched tier is tier-0 but more than one person or an automated job depends on the result, the requirement rises to tier-1. Reversibility may relax a requirement by at most one tier, never below tier-1 once more than one person depends on the result. Regulation and safety obligations only ever raise the requirement.

## Procedure

1. Record the six inputs; write `unknown` where unknown and treat unknown blast radius as **high** for this decision.
2. Evaluate the rule set top-down; the first matching condition sets the required tier.
3. Apply the reversibility adjustment with the reason written down.
4. Compare the required tier to the requested tier:
   - requested < required → `gap`; state which controls must be added.
   - requested > required → `excess`; state what cost the extra tier buys and who approved paying it.
   - equal → `aligned`.
5. Write the tier requirement into the task record so later reviews judge against it, not against a different standard.
6. Route to [decision-code-quality-tiers](../decision-code-quality-tiers/SKILL.md) for the assessment and [decision-code-writing-practice](../decision-code-writing-practice/SKILL.md) for implementation at that tier.

## Interpretation limits

- The rules are heuristics for a stated context. A named accountable human may override them, and the override must be recorded with a reason.
- "Required tier" is a floor, not a target. Exceeding it is allowed if the cost is approved.
- Nothing here decides staffing, schedule or budget.
- Unknown inputs make the answer conservative, not wrong; resolving them may lower the requirement.

## Failure modes

- **Throwaway drift.** A prototype quietly becomes production because nobody re-ran the tier decision.
- **Vanity tiering.** Demanding HXMax for an internal report generator, then missing the deadline and skipping review entirely.
- **Reversibility hand-waving.** Calling a data migration reversible because a backup "exists" without testing the restore.
- **Unknown treated as low risk.** Missing blast-radius information recorded as small.
- **Silent downgrade.** Accepting a lower tier than required without recording who accepted the residual risk.
