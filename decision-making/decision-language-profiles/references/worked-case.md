# Language profile selection — worked case

Four filters are run against the real 148-row profile table. The results below are the actual output of `scripts/select_profile.py`, not hand-written expectations.

## 1. Manual memory model with fuzzing tooling on a native target

```bash
python3 scripts/select_profile.py --require memory=manual --require fuzz-not=n/a --require platform=native
```

Result: **D** only — one candidate of 148. Twenty-five profiles record a manual memory model, but almost none of them also record fuzzing tooling and a native target. That is useful information: choosing a manual-memory language for tier-4 or tier-5 work usually means building the fuzzing tooling yourself.

## 2. Ownership-based memory with fuzzing and verification tooling

```bash
python3 scripts/select_profile.py --require memory=ownership --require fuzz-not=n/a --require verify-not=n/a
```

Result: **Rust** only. Note that the first filter did *not* return Rust: its memory model is recorded as `ownership-move-semantics`, not `manual`. Substring matching on `manual` therefore excludes it, which is exactly why the requirement should be stated as the property you need rather than as a familiar word.

## 3. Conflicting requirements

```bash
python3 scripts/select_profile.py --require memory-equals=gc --require memory=manual
```

Result: **infeasible**, 0 of 148. `memory-equals=gc` demands the field be exactly `gc`; `memory=manual` demands the same field contain `manual`. No row can do both. The correct response is to relax one requirement explicitly and record which, not to pick a language because the list came back empty.

## 4. Domain-narrowed choice

```bash
python3 scripts/select_profile.py --require memory-equals=gc --require platform=math
```

Result: **Maple**, **Mathematica**, **Wolfram Language**. The `notes` column flags licence cost and lock-in for all three, which is a genuine decision factor. If the work must ship inside existing infrastructure, none may be acceptable and the requirement set itself has to change.

## What the table cannot tell you

Whether a library exists for your problem, how the current language version behaves, what hiring looks like where you are, or whether your team can maintain the result. Those usually decide the outcome, and they belong in the decision record next to the filter output.

## Machine-checkable fixture

The numbers below are synthetic teaching data, not measured results from a real project.

```json
{
  "skill": "decision-language-profiles",
  "profile-table": "references/language-profiles.csv",
  "match-rule": "substring match per requirement; `-not` negates; `-equals` requires an exact field match; every requirement must hold; names sorted ascending",
  "cases": [
    {
      "id": "manual-fuzz-native",
      "requirements": {
        "memory": "manual",
        "fuzz-not": "n/a",
        "platform": "native"
      },
      "expected": {
        "status": "candidates",
        "matched": [
          "D"
        ],
        "profile-count": 148
      }
    },
    {
      "id": "ownership-fuzz-verify",
      "requirements": {
        "memory": "ownership",
        "fuzz-not": "n/a",
        "verify-not": "n/a"
      },
      "expected": {
        "status": "candidates",
        "matched": [
          "Rust"
        ],
        "profile-count": 148
      }
    },
    {
      "id": "conflicting-memory-models",
      "requirements": {
        "memory-equals": "gc",
        "memory": "manual"
      },
      "expected": {
        "status": "infeasible",
        "matched": [],
        "profile-count": 148
      }
    },
    {
      "id": "math-platform-with-gc",
      "requirements": {
        "memory-equals": "gc",
        "platform": "math"
      },
      "expected": {
        "status": "candidates",
        "matched": [
          "Maple",
          "Mathematica",
          "Wolfram Language"
        ],
        "profile-count": 148
      }
    }
  ]
}
```

Validated locally by `skills/_catalog/validate_decision_code_quality.py`.
