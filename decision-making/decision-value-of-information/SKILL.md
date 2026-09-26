---
name: decision-value-of-information
description: Decide whether to act, ask a question, research, run a bounded experiment or defer. Estimates
  how new evidence could change the choice and compares that benefit with cost, delay and exposure.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- value-of-information
- experiments
- research-budget
when-to-use:
- Decide whether to act, ask a question, research, run a bounded experiment or defer. Estimates how new
  evidence could change the choice and compares that benefit with cost, delay and exposure.
metadata:
  role: specialized decision module
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-skills
---

# Decision Value of Information

## Ask what would change
Start with the current best feasible action and the uncertain assumptions that could reverse it. For each proposed information step, state the question, possible observations, decision rule after each observation, collection cost, latency, and any privacy or operational exposure. Information that cannot affect the choice may still serve compliance or documentation, but should not be sold as decision improvement.

## Expected value framework
When utilities and probabilities are defensible, expected value of sample information is E[max_a E[U(a, state) | observation]] − max_a E[U(a, state)]. Subtract collection cost, delay cost and any added exposure. Keep all quantities in compatible units and count only feasible, authorized actions. Perfect information is an upper bound under the same assumptions, not an attainable promise.

If trustworthy probabilities are unavailable, use a threshold question instead: what finding would reverse the choice, how plausible is it, and can a small, low-risk observation distinguish the cases? This is often more useful than manufactured precision.

## Procedure
1. Rank unresolved uncertainties by decision sensitivity, not intellectual interest.
2. Prefer a targeted owner question or existing reliable evidence before an expensive experiment.
3. Design the smallest informative test with a hypothesis, comparison/control where feasible, measurement plan, cost ceiling and stopping rule.
4. Account for false positives/negatives, selection bias and whether a small test transfers to the real environment. Do not equate an available result with a useful one.
5. Before looking at the result, specify which action each relevant result would support. Include inconclusive and failed-test outcomes.
6. Update the decision record once, preserve the earlier prediction, and stop when marginal information value is below its cost or the analysis budget expires.

## Hypothetical example
Suppose a study has a 0.25 chance of leading to a switch that improves utility by 40 units, with no decision change otherwise. Ignoring other effects, gross value is 10 units. If the study costs 6 units and delay costs 5, net value is −1. These are invented values to demonstrate the calculation, not evidence that a real study is worthless.

## Deliverable
Return decide-now, clarify, research, bounded experiment or defer; the decision-changing question; expected or qualitative value; limits; and a result-to-action mapping. Never run repeated open-ended research or experiments merely to avoid making a bounded choice.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. Return to [the main Decision Skills guide](../decision-skills/SKILL.md) to choose the next bounded step. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
