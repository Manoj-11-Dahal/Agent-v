---
name: decision-hxmax-standard
description: The library-defined top tier for code — fifteen required controls, an independent reviewer, a named human sign-off and a release gate that reports ready, conditional or blocked. Explicitly a local standard, not an external certification or a defect-freedom claim.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision module; examples and fixtures are synthetic teaching data.
compatibility: Documentation-first. No SDK, inference service, compiler or external execution is required.
tags:
- decision-suite
- advanced-decisions
- code-quality
- hxmax
- assurance
- release-gate
- highest-assurance
when-to-use:
- Decide whether a revision meets the HXMax v1 assurance bar with recorded evidence.
- Evaluate a release gate and report ready, conditional or blocked with the exact missing controls.
- Keep a top-tier label honest across revisions instead of reusing an old approval.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution or guaranteed outcome.
  related-skills:
  - decision-skills
  - decision-code-quality-tiers
  - decision-code-review-and-verification
  - decision-commit-and-monitor
  - decision-scenarios-and-premortem
---
# Decision Skills: HXMax v1 — A Custom Highest-Assurance Engineering Standard

**Scope.** HXMax is **this library's own defined top tier** for engineering work. It is not an industry certification, not an ISO/IEC standard, and not a claim that code is defect-free. It is a documented control set with a release gate that refuses to pass when evidence is missing.

## HXMax v1 — definition

A revision may be labelled HXMax only when **all fifteen controls have recorded evidence**, an **independent reviewer** has verified that evidence, and a **named human has signed the release decision**. The label applies to that exact revision and that evidence set only; it does not transfer to the next commit, the next release, or the team that produced it.

### Control set

| ID | Control | Evidence that satisfies it |
|---|---|---|
| C1 | Reproducible build | Clean-checkout build with pinned dependencies and a recorded toolchain version |
| C2 | Behaviour tests | Named tests for every claimed behaviour, run in CI |
| C3 | Failure-path tests | Named tests for malformed input, limits, partial failure and timeout |
| C4 | Fuzz or property tests | Corpus or generator identifier, run duration, findings and their disposition |
| C5 | Concurrency and race testing | Detector or stress-run record with the interleavings exercised |
| C6 | Fault injection and degradation | Record of dependency outage, disk full, clock skew or similar, with observed behaviour |
| C7 | Resource bounds and leaks | Measured ceilings for memory, descriptors, threads and time under the stated load |
| C8 | Static analysis | Tool and rule-set identifier, with every high-severity finding resolved or explicitly accepted |
| C9 | Measured performance | Benchmark identifier, workload definition, budget and comparison to a baseline |
| C10 | Degraded-mode behaviour | Verified behaviour under limits: queueing, shedding, retry with backoff, safe refusal |
| C11 | Trust boundaries and secrets | Input validation points, allowlists, secret handling, least-privilege configuration |
| C12 | Observability | Log, metric and trace names, alert definitions, and their runbook links |
| C13 | Operational readiness | Runbook, tested rollback, on-call owner, and a rehearsed restore |
| C14 | Independent review and sign-off | Reviewer not the author, named approver, date, and the revision identifier |
| C15 | Legal, privacy, accessibility, safety | Licence compatibility, data-minimisation note, accessibility check, and safety review where applicable |

### Release gate

| Condition | Status |
|---|---|
| All 15 controls satisfied, independent reviewer and named approver recorded | `ready` |
| All controls except C14 or C15 satisfied, with a written conditional-approval plan | `conditional` |
| Any other control missing or unknown | `blocked` |

`conditional` is the only path that allows release planning before full sign-off, and it requires the plan to name who will complete C14/C15 and by when. Missing C14 means nobody independent has verified the evidence; missing C15 means the work may not be lawful to ship. Both are reasons to stop, not to soften.

## Procedure

1. Confirm the required tier really is tier-5 using [decision-code-tier-selection](../decision-code-tier-selection/SKILL.md). HXMax on work that needs tier-2 is waste.
2. Open the control table and record evidence identifiers for each of the fifteen controls. `unknown` is a valid entry and blocks the gate.
3. Resolve or explicitly accept each finding; acceptance names the acceptor and the harm.
4. Obtain independent review (C14) — the author cannot satisfy this control.
5. Complete the legal, privacy, accessibility and safety review (C15).
6. Evaluate the release gate and record `ready`, `conditional` or `blocked` with the exact missing controls.
7. Have a named human sign the decision, including the revision identifier. Store the assurance case with the revision.
8. On any change, re-run steps 2–7. The label does not persist across revisions.

## Interpretation limits

- HXMax states that evidence exists and was independently checked. It does not state that the system cannot fail.
- Controls are necessary, not sufficient: passing all fifteen with weak evidence still yields weak assurance. Judge evidence quality separately.
- This standard is local. Do not represent it to third parties as an external certification.
- No tool in this library performs the verification. Every control requires a human or an external system to produce the evidence.

## Failure modes

- **Label reuse.** Calling a service "HXMax" forever after one approved revision.
- **Self-verification.** The author recording their own independent review.
- **Evidence by assertion.** "Fuzzed extensively" with no corpus identifier, duration or findings.
- **Conditional drift.** `conditional` status left open past its stated completion date with no escalation.
- **Gate softening.** Reclassifying a missing control as "not applicable" after the deadline, without recording who decided and why.
