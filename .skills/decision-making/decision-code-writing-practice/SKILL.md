---
name: decision-code-writing-practice
description: Turn a required code quality tier into concrete engineering practice — contracts first, reviewable slices, tier-appropriate tests, resource bounds, observability, measured performance and recorded evidence. Includes per-tier practices and anti-patterns.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision module; examples and fixtures are synthetic teaching data.
compatibility: Documentation-first. No SDK, inference service, compiler or external execution is required.
tags:
- decision-suite
- advanced-decisions
- code-quality
- code-writing
- engineering-practice
when-to-use:
- Implement or extend code so it genuinely reaches a required quality tier.
- Decide which engineering practices are worth their cost for a given tier.
- Produce evidence that a tier claim can survive review.
metadata:
  role: advanced decision method
  scope: Advisory methods within actual user authority; no automatic execution or guaranteed outcome.
  related-skills:
  - decision-skills
  - decision-code-tier-selection
  - decision-code-quality-tiers
  - decision-language-profiles
  - decision-commit-and-monitor
---
# Decision Skills: Code Writing Practice — Implement to the Required Tier

**Scope.** Decide how to write or extend code so it lands at a required tier — and how to prove it. This module turns a tier requirement into concrete engineering practices and evidence, rather than into adjectives.

## The tier ladder in practice

| Tier | What you must actually do | What you record |
|---|---|---|
| basic | Make it run once; keep it short; say in a comment that it is throwaway | The command run and its output |
| good | Name things after their meaning; normal-path tests; one non-author read | Test list and reviewer note |
| very good | Hostile input and error paths tested; explicit resource bounds; no silent catch | Failure-path test names, limit values |
| excellent | Seams for testing; invariants stated; observable behaviour; documented failure modes | Coverage on decision paths, log/metric names |
| advanced | Benchmarked against a budget; concurrency and fault behaviour characterized | Benchmark numbers, race and fault-injection records |
| hxmax | Full control set, independent verification, assurance case, named sign-off | Assurance case file and approval record |

## Procedure

1. **Start from the required tier**, decided by [decision-code-tier-selection](../decision-code-tier-selection/SKILL.md). Do not re-derive it here.
2. **Write the contract first:** inputs, outputs, error conditions, invariants, resource limits. The contract is what tests will check.
3. **Pick the smallest design that satisfies the contract.** Complexity is a cost paid by every future reader; add it only when a stated requirement forces it.
4. **Choose language and libraries** with [decision-language-profiles](../decision-language-profiles/SKILL.md). Record why, including what you gave up.
5. **Implement in reviewable slices.** Each slice compiles, passes its own tests, and can be reverted independently.
6. **Write the tests that the tier requires**, not the tests that are easy. For tier-2 and above, that includes failure paths and hostile input before features.
7. **Record evidence as you go**: test names, benchmark output, analysis findings, resource measurements. Evidence written later is usually wrong.
8. **Check the gate** with [decision-code-quality-tiers](../decision-code-quality-tiers/SKILL.md) before claiming the tier.
9. **Send for review** with [decision-code-review-and-verification](../decision-code-review-and-verification/SKILL.md).

## Practices that move a tier

- **Naming and structure (tier-1 → tier-2).** Names describe intent, not mechanism. One function, one reason to change. Depth over breadth: fewer, more useful interfaces.
- **Failure behaviour (tier-2).** Decide for every external input whether it is rejected, sanitized, or propagated. No empty catch blocks. Errors carry enough context to diagnose without a debugger.
- **Resource bounds (tier-2 → tier-3).** Every loop, allocation, connection and file has a stated limit. Timeouts on every network and lock path. Cleanup on both success and failure paths.
- **Testability (tier-3).** Seams where behaviour can be substituted: time, randomness, network, filesystem, clock. Pure logic separated from I/O. Deterministic tests; no sleep-based synchronization where an explicit signal exists.
- **Observability (tier-3).** Structured logs with correlation identifiers; metrics for rate, errors, duration and saturation; alerts that map to a runbook step.
- **Performance and concurrency (tier-4).** Measure before optimizing, then keep the measurement. Concurrency: state ownership, message passing over shared mutable state, bounded queues, no unbounded retries.
- **Assurance (tier-5).** Follow [decision-hxmax-standard](../decision-hxmax-standard/SKILL.md). The extra work is evidence and independent verification, not more code.

## Interpretation limits

- Practices do not guarantee outcomes. They make failures easier to detect and cheaper to fix.
- A tier is a floor for a context, not a virtue signal. Higher tier on a throwaway script is waste.
- These rules are language-neutral. Language-specific tooling is in the profile table, and the profile is guidance, not a guarantee about any particular version.
- Nothing in this module executes code, installs packages, or grants permission to deploy.

## Failure modes

- **Practice theatre.** Adding logs and tests that assert nothing, to look like a higher tier.
- **Gold-plating.** Designing for tier-4 in code whose required tier is tier-1, then missing the deadline and shipping unreviewed.
- **Untested abstractions.** Generic frameworks built before a second concrete use exists.
- **Optimization without measurement.** Rewriting hot paths on intuition and losing correctness.
- **Evidence after the fact.** Writing "we fuzzed it" with no recorded findings or seeds.
