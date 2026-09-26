# Code quality tier selection — worked case

Three contexts are classified, one of them carrying a requested tier that is too low for its risk.

## 1. Local throwaway analysis script

Blast radius low (only the author), reversible, no external input, no regulation, throwaway lifetime. First matching rule: single-user local exploration → **tier-0 basic**. No requested tier, so status `no-request`.

## 2. Customer-facing service

Blast radius medium, reversible within one hour, externally reachable, unregulated, three-year lifetime. First matching rule: customer-facing production service → **tier-2 very good**. Reversibility within one hour does not lower the requirement below tier-2, because more than one person depends on the result.

## 3. Billing system with a requested tier that is too low

Blast radius high (customers are charged incorrectly), **irreversible** financial records, externally reachable, contractually regulated, five-year lifetime. First matching rule: safety-relevant / irreversible / regulated / third-party money → **tier-5 hxmax**. Requested tier was tier-3 excellent, so status is **`gap`** and the missing controls are C4, C5, C6, C9, C10, C14, C15. Reversibility is `false`, so no relaxation applies.

The gap matters more than the score: an excellent-tier billing system without independent sign-off (C14) and legal review (C15) cannot carry the obligation, however readable it is.

## What this does not decide

The rule set outputs a required floor. It does not authorize work, set a deadline, or override a named accountable human who records a different decision.

## Machine-checkable fixture

The numbers below are synthetic teaching data, not measured results from a real project.

```json
{
  "skill": "decision-code-tier-selection",
  "cases": [
    {
      "id": "local-throwaway",
      "context": {
        "blast-radius": "low",
        "reversible": true,
        "external-input": false,
        "regulated": false,
        "lifetime": "throwaway",
        "users-dependent": 1
      },
      "requested-tier": null,
      "expected": {
        "required-tier": "tier-0",
        "matched-rule": "single-user-local-exploration",
        "reversibility-adjustment": 0,
        "status": "no-request",
        "missing-controls": []
      }
    },
    {
      "id": "customer-service",
      "context": {
        "blast-radius": "medium",
        "reversible": true,
        "external-input": true,
        "regulated": false,
        "lifetime": "years",
        "users-dependent": 50000
      },
      "requested-tier": null,
      "expected": {
        "required-tier": "tier-2",
        "matched-rule": "customer-facing-production",
        "reversibility-adjustment": 0,
        "status": "no-request",
        "missing-controls": []
      }
    },
    {
      "id": "billing-gap",
      "context": {
        "blast-radius": "high",
        "reversible": false,
        "external-input": true,
        "regulated": true,
        "lifetime": "years",
        "users-dependent": 250000
      },
      "requested-tier": "tier-3",
      "expected": {
        "required-tier": "tier-5",
        "matched-rule": "safety-irreversible-regulated",
        "reversibility-adjustment": 0,
        "status": "gap",
        "missing-controls": [
          "C4",
          "C5",
          "C6",
          "C9",
          "C10",
          "C14",
          "C15"
        ]
      }
    }
  ]
}
```

Validated locally by `skills/_catalog/validate_decision_code_quality.py`.
