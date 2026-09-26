# Code quality tiers — worked case

One candidate module is assessed three ways: as delivered, after adding fuzz and property tests, and in a variant where a strong score hides a failing safety control. A fourth input shows an assessment with unknown evidence.

## 1. As delivered

Weights (sum = 1.0): correctness 0.30, failure handling 0.20, readability and structure 0.15, testability 0.15, operational readiness 0.10, performance 0.05, security 0.05.

Weighted score = 0.30×0.85 + 0.20×0.70 + 0.15×0.80 + 0.15×0.75 + 0.10×0.60 + 0.05×0.70 + 0.05×0.65
= 0.255 + 0.14 + 0.12 + 0.1125 + 0.06 + 0.035 + 0.0325 = **0.755**.

Controls: C1, C2, C3, C7, C8, C11, C12, C13 satisfied (C7 because memory ceilings were measured); C4, C5, C6, C9, C10, C14, C15 not satisfied. The tier-3 gate `{C1,C2,C3,C7,C8,C11,C12,C13}` is therefore fully satisfied, so the gate-derived tier is tier-3. The score-derived tier is tier-2, because 0.755 < 0.80.

**Reported tier: tier-2 very good.** Blocking gap: tier-3, missing the score floor 0.80 (all tier-3 controls are satisfied). Note the two different reasons a promotion can fail: a control gate or the score floor.

## 2. After adding fuzz and property tests

The same weights, but failure handling rises to 0.80, testability to 0.85, security to 0.80 and operational readiness to 0.70 because the new tests exposed and fixed two parsers bugs:

0.30×0.85 + 0.20×0.80 + 0.15×0.80 + 0.15×0.85 + 0.10×0.70 + 0.05×0.70 + 0.05×0.80
= 0.255 + 0.16 + 0.12 + 0.1275 + 0.07 + 0.035 + 0.04 = **0.8075**, with C4 now `true`.

Score 0.8075 ≥ 0.80 and the tier-3 gate is satisfied, so **tier-3 excellent**. Tier-4 is still blocked by C5, C6, C9, C10.

## 3. High score, failing safety control

Same 0.8075 score, but the input trust boundary work was never done, so C11 is `false`. Tier-2 requires C11, so no tier at or above tier-2 is available; the highest satisfied gate is tier-1.

**Reported tier: tier-1 good — score-derived tier-3 is not honoured.** This is the AND rule doing its job: 0.8075 cannot buy its way past a missing input-validation control.

## 4. Unknown evidence

If any control is recorded `unknown`, the assessment reports `evidence-incomplete` and issues no tier, listing the controls that must be resolved. Guessing a status would convert missing evidence into a promotion.

## What the arithmetic does not prove

These are synthetic numbers. A tier is a recorded judgement about one revision under stated evidence — not a certification, not a correctness proof, and not deployment approval.

## Machine-checkable fixture

The numbers below are synthetic teaching data, not measured results from a real project.

```json
{
  "skill": "decision-code-quality-tiers",
  "controls": [
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
    "C11",
    "C12",
    "C13",
    "C14",
    "C15"
  ],
  "weights": {
    "correctness": 0.3,
    "failure-handling": 0.2,
    "readability-structure": 0.15,
    "testability": 0.15,
    "operational-readiness": 0.1,
    "performance": 0.05,
    "security": 0.05
  },
  "cases": [
    {
      "id": "as-delivered",
      "components": {
        "correctness": 0.85,
        "failure-handling": 0.7,
        "readability-structure": 0.8,
        "testability": 0.75,
        "operational-readiness": 0.6,
        "performance": 0.7,
        "security": 0.65
      },
      "gate": {
        "C1": true,
        "C2": true,
        "C3": true,
        "C4": false,
        "C5": false,
        "C6": false,
        "C7": true,
        "C8": true,
        "C9": false,
        "C10": false,
        "C11": true,
        "C12": true,
        "C13": true,
        "C14": false,
        "C15": false
      },
      "expected": {
        "status": "tier-assigned",
        "weighted-score": 0.755,
        "score-derived-tier": "tier-2",
        "gate-derived-tier": "tier-3",
        "reported-tier": "tier-2",
        "blocking-tier": "tier-3",
        "blocking-controls": [],
        "blocking-reason": "score-floor"
      }
    },
    {
      "id": "with-fuzzing",
      "components": {
        "correctness": 0.85,
        "failure-handling": 0.8,
        "readability-structure": 0.8,
        "testability": 0.85,
        "operational-readiness": 0.7,
        "performance": 0.7,
        "security": 0.8
      },
      "gate": {
        "C1": true,
        "C2": true,
        "C3": true,
        "C4": true,
        "C5": false,
        "C6": false,
        "C7": true,
        "C8": true,
        "C9": false,
        "C10": false,
        "C11": true,
        "C12": true,
        "C13": true,
        "C14": false,
        "C15": false
      },
      "expected": {
        "status": "tier-assigned",
        "weighted-score": 0.8075,
        "score-derived-tier": "tier-3",
        "gate-derived-tier": "tier-3",
        "reported-tier": "tier-3",
        "blocking-tier": "tier-4",
        "blocking-controls": [
          "C5",
          "C6",
          "C9",
          "C10"
        ],
        "blocking-reason": "controls"
      }
    },
    {
      "id": "high-score-failing-safety-control",
      "components": {
        "correctness": 0.85,
        "failure-handling": 0.8,
        "readability-structure": 0.8,
        "testability": 0.85,
        "operational-readiness": 0.7,
        "performance": 0.7,
        "security": 0.8
      },
      "gate": {
        "C1": true,
        "C2": true,
        "C3": true,
        "C4": true,
        "C5": false,
        "C6": false,
        "C7": true,
        "C8": true,
        "C9": false,
        "C10": false,
        "C11": false,
        "C12": true,
        "C13": true,
        "C14": false,
        "C15": false
      },
      "expected": {
        "status": "tier-assigned",
        "weighted-score": 0.8075,
        "score-derived-tier": "tier-3",
        "gate-derived-tier": "tier-1",
        "reported-tier": "tier-1",
        "blocking-tier": "tier-2",
        "blocking-controls": [
          "C11"
        ],
        "blocking-reason": "controls"
      }
    },
    {
      "id": "unknown-evidence",
      "components": {
        "correctness": 0.85,
        "failure-handling": 0.8,
        "readability-structure": 0.8,
        "testability": 0.85,
        "operational-readiness": 0.7,
        "performance": 0.7,
        "security": 0.8
      },
      "gate": {
        "C1": true,
        "C2": true,
        "C3": true,
        "C4": true,
        "C5": false,
        "C6": false,
        "C7": true,
        "C8": true,
        "C9": false,
        "C10": false,
        "C11": true,
        "C12": true,
        "C13": null,
        "C14": false,
        "C15": false
      },
      "expected": {
        "status": "evidence-incomplete",
        "weighted-score": 0.8075,
        "score-derived-tier": "tier-3",
        "gate-derived-tier": null,
        "reported-tier": null,
        "blocking-tier": null,
        "blocking-controls": [
          "C13"
        ],
        "blocking-reason": "unknown-evidence"
      }
    }
  ]
}
```

Validated locally by `skills/_catalog/validate_decision_code_quality.py`.
