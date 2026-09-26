---
name: decision-causal-inference
description: Choose interventions by separating causal effects from correlations. Defines the target effect,
  maps confounding and selection, checks identification assumptions, compares feasible study designs,
  and records what evidence could falsify the proposed mechanism.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- causal-inference
- confounding
- interventions
when-to-use:
- Choose interventions by separating causal effects from correlations. Defines the target effect, maps
  confounding and selection, checks identification assumptions, compares feasible study designs, and records
  what evidence could falsify the proposed mechanism.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-evidence-and-uncertainty
  - decision-sequential-experiments
---

# Causal Decision Analysis

## When this method is useful
Use when deciding whether changing X will improve Y: redesigning a workflow, adding an agent tool, changing a policy or funding an intervention. Prediction alone is insufficient: a feature can predict an outcome without being a useful lever. Do not demand a causal study for a purely descriptive lookup.

## Required inputs and target effect
State the intervention, comparison, population, outcome definition, observation horizon and unit of assignment. Distinguish intention-to-treat effects from effects among people who actually comply. Specify whether the decision needs an average effect, an effect for a subgroup, or a policy outcome including costs and spillovers. Write the counterfactual question before choosing the estimator.

## Procedure
1. Draw a small directed graph of the believed mechanism. Mark treatment, outcome, pre-treatment common causes, mediators, selection variables and important unobserved factors. An arrow is an assumption to investigate, not established evidence.
2. Inventory how data were generated. Who was eligible, assigned, observed, excluded or lost? Check measurement timing and whether the intervention changes measurement itself.
3. Identify a defensible comparison. Random assignment, when ethical and feasible, reduces assignment confounding but does not automatically solve noncompliance, attrition, interference or external validity.
4. If observational data are necessary, explain the identification strategy and its limitations. Regression adjustment or matching requires adequate measured confounding control and overlap; difference-in-differences needs a defensible parallel-trends assumption and appropriate treatment-timing analysis. An instrumental variable needs relevance and credible exclusion/independence assumptions, not merely correlation with treatment.
5. Select controls based on the causal question, not automated predictive importance. Adjusting for a mediator changes the estimand; conditioning on a collider can introduce bias. Avoid controls that occur after the intervention unless the method explicitly models them.
6. Check overlap and measurement comparability. Do not extrapolate a treatment effect to people or operating conditions absent from the comparison without stating the transfer assumption.
7. Estimate effects with uncertainty appropriate to assignment and sampling. Respect clustering, repeated measurements, missingness and spillovers. Distinguish statistical evidence from practical importance and cost-effectiveness.
8. Challenge the interpretation with alternative mechanisms, pre-trends where applicable, placebo/negative-control ideas, sensitivity to unmeasured confounding and specification changes. These checks can reveal problems; passing them is not proof of identification.
9. Translate the estimate into a bounded decision: expected benefit over the real baseline, affected groups, implementation costs, risks, and what must be learned before scaling.

## Decision rule and escalation
Prefer an intervention only when the proposed effect is identified credibly enough for the stakes and its decision value survives relevant uncertainty. If plausible confounding could reverse the recommendation, recommend a better design or a reversible learning step. For consequential domain-specific inference, involve an appropriately qualified analyst rather than treating a generic formula as sufficient.

## Failure modes
Aggregated data can reverse subgroup patterns. Before-and-after comparisons can confuse seasonality or concurrent changes with treatment effects. A statistically precise association can remain causally wrong. Subgroup searches after seeing outcomes can create false discoveries. Conditioning on users who remained active can hide harms that caused others to leave.

## Deliverable and completion gate
Return the target effect, graph assumptions, study/comparison design, evidence and provenance, identification threats, estimates with units and uncertainty, sensitivity results, and a recommendation or explicit non-identification statement. Stop when the design cannot answer the causal question with the available data; more elaborate arithmetic does not repair missing identification.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-evidence-and-uncertainty](../decision-evidence-and-uncertainty/SKILL.md).
- [Related method: decision-sequential-experiments](../decision-sequential-experiments/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
