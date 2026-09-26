---
name: decision-scenarios-and-premortem
description: Stress-test a proposed decision against plausible futures, dependency failures and second-order
  effects. Uses independent failure generation, mitigations and leading indicators rather than claiming
  that consensus proves robustness.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- scenarios
- premortem
- robustness
when-to-use:
- Stress-test a proposed decision against plausible futures, dependency failures and second-order effects.
  Uses independent failure generation, mitigations and leading indicators rather than claiming that consensus
  proves robustness.
metadata:
  role: specialized decision module
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-skills
---

# Decision Scenarios and Premortem

## Scenario design
Select the few uncertain drivers that could materially change the result. Build internally coherent scenarios: favorable, central and adverse conditions are useful only if their assumptions fit together. Do not label a scenario a probability distribution unless likelihood estimates are defensible. Include a severe plausible tail case when stakes justify it.

## Stress-test each option
For every scenario, record whether hard gates still pass, the expected mechanism of success or failure, resource demands, affected stakeholders, recovery possibilities and unknowns. Include correlated shocks and shared dependencies; changing one input at a time can miss joint failure. Separate a robust option from an option that looks good only at the central estimate.

## Premortem procedure
1. Describe the proposed commitment and its success criteria without selling it.
2. Ask participants, or distinct structured review passes, to assume it failed and list concrete causal mechanisms before discussion.
3. Distinguish genuinely independent evidence from multiple model outputs based on the same assumptions. Synthetic reviewer personas are prompts for critique, not independent experts or votes.
4. Consolidate failure mechanisms, identify early observable signals, and assign mitigations and owners.
5. Challenge the mitigations: do they prevent failure, detect it early, contain damage, or merely make the report sound reassuring?
6. Recompare the strongest alternative and a staged commitment. Record which scenario would trigger a switch or stop.

## Choosing a robustness criterion
Expected utility needs justified probabilities and utilities. Worst-case approaches may be too conservative if the scenario set includes implausible combinations. Regret compares an action with the best feasible action under each scenario; it depends on which alternatives and scenarios were included. Explain the chosen criterion rather than silently using whatever favors the preferred plan.

## Output and stop rule
Produce a scenario table, causal failure register, indicators, mitigation verification, unresolved objections, and revised recommendation or test. Stop adding scenarios when they no longer change safeguards or the choice enough to justify more analysis. Keep the final rationale concise and preserve material dissent.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. Return to [the main Decision Skills guide](../decision-skills/SKILL.md) to choose the next bounded step. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
