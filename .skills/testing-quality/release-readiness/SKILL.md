---
name: release-readiness
description: "Assess whether a project is ready for release using tests, security checks, migration plans, operational checks, and rollback evidence."
---
# Release readiness

1. Identify target environment, release scope, user impact, and release owner.
2. Verify lint/type checks, unit and integration tests, build artifacts, and relevant
   end-to-end tests. Record exact commands, revision, and known gaps.
3. Review dependency and secret findings, permissions, license requirements, configuration,
   migration compatibility, backup availability, and data-retention requirements.
4. Check observability, health checks, resource limits, and rollback instructions.
   Confirm rollback is feasible before changing irreversible schema or data.
5. Review changelog, user-facing behavior, accessibility, and performance criteria relevant
   to this project. Do not invent universal numeric thresholds.
6. Produce go/no-go/conditional-go with evidence and named unresolved blockers.
7. Request deployment approval separately. This skill must not publish or deploy by default.

Acceptance: release decision is traceable to evidence, not just a green build command.
