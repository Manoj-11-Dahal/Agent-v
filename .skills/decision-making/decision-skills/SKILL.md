---
name: decision-skills
description: Primary decision-making workflow for consequential agent actions and strategic choices. Frames
  goals, verifies evidence, gates inadmissible options, compares trade-offs, tests uncertainty, and records
  a bounded commitment with review triggers. Routes to specialized decision skills; TypeSafe is optional.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- strategy
- agent-actions
- decision-routing
when-to-use:
- Primary decision-making workflow for consequential agent actions and strategic choices. Frames goals,
  verifies evidence, gates inadmissible options, compares trade-offs, tests uncertainty, and records a
  bounded commitment with review triggers. Routes to specialized decision skills; TypeSafe is optional.
metadata:
  role: primary decision workflow
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-framing-and-goals
  - decision-evidence-and-uncertainty
  - decision-options-and-tradeoffs
  - decision-risk-and-reversibility
  - decision-value-of-information
  - decision-agent-action-routing
  - decision-resource-and-priority
  - decision-scenarios-and-premortem
  - decision-commit-and-monitor
  - decision-review-and-calibration
  - decision-typesafe-judgments
---

# Decision Skills — Main Guide

## Purpose and limits
Use this as the main entry point when choosing matters: alternatives differ meaningfully, evidence is uncertain, resources are scarce, stakeholders face different consequences, or an action is difficult to reverse. It is a decision-quality framework, not a promise of correct predictions or permission to act. Follow the user's actual objective and constraints; never replace them with a hidden optimization goal.

For an obvious, low-impact, reversible task, a short check is enough: understand the request, confirm the action is in scope, act, and verify. Do not turn routine file edits into a committee process.

## The decision contract
Before evaluating options, state: **who decides what, for whom, by when, under which constraints, with what evidence, and with what review trigger**. Separate proposing a choice from being authorized to execute it. Identify people affected by the decision who do not get to choose the weights.

Use a lightweight mode for reversible local work, a standard mode for uncertain project choices, and an expanded review for material cost, sensitive information, external commitments, irreversible change, or safety/legal exposure. Stakes—not the apparent confidence of a model—determine scrutiny. Seek qualified domain review where appropriate.

## Decision loop
1. **Frame.** Write the decision in one sentence, define observable success and the status-quo baseline, set a deadline, and separate hard constraints from preferences.
2. **Ground.** Separate observations, source claims, assumptions, estimates and unknowns. Record source dates and contradictions. Distinguish a reliable source from evidence that actually answers this question.
3. **Generate.** Include a feasible status quo, a different mechanism, and—when useful—a bounded experiment or staged option. Avoid a false choice between two versions of the same plan.
4. **Gate.** Exclude known constraint violations. Hold options with unresolved mandatory gates out of the eligible set. No weighted advantage compensates for missing authorization or a hard prohibition.
5. **Compare.** Use a method appropriate to the stakes and evidence: a qualitative comparison, anchored weighted matrix, expected utility, scenario comparison or explicit regret analysis. Do not manufacture precise probabilities to fill a template.
6. **Challenge.** Check the strongest alternative, adverse scenarios, correlated criteria, missing stakeholders, and the assumptions that would reverse the choice. Distinguish agreement among copied sources from independent evidence.
7. **Choose the next commitment.** Commit, conduct a bounded experiment, gather one decision-relevant fact, escalate, or abstain. Set a stopping condition for analysis; more information is not automatically worth its delay or cost.
8. **Authorize and execute.** Confirm the action remains inside the user's authority, scope and budget. Recheck stale state before external or consequential actions. Use the least broad action that can achieve the agreed objective.
9. **Observe and revisit.** Define leading indicators, guardrails, an owner, rollback/containment steps, and review triggers. Log outcomes without rewriting the original forecast.

## Route only to needed modules
| Need | Skill |
|---|---|
| Unclear question, owner or success | [Framing](../decision-framing-and-goals/SKILL.md) |
| Weak evidence or uncertain forecasts | [Evidence and uncertainty](../decision-evidence-and-uncertainty/SKILL.md) |
| Compare alternatives and weights | [Options and trade-offs](../decision-options-and-tradeoffs/SKILL.md) |
| Serious downside or irreversible action | [Risk and reversibility](../decision-risk-and-reversibility/SKILL.md) |
| Research, ask, experiment or decide now | [Value of information](../decision-value-of-information/SKILL.md) |
| Choose a tool, skill or next agent action | [Agent action routing](../decision-agent-action-routing/SKILL.md) |
| Schedule scarce capacity or manage budget | [Resources and priority](../decision-resource-and-priority/SKILL.md) |
| Stress-test futures and failure modes | [Scenarios and premortem](../decision-scenarios-and-premortem/SKILL.md) |
| Translate a choice into bounded execution | [Commit and monitor](../decision-commit-and-monitor/SKILL.md) |
| Learn from outcomes without hindsight bias | [Review and calibration](../decision-review-and-calibration/SKILL.md) |
| Optional typed semantic judgments | [TypeSafe judgments](../decision-typesafe-judgments/SKILL.md) |

## Compact output contract
Return the decision/question, owner, recommendation or current hold, eligible alternatives, hard-gate status, key evidence, material assumptions, principal downside, what would change the decision, and the next bounded step. Include uncertainty and the strongest objection. Provide a concise auditable rationale, calculations and evidence references—not a transcript of private internal reasoning.

For a material decision, use [the record template](templates/decision-record.json). Leave missing inputs null or explicitly unknown. The template is not completed evidence.

## Local scoring aid
The optional [scoring helper](scripts/score_options.py) performs only deterministic arithmetic on a supplied local JSON file. It does not call TypeSafe, contact a service, execute a selected option, or verify that an asserted approval is authentic. It requires evidence references for positive gate assertions and score estimates. Review those references yourself.

See [scoring rules](references/scoring-guide.md), [the worked example](references/worked-example.md), and [the synthetic input](examples/options.json). A highest score is a comparison under assumptions—not authority, certainty or a universal optimum.

```bash
python3 /home/user/skills/decision-making/decision-skills/scripts/score_options.py /home/user/skills/decision-making/decision-skills/examples/options.json
```

## Complementary installed skills
Use existing implementation guidance where relevant rather than duplicating it:
[planning and task breakdown](../../agent-orchestration/planning-and-task-breakdown/SKILL.md),
[capability-aware routing](../../agent-orchestration/capability-aware-router/SKILL.md),
[action budgets](../../agent-orchestration/agent-budget-guard/SKILL.md),
[approval gates](../../sandbox-access-control/approval-gates/SKILL.md),
[evidence ledger](../../testing-quality/evidence-ledger/SKILL.md), and
[checkpoint/resume](../../memory-context/checkpoint-resume/SKILL.md).
Inspect actual capabilities and scope before using any workflow. These references do not activate it.

## Anti-patterns
Do not decide first and retrofit weights; let an attractive score override a failed gate; count the same evidence repeatedly; mistake confidence for correctness; silently choose for people on high-impact personal matters; claim unavailable tools or fabricated test results; or continue an agent loop without a budget and stop condition. Maintain an actionable fallback rather than pretending uncertainty has disappeared.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
