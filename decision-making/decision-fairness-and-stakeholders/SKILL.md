---
name: decision-fairness-and-stakeholders
description: Assess how a decision distributes benefits, errors, burdens and recourse across affected
  groups. Separates hard rights and legal requirements from policy preferences, inspects subgroup metrics
  with uncertainty, and designs meaningful human review and appeal.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- fairness
- stakeholder-impact
- contestability
when-to-use:
- Assess how a decision distributes benefits, errors, burdens and recourse across affected groups. Separates
  hard rights and legal requirements from policy preferences, inspects subgroup metrics with uncertainty,
  and designs meaningful human review and appeal.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-group-deliberation
  - decision-risk-and-reversibility
---

# Fairness, Stakeholder Impact and Contestability

## When to use
Use when allocation, screening, prioritization or automation materially affects people's opportunities, access, privacy or workload. Technical performance alone cannot determine acceptable distributions of harm. Do not infer sensitive traits from ambiguous signals merely to fill a fairness worksheet; use authorized, appropriate data and domain/legal review.

## Stakeholder and authority contract
Identify who benefits, who pays, who may be incorrectly included or excluded, who cannot opt out, and who can challenge the result. Record the decision owner and applicable policy, legal and rights-based constraints. A majority preference or higher aggregate score does not waive mandatory protections.

## Procedure
1. Define the actual decision and consequence, not just a model output. Separate predicting an event from allocating a benefit or imposing a burden based on that prediction.
2. Map affected groups and intersections relevant to the context, including non-users and indirect effects. Consult affected parties where feasible; do not substitute a model-generated persona for their views.
3. Inventory data provenance, consent/authority, missingness, label quality and proxy variables. Historical outcomes can reflect earlier exclusion rather than an unbiased target.
4. Identify material error types and their consequences. False positives and false negatives may impose very different burdens, and burdens can differ across groups.
5. Choose metrics tied to the intended protection or policy goal: selection rates, true/false positive rates, predictive value, calibration, service delay or other relevant outcomes. Define denominators and compare comparable populations and time windows.
6. Quantify uncertainty and small-sample limitations. Inspect intersectional outcomes without treating sparse estimates as precise. Privacy-preserving analysis may limit granularity; document that limitation rather than inventing values.
7. Compare candidate policies and feasible remedies, including better data, improved access, changed process, review support or limiting automation. Some fairness goals can conflict depending on prevalence and prediction quality; do not claim one dashboard score settles fairness.
8. Evaluate human review as a real process: reviewer expertise, time, evidence access, ability to override, accountability and appeal. A nominal human-in-the-loop who routinely rubber-stamps is not meaningful recourse.
9. Design notice, explanation, correction, contestability and outcome monitoring proportionate to stakes. Avoid exposing confidential information or unnecessary sensitive attributes in individual explanations.
10. Obtain the appropriate owner and domain/legal review before consequential deployment or policy changes. Record unresolved objections and rollback triggers if disparate burdens worsen.

## Interpretation limits
Equal error rates do not prove equal lived impact, and unequal rates do not by themselves establish the cause or legality of a difference. Metrics require context, causal understanding and policy judgment. Do not implement group-specific treatment based on a generic fairness formula without checking the actual legal and ethical requirements.

## Failure modes
Watch for aggregate accuracy masking harmful subgroups, biased labels, excluding people whose data are missing, choosing metrics after seeing favorable results, conflating protected rights with preferences and withholding an appeal path. Avoid claiming a model or workflow is “fair” based solely on a small retrospective sample.

## Deliverable and stop conditions
Return the stakeholder map, mandatory protections, data limitations, error/burden table, metric definitions with denominators and uncertainty, policy trade-offs, recourse design, authorization status and monitoring plan. Hold consequential deployment when critical data authority, unacceptable harm or required review is unresolved. This guide supports analysis; it is not jurisdiction-specific legal advice.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-group-deliberation](../decision-group-deliberation/SKILL.md).
- [Related method: decision-risk-and-reversibility](../decision-risk-and-reversibility/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
