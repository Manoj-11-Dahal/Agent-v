# Fairness, Stakeholder Impact and Contestability — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## Equal false-positive rates are not the whole story
Consider two hypothetical groups of 100 cases each. Positive/negative outcomes and prediction thresholds are defined consistently for illustration.

| Group | True positive | False negative | False positive | True negative |
|---|---:|---:|---:|---:|
| A | 16 | 4 | 8 | 72 |
| B | 42 | 18 | 4 | 36 |

For A, the true-positive rate is 16/(16+4)=0.80, false-positive rate is 8/(8+72)=0.10, and positive predictive value is 16/(16+8)=2/3. For B, those values are 42/60=0.70, 4/40=0.10, and 42/46, about 0.9130.

The same false-positive rate coexists with different true-positive rates and predictive values. The observed outcome prevalence also differs: 0.20 versus 0.60. These invented counts demonstrate denominators, not statistical evidence about any real demographic group.

## Policy interpretation
If a false negative withholds an important opportunity, the difference in missed positive cases may matter. If a false positive triggers an intrusive review, its burden also matters. Group size, exposure, severity and recourse affect impact; one equal rate does not settle all those questions.

Investigate data comparability, label quality, selection, sampling uncertainty and access before changing thresholds. Do not assume the group itself causes the difference, infer sensitive membership for individuals, or automatically choose group-specific treatment from these numbers.

## Bounded next step
Have the appropriate owner and qualified reviewers identify the relevant protection and acceptable process. Consider better measurement, targeted process improvements that comply with applicable requirements, meaningful review, notice and correction. Preserve uncertainty and affected-party concerns. No real policy change or protected-trait inference is performed by the example.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "fairness",
  "groups": {
    "a": {
      "tp": 16,
      "fn": 4,
      "fp": 8,
      "tn": 72
    },
    "b": {
      "tp": 42,
      "fn": 18,
      "fp": 4,
      "tn": 36
    }
  },
  "expected": {
    "a": {
      "tpr": 0.8,
      "fpr": 0.1,
      "ppv": 0.6666666666666666,
      "prevalence": 0.2
    },
    "b": {
      "tpr": 0.7,
      "fpr": 0.1,
      "ppv": 0.9130434782608695,
      "prevalence": 0.6
    }
  }
}
```
