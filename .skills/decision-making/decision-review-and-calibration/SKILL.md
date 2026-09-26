---
name: decision-review-and-calibration
description: Evaluate decision process and forecast accuracy without confusing outcomes with reasoning
  quality. Supports probability calibration, decision journals and measured policy updates while avoiding
  hindsight bias and overfitting small samples.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- review
- calibration
- learning
when-to-use:
- Evaluate decision process and forecast accuracy without confusing outcomes with reasoning quality. Supports
  probability calibration, decision journals and measured policy updates while avoiding hindsight bias
  and overfitting small samples.
metadata:
  role: specialized decision module
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-skills
---

# Decision Review and Calibration

## Preserve the original record
Keep the decision-time objective, feasible options, evidence, assumptions, prediction and approval boundary. After the outcome, add a separate observation record with its timestamp and measurement method. Do not edit the original forecast or omit bad outcomes from the review set.

## Review in two layers
1. Assess process quality using what was knowable then: framing, evidence relevance, options, gates, uncertainty, execution plan and monitoring.
2. Assess the observed result and compare it with the forecast. Good process can have a poor outcome by chance; success can hide a fragile or unauthorized process. Neither layer substitutes for the other.

## Forecast calibration
Use clearly defined events with settled outcomes. For binary events, the Brier score is the mean of (p − y)^2, where y is 0 or 1; smaller is better under the same evaluation setup. This evaluates probability forecasts, not weighted preference scores or raw model confidence statistics.

Inspect calibration by probability bands with counts and uncertainty, and separate meaningful domains when sample size permits. Selection bias, unresolved cases, changing definitions and distribution shift can distort apparent accuracy. Do not conclude “well calibrated” from a handful of successes. Use held-out outcomes when tuning thresholds or policies.

## Hypothetical arithmetic
For forecasts 0.8, 0.6 and 0.2 with outcomes 1, 0 and 0, squared errors are 0.04, 0.36 and 0.04. Their average is about 0.1467. This example demonstrates the formula; it does not establish the performance of any model or team.

## Improve one thing deliberately
Identify whether the main error came from the frame, missing information, an unsupported assumption, a prediction, preference weights, policy or execution. Record an alternative explanation. Propose a small change with an expected effect and evaluation plan, not an unbounded rewrite after one outcome.

## Deliverable
Return the frozen prediction, observed outcome, process-quality findings, forecast metrics where meaningful, uncertainty, and a versioned improvement proposal. Store concise evidence-backed lessons, not secrets or private internal reasoning. Avoid automated self-modification or promotion of a policy without the appropriate owner review.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. Return to [the main Decision Skills guide](../decision-skills/SKILL.md) to choose the next bounded step. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
