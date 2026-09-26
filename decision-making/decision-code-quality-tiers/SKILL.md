---
name: decision-code-quality-tiers
description: Assess existing code against a six-tier quality ladder (basic, good, very good, excellent, advanced, HXMax) using explicit control gates, weighted component scores and an AND rule that prevents a high score from hiding a missing safety control.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision module; examples and fixtures are synthetic teaching data.
compatibility: Documentation-first. No SDK, inference service, compiler or external execution is required.
tags:
- decision-suite
- advanced-decisions
- code-quality
- code-assessment
- quality-tiers
- hxmax
when-to-use:
- Judge whether existing code is basic, good, very good, excellent, advanced or HXMax grade with recorded evidence.
- Decide whether a high-looking score is allowed to pass a tier whose safety controls are missing.
- Produce a blocking gap list that a reviewer or approver can act on.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution or guaranteed outcome.
  related-skills:
  - decision-skills
  - decision-code-tier-selection
  - decision-code-improvement-priority
  - decision-hxmax-standard
  - decision-evidence-and-uncertainty
---
# Decision Skills: Code Quality Tiers — Assess Code Against a Fixed Tier Ladder

**Scope.** Classify existing code against a fixed tier ladder so that a later choice — accept, improve, block, rewrite — is defensible. This module judges quality; it does not by itself decide what to do about it. Use [decision-code-tier-selection](../decision-code-tier-selection/SKILL.md) to choose the required tier for a context, [decision-code-improvement-priority](../decision-code-improvement-priority/SKILL.md) to order fixes, and [decision-code-writing-practice](../decision-code-writing-practice/SKILL.md) to implement changes.

## Tier ladder (six tiers)

| Tier | Name | Core meaning | Minimum evidence |
|---|---|---|---|
| tier-0 | basic | Runs at least once; understandable to its author; expected to be discarded or replaced | A recorded run and its output |
| tier-1 | good | Correct on normal input; named; reviewed by someone other than the author | Normal-path tests plus one review record |
| tier-2 | very good | Correct on hostile and edge input; safe resource use; explicit failure behaviour | Edge/error tests, resource limits, one independent review |
| tier-3 | excellent | Testable design with seams; observable; documented invariants and failure modes | Coverage evidence on decision paths, observability, written invariants |
| tier-4 | advanced | Performance, concurrency and fault behaviour characterized, not assumed | Benchmarks, concurrency and fault-injection evidence |
| tier-5 | HXMax | Full assurance case, independent verification and named human sign-off | All 15 HXMax controls plus signed approval |

Tier names are local labels defined in [../decision-language-profiles/references/tier-definitions.json](../decision-language-profiles/references/tier-definitions.json). They are not an industry certification and tier-5 is not a claim that the code is defect-free.

## Control set used by the gates

C1 reproducible build · C2 automated tests on the claimed behaviour · C3 failure-path tests · C4 fuzz/property tests on external input · C5 concurrency and race testing · C6 fault injection and degradation tests · C7 resource bounds and leak checks · C8 static analysis with no unresolved high findings · C9 measured performance against a budget · C10 degraded-mode behaviour verified · C11 input trust boundaries and secret handling · C12 observability · C13 operational runbook, rollback and ownership · C14 independent review and named human approval · C15 legal, privacy, accessibility and safety review.

Each tier's gate is a fixed set of these controls: tier-0 `{C1}`, tier-1 `{C1,C2,C8}`, tier-2 `{C1,C2,C3,C8,C11}`, tier-3 adds `{C7,C12,C13}`, tier-4 adds `{C4,C5,C6,C9,C10}`, tier-5 requires all fifteen plus C14 sign-off.

## Required inputs

1. Exact code under assessment: revision identifier and file list.
2. Intended use and blast radius (who is harmed if it fails, and can the effect be reversed?).
3. Evidence inventory: which controls actually have recorded evidence, and which are unknown.
4. Component assessments, each scored 0.0–1.0 with a written reason: correctness, failure handling, readability and structure, testability and coverage, operational readiness, performance and resources, security and safety.
5. Reviewer identity and independence from the author.

## Procedure

1. **Fix the revision.** Record the identifier being judged. Judgements do not carry over to later revisions.
2. **Score components 0.0–1.0** with one sentence of evidence each. No component may exceed the evidence it cites; missing evidence is `unknown`, never a default score.
3. **Weight the components** so weights sum to 1.0. Weighting is a preference statement — record who chose it and why.
4. **Determine control status** as `true`, `false`, or `unknown`. Unknown never counts as satisfied.
5. **Compute the weighted score** and the highest tier whose gate every control satisfies.
6. **Apply the AND rule**: reported tier = the lower of the score-derived tier and the gate-derived tier. A high score with a failing gate does not promote the code.
7. **Record the blocking gap** — the lowest tier that is not satisfied and which controls block it.
8. **If any control is unknown, report `evidence-incomplete`** and do not issue a tier. Say which evidence is missing.
9. **Hand off** to tier selection, improvement priority, or HXMax verification with the gap list attached.

## Interpretation limits

- The score is an ordinal comparison aid, not a measurement of correctness. Two different weightings can rank the same code differently.
- Gates are binary; the score is continuous. Never present the score as a pass/fail line by itself.
- Component scores from the author are weaker evidence than from an independent reviewer.
- Nothing here authorizes deployment. Approval is a separate human act recorded outside this module.
- A tier describes the assessed revision only, under the stated evidence.

## Failure modes

- **Score laundering.** High readability score used to offset an untested failure path. The AND rule blocks this.
- **Unknown treated as pass.** Missing evidence recorded as `true`. Validators reject non-boolean control status.
- **Tier inflation by naming.** Calling a script "production-grade" without C2/C3/C11 evidence.
- **Weight fiddling.** Lowering the weight of the failing component instead of fixing it. Record weight changes and their reason.
- **Assessment drift.** Reusing an old judgement for new code because the diff looked small.

## Worked example and template

See [references/worked-case.md](references/worked-case.md) for a full calculation with a blocked promotion, and [templates/worksheet.md](templates/worksheet.md) for recording an assessment.
