---
name: decision-crisis-triage
description: Make bounded operational decisions under time pressure using explicit authority, imminent-harm
  checks, verified state, containment and feasible sequencing. Preserves uncertainty, role clarity, communication
  and handoff without converting urgency into unlimited permission.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored advanced decision module; examples are explicitly synthetic, not measured results.
compatibility: Documentation-first. No SDK, inference service or external execution is required. Local
  example checks use Python standard library.
tags:
- decision-suite
- advanced-decisions
- decision-making
- incident-decisions
- time-pressure
- triage
- containment
when-to-use:
- Make bounded operational decisions under time pressure using explicit authority, imminent-harm checks,
  verified state, containment and feasible sequencing. Preserves uncertainty, role clarity, communication
  and handoff without converting urgency into unlimited permission.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution.
  related-skills:
  - decision-skills
  - decision-agent-action-routing
  - decision-commit-and-monitor
---

# Time-critical Decision Triage and Incident Command

## When to use
Use for urgent operational incidents, rapidly expiring choices or failures where delay has material cost. This is not a substitute for qualified emergency services, medical response or the organization's actual incident plan. For immediate danger to people, prioritize appropriate emergency help and authorized safety procedures.

## First-pass contract
State what is known, what is suspected, what is at risk, the current incident owner, available capabilities and actual response authority. Timestamp observations. Separate reversible containment from diagnosis, restoration and irreversible cleanup. A declared emergency does not automatically grant access, spending or deletion rights.

## Procedure
1. Check imminent harm and mandatory response duties. Use the applicable escalation path; do not delay critical containment to complete a long decision worksheet.
2. Establish one accountable coordinator, clear roles and a shared factual status. Record who can authorize actions, who executes, and who communicates. Avoid several agents independently making conflicting writes.
3. Verify the critical state using the safest adequate observations. Treat missing telemetry and tool timeouts as uncertainty, not proof that a system is healthy or an operation failed.
4. Generate a small set of feasible next actions, including containment and no-change where appropriate. Prefer limiting blast radius and preserving recovery options over optimizing a speculative full fix.
5. Evaluate severity, time to harm, scope, reversibility, action duration, dependencies and required resources. Hard safety/authority constraints come first; an arbitrary urgency score cannot override them.
6. Simulate the near-term sequence when actions compete for the same operator or tool. A shortest-task, least-slack or earliest-deadline heuristic can fail under other conditions; inspect the actual feasible schedule and uncertainty.
7. Set a short decision checkpoint and explicit stop conditions. Bound retries, spend, exposure and concurrency. Before retrying an ambiguous write, check whether it already committed.
8. Execute only approved actions, log observations and verify their effect. Preserve evidence where required and avoid irreversible cleanup that destroys diagnostic information or expands harm.
9. Communicate concise known/unknown/next-step updates with timestamps, owner and next update time. Do not invent an estimated recovery time or claim a background monitor exists without evidence.
10. Reassess as state changes. Escalate when authority, capacity or containment is inadequate; hand off with current state, actions taken, unresolved risks and pending checks. After stabilization, separate restoration, root-cause analysis and long-term improvement.

## Scheduling under uncertainty
Latest nominal start time equals deadline minus estimated duration, but this is only a local quantity. Resource contention, precedence, setup time, interruptions and duration uncertainty determine whether the full sequence is feasible. Add justified buffers and fallback branches rather than treating point estimates as guarantees. If every authorized sequence misses a critical deadline, escalate capacity or containment needs explicitly.

## Failure modes
Avoid analysis paralysis, premature certainty, duplicated side effects, shifting incident command without handoff, hiding failed attempts, and expanding the target boundary under the label of urgency. Do not let a polished postmortem rewrite the incomplete information available during the incident.

## Deliverable
Return the next bounded action, authority, observed evidence and uncertainty, priority rationale, resource/sequence feasibility, verification, stop/escalation trigger and next checkpoint. Keep the immediate record short enough to use under pressure, then add the fuller outcome review after stabilization. Recommendations remain conditional on actual capabilities and domain procedures.

## Resources and handoff

- [Detailed worked case](references/worked-case.md): hypothetical inputs, calculations, interpretation and limitations.
- [Method worksheet](templates/worksheet.md): fill unknowns explicitly; blank fields are not approvals.
- [Decision Skills main guide](../decision-skills/SKILL.md): return the result to the broader decision process.
- [Related method: decision-agent-action-routing](../decision-agent-action-routing/SKILL.md).
- [Related method: decision-commit-and-monitor](../decision-commit-and-monitor/SKILL.md).

This is an advisory method, not permission, an installed capability, a domain credential or a guarantee. Keep concise rationales and verifiable evidence; do not request private internal reasoning. Optional AI judgments do not replace evidence, stakeholder authority or deterministic policy checks. No TypeSafe API call, background process or external action is activated by these files.
