# Robust Decisions and Minimax Regret — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## Three possible strategies
All actions below are hypothetically feasible. Payoffs are invented comparable utility units, not money or calibrated expected business outcomes.

| Action | Favorable | Central | Adverse | Minimum payoff |
|---|---:|---:|---:|---:|
| A: aggressive commitment | 100 | 20 | -60 | -60 |
| B: balanced commitment | 60 | 45 | 10 | 10 |
| C: conservative commitment | 35 | 35 | 30 | 30 |

The best payoff in each state is 100, 45 and 30. Regret is the gap from that state's best feasible action.

| Action | Favorable regret | Central regret | Adverse regret | Maximum regret |
|---|---:|---:|---:|---:|
| A | 0 | 25 | 90 | 90 |
| B | 40 | 0 | 20 | 40 |
| C | 65 | 10 | 0 | 65 |

Minimax regret selects B; maximin selects C. Neither criterion is universally correct. An owner who prioritizes a modeled utility floor may prefer C, while one focused on limiting foregone value may prefer B.

## Add hypothetical probabilities cautiously
With state probabilities 0.5, 0.3 and 0.2, expected utilities are A=44, B=45.5, C=34. With probabilities 0.7, 0.2 and 0.1, they become A=68, B=52, C=34.5. Expected-utility preference changes because the assumed state likelihoods change; the payoff table alone cannot settle those likelihoods.

## Review before acting
Challenge the -60 adverse outcome and whether it is acceptable at all. If it violates a hard loss boundary, A may be inadmissible regardless of favorable-state upside. Consider a pilot that preserves some upside while reducing exposure, but add its actual costs and feasible triggers before ranking it. Do not claim B is optimal outside this specified scenario set.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "robust",
  "utilities": {
    "a": [
      100,
      20,
      -60
    ],
    "b": [
      60,
      45,
      10
    ],
    "c": [
      35,
      35,
      30
    ]
  },
  "probabilities": [
    0.5,
    0.3,
    0.2
  ],
  "alternativeProbabilities": [
    0.7,
    0.2,
    0.1
  ],
  "expected": {
    "worstRegret": {
      "a": 90,
      "b": 40,
      "c": 65
    },
    "minimaxRegret": "b",
    "maximin": "c",
    "expectedUtilities": {
      "a": 44,
      "b": 45.5,
      "c": 34
    },
    "alternativeUtilities": {
      "a": 68,
      "b": 52,
      "c": 34.5
    }
  }
}
```
