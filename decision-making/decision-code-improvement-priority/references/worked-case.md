# Code improvement priority — worked case

Four known problems are ranked, split into mandatory and optional, and the optional ones are fitted into the available effort. One candidate deliberately has no harm statement in the boundary tests.

## Candidates

| ID | Harm if deferred | Severity | Blast radius | Confidence | Fix risk | Irreversible | Effort |
|---|---|---|---|---|---|---|---|
| F1 | silent data loss in customer records | 0.9 | 0.8 | 0.9 | 0.2 | yes | 0.5 |
| F2 | weekly export corruption | 0.7 | 0.6 | 0.8 | 0.4 | no | 0.3 |
| F3 | occasional misleading log line | 0.4 | 0.2 | 0.6 | 0.1 | no | 0.1 |
| F4 | slow report under peak load | 0.6 | 0.5 | 0.7 | 0.3 | no | 0.2 |

## Calculation

F1 raw = 0.40×0.9 + 0.25×0.8 + 0.15×0.9 + 0.20×0.2 = 0.36 + 0.20 + 0.135 + 0.04 = 0.735; irreversible → 0.735 × 1.25 = 0.91875; cost-adjusted = 0.91875 ÷ 0.5 = **1.8375**.

F2 raw = 0.28 + 0.15 + 0.12 + 0.08 = 0.63; cost-adjusted = 0.63 ÷ 0.3 = **2.1**.

F3 raw = 0.16 + 0.05 + 0.09 + 0.02 = 0.32; cost-adjusted = 0.32 ÷ 0.1 = **3.2** — the effort is exactly at the 0.10 floor, so the division is defined.

F4 raw = 0.24 + 0.125 + 0.105 + 0.06 = 0.53; cost-adjusted = 0.53 ÷ 0.2 = **2.65**.

## Mandatory split, ranking and classification

Mandatory items (irreversible harm or severity ≥ 0.80): **F1** only. Optional: F2, F3, F4.

Ranked order by cost-adjusted priority: F3 3.2, F4 2.65, F2 2.1, F1 1.8375.

F1 is `fix-now` because it is mandatory — irreversibility overrides cheapness, and a mandatory item is never dropped to fit the cap. It consumes 0.5 of the 0.6 available effort. The optional items are then considered in ranked order: F3 needs 0.1, which exactly fits the remaining 0.1, so it is `fix-now` and the used effort reaches 0.6. F4 (0.2) and F2 (0.3) no longer fit, so both are `defer-with-risk` with their harm statements recorded. No candidate has a fix risk above the 0.60 accept floor, so the accepted list is empty.

Note the tension the record makes visible: F1 ranks **last** on cost-adjusted priority and is still the item that must be done. The formula orders attention; irreversibility sets a floor under it.

## Tie handling

If two candidates produced identical cost-adjusted priorities, both would be listed in `ties` at the same rank. Ordering them by identifier or ticket number would manufacture a distinction the evidence does not support.

## What this does not prove

The factors are judgements, not measurements. A different weight set can reorder the list, which is why the weights and the reason for choosing them are part of the record.

## Machine-checkable fixture

The numbers below are synthetic teaching data, not measured results from a real project.

```json
{
  "skill": "decision-code-improvement-priority",
  "weights": {
    "severity": 0.4,
    "blast-radius": 0.25,
    "confidence": 0.15,
    "fix-risk": 0.2
  },
  "irreversibility-multiplier": 1.25,
  "effort-floor": 0.1,
  "accept-floor": 0.6,
  "available-effort": 0.6,
  "candidates": [
    {
      "id": "F1",
      "harm-if-deferred": "silent data loss in customer records",
      "severity": 0.9,
      "blast-radius": 0.8,
      "confidence": 0.9,
      "fix-risk": 0.2,
      "irreversible": true,
      "effort": 0.5
    },
    {
      "id": "F2",
      "harm-if-deferred": "weekly export corruption",
      "severity": 0.7,
      "blast-radius": 0.6,
      "confidence": 0.8,
      "fix-risk": 0.4,
      "irreversible": false,
      "effort": 0.3
    },
    {
      "id": "F3",
      "harm-if-deferred": "occasional misleading log line",
      "severity": 0.4,
      "blast-radius": 0.2,
      "confidence": 0.6,
      "fix-risk": 0.1,
      "irreversible": false,
      "effort": 0.1
    },
    {
      "id": "F4",
      "harm-if-deferred": "slow report under peak load",
      "severity": 0.6,
      "blast-radius": 0.5,
      "confidence": 0.7,
      "fix-risk": 0.3,
      "irreversible": false,
      "effort": 0.2
    }
  ],
  "expected": {
    "cost-adjusted": {
      "F1": 1.8375,
      "F2": 2.1,
      "F3": 3.2,
      "F4": 2.65
    },
    "ranking": [
      "F3",
      "F4",
      "F2",
      "F1"
    ],
    "ties": [],
    "fix-now": [
      "F1",
      "F3"
    ],
    "defer-with-risk": [
      "F2",
      "F4"
    ],
    "accepted": [],
    "fix-now-effort": 0.6
  }
}
```

Validated locally by `skills/_catalog/validate_decision_code_quality.py`.
