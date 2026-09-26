---
name: decision-real-options
description: Value the flexibility to wait, pilot, expand, switch or abandon before irreversible commitments.
  Builds decision trees with information quality, timing, option expiry and switching costs instead of
  comparing only all-or-nothing plans.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- real-options
- staged-investment
- decision-trees
when-to-use:
- Value the flexibility to wait, pilot, expand, switch or abandon before irreversible commitments. Builds
  decision trees with information quality, timing, option expiry and switching costs instead of comparing
  only all-or-nothing plans.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-value-of-information
  - decision-risk-and-reversibility
---

# Real Options and Staged Commitments

## When to use
Use when important uncertainty may resolve before a costly irreversible commitment, and an initial step can preserve a later choice. Examples include piloting a service, staging an architecture migration or reserving capacity. Not every delay creates an option: missed windows, irreversible learning costs and dependencies can destroy value.

## Define the option precisely
Identify the initial cost, what right or capability it preserves, decision dates, expiry, observable signals, later actions, resource limits and authorized decision owners. Distinguish the right to act from an obligation to act. Do not use financial-option terminology to imply market pricing or guaranteed tradability for an operational project.

## Procedure
1. Establish feasible immediate actions and the no-commitment baseline. Use comparable net payoffs or utilities, including implementation and maintenance; do not double-count costs already included.
2. Identify what can be delayed without losing feasibility and what genuinely becomes irreversible at each stage. Include data disclosure and external commitments, not just cash expenditure.
3. Build a small tree with decision nodes, chance/observation nodes and terminal consequences. Distinguish the true state from an imperfect signal about that state.
4. Record state probabilities or defensible scenarios, signal accuracy and evidence dependence. If these are weak, analyze ranges rather than presenting a precise option value.
5. At each future decision node choose the best feasible authorized action given the information then available, including abandon or do nothing. Work backward to evaluate the staged policy.
6. Subtract pilot/learning costs, delay costs, switching costs and any exposure created by the experiment. Discount consistently if money and timing require it; do not mix undiscounted long-term benefits with discounted costs.
7. Compare the staged policy with immediate commitment and waiting without learning. Compute incremental value over the best feasible baseline, not over an artificially poor alternative.
8. Stress-test forecast errors, signal transfer, inability to abandon, expiring opportunities and correlated failures. Perfect information is an upper bound under the same assumptions, not a realistic pilot guarantee.
9. Define actual stage-gate evidence, owners, maximum cumulative spend and stop conditions. The second stage requires its own scope/approval check when appropriate; the initial pilot is not blanket authorization.

## Decision logic
A stage is attractive when the value of adaptation and learning exceeds its costs and lost opportunity, within hard constraints. Keep the distinction between information value and operational benefits of the pilot itself. A test that teaches little might still deliver direct value; a highly informative test might expose users to unacceptable harm.

## Failure modes
Avoid a tree that assumes a clear signal when the test is noisy, an abandonment branch that the organization would not honor, or “small” stages whose cumulative cost becomes an unapproved full project. Sunk cost does not create future benefit. Conversely, ignore sunk expenditure only when it truly cannot be recovered and does not affect future constraints.

## Deliverable
Return the decision tree, timing and expiry, payoff units, information model, staged-policy value and sensitivity, cumulative resource envelope, exact exercise/abandon triggers and residual risk. State which pieces are estimated, assumed or unidentifiable. This supports operational planning; domain-specific financial commitments require qualified review and actual authority.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-value-of-information](../decision-value-of-information/SKILL.md).
- [Related method: decision-risk-and-reversibility](../decision-risk-and-reversibility/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
