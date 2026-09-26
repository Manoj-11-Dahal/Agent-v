---
name: decision-robust-optimization
description: Compare feasible choices when future-state probabilities are weak or disputed. Builds coherent
  scenario payoff tables, computes worst-case outcomes and minimax regret, and distinguishes robust policy
  choices from probability-weighted preferences.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- robust-decisions
- minimax-regret
- scenario-analysis
when-to-use:
- Compare feasible choices when future-state probabilities are weak or disputed. Builds coherent scenario
  payoff tables, computes worst-case outcomes and minimax regret, and distinguishes robust policy choices
  from probability-weighted preferences.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-scenarios-and-premortem
  - decision-risk-and-reversibility
---

# Robust Decisions and Minimax Regret

## Use and non-use
Use when choices face several plausible futures and a single probability estimate would dominate the recommendation without adequate evidence. Robustness means tolerating specified uncertainty, not being safe under every imaginable world. Do not add absurd scenarios solely to force a preferred conservative answer.

## Define the comparison
List feasible actions, coherent future states, units of payoff or loss, horizon, stakeholder perspective and mandatory conditions. Use higher-is-better utility consistently or clearly reverse formulas for losses. If a gate fails in a scenario, describe contingency feasibility explicitly rather than giving a forbidden action a merely low score.

## Procedure
1. Select material drivers and construct scenarios that fit together. Include the status quo and an adverse but plausible case. Document exclusions and correlations among drivers.
2. Estimate each action-state consequence with evidence and ranges. Keep resource feasibility, catastrophic downside and non-compensatory constraints separate from ordinary utility.
3. Agree the robustness criterion before seeing which action wins. Expected utility needs defensible state probabilities. Maximin protects the lowest modeled utility. Minimax regret limits the largest foregone benefit relative to the best feasible action in each state.
4. For utility U(a,s), calculate scenario best B(s)=max_a U(a,s), regret R(a,s)=B(s)−U(a,s), and worst regret max_s R(a,s). A minimax-regret choice minimizes that last value. Verify units and feasibility are comparable across actions.
5. Report the full consequence and regret tables, not only the selected row. Include ties and explain the difference between a disappointing absolute outcome and a large opportunity loss.
6. Stress-test scenario inclusion, payoff estimates, hard constraints and the alternative set. Adding a genuinely feasible option can change the regret benchmark; adding an impossible option should not.
7. If credible probabilities exist, show expected utility alongside robust criteria. A disagreement between criteria is a value or risk-policy question, not an arithmetic error to hide.
8. Consider contingent or staged policies when later observations allow adaptation. Include information delays, switching costs, authority and whether the trigger is actually observable.
9. Recommend a bounded commitment, a discriminating information step, or owner review when plausible assumptions reverse the result. Record explicit revisit conditions.

## Important boundaries
A minimax-regret action need not maximize expected utility or avoid severe harm. Maximin can overreact to a weakly justified worst case. Worst-case optimization over an overly broad uncertainty set can be impractical; an overly narrow set can create false confidence. Robustness to listed scenarios is not robustness to all distributions, tail events or implementation failures.

Do not subtract utilities that use incompatible stakeholder scales and claim objective regret. If some scenarios make an action unavailable, define a feasible contingency policy or remove that policy from that scenario comparison with an explicit methodology; never conceal missing feasibility as an ordinary numeric loss.

## Output and stopping condition
Return the scenario basis, feasibility matrix, consequence/regret tables, selected criterion and owner, sensitivity results, alternative recommendation under other criteria, and trigger-based commitment. Stop adding scenarios when they no longer change the practical choice or safeguards enough to justify more analysis, while retaining material unresolved tail risks.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-scenarios-and-premortem](../decision-scenarios-and-premortem/SKILL.md).
- [Related method: decision-risk-and-reversibility](../decision-risk-and-reversibility/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
