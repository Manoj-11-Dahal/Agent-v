# Custom hacking skills

**12 locally authored skills + 12 assessment worksheets.**

Designed for authorized assessments and controlled labs. No tools were installed, targets tested, or existing skills replaced. Each package contains an entry point and a reusable evidence worksheet. Technical overlap is intentional where these specialized audit/regression workflows complement the existing broader playbooks.

| Skill | Category | Focus |
|---|---|---|
| [security-scope-and-test-budget](../security-pentesting/security-scope-and-test-budget/SKILL.md) | security-pentesting | Translate an authorized web/API assessment into a bounded test plan with asset allowlists, test identities, request and concurrency budgets, evidence handling, and stop conditions. Complements technical pentest skills rather than running them. |
| [web-authorization-regression-matrix](../security-pentesting/web-authorization-regression-matrix/SKILL.md) | security-pentesting | Build repeatable role, object-owner, and tenant authorization regression tests using synthetic accounts and differential controls. Focuses on durable negative-test coverage and evidence, complementing existing BOLA and IDOR playbooks. |
| [api-state-machine-abuse-lab](../security-pentesting/api-state-machine-abuse-lab/SKILL.md) | security-pentesting | Model an API business workflow as states, transitions, and invariants, then test out-of-order, duplicate, and stale actions against synthetic lab fixtures. Emphasizes idempotency and auditability without touching real financial or customer workflows. |
| [graphql-cost-budget-assessment](../security-pentesting/graphql-cost-budget-assessment/SKILL.md) | security-pentesting | Assess GraphQL query-cost controls, resolver authorization, pagination limits, and error handling using schema review and small approved staging probes. Complements GraphQL discovery without generating denial-of-service workloads. |
| [network-exposure-differential-audit](../security-pentesting/network-exposure-differential-audit/SKILL.md) | security-pentesting | Compare approved network inventory snapshots to identify newly exposed services, ownership gaps, and reachability changes. Separates inventory drift from verified vulnerabilities and uses bounded validation rather than broad autonomous scanning. |
| [linux-privilege-boundary-review](../security-pentesting/linux-privilege-boundary-review/SKILL.md) | security-pentesting | Review Linux service identities, executable/configuration ownership, delegation rules, scheduled jobs, and writable trust paths using approved read-only evidence. Complements privilege-escalation techniques with a non-exploitative boundary audit and remediation plan. |
| [cloud-iam-effective-access-review](../security-pentesting/cloud-iam-effective-access-review/SKILL.md) | security-pentesting | Trace cloud identity, resource, session, organization, and trust policies to explain effective access for specific approved actions. Produces evidence-backed least-privilege findings without enumerating secrets or changing roles. |
| [container-runtime-boundary-audit](../security-pentesting/container-runtime-boundary-audit/SKILL.md) | security-pentesting | Compare declared container or pod configuration with runtime isolation boundaries, mounts, capabilities, identities, and network intent. Focuses on read-only configuration evidence and remediation, not host escape execution. |
| [ctf-binary-triage-workbench](../reverse-engineering-forensics/ctf-binary-triage-workbench/SKILL.md) | reverse-engineering-forensics | Triage an authorized CTF or owned binary using hashes, file-format metadata, imports, strings, and a hypothesis-driven analysis plan before any execution. Produces a reproducible artifact map and separates observations from guesses. |
| [ctf-crash-minimization](../reverse-engineering-forensics/ctf-crash-minimization/SKILL.md) | reverse-engineering-forensics | Reduce a crashing input for an owned parser or CTF program into a stable minimal reproducer, classify the failure, and propose a regression test. Emphasizes bounded isolated execution and does not convert crashes into exploit payloads. |
| [firmware-static-trust-map](../reverse-engineering-forensics/firmware-static-trust-map/SKILL.md) | reverse-engineering-forensics | Map an authorized firmware image into partitions, filesystems, boot components, update metadata, and trust relationships using static evidence. Documents parser risks, authenticity uncertainty, and configuration exposure without flashing devices or extracting credentials. |
| [reverse-engineering-patch-diff-review](../reverse-engineering-forensics/reverse-engineering-patch-diff-review/SKILL.md) | reverse-engineering-forensics | Compare authorized pre- and post-fix binaries or source snapshots to locate security-relevant changes, explain likely invariants, and design benign regression tests. Separates compiler/layout noise from evidence without deriving attack payloads. |

## Quick lookup

```bash
python3 /home/user/skills/_catalog/find.py --tag custom-hacking --limit 20
python3 /home/user/skills/_catalog/find.py --skill web-authorization-regression-matrix --outline
```

The detailed JSON, CSV tables, category pages, and catalog are rebuilt after addition. Existing missing references remain missing; the removed archive and template are not restored.
