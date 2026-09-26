---
name: decision-sequential-experiments
description: Design bounded experiments with predeclared hypotheses, valid interim decision rules, error
  budgets and inconclusive outcomes. Distinguishes fixed-horizon testing, sequential methods and Bayesian
  monitoring while preventing repeated peeking from becoming false confidence.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- sequential-testing
- experiments
- stopping-rules
when-to-use:
- Design bounded experiments with predeclared hypotheses, valid interim decision rules, error budgets
  and inconclusive outcomes. Distinguishes fixed-horizon testing, sequential methods and Bayesian monitoring
  while preventing repeated peeking from becoming false confidence.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-value-of-information
  - decision-causal-inference
---

# Sequential Experiments and Stopping Decisions

## When to use
Use when observations arrive over time and deciding when to stop, continue or expand a test affects cost or exposure. The experiment must be authorized and its risks acceptable. A statistical stopping boundary is not permission to expose users or deploy a feature.

## Experiment contract
Specify the decision, hypothesis or estimand, target population, randomization unit, primary outcome, minimum meaningful effect, measurement delay, resource ceiling and safety guardrails. Predeclare treatment of missing outcomes and exclusions. Assign a person responsible for stopping when guardrails fail, even if the primary result appears favorable.

## Choose one coherent inference design
A fixed-horizon frequentist test generally needs its planned sample and analysis, rather than repeatedly applying the same unadjusted significance threshold after every new observation. Valid sequential designs may use group-sequential error spending, confidence sequences or other justified methods. A sequential probability ratio test (SPRT) compares specified simple hypotheses under its likelihood assumptions. Bayesian monitoring requires an explicit prior/model and a decision loss or utility rule; it does not automatically provide frequentist error guarantees.

## Procedure
1. Translate the business or agent question into an observable endpoint. Ensure the measurement window captures delayed failures instead of counting early apparent success only.
2. Check assignment, dependence and contamination. Repeated observations from one user or service may not be independent; choose an appropriate unit and model.
3. Set error tolerances, power or precision goals, maximum sample/time, and rules for efficacy, futility and harm. Keep these separate from a budget-driven stop, which may leave the result inconclusive.
4. Write the interim analysis schedule or valid always-valid method before collecting outcomes. Multiple metrics, arms, segments and repeated decisions require a multiplicity strategy, not selective reporting of the first winner.
5. Simulate or analytically check the design under plausible effects and assumption failures before a consequential deployment. Use appropriate statistical expertise for nontrivial designs rather than generalizing the simple worked case.
6. Collect according to the protocol and maintain an audit trail. Track missingness, instrumentation changes, leakage, novelty effects and interference between arms.
7. At a planned or otherwise valid look, apply the chosen rule. Distinguish evidence for an effect from practical value, and report uncertainty rather than only a binary label.
8. If a guardrail fails, stop or contain within authorized procedures. If maximum resources are reached without a boundary, label the result inconclusive under the design; do not reinterpret it as equivalence.
9. Reassess external validity and operational readiness before any rollout. A successful controlled test can fail in a different workload, time period or population.

## SPRT arithmetic boundary
For independent binary outcomes and simple hypotheses p0 versus p1, log LR = s log(p1/p0) + f log((1−p1)/(1−p0)). Illustrative Wald thresholds are log((1−beta)/alpha) and log(beta/(1−alpha)); discrete overshoot and model assumptions matter. Do not reuse these numbers for composite hypotheses, adaptive assignment or dependent events without an appropriate design.

## Failure modes and deliverable
Avoid ending the test at the first favorable ordinary p-value, silently moving the target effect, discarding delayed harms, treating non-significance as no effect, or repeatedly restarting until success. Return the protocol, assumptions, information collected, stopping reason, inference with limits, guardrail outcomes and bounded next decision. Preserve an inconclusive result honestly.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-value-of-information](../decision-value-of-information/SKILL.md).
- [Related method: decision-causal-inference](../decision-causal-inference/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
