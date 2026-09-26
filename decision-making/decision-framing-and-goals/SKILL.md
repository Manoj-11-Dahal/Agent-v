---
name: decision-framing-and-goals
description: Turn an ambiguous request into an owned, bounded decision with measurable outcomes, explicit
  constraints, a status-quo baseline and a proportional analysis plan. Avoids optimizing the wrong proxy
  or inventing stakeholder preferences.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- problem-framing
- goals
- stakeholders
when-to-use:
- Turn an ambiguous request into an owned, bounded decision with measurable outcomes, explicit constraints,
  a status-quo baseline and a proportional analysis plan. Avoids optimizing the wrong proxy or inventing
  stakeholder preferences.
metadata:
  role: specialized decision module
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-skills
---

# Decision Framing and Goals

## Start with the real choice
Write: “Choose [action or policy] for [scope] by [deadline] to improve [observable outcome], subject to [constraints].” Distinguish a decision from a research question, implementation task, preference, or disagreement about facts. If no choice is currently required, define the deliverable instead of forcing a decision matrix.

## Frame in six passes
1. Name the accountable decision owner and the person who may authorize execution. Record affected parties and consultation needs. Do not assume the requester can grant rights over someone else's system or data.
2. Describe the current baseline and why a change is being considered. Separate the symptom from the mechanism believed to cause it.
3. Identify one primary outcome and a small number of guardrails. Specify how, when and where they can be observed. Pair proxy metrics with failure checks: more completed tasks is not success if they are incorrect.
4. Divide constraints into hard limits, preferences and unresolved policy. Label who supplied each constraint and its evidence. Ask a targeted question if different plausible answers would change an important choice.
5. Set the decision horizon, time available for analysis, uncertainty tolerance and reversibility. A temporary operational choice and a five-year commitment need different methods.
6. Define acceptance and review: what result would make the choice successful, what would falsify the premise, and when should the decision reopen?

## Resolve competing goals
List trade-offs openly rather than compressing all interests into a single unexplained number. Separate minimum acceptable service, affordability, privacy and feasibility from preferences about speed or convenience. Where people disagree about values, show the competing recommendations under their assumptions; additional technical research may not resolve a value disagreement.

## Hypothetical example
“Make support better” is underspecified. A useful frame could be: choose a four-week triage pilot to reduce median first-response delay for a defined queue, without worsening incorrect routing or exposing customer data, within an owner-approved spend. The owner must supply actual targets; example numbers are not recommended thresholds.

## Failure checks and output
Check whether the chosen metric can be gamed, whether the baseline is current, whether the decision boundary excludes a key dependency, and whether the deadline is real. Deliver the one-sentence frame, objective/guardrail table, constraint sources, unresolved questions and chosen review depth. Escalate ownership ambiguity before making a consequential commitment.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. Return to [the main Decision Skills guide](../decision-skills/SKILL.md) to choose the next bounded step. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
