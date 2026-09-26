# Time-critical Decision Triage and Incident Command — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## Two actions, one qualified operator
Assume two hypothetical authorized containment tasks are both available now. Durations are deterministic teaching values, tasks cannot be interrupted, and there is no setup time or dependency. Both deadlines refer to completion, not start.

| Task | Duration | Completion deadline | Latest nominal start |
|---|---:|---:|---:|
| A | 8 minutes | 12 minutes | 4 minutes |
| B | 2 minutes | 8 minutes | 6 minutes |

A least-slack-first intuition might choose A because its latest nominal start is earlier. But the sequence matters:
- A then B: A finishes at minute 8; B finishes at minute 10 and misses its minute-8 deadline.
- B then A: B finishes at minute 2; A finishes at minute 10; both meet their deadlines.

This small example shows why a local urgency heuristic is not a full feasible schedule. It does not prove earliest-deadline-first is always optimal under all resources, priorities, dependencies or uncertainty.

## Real incident boundary
Imminent severe harm, mandatory response duties or authority limits can override these scheduling preferences. If A cannot safely wait two minutes, that fact changes the feasible set. If duration estimates are uncertain, use buffers, parallel qualified capacity where permitted, or smaller containment steps rather than promising both deadlines will be met.

## Operational handoff
State the actual observations and authorized tasks, nominate one coordinator, reserve the needed operator, and verify each action's effect. Communicate the next checkpoint and contingency if a task runs long. Avoid executing both in parallel on shared mutable state merely because two agent tools are available.

The example performs no real incident response. After stabilization, compare estimated and observed durations and update future planning without concealing the uncertainty that existed at decision time.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "crisis",
  "jobs": {
    "a": {
      "duration": 8,
      "deadline": 12
    },
    "b": {
      "duration": 2,
      "deadline": 8
    }
  },
  "orders": [
    [
      "a",
      "b"
    ],
    [
      "b",
      "a"
    ]
  ],
  "expected": {
    "latestStarts": {
      "a": 4,
      "b": 6
    },
    "completionTimes": [
      {
        "a": 8,
        "b": 10
      },
      {
        "b": 2,
        "a": 10
      }
    ],
    "lateJobs": [
      [
        "b"
      ],
      []
    ]
  }
}
```
