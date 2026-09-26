# Multi-objective Decisions and Pareto Frontiers — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## Two minimized objectives
Consider four hypothetical system configurations. Latency and cost use fixed comparable measurement conditions and time horizons.

| Option | Latency units | Cost units |
|---|---:|---:|
| A | 10 | 90 |
| B | 15 | 70 |
| C | 20 | 100 |
| D | 10 | 110 |

A dominates C and D. B also dominates C. A and B do not dominate one another: A is faster, B is cheaper. The point-estimate Pareto frontier is {A,B}. This does not authorize either option or prove its estimates are reliable.

## Explicit preference elicitation
With a hard cost ceiling of 80, B is the only eligible frontier option. With only a latency ceiling of 12, A is the eligible frontier option. D also passes that latency limit, but remains dominated by A. If both ceilings are mandatory simultaneously, neither A nor B is feasible, and neither C nor D rescues feasibility. The correct result is an infeasible requirement set for these candidates—not a weighted compromise that violates one of the limits.

The owner can seek a new configuration, relax a preference if it truly is a preference, or change the objective/scope with authority. The analyst should not reinterpret a hard constraint just because the optimizer returned no winner.

## Uncertainty and omitted objectives
Suppose latency values are noisy or the cost estimates cover different workloads. Resolve comparability before pruning. If D provides a required capability absent from A, that capability belongs in the feasibility gate or objective set; A's apparent dominance no longer answers the actual decision. Equal latency does not mean equal privacy, reliability or maintainability.

## Bounded handoff
Present the A/B frontier and ask what latency improvement is worth in the same planning horizon. Record the owner's answer, its evidence and any affected-party objections. Use a small representative benchmark if the measurements could change the choice, keeping the original frontier and later revision separately recorded.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "pareto",
  "points": {
    "a": [
      10,
      90
    ],
    "b": [
      15,
      70
    ],
    "c": [
      20,
      100
    ],
    "d": [
      10,
      110
    ]
  },
  "costCeiling": 80,
  "latencyCeiling": 12,
  "expected": {
    "frontier": [
      "a",
      "b"
    ],
    "costOnly": [
      "b"
    ],
    "latencyOnly": [
      "a",
      "d"
    ],
    "both": []
  }
}
```
