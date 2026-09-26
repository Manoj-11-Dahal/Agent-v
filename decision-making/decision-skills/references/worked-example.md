# Worked examples — strategy and agent actions

All people, approvals, estimates and outcomes below are hypothetical. These examples do not report actual experiments, authorize a deployment, or claim a TypeSafe evaluation.

## 1. Strategic choice: a bounded support-triage pilot

**Frame:** choose a pilot approach within an owner-defined time window and spend limit, using only permitted data. The objective is better first-response handling without unacceptable routing errors. The baseline is the current workflow. Before a real decision, collect actual baseline measurements, budget, quality targets and owner preferences.

**Alternatives:** A, pilot using the existing system; B, pilot an alternative service; C, a shortcut that violates data-handling policy; D, an expanded rollout whose authority has not been established. A and B receive hypothetical pass assertions. C is excluded despite perfect hypothetical scores. D is held even though other constraints pass.

**Preference rubric:** delivery 0.30, reliability 0.45, affordability 0.25. These assumed weights are not universal business advice. Scores are invented preferences on fixed 0–1 anchors, not success probabilities.

| Eligible option | Delivery | Reliability | Affordability | Weighted point score | Supplied weighted bounds |
|---|---:|---:|---:|---:|---:|
| A | 0.80 | 0.90 | 0.60 | 0.7950 | 0.6950–0.8725 |
| B | 0.90 | 0.65 | 0.90 | 0.7875 | 0.6650–0.8825 |

A's point score is 0.30×0.80 + 0.45×0.90 + 0.25×0.60 = 0.795. The gap of 0.0075 is inside the example's 0.01 near-tie tolerance, and ranges overlap. The helper therefore reports `near_tie_requires_judgment`, not “A wins with 79.5% confidence.” No such confidence claim follows from preference arithmetic.

**Sensitivity:** reducing reliability's weight from 0.45 to 0.35 and proportionally redistributing the rest yields approximately 0.7759 for A and 0.8125 for B. The leading option can change. This suggests discussing the owner's values and obtaining better reliability evidence rather than adding decimal places.

**Information step:** define a small representative routing evaluation before collecting data. Specify the cases, consent/privacy boundary, success and error criteria, cost ceiling, comparison method and result-to-action rule. Ask whether a plausible result could change the choice enough to justify delay. No test is executed by this example.

**Commitment:** recommend a bounded evaluation or owner discussion, keep C excluded and D held, and record the strongest objection to each eligible option. Only after the owner selects and authorizes the next step should execution be planned. Set stop triggers, an outcome owner and a review date.

Run [the local example input](../examples/options.json) through the helper to reproduce all scores, ranges, exclusions and six one-way sensitivity trials.

## 2. Agent choice: report a timeout or retry an external write?

**Frame:** a hypothetical agent attempted an authorized external update, but the tool timed out and did not confirm whether the write committed. The objective is the requested final state—not maximizing the number of tool calls.

**Candidates:** retry immediately; inspect current state read-only; ask the user; abandon the task. A retry could duplicate a non-idempotent operation. A timeout is missing evidence, not proof of failure. The relevant uncertainty is whether the target already reached the requested state.

**Next bounded action:** if a permitted read-only status check is available, inspect the exact target without expanding scope. If the write already committed, verify and report that observation. If it did not, retry only when idempotency, authorization and the remaining budget make it appropriate. If state cannot be checked safely, explain the uncertainty and seek confirmation before risking a duplicate consequential write.

**Stop conditions:** no-progress retry limit, changed target state, missing authority, exhausted budget, or inconsistent evidence. A model's confidence does not settle whether the remote write happened. No weighted matrix or TypeSafe call is necessary for this routing choice.

**Record:** attempted action, verified observations, unresolved state, authorized boundary, selected verification step and any needed user question. Do not claim the operation succeeded or that a background monitor is running without evidence.
