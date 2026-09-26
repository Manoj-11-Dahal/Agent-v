# Real Options and Staged Commitments — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## Immediate commitment versus learning
A hypothetical project pays +80 utility units in a favorable state and -50 in an unfavorable state. These are net project payoffs. Assume state probabilities 0.4 and 0.6. Immediate expected utility is 0.4×80 + 0.6×(-50)=2. Doing nothing has utility 0.

A pilot costs 5 additional units and preserves the right to proceed or abandon. First consider an unrealistically perfect signal: proceed only in the favorable state. The staged policy has expected utility 0.4×80−5=27, an incremental gain of 25 over immediate commitment. This is an optimistic bound for that cost and model, not a claim that a pilot reveals the future perfectly.

## Use an imperfect signal
Assume the pilot is positive in 80% of favorable states and 10% of unfavorable states. P(positive)=0.4×0.8+0.6×0.1=0.38. After a positive, the favorable-state probability is 0.32/0.38, about 0.8421; proceeding has positive conditional utility. After a negative it is 0.08/0.62, about 0.1290; proceeding has negative conditional utility, so abandon.

The policy “pilot, proceed only if positive” has expected utility 0.4×0.8×80 + 0.6×0.1×(-50) − 5 = 17.6. Its modeled advantage over immediate commitment is 15.6. All probabilities and utility units are invented.

## What could reverse this choice?
If waiting loses the opportunity, the signal fails to transfer, the pilot itself causes exposure, or decision makers cannot actually abandon, the computed option value is overstated. Include those effects before claiming the staged policy is preferable. If a hard constraint blocks the eventual project, learning whether it would succeed does not make it admissible.

## Commitment boundary
Authorize only the agreed first stage, with a cost ceiling, evidence target, expiry and named review owner. Record the stop branch as a real option the owner will respect. Recheck authority before proceeding to a larger commitment; no calculation automatically exercises the option.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "real-options",
  "probabilityGood": 0.4,
  "goodPayoff": 80,
  "badPayoff": -50,
  "pilotCost": 5,
  "sensitivity": 0.8,
  "falsePositiveRate": 0.1,
  "expected": {
    "immediate": 2,
    "perfectSignalPolicy": 27,
    "positiveProbability": 0.38,
    "posteriorPositive": 0.8421052631578947,
    "posteriorNegative": 0.12903225806451613,
    "imperfectSignalPolicy": 17.6,
    "incrementalValue": 15.6
  }
}
```
