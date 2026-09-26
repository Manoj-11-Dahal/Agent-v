---
name: decision-game-theory-and-incentives
description: Analyze choices when other actors adapt to policies or pursue different goals. Maps players,
  information, timing and incentives; checks best responses and mechanism failure modes; and favors enforceable,
  ethical designs over predictions based on assumed cooperation.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- game-theory
- incentives
- mechanism-design
when-to-use:
- Analyze choices when other actors adapt to policies or pursue different goals. Maps players, information,
  timing and incentives; checks best responses and mechanism failure modes; and favors enforceable, ethical
  designs over predictions based on assumed cooperation.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-negotiation-design
  - decision-systems-and-feedback
---

# Game Theory and Incentive-aware Decisions

## When to use
Use when a proposed policy changes what teams, users, vendors or agents are rewarded for doing. An action that looks good against a passive environment can fail when others adapt. Game-theoretic models are structured hypotheses about behavior, not proof that real people optimize a known payoff table.

## Model contract
List actors, available actions, information, timing, repeated interactions, outside options and enforceable commitments. Distinguish observed incentives from assumed utilities. Include people affected by the mechanism who do not participate in the strategic interaction. Respect legal, privacy, labor and other applicable constraints.

## Procedure
1. Define the operational objective and hard boundaries. Make clear whose utility is being represented; do not silently equate the designer's metric with everyone's welfare.
2. Map the interaction structure: simultaneous or sequential choices, hidden information or hidden action, one-shot or repeated play. A matrix for simultaneous choices cannot answer every sequential commitment question.
3. Describe plausible payoffs with sources and ranges. Include effort, delay, reputation, risk and future opportunities where relevant. Ordinal preferences may support best-response comparisons without justifying arithmetic comparisons of total welfare.
4. Compute each actor's best response under the stated assumptions. Identify dominant strategies or equilibria when the model supports them, and note ties or multiple equilibria. Failure to find a pure equilibrium does not mean no strategic solution exists.
5. Compare individually attractive behavior with the intended system outcome. Look for externalities, free riding, adverse selection, moral hazard, metric gaming and incentives to hide failures.
6. Generate mechanism changes: better observability, simpler compliant paths, verified eligibility, aligned rewards, shared benefits, reversible commitments and proportionate accountability. Ensure controls are lawful and authorized; avoid manipulative or coercive exploitation.
7. Recompute incentives under realistic enforcement and measurement error. A stated penalty with little chance of detection may not change expected incentives; a false-positive-prone control can create new harms.
8. Stress-test adaptation, collusion, identity splitting, substitute metrics, unequal resources and behavior outside the model. Do not provide exploitation tactics; use these checks to strengthen legitimate governance and system design.
9. Pilot within approved boundaries, observe actual behavior and update the model. State which observations would falsify the predicted response.

## Interpretation boundaries
An equilibrium is not automatically efficient, fair, stable under learning, or what real actors will choose. Multiple equilibria need an account of coordination and expectations. Repeated-game reasoning depends on horizons, observability and credible future responses; do not assume cooperation simply because parties might interact again.

## Failure modes
Avoid inventing precise utility numbers, assuming everyone shares the designer's objective, adding unenforceable commitments, or claiming an adversarial review certifies security. Optimize the mechanism's real outcome rather than an easily gamed proxy. Apparent agreement can mask asymmetric power or excluded stakeholders.

## Deliverable
Return the actor/action/information map, payoff assumptions, best-response analysis, intended and unintended incentives, candidate design changes, enforcement and fairness limits, and a bounded evaluation plan. If private information or behavior is too uncertain, present scenario-dependent recommendations rather than a single confident prediction. No recommendation authorizes sanctions, surveillance or communication by itself.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-negotiation-design](../decision-negotiation-design/SKILL.md).
- [Related method: decision-systems-and-feedback](../decision-systems-and-feedback/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
