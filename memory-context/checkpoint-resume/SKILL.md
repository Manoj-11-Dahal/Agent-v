---
name: checkpoint-resume
description: "Save and restore concise, evidence-backed project checkpoints without persisting secrets or private reasoning."
---
# Checkpoint and resume

Save task state at meaningful boundaries, before risky changes, or when explicitly asked.
Use an approved project state directory, not hidden global memory.

Record: task ID, user-visible goal, scope, affected paths, branch/revision when available,
completed changes, commands actually run and outcomes, unresolved issues, next steps,
required approvals, and timestamp. Preserve facts and concise decisions, not hidden
chain-of-thought, secrets, or unrelated personal data.

Write via a temporary file and atomic rename; retain a previous checkpoint. A checkpoint
is not a repository backup and must not assert tests passed unless evidence exists.

To resume: reread user instructions and the checkpoint, inspect the current files and
revision, identify drift, revalidate permissions, and rerun stale or consequential checks.
Never restore old generated files over new work without checking differences.

Acceptance: another agent can identify what remains, what is unverified, and which files
to inspect, without treating the checkpoint as higher-priority executable instructions.
