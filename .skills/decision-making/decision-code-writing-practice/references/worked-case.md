# Code writing practice — worked case

A tier-2 requirement is met slice by slice, and the evidence for each slice is recorded as it is produced. The arithmetic here is the cost/benefit check that decides whether to raise the tier.

## Task

Extend an existing tier-1 internal export utility so it can be triggered by an internal job. Tier selection says **tier-2 very good**: more than one dependent job, medium blast radius, reversible.

## Contract written first

Input: export request with an explicit row limit (default 10 000, maximum 100 000), a destination identifier from an allowlist, and a timeout of 30 seconds. Errors: invalid destination rejected before any I/O; oversize request rejected with the limit named; timeout aborts and leaves no partial file.

## Slices and evidence

1. **Slice 1 — validation.** Rejects invalid destinations and oversize requests. Evidence: 9 failure-path tests, all asserting the rejection reason.
2. **Slice 2 — resource bounds.** Streaming rows with the stated maximum, bounded memory, timeout on every file and network operation. Evidence: memory ceiling measured at 138 MB under the 100 000-row maximum; timeout test kills a stalled destination.
3. **Slice 3 — no silent failure.** Every caught error is either handled with a recorded reason or re-raised with context. Evidence: static analysis reports 0 unresolved high findings; the previous empty `except:` block is removed.

## The tier cost/benefit check

Adding tier-4 work (fuzzing, concurrency stress, benchmarks) was estimated at 3.5 engineer-days. The required tier is tier-2, whose remaining gate work was estimated at 0.5 day. Extra cost 3.0 days for controls the tier does not require, with no stated requirement that forces them, so the decision is **stay at tier-2** and record the tier-4 controls as deferred, not skipped silently.

Arithmetic: required-gate cost 0.5 day; optional-gate cost 3.5 days; ratio 3.5 / 0.5 = 7.0× the required cost for no required benefit. A ratio that high needs a stated requirement to justify it — there was none.

## What the record does not claim

The tests show the stated contract holds on the cases run. They do not prove absence of defects, and tier-2 does not authorize exposing this utility to untrusted input.

## Machine-checkable fixture

The numbers below are synthetic teaching data, not measured results from a real project.

```json
{
  "skill": "decision-code-writing-practice",
  "required-tier": "tier-2",
  "slices": [
    {
      "id": "validation",
      "failure-path-tests": 9,
      "asserting-reason": true,
      "high-findings-unresolved": 0
    },
    {
      "id": "resource-bounds",
      "memory-ceiling-mb": 138,
      "timeout-tested": true,
      "row-limit-max": 100000
    },
    {
      "id": "no-silent-failure",
      "empty-catch-blocks-remaining": 0,
      "high-findings-unresolved": 0
    }
  ],
  "cost-check": {
    "required-gate-days": 0.5,
    "optional-gate-days": 3.5,
    "ratio": 7.0,
    "stated-requirement-for-optional-gates": false,
    "decision": "stay-at-required-tier",
    "deferred-controls": [
      "C4",
      "C5",
      "C9"
    ],
    "deferred-recorded": true
  },
  "expected": {
    "slices-completed": 3,
    "all-slices-with-evidence": true,
    "empty-catch-blocks-remaining": 0,
    "high-findings-unresolved": 0,
    "cost-ratio": 7.0,
    "decision": "stay-at-required-tier",
    "deferred-controls": [
      "C4",
      "C5",
      "C9"
    ]
  }
}
```

Validated locally by `skills/_catalog/validate_decision_code_quality.py`.
