# Negotiation Design and Agreement Decisions — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## A price-only teaching model
Suppose a buyer's maximum acceptable total price is 120 utility-equivalent units and a seller's minimum is 90, after considering their respective alternatives. A price between 90 and 120 can create nonnegative modeled surplus for both. At price 105, the buyer's surplus is 15 and the seller's is 15.

These invented reservation values are not a method for discovering a real counterpart's private limit. The midpoint happens to split modeled surplus equally; it is not automatically fair or optimal.

## Expand the issue set
A service add-on costs the seller 5 units but creates 15 units of value for the buyer. With that add-on, the buyer's maximum becomes 135 and the seller's minimum becomes 95. The modeled bargaining range expands from 30 to 40 units.

At a total package price of 115, buyer surplus is 135−115=20 and seller surplus is 115−95=20. Each gains 5 relative to the earlier price-only example, while the seller's extra delivery cost is already included in the revised minimum. This is an illustration of joint value creation, not a recommendation to choose that price in a real negotiation.

## What could invalidate the package?
The buyer may not really value the add-on, its scope may be ambiguous, or the seller's actual support burden may exceed 5. Deadlines, warranties, data handling and exit rights can matter more than the arithmetic. If the add-on exposes sensitive data without permission, surplus cannot compensate for that hard failure.

## Authorized next step
Prepare a clear hypothetical package and questions to test the assumptions. Do not send it as a binding offer without the user's mandate. Before agreement, verify the exact deliverable, acceptance criteria, parties' authority, contingent terms and review requirements. Preserve a workable alternative if negotiation fails.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "negotiation",
  "buyerMaximum": 120,
  "sellerMinimum": 90,
  "basePrice": 105,
  "addOnBuyerValue": 15,
  "addOnSellerCost": 5,
  "packagePrice": 115,
  "expected": {
    "baseRange": 30,
    "baseSurpluses": [
      15,
      15
    ],
    "packageRange": 40,
    "packageSurpluses": [
      20,
      20
    ],
    "jointGain": 10
  }
}
```
