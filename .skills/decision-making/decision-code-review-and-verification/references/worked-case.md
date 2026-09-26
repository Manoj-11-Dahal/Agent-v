# Code review sufficiency — worked case

A tier-4 review plan is checked for coverage, then re-checked after the missing evidence is added.

## Required controls for tier-4

`C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11` — eleven controls.

## Proposed evidence and the mapping

| Evidence item | Covers |
|---|---|
| `test_concurrent_export_race` | C2, C5 |
| `test_timeout_kills_stalled_destination` | C3, C10 |
| `test_rejects_oversize_and_bad_destination` | C3, C11 |
| CI build from clean checkout | C1 |
| Static analysis report `sa-2026-041` | C8 |
| Benchmark `bench/export-100k.json` | C9 |
| Memory ceiling measurement | C7 |

Covered: C1, C2, C3, C5, C7, C8, C9, C10, C11 = 9. Uncovered: **C4 (fuzz/property tests)** and **C6 (fault injection)**.

Coverage = 9 ÷ 11 = **0.8181818181818182**. Verdict **insufficient**, uncovered `["C4", "C6"]`. The reviewer is independent of the author, so C14 is not the problem here — but C14 is not in the tier-4 gate anyway; it becomes required only at tier-5.

## After adding evidence

Two new items are added: `fuzz/export-corpus-v3` (C4) and `fault/dependency-blackout-run-7` (C6). Covered = 11 ÷ 11 = **1.0**, verdict **sufficient**, uncovered list empty.

## Why the arithmetic is not the whole story

Coverage says every required control has named evidence. It does not say the fuzz corpus was long enough or that the fault run exercised a realistic dependency failure — those are separate judgements a competent reviewer must make.

## If the gap were accepted instead

A named accountable human would record: uncovered control C4; harm "a malformed external record could crash the exporter"; detection "crash alerts plus a restart runbook"; review date. That record, not a blank checkbox, is what makes the acceptance auditable.

## Machine-checkable fixture

The numbers below are synthetic teaching data, not measured results from a real project.

```json
{
  "skill": "decision-code-review-and-verification",
  "required-tier": "tier-4",
  "required-controls": [
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "C6",
    "C7",
    "C8",
    "C9",
    "C10",
    "C11"
  ],
  "proposed-evidence": [
    {
      "id": "test_concurrent_export_race",
      "covers": [
        "C2",
        "C5"
      ]
    },
    {
      "id": "test_timeout_kills_stalled_destination",
      "covers": [
        "C3",
        "C10"
      ]
    },
    {
      "id": "test_rejects_oversize_and_bad_destination",
      "covers": [
        "C3",
        "C11"
      ]
    },
    {
      "id": "ci-clean-checkout-build",
      "covers": [
        "C1"
      ]
    },
    {
      "id": "sa-2026-041",
      "covers": [
        "C8"
      ]
    },
    {
      "id": "bench/export-100k.json",
      "covers": [
        "C9"
      ]
    },
    {
      "id": "memory-ceiling-measurement",
      "covers": [
        "C7"
      ]
    }
  ],
  "reviewer-independent": true,
  "cases": [
    {
      "id": "initial-plan",
      "added-evidence": [],
      "expected": {
        "covered-count": 9,
        "required-count": 11,
        "coverage": 0.8181818181818182,
        "uncovered": [
          "C4",
          "C6"
        ],
        "verdict": "insufficient"
      }
    },
    {
      "id": "after-adding-evidence",
      "added-evidence": [
        {
          "id": "fuzz/export-corpus-v3",
          "covers": [
            "C4"
          ]
        },
        {
          "id": "fault/dependency-blackout-run-7",
          "covers": [
            "C6"
          ]
        }
      ],
      "expected": {
        "covered-count": 11,
        "required-count": 11,
        "coverage": 1.0,
        "uncovered": [],
        "verdict": "sufficient"
      }
    }
  ]
}
```

Validated locally by `skills/_catalog/validate_decision_code_quality.py`.
