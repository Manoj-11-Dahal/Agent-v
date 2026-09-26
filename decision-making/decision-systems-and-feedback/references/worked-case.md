# Systems Thinking and Feedback Decisions — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## Why a small load increase can matter
Assume a hypothetical M/M/1 queue with service capacity mu=100 tasks/hour. This means Poisson arrivals, exponential service times, one server and a stable steady state—strong assumptions to check in any real system.

| Arrival rate lambda | Utilization | Mean time in system | Mean population L |
|---|---:|---:|---:|
| 90/hour | 0.90 | 1/(100−90)=0.1 hour = 6 minutes | 90×0.1=9 |
| 95/hour | 0.95 | 0.2 hour = 12 minutes | 19 |
| 99/hour | 0.99 | 1 hour = 60 minutes | 99 |

Moving from 90 to 95 arrivals/hour raises arrival load by only about 5.6%, but doubles modeled mean time in the system. Near saturation, the relationship is nonlinear. These averages do not state a tail-latency guarantee.

## Invalid operating region
If lambda is at least mu, this queue model has no finite stable steady-state mean. Do not return zero or a negative time by blindly evaluating the expression. Transient backlog growth, admission policy and time-varying demand require different analysis.

## Decision alternatives
Adding more concurrent agent work can increase arrival rate without increasing the bottleneck's service capacity. Alternatives include reducing unnecessary arrivals, improving the constrained service stage, smoothing bursts, or adding genuinely usable capacity. Moving work into another queue can make one dashboard look better while leaving end-to-end delay unchanged.

## Bounded experiment
Measure arrivals, completed work, work-in-progress and end-to-end time over comparable windows. Distinguish service time from waiting, and check burstiness and repeated-task dependence. Pilot one change with resource limits and rollback, monitoring downstream queues and error rates. If observations depart from the assumptions, use a better-matched model rather than interpreting the toy calculation as measured reality.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "queue",
  "serviceRate": 100,
  "arrivalRates": [
    90,
    95,
    99
  ],
  "expected": {
    "utilization": [
      0.9,
      0.95,
      0.99
    ],
    "systemMinutes": [
      6,
      12,
      60
    ],
    "meanPopulation": [
      9,
      19,
      99
    ]
  }
}
```
