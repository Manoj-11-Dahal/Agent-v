---
name: decision-risk-and-reversibility
description: Assess downside, exposure, recoverability and blast radius before consequential actions.
  Distinguishes hard safety boundaries from uncertain performance trade-offs and defines approval, containment
  and rollback conditions.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- risk
- reversibility
- approval
when-to-use:
- Assess downside, exposure, recoverability and blast radius before consequential actions. Distinguishes
  hard safety boundaries from uncertain performance trade-offs and defines approval, containment and rollback
  conditions.
metadata:
  role: specialized decision module
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-skills
---

# Decision Risk and Reversibility

## Classify consequences, not appearances
Record what can be harmed, who is exposed, scale, duration, detectability, time to recovery, and whether restoration is genuinely possible. Deleting a file with a verified backup differs from publishing a secret that can be copied. A small command can have a large blast radius; a read-only action can still expose confidential data.

## Risk review
1. Enumerate credible failure modes, misuse paths and unintended side effects. Include external communications, cost, privacy, access control and dependency failure where relevant.
2. Separate hard prohibitions and required authorization from tolerable uncertain outcomes. A predicted success probability does not satisfy an approval requirement.
3. Estimate frequency/probability and impact only when evidence supports them. Show ranges and severe tail scenarios; expected value can hide ruinous downside or harm concentrated on others.
4. Reduce exposure through smaller scope, sandboxing, dry runs, least privilege, reversible pilots, backups and independent checks. Mitigation must be applicable and verified, not just named.
5. Define containment and rollback before execution: exact owner, triggers, accessible artifacts, restoration test, and estimated recovery time. Rollback is itself an action that may need permission.
6. Set a decision disposition: within approved bounds, approved only with controls, unresolved pending review, or excluded. Record residual risk and who may accept it.

## Qualitative scales and numerical traps
Risk categories can help triage, but multiplying arbitrary ordinal severity and likelihood labels does not produce an objective probability or financial loss. Use explicit scenarios and distinguish exposure limits from performance preferences. Avoid a universal “90% confidence means safe” rule.

## Example boundary
For a proposed database migration, distinguish a read-only assessment, a staging migration, a production write and deletion of old data. Approval for the first does not cover the others. Verify restoration on an appropriate copy before treating the production step as reversible.

## Escalation and completion
Escalate unresolved authority, unacceptable downside, missing containment, or critical stale evidence. For personal medical, legal, financial or comparable high-impact decisions, support informed choice and qualified review rather than acting as the final authority. Return the risk register, mitigations, residual exposure, approval status, and explicit stop/rollback rules.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. Return to [the main Decision Skills guide](../decision-skills/SKILL.md) to choose the next bounded step. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
