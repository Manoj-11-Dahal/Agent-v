---
name: decision-group-deliberation
description: Design accountable multi-person decisions with clear ownership, independent input, evidence
  review, predeclared aggregation rules and preserved dissent. Prevents consensus theater, voting-rule
  manipulation and synthetic-agent agreement from being mistaken for independent authority.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- group-decisions
- governance
- dissent
when-to-use:
- Design accountable multi-person decisions with clear ownership, independent input, evidence review,
  predeclared aggregation rules and preserved dissent. Prevents consensus theater, voting-rule manipulation
  and synthetic-agent agreement from being mistaken for independent authority.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-framing-and-goals
  - decision-fairness-and-stakeholders
---

# Group Deliberation and Decision Governance

## When to use
Use when several people hold different knowledge, interests or decision rights and a single analyst should not silently choose the values. Separate consultation, recommendation, consent and final authorization. A technical majority is not automatically entitled to impose costs on a nonparticipating group.

## Governance contract
Identify the accountable owner, participants, affected nonparticipants, required approvals, consultation obligations, deadline and dispute path. Specify quorum and what happens if it is not met. Clarify which requirements are hard constraints, which objections require review and which preferences can legitimately be aggregated.

## Procedure
1. Define the decision and feasible options before asking for a vote. Make evidence and constraints accessible in comparable form; exclude known gate failures instead of allowing enthusiasm to override them.
2. Choose the process in advance: owner decides after advice, consensus, consent with defined objections, voting, expert recommendation or another authorized rule. State the tie, abstention, missing-response and appeal rules.
3. Collect initial estimates and concerns independently where practical, before a senior person's preference anchors the group. Allow a safe way to surface material concerns without unnecessary disclosure of personal or confidential information.
4. Separate disagreements about facts, models, values and authority. Evidence gathering can help factual disagreement; it cannot by itself settle legitimate differences in preferences or rights.
5. Review claim provenance and independence. Five agents repeating one document are not five sources. Synthetic personas can help organize critique but are not independent human stakeholders, experts or votes.
6. Facilitate focused challenge: strongest alternative, missing stakeholder, plausible failure mechanism and what finding would change each position. Preserve minority concerns proportionate to their consequence, not their popularity.
7. Apply the predeclared rule and show how the result follows. Distinguish a ranking exercise from an approval event. Avoid changing the rule after observing which option wins.
8. Have the authorized owner record the choice, rationale, residual objections, conditions and responsible executors. If required consent or approval is absent, record a hold rather than falsely describing consensus.
9. Set a review trigger and appeal path. Evaluate whether the process heard affected parties and produced usable evidence, not merely whether everyone signed a document.

## Aggregation cautions
Plurality, majority comparisons, ranked-choice methods and Borda scoring can disagree. None is a universally correct substitute for the governance contract. Preference intensity, strategic reporting, agenda selection and the set of alternatives affect outcomes. A numerical average of incomparable scores can obscure value conflicts rather than resolve them.

For expert forecasts, aggregation needs an account of calibration and dependence. Weighting a famous or confident participant more heavily without relevant evidence can worsen performance. Do not infer reliability from style, role-play or apparent unanimity among correlated model outputs.

## Failure modes and deliverable
Watch for performative consultation after a decision is already fixed, vague veto rights, hidden conflicts of interest, quorum shortcuts, pressure to erase dissent and attributing decisions to absent participants. Return the governance contract, participant coverage, evidence/disagreement map, method-specific result, actual authorization status, unresolved dissent and review plan. Stop or escalate if the rule cannot legitimately decide the matter.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-framing-and-goals](../decision-framing-and-goals/SKILL.md).
- [Related method: decision-fairness-and-stakeholders](../decision-fairness-and-stakeholders/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
