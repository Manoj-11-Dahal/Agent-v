---
name: decision-resource-and-priority
description: Allocate scarce time, compute, money and team capacity across candidate work while accounting
  for dependencies, marginal value, risk and uncertainty. Avoids false precision and score-only scheduling.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- prioritization
- budget
- capacity
when-to-use:
- Allocate scarce time, compute, money and team capacity across candidate work while accounting for dependencies,
  marginal value, risk and uncertainty. Avoids false precision and score-only scheduling.
metadata:
  role: specialized decision module
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-skills
---

# Decision Resource and Priority Planning

## Define the capacity envelope
State the planning horizon, usable capacity, binding bottleneck, protected commitments and contingency reserve. Separate cash budget, calendar time, specialist effort, compute and attention; they are not interchangeable. Identify who owns changes to the envelope and whether estimates include coordination, verification and maintenance.

## Prioritize in context
1. Remove work that fails mandatory constraints or has no accountable owner. Preserve urgent safety/compliance obligations as constraints where applicable, not optional low-scoring features.
2. Map prerequisites, shared enabling work and mutually exclusive alternatives. An item blocked on an unavailable dependency is not an immediately executable priority.
3. Estimate incremental value against the status quo, total effort and time to benefit. Show ranges and the evidence behind each estimate. Avoid counting the same benefit in several projects.
4. Consider cost of delay, option value, uncertainty reduction and consequences of interrupting current work. Value/effort ratios are screening aids, not a substitute for resource-constrained scheduling.
5. Compare portfolios rather than only individual ranks. A large high-value project can crowd out several complementary smaller ones; sequencing and capacity determine feasibility.
6. Limit simultaneous work and reserve room for recovery. Define a review cadence and triggers for reprioritization when estimates, dependencies or user objectives change.

## Use scoring responsibly
Methods such as weighted scoring or cost-of-delay divided by duration can make assumptions visible, but units and denominators must be consistent. Do not call arbitrary ordinal numbers financial ROI. Scores are proposals for discussion, not authority to spend money or reassign someone else's time.

## Hypothetical scheduling lesson
Two projects can share a prerequisite and appear individually efficient while exceeding the same specialist's weekly capacity. Put the shared prerequisite on the schedule once, model the bottleneck, and compare feasible sequences. Do not add two independent benefit estimates if they describe the same users or outcome.

## Deliverable
Return a now/next/later or constrained portfolio plan, capacity by resource, dependency map, value/effort ranges, deferred work and consequences, reserve, and reprioritization triggers. State which assumptions would change the ordering and who must approve any extra resources.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. Return to [the main Decision Skills guide](../decision-skills/SKILL.md) to choose the next bounded step. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
