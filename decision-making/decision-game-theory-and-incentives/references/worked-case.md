# Game Theory and Incentive-aware Decisions — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## A two-team coordination problem
Two hypothetical teams can verify a release handoff or skip verification. Entries are (row-team payoff, column-team payoff), in invented cardinal utility units.

| Row / column | Verify | Skip |
|---|---|---|
| Verify | (3,3) | (0,5) |
| Skip | (5,0) | (1,1) |

For either team, skipping yields more utility regardless of the other's action: 5 instead of 3 against Verify, and 1 instead of 0 against Skip. Skip is strictly dominant in this simplified one-shot game. The pure-strategy equilibrium is (Skip,Skip), despite (Verify,Verify) giving both a higher payoff.

## An illustrative incentive change
Suppose a legitimate, authorized mechanism creates an expected additional cost of 2.5 utility units for choosing Skip, without changing other payoffs. This might represent a modeled operational cost; it is not a proposal to impose unapproved penalties on people.

Against Verify, Skip now gives 2.5 while Verify gives 3. Against Skip, Skip gives -1.5 while Verify gives 0. Verify becomes strictly dominant, and (Verify,Verify) is the pure-strategy equilibrium under the revised assumptions.

If a nominal cost of 5 occurs only with probability 0.5, its expected value is 2.5 in a risk-neutral model. Real enforcement errors, distributional harm, hidden actions or risk preferences can invalidate that shortcut. The hypothetical mechanism is not necessarily the best design; making verification cheaper or automatically checking prerequisites may be better and less punitive.

## Test the real mechanism
Observe whether actors can actually choose the modeled actions, whether verification has the assumed cost, and whether metrics reward real quality rather than appearances. Review privacy and fairness before collecting behavioral data. If a control is unenforceable, easily gamed or unauthorized, do not count its theoretical effect as achieved.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "game",
  "payoffs": [
    [
      [
        3,
        3
      ],
      [
        0,
        5
      ]
    ],
    [
      [
        5,
        0
      ],
      [
        1,
        1
      ]
    ]
  ],
  "skipExpectedCost": 2.5,
  "expected": {
    "baselinePureEquilibria": [
      [
        1,
        1
      ]
    ],
    "revisedPureEquilibria": [
      [
        0,
        0
      ]
    ]
  }
}
```
