# HXMax release gate — worked case

Two revisions are evaluated: one blocked only by sign-off and legal review, one blocked by a missing safety control.

## Revision A — strong evidence, no sign-off yet

Satisfied: C1–C13. Missing: **C14** (no independent reviewer has verified the evidence yet) and **C15** (no legal/privacy/accessibility/safety review).

Satisfied count 13 ÷ 15 = 0.8666666666666667. Because the only missing controls are C14 and C15, and a written conditional-approval plan exists naming the reviewer and the review date, the gate reports **`conditional`** — release *planning* may proceed, release may not. The missing controls are `["C14", "C15"]`.

## Revision B — sign-off recorded, safety control missing

Satisfied: C1–C13 and C14. Missing: **C15**.

Satisfied count 14 ÷ 15 = 0.9333333333333333, which is higher than revision A. The gate still reports **`blocked`**, because the conditional path requires *both* C14 and C15 to be the only gaps — here C15 alone is missing and C15 is a lawful-to-ship control, so the plan must stop until the review is done.

Note the deliberate asymmetry: a higher satisfied ratio produced a stricter verdict. The gate is about *which* controls are missing, not how many.

## Revision C — a missing control recorded as unknown

If any control is `unknown`, the gate reports `blocked` and lists it. Recording an unverified control as satisfied would convert missing evidence into an approval, which is exactly what the gate exists to prevent.

## What the label means and does not mean

Revision A's `conditional` status does not mean the code is safe to ship; it means the evidence is complete enough to plan. Revision B's higher ratio does not make it closer to release. Neither revision is certified by any external body, and neither result predicts future failures.

## Machine-checkable fixture

The numbers below are synthetic teaching data, not measured results from a real project.

```json
{
  "skill": "decision-hxmax-standard",
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
  "cases": [
    {
      "id": "revision-a-no-signoff",
      "gate": {
        "C1": true,
        "C2": true,
        "C3": true,
        "C4": true,
        "C5": true,
        "C6": true,
        "C7": true,
        "C8": true,
        "C9": true,
        "C10": true,
        "C11": true,
        "C12": true,
        "C13": true,
        "C14": false,
        "C15": false
      },
      "independent-reviewer": null,
      "named-approver": null,
      "conditional-plan-recorded": true,
      "expected": {
        "satisfied-count": 13,
        "required-count": 15,
        "satisfied-ratio": 0.8666666666666667,
        "missing": [
          "C14",
          "C15"
        ],
        "status": "conditional",
        "release-allowed": false,
        "signed": false
      }
    },
    {
      "id": "revision-b-missing-c15",
      "gate": {
        "C1": true,
        "C2": true,
        "C3": true,
        "C4": true,
        "C5": true,
        "C6": true,
        "C7": true,
        "C8": true,
        "C9": true,
        "C10": true,
        "C11": true,
        "C12": true,
        "C13": true,
        "C14": true,
        "C15": false
      },
      "independent-reviewer": "reviewer-7",
      "named-approver": null,
      "conditional-plan-recorded": true,
      "expected": {
        "satisfied-count": 14,
        "required-count": 15,
        "satisfied-ratio": 0.9333333333333333,
        "missing": [
          "C15"
        ],
        "status": "blocked",
        "release-allowed": false,
        "signed": false
      }
    },
    {
      "id": "revision-c-unknown-control",
      "gate": {
        "C1": true,
        "C2": true,
        "C3": true,
        "C4": true,
        "C5": true,
        "C6": true,
        "C7": true,
        "C8": true,
        "C9": true,
        "C10": true,
        "C11": true,
        "C12": true,
        "C13": null,
        "C14": true,
        "C15": true
      },
      "independent-reviewer": "reviewer-7",
      "named-approver": "approver-2",
      "conditional-plan-recorded": true,
      "expected": {
        "satisfied-count": 14,
        "required-count": 15,
        "satisfied-ratio": 0.9333333333333333,
        "missing": [
          "C13"
        ],
        "status": "blocked",
        "release-allowed": false,
        "signed": false
      }
    },
    {
      "id": "revision-d-complete",
      "gate": {
        "C1": true,
        "C2": true,
        "C3": true,
        "C4": true,
        "C5": true,
        "C6": true,
        "C7": true,
        "C8": true,
        "C9": true,
        "C10": true,
        "C11": true,
        "C12": true,
        "C13": true,
        "C14": true,
        "C15": true
      },
      "independent-reviewer": "reviewer-7",
      "named-approver": "approver-2",
      "conditional-plan-recorded": false,
      "expected": {
        "satisfied-count": 15,
        "required-count": 15,
        "satisfied-ratio": 1.0,
        "missing": [],
        "status": "ready",
        "release-allowed": true,
        "signed": true
      }
    }
  ]
}
```

Validated locally by `skills/_catalog/validate_decision_code_quality.py`.
