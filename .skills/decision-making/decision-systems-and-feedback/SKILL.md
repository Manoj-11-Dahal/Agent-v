---
name: decision-systems-and-feedback
description: Evaluate delayed, nonlinear and second-order effects before changing a system. Maps stocks,
  flows, reinforcing/balancing loops, bottlenecks and queue utilization, and defines interventions with
  measurable mechanisms and bounded feedback control.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- systems-thinking
- feedback
- queues
- second-order-effects
when-to-use:
- Evaluate delayed, nonlinear and second-order effects before changing a system. Maps stocks, flows, reinforcing/balancing
  loops, bottlenecks and queue utilization, and defines interventions with measurable mechanisms and bounded
  feedback control.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-causal-inference
  - decision-commit-and-monitor
---

# Systems Thinking and Feedback Decisions

## When to use
Use when a local improvement can move a bottleneck, create rebound behavior, accumulate a backlog, or trigger delayed consequences. Examples include agent concurrency, operational queues, staffing or product incentives. A feedback-loop sketch organizes hypotheses; it does not establish causal effects without evidence.

## System boundary and state
Define the objective, actors, time horizon, resources, inputs, outputs and external conditions. Identify stocks that accumulate (backlog, inventory, debt, trust) and flows that change them. Keep units consistent: a stock measured in tasks is not directly comparable to a flow measured in tasks per hour.

## Procedure
1. Draw the simplest useful stock/flow map. Record inflows, outflows, losses and measurement delays. Check conservation/accounting where applicable before fitting a complex model.
2. Identify reinforcing and balancing feedback loops, marking hypothesized causal direction, sign and delay. Include the behavior of people or agents reacting to the policy.
3. Locate capacity constraints and utilization. Improving a non-bottleneck may increase work-in-progress without improving throughput. Check shared specialist, API, storage or attention limits.
4. Model the decision-relevant mechanism with an appropriate level of detail. Begin with measured rates and simple queue or accounting models; do not claim a simulation is validated merely because it produces a smooth chart.
5. Test transient and steady-state behavior separately. Initial success can conceal delayed failure; a steady-state formula may not apply during rapid growth or changing arrival patterns.
6. Compare interventions at the system level: reduce unnecessary demand, remove a bottleneck, smooth variability, improve routing, add capacity or change incentives. Include downstream load and who absorbs the cost.
7. Stress-test nonlinearity, saturation, feedback delay, simultaneous policy changes and second-order adaptation. One-variable-at-a-time tests can miss interacting bottlenecks.
8. Define observable leading indicators and guardrails. For a feedback controller, specify measurement frequency, action limits, deadbands where appropriate, and anti-oscillation controls. Do not let a noisy metric trigger unbounded automatic changes.
9. Roll out a bounded change with checkpoints, an owner and a reversible path when available. Compare observed response with the predicted mechanism and revise the model if it fails.

## Useful equations with assumptions
Backlog change equals arrivals minus completed or removed work over the same interval. Little's law, L=lambda×W, relates long-run average population, throughput and time in a stable system under suitable conditions. For a stable M/M/1 queue with Poisson arrivals, exponential independent service and one server, mean time in the system is 1/(mu−lambda), provided lambda<mu. It includes service time, not just waiting. This special model is not a universal latency estimator.

## Failure modes
Watch for unit mismatches, averaging away bursts, treating capacity as throughput, targeting 100% utilization without accounting for variability, mistaking a temporary backlog drop for sustainable improvement, and optimizing a local metric while moving work elsewhere. A system can satisfy average targets while producing unacceptable tail delay or unequal service.

## Deliverable
Return the system boundary, stock/flow and feedback hypotheses, bottleneck evidence, model assumptions, intervention alternatives, predicted direct and delayed effects, sensitivity, monitoring and rollback plan. If evidence cannot support the model's detail, simplify it and state uncertainty rather than embellishing the simulation.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-causal-inference](../decision-causal-inference/SKILL.md).
- [Related method: decision-commit-and-monitor](../decision-commit-and-monitor/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
