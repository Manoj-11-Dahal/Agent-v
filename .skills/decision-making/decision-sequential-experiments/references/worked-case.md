# Sequential Experiments and Stopping Decisions — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## A narrow binary illustration
Assume independently observed binary task outcomes, a simple null p0=0.50 and alternative p1=0.75. These are fixed teaching hypotheses, not inferred performance rates. Set alpha=0.05 and beta=0.10. The nominal upper log-likelihood boundary is log(18), about 2.8904; the lower is log(0.10/0.95), about -2.2513.

The log likelihood ratio after s successes and f failures is s×log(1.5)+f×log(0.5).

| Observed path summary | Log LR | Boundary decision under these assumptions |
|---|---:|---|
| 6 successes, 0 failures | 2.4328 | Continue, if within the predeclared resource limit |
| 8 successes, 0 failures | 3.2437 | Cross upper boundary, favor p1 over p0 |
| 2 successes, 5 failures | -2.6548 | Cross lower boundary, favor p0 over p1 |

The first two rows can describe one path of consecutive successes. The third is a separate path, starting with two successes followed by five failures; it is not a continuation after the upper boundary was already crossed. A real sequential test stops at its first crossing, so a final success/failure count alone cannot reconstruct whether an earlier crossing occurred.

## Interpretation boundaries
Favoring p1 over p0 does not estimate a universal success probability, prove an effect caused by a treatment, or authorize production deployment. If the real success rate lies between the simple hypotheses, the model and decision interpretation require care. If outcomes are correlated or selected, the assumed likelihood is wrong.

## Inconclusive and safety outcomes
Set a maximum observation budget in advance. If the boundary has not been crossed by that limit, report the design's inconclusive/budget-stop disposition rather than inventing a win. Stop for serious safety or privacy issues under the applicable response plan, independently of the likelihood ratio. A real test needs assignment, measurement, error handling and approved exposure controls beyond this arithmetic.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "sequential",
  "p0": 0.5,
  "p1": 0.75,
  "alpha": 0.05,
  "beta": 0.1,
  "paths": [
    "SSSSSS",
    "SSSSSSSS",
    "SSFFFFF"
  ],
  "expected": {
    "upper": 2.8903717578961645,
    "lower": -2.2512917986064953,
    "finalLogLR": [
      2.4327906486489863,
      3.243720864865315,
      -2.654805686583398
    ],
    "firstCrossing": [
      null,
      8,
      7
    ]
  }
}
```
