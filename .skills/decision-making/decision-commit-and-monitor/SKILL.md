---
name: decision-commit-and-monitor
description: Convert an approved choice into a bounded execution plan with scope, ownership, checkpoints,
  observable success, guardrails and rollback. Prevents recommendations from silently becoming permission
  or unbounded agent action.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- execution
- monitoring
- rollback
when-to-use:
- Convert an approved choice into a bounded execution plan with scope, ownership, checkpoints, observable
  success, guardrails and rollback. Prevents recommendations from silently becoming permission or unbounded
  agent action.
metadata:
  role: specialized decision module
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-skills
---

# Decision Commitment and Monitoring

## Separate recommendation from commitment
Record the selected option, the authorizer, the exact approved scope and any conditions. A recommendation, high score or model output is not an approval event. If the decision owner chose a different option, retain the analysis and record the owner's choice without rewriting history to make the original ranking agree.

## Commitment checklist
1. Confirm the premises are still current: target identity, inputs, permissions, dependencies and resource limits. Resolve material state changes before execution.
2. Choose a bounded initial commitment with an explicit end. Identify changes, writes, external messages, costs and sensitive data involved.
3. Assign an execution owner and verification owner where stakes justify separation. Specify artifacts and evidence to be produced, not just commands to run.
4. Set success criteria, leading indicators, guardrail thresholds and observation windows. Distinguish a lagging business outcome from an immediate technical health check.
5. Define stop, rollback and escalation triggers with responsible people and required permissions. Test recovery where appropriate before treating it as available.
6. Checkpoint before consequential or hard-to-reverse steps, and verify state afterward. Avoid duplicate writes after ambiguous failures.

## Monitor without moving the goalposts
Keep the original success definition, forecast and approved budget visible. Record deviations, intervention decisions and explanations. Do not redefine success after seeing disappointing results without explicitly recording a revised objective. Respect privacy and retention limits when collecting telemetry.

## Example commitment
A four-week pilot might have an owner, limited participant group, spend ceiling, synthetic-data rehearsal, opt-out path, review date and rollback procedure. Actual thresholds must come from the domain and owner; this guide supplies structure rather than universal numbers.

## Exit and handoff
Close the decision as completed, stopped, superseded or still under observation. Distinguish work performed from results verified. Hand over current state, residual risks, next review, artifacts and ownership. An agent should not claim background monitoring is running unless a real authorized process exists and has been verified.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. Return to [the main Decision Skills guide](../decision-skills/SKILL.md) to choose the next bounded step. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
