# Causal Decision Analysis — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## Question and observed data
A team asks whether workflow A improves task success relative to B. Tasks differ in difficulty, and assignment was not randomized.

| Workflow | Easy successes / tasks | Hard successes / tasks | All successes / tasks |
|---|---:|---:|---:|
| A | 9 / 10 | 1 / 10 | 10 / 20 |
| B | 80 / 100 | 0 / 5 | 80 / 105 |

The aggregate success rates are 0.50 for A and about 0.7619 for B. A naive recommendation favors B. Within each recorded difficulty group, however, A has the higher observed rate: 0.90 versus 0.80 for easy tasks, and 0.10 versus 0 for hard tasks.

## Standardized comparison
For a hypothetical target population with equal numbers of easy and hard tasks, standardized observed rates are:
- A: 0.5×0.90 + 0.5×0.10 = 0.50.
- B: 0.5×0.80 + 0.5×0 = 0.40.

The direction reverses because B received a much easier task mix. This is a warning about aggregation, not proof that A causes better performance. The hard-task samples are especially small, and recorded difficulty may omit other confounders.

## What must be true for an intervention claim?
Difficulty must be measured comparably before assignment. Relevant common causes of assignment and success need adequate handling. Both workflows must be feasible for the target task types. Success definitions and observation periods must match. Consider whether worker experience, tools or customer selection also differ.

A graph might contain difficulty → workflow assignment, difficulty → success, and workflow → success. Add other causes before adjusting; do not declare this minimal graph complete simply because its calculations are convenient.

## Bounded next step
If permissible, design a randomized or otherwise credible comparison with assignment balanced by pre-treatment difficulty, enough observations, explicit failure tracking and a fixed outcome horizon. If only observational analysis is feasible, state the required assumptions and resulting uncertainty. Do not deploy A solely on the standardized point estimate or B solely on the aggregate rate.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "causal-standardization",
  "groups": {
    "a": [
      [
        9,
        10
      ],
      [
        1,
        10
      ]
    ],
    "b": [
      [
        80,
        100
      ],
      [
        0,
        5
      ]
    ]
  },
  "targetWeights": [
    0.5,
    0.5
  ],
  "expected": {
    "aggregateA": 0.5,
    "aggregateB": 0.7619047619047619,
    "standardizedA": 0.5,
    "standardizedB": 0.4
  }
}
```
