---
name: decision-pareto-frontiers
description: Compare competing objectives without hiding value conflicts in arbitrary weights. Removes
  genuinely dominated options, distinguishes hard constraints from trade-offs, explores Pareto frontiers
  and uses stakeholder-approved aspiration or epsilon-constraint rules.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- pareto-frontier
- multi-objective
- dominance
when-to-use:
- Compare competing objectives without hiding value conflicts in arbitrary weights. Removes genuinely
  dominated options, distinguishes hard constraints from trade-offs, explores Pareto frontiers and uses
  stakeholder-approved aspiration or epsilon-constraint rules.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-options-and-tradeoffs
  - decision-fairness-and-stakeholders
---

# Multi-objective Decisions and Pareto Frontiers

## When to use
Use when options trade speed against cost, reliability against flexibility, or different stakeholder outcomes and no defensible single utility scale has been agreed. A Pareto frontier exposes trade-offs; it does not identify a uniquely fair or authorized winner. For an obvious dominated alternative, simple comparison may be enough.

## Required inputs
Define a feasible option set, objective directions, consistent units, relevant horizon and evidence ranges. Separate mandatory limits from aspirations. Record who may decide acceptable sacrifices, especially when costs and benefits fall on different people. A missing objective value is unknown, not automatically favorable or zero.

## Procedure
1. Apply hard gates before comparing objectives. Explicitly hold options with unresolved mandatory conditions outside the eligible frontier.
2. Choose a small set of distinct objectives. Inspect redundancy and missing stakeholders; renaming the same benefit three times does not create three independent reasons to favor an option.
3. Verify direction and units. Lower latency and lower cost are minimized; coverage or reliability may be maximized. Convert only when the transformation preserves the intended ordering and has a clear interpretation.
4. Define dominance. For minimization, A dominates B if A is no worse on every objective and strictly better on at least one. For mixed directions, compare each objective in its declared direction. Equal objective vectors are ties, not strict domination.
5. Remove dominated options only when the evidence justifies that relationship. With noisy estimates, distinguish point-estimate dominance from dominance robust to the supplied uncertainty ranges. Preserve near ties if measurement error could reverse them.
6. Display nondominated choices as a frontier or table, with differences in meaningful units. Explain what must be sacrificed to improve another objective; avoid presenting a visually attractive curve as an objective recommendation.
7. Elicit preferences through concrete trade-off questions or aspiration levels. An epsilon-constraint approach optimizes one objective while bounding others. Vary those bounds to show how the feasible recommendation changes.
8. If using a weighted sum, document scaling and weight meaning. Weighted sums can miss non-convex portions of a frontier; changing normalization can change rankings. Do not use weights as a hidden substitute for stakeholder agreement.
9. Select a bounded option or bring the unresolved value conflict to the owner. If no option satisfies all hard limits, revise scope, generate alternatives or ask for an explicit permitted constraint change; do not quietly soften a limit.

## Advanced checks
Include implementation cost, interactions and switching cost when moving along a frontier. Avoid comparing one option's best-case latency with another's observed average. If a frontier uses subgroup averages, inspect who bears the worst outcomes. Sensitivity to measurement and feasibility can matter more than minor point-estimate gains.

## Failure modes and output
An attractive nondominated option can still be unacceptable. A dominated option may only appear so because an important objective was omitted. The frontier depends on which feasible alternatives were generated, not only on the mathematics. Return eligible options, objective definitions, dominance witnesses, uncertainty treatment, frontier, preference/constraint sensitivity and a recommendation or explicit value disagreement.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-options-and-tradeoffs](../decision-options-and-tradeoffs/SKILL.md).
- [Related method: decision-fairness-and-stakeholders](../decision-fairness-and-stakeholders/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
