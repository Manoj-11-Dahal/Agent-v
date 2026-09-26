---
name: decision-evidence-and-uncertainty
description: Build an evidence ledger, test source relevance and independence, express uncertainty honestly,
  and update beliefs without double-counting observations. Separates forecast probability, model confidence,
  assumption quality and permission.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- evidence
- uncertainty
- forecasting
when-to-use:
- Build an evidence ledger, test source relevance and independence, express uncertainty honestly, and
  update beliefs without double-counting observations. Separates forecast probability, model confidence,
  assumption quality and permission.
metadata:
  role: specialized decision module
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-skills
---

# Decision Evidence and Uncertainty

## Evidence ledger
For each decision-relevant claim, record the observation or quotation, source, date, method, scope, limitations, and consequence if wrong. Label it observed, reported, inferred, assumed, estimated or unknown. A source can be trustworthy yet irrelevant to the operating environment. A tool failure is not evidence that the underlying claim is false.

## Acquisition and challenge
1. Prioritize claims that could reverse the choice or invalidate a gate; do not gather background merely because it is available.
2. Prefer direct measurements when feasible. Record sample selection, missing data, environment and whether an outcome was actually measured or merely predicted.
3. Trace secondhand sources to their origin where material. Five summaries of one study are one evidence lineage, not five independent confirmations.
4. Seek a disconfirming observation and a plausible alternative explanation. Distinguish absence of evidence from evidence of absence; state detection limits.
5. Check freshness and distribution shift. Evidence from another team, workload or user population may require a transfer assumption rather than a direct inference.
6. Preserve contradictions until resolved. Do not average mutually incompatible measurements without understanding units, definitions and collection conditions.

## Quantify only what is defensible
A probability concerns a clearly defined event and time horizon. An interval may represent estimation uncertainty, plausible scenarios, or a statistical confidence interval; name which one it is. A score on a preference rubric is not a probability. Qualitative low/medium/high labels need explicit definitions if used consistently.

For a genuine binary hypothesis, odds updating can be written as posterior odds = prior odds × likelihood ratio. Use it only when the prior and likelihood estimates are defensible. Do not multiply correlated likelihood ratios or invent precise values to make an argument look scientific. Where probabilities are weak, carry a range or scenario analysis instead.

## Hypothetical update
A prior event probability of 0.20 has odds 0.25. An independent observation with an assumed likelihood ratio of 3 changes odds to 0.75, or probability about 0.429. This is arithmetic under stated assumptions, not a calibrated forecast. Reusing the same observation a second time would overstate the update.

## Output and stop rule
Return the critical-claim ledger, confidence limitations, contradictory evidence, bounded probability/range estimates where justified, and the smallest unresolved fact that might matter. Stop when additional evidence is unlikely to change the decision enough to justify its cost, or when the agreed analysis budget expires. Route unresolved mandatory conditions to review instead of declaring them passed.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. Return to [the main Decision Skills guide](../decision-skills/SKILL.md) to choose the next bounded step. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
