---
name: decision-language-profiles
description: Choose an implementation language from a compact profile of 148 languages — paradigm, type system, memory model, concurrency, error handling, build, tests, linting, fuzzing, verification tooling and platform. Reports infeasible requirement sets instead of defaulting.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision module; examples and fixtures are synthetic teaching data.
compatibility: Documentation-first. No SDK, inference service, compiler or external execution is required.
tags:
- decision-suite
- advanced-decisions
- code-quality
- language-selection
- language-profiles
- tooling
when-to-use:
- Choose an implementation language for a task from stated requirements rather than familiarity.
- Check whether candidate languages can support the fuzzing or verification the required tier needs.
- Detect a requirement set that no language satisfies and decide what to relax.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution or guaranteed outcome.
  related-skills:
  - decision-skills
  - decision-code-tier-selection
  - decision-code-writing-practice
  - decision-hxmax-standard
  - decision-options-and-tradeoffs
---
# Decision Skills: Language Profiles — Choose the Implementation Language From Evidence

**Scope.** Decide which implementation language to use for a task, using a compact profile of **148 languages** instead of familiarity. The profile table lives in [references/language-profiles.csv](references/language-profiles.csv); the quality bar it must meet lives in [references/tier-definitions.json](references/tier-definitions.json).

## What a profile records

`name, paradigm, type-system, memory, concurrency, error-handling, build, tests, lint, fuzz, verify, platform, notes`

Each row is a one-line orientation, not documentation for a specific language version. It is guidance for narrowing a choice; the actual decision must be confirmed against the version and libraries you will really use.

## Procedure

1. **State the requirements as field values**, not vibes: memory model (`manual`, `gc`, `ownership`), concurrency model, platform target, error-handling style, and whether fuzzing or formal verification is needed for the required tier.
2. **Filter the table** by those values. Substring matching on a field is enough for narrowing; a match means "worth examining", never "correct choice".
3. **Sort the survivors by the cost that actually matters to you:** team familiarity, hiring pool, library maturity, deployment constraints, licence cost.
4. **Check the tier fit.** If the required tier is tier-4 or tier-5, prefer languages whose `fuzz` and `verify` columns name real tools — otherwise you are committing to build the missing tooling yourself.
5. **Record what you gave up.** Every choice excludes something; write down the excluded alternative and why.
6. **If nothing satisfies the requirements, say so.** Report `infeasible` with the conflicting requirements and either relax a requirement explicitly or change the design. Do not pick a default because the list came back empty.

## Interpretation limits

- The table is a decision aid maintained locally. It is not authoritative about any language, and languages change faster than the table does.
- "No tool listed" means none is recorded here, not that none exists.
- Language choice never removes the need for the tier's controls. A memory-safe language does not satisfy C3, C6 or C11 by itself.
- Nothing here installs anything or executes code.

## Failure modes

- **Familiarity laundering.** Choosing a language the team knows and recording a requirement list invented afterwards.
- **Table worship.** Treating a profile row as verified documentation for the current version.
- **Default on empty result.** Silently picking the first row when the filter returned nothing.
- **Tier mismatch.** Selecting a language with no recorded fuzzing or verification tooling for tier-5 work, then discovering the gap at release.
- **Ignoring deployment constraints.** A technically elegant language the target platform cannot run.
- **Licence blindness.** Overlooking that a platform or toolchain imposes cost or lock-in.
