# Probabilistic Forecasting and Base Rates — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## A release-warning signal
Suppose 10% of comparable releases have a defined incident within seven days. A warning signal appears in 80% of incident releases and 10% of non-incident releases. Assume these rates apply to the present release; that assumption needs evidence in a real case.

For 1,000 hypothetical releases:
- 100 have incidents; 80 of these produce a warning.
- 900 have no incident; 90 of these also produce a warning.
- Among 170 warnings, 80 correspond to incidents.

Therefore P(incident | warning)=0.08/(0.08+0.09)=8/17, about 0.4706. The signal's 80% sensitivity does not mean an 80% incident probability after a warning. The prior odds are 1/9, the positive likelihood ratio is 8, and posterior odds are 8/9.

## Sensitivity and action
With a 2% base rate and the same signal characteristics, posterior probability becomes 0.016/(0.016+0.098), about 0.1404. Choosing an inappropriate reference class can materially change the forecast. Neither posterior value automatically justifies blocking or shipping: compare feasible investigation cost, delay, incident loss and existing release requirements.

A useful next action might be a bounded diagnostic check if it has enough information value. Do not count the same warning once as a tool report and again as an engineer's summary of that report.

## A separate conjugate-update illustration
For exchangeable binary observations, a Beta(2,8) prior has mean 0.20. Observing three events and one non-event gives Beta(5,9), mean 5/14 or about 0.3571. This separate illustration does not update the warning example: it has different data and assumptions. A posterior mean alone is not a credible interval or proof of calibration.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "forecasting",
  "prior": 0.1,
  "sensitivity": 0.8,
  "falsePositiveRate": 0.1,
  "alternativePrior": 0.02,
  "betaPrior": [
    2,
    8
  ],
  "eventCounts": [
    3,
    1
  ],
  "expected": {
    "posterior": 0.47058823529411764,
    "alternativePosterior": 0.14035087719298245,
    "betaPosteriorMean": 0.35714285714285715
  }
}
```
