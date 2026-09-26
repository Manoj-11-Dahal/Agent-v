---
name: decision-probabilistic-forecasting
description: Produce explicit event forecasts using reference classes, base rates and defensible updates.
  Separates event probability from model confidence, handles dependent evidence, and defines resolution
  rules and forecast revision triggers before outcomes are known.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- forecasting
- base-rates
- bayesian-updating
when-to-use:
- Produce explicit event forecasts using reference classes, base rates and defensible updates. Separates
  event probability from model confidence, handles dependent evidence, and defines resolution rules and
  forecast revision triggers before outcomes are known.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-evidence-and-uncertainty
  - decision-review-and-calibration
---

# Probabilistic Forecasting and Base Rates

## When to use
Use for forecasts that affect staffing, launch readiness, budget exposure or whether to investigate an alert. The output is a probability of a specified event by a specified time, not a preference score or certainty that a recommended action is correct. If the event cannot be defined or resolved consistently, repair the question first.

## Forecast contract
Write the event, time zone and deadline, resolution source, ambiguous-case rules, current information cutoff, and owner. Define what counts as a success, failure or unresolved observation. Do not retrospectively narrow the event after learning what happened. Record the decision that the forecast could influence and the cost of each relevant mistake.

## Procedure
1. Establish an outside-view reference class. Describe inclusion/exclusion rules, sample size, period, environment and missing outcomes. Compare several plausible classes when the choice of class is itself uncertain.
2. Estimate the base rate with uncertainty. Small samples and selective reporting require caution. A convenient historical percentage is not automatically transferable to a changed deployment or population.
3. Identify case-specific evidence and its expected diagnostic value. Ask how often the observation would occur if the event happens and if it does not—not merely whether the observation sounds alarming.
4. Update with a defensible model. For binary evidence, posterior odds = prior odds × likelihood ratio. Record estimates and source dependence. Do not multiply likelihood ratios from duplicated reports or correlated telemetry as if independent.
5. Where a simple exchangeable Bernoulli model is reasonable, a Beta(a,b) prior updated by s events and f non-events becomes Beta(a+s,b+f). Label the model, effective prior strength and exchangeability assumption. This is not a license to pool changing environments indiscriminately.
6. Decompose complex events only when conditional relationships are explicit. P(A and B)=P(A)P(B|A); replacing the conditional probability by P(B) assumes independence. Avoid multiplying arbitrary component estimates until the final number looks small.
7. Test sensitivity to the reference class, prior, evidence reliability and alternative mechanisms. Give a justified range or scenarios if a single value would imply false precision.
8. Publish the forecast before resolution, with a concise evidence summary and revision triggers. Log each revision alongside new evidence instead of overwriting the earlier value.
9. Evaluate a series of resolved forecasts using proper scoring rules and calibration analysis. Compare meaningful baselines and account for correlated cases and unresolved outcomes.

## From probability to action
Combine forecasts with feasible actions, error costs and approval boundaries. A 0.8 probability can support opposite actions in two settings with different losses. Service-provided confidence may describe a model's output distribution; it is not automatically a calibrated probability of the event defined here. Keep forecasting and authorization separate.

## Failure modes and stop rules
Watch for neglecting low base rates, choosing the reference class to fit a preferred answer, treating a narrative as diagnostic evidence, sample leakage, survivorship bias, and implying precision beyond the data. If evidence dependence is unknown, use conservative scenarios rather than compounding it mechanically. Stop updating when no new independent information arrived; repeated reconsideration is not new data.

## Deliverable
Return the event contract, base-rate basis, assumptions, updating calculation, forecast/range, most influential uncertainty, revision triggers and resolution plan. Include the decision implication separately, with losses and authority made explicit.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-evidence-and-uncertainty](../decision-evidence-and-uncertainty/SKILL.md).
- [Related method: decision-review-and-calibration](../decision-review-and-calibration/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
