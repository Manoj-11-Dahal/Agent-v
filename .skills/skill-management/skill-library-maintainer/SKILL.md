---
name: skill-library-maintainer
description: "Maintain a canonical agent skill library through staged installs, source tracking, conflict checks, integrity verification, and rollback."
---
# Skill library maintainer

## Inputs
Canonical library, lock file, requested repositories or versions, and conflict policy.
Default here: `/home/user/.agentic/skills/`; keep existing skill names unless the user
explicitly approves replacement. Do not execute downloaded scripts while installing.

## Procedure
1. Inventory installed entry points, source records, and current hashes. Save a backup
   before modifications. If supporting files are archived, use `.agentic/bin/skill-files.py`
   to materialize a complete skill rather than treating packed references as missing.
2. Stage each requested source under `.cache/`, using the Skills CLI with explicit
   non-interactive scope. Use `--full-depth` when all nested skills are requested.
3. Parse SKILL.md metadata, map original names to actual staged folders, and reject
   path traversal, broken references required at runtime, and unexpected symlinks.
4. Report invalid metadata, inaccessible sources, duplicate names, and security warnings.
   Keep local repairs distinct from upstream originals; record provenance and license.
5. Apply the approved conflict policy. Never silently replace existing skill behavior.
6. Check projected workspace size and file count before promotion. For this environment,
   maintain headroom below the snapshot file limit; archive references with verified
   on-demand extraction when necessary. Do not archive skill entry points.
7. Copy or swap verified additions, preserve old versions until checks pass, and update
   the lock file, index, manifest, domain guide, and installation report together.
8. Verify original files are unchanged, additions match staged hashes, archive members
   match their originals, index links resolve, and no duplicate skill directory appeared.
9. Roll back a failed promotion. Remove temporary downloads only after verification.

## Output and acceptance
Report added, skipped, replaced, repaired, unavailable, and locally authored counts
separately. Include exact installed paths and checks run. A risk scanner is not a
security audit, and metadata registration is not proof of runtime capability.
