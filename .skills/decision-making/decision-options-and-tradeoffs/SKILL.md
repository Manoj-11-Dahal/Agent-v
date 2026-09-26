---
name: decision-options-and-tradeoffs
description: Generate meaningfully different alternatives, apply hard constraints before scoring, use
  anchored preference scales, and test whether rankings survive plausible changes. Supports transparent
  comparison without false precision or hidden value judgments.
author: Local custom (AI-assisted)
version: 1.0.0
source: Locally authored decision suite; official TypeSafe sources are linked where applicable.
compatibility: Documentation-first. The optional scoring helper uses Python standard library only. TypeSafe
  SDK/network access is not required.
tags:
- decision-suite
- decision-making
- tradeoffs
- weighted-scoring
- sensitivity
when-to-use:
- Generate meaningfully different alternatives, apply hard constraints before scoring, use anchored preference
  scales, and test whether rankings survive plausible changes. Supports transparent comparison without
  false precision or hidden value judgments.
metadata:
  role: specialized decision module
  scope: Authorized agent actions and strategic choices; no automatic permission or execution.
  related-skills:
  - decision-skills
---

# Decision Options and Trade-offs

## Generate useful alternatives
Include the status quo and an option that changes the mechanism, not just the vendor or label. Consider a smaller reversible commitment, staged rollout, or test if that changes the risk profile. Remove straw alternatives and describe each option at comparable detail. State what is actually feasible with current tools, skills, capacity and permissions.

## Gate before preference scoring
For each hard requirement, use pass, fail or unknown with evidence and an owner. Exclude known failures; hold unresolved mandatory requirements out of the eligible set. Never buy permission, legality, safety or a hard budget constraint with a higher score elsewhere. If all options are excluded, revise the frame or escalate rather than rank an inadmissible winner.

## Build an interpretable matrix
1. Use a few nonredundant criteria. If several criteria reflect the same benefit, combine them or explicitly address double counting.
2. Define fixed scoring anchors before seeing which option wins. Transform costs into preference scores consistently so all scores use the same higher-is-better direction. Avoid silently rescaling against whichever options happen to be in the table.
3. Obtain weights from the decision owner or label proposed weights as assumptions. Weights express trade-offs over the stated score ranges, not universal importance.
4. Attach evidence and uncertainty intervals to estimates. Missing information is not a score of zero; gather it, hold the comparison, or explicitly agree a conservative assumption.
5. Compute a weighted sum only when compensating trade-offs are acceptable and the chosen rubric is coherent. Present non-compensatory constraints separately.
6. Test plausible weight and score changes, ties, rank reversals, dominance and the strongest alternative. Consider option interaction and shared dependencies outside the arithmetic.

## Worked comparison
With delivery, reliability and affordability weights 0.30, 0.45 and 0.25, synthetic option A scores 0.80, 0.90 and 0.60, yielding 0.795. Option B scores 0.90, 0.65 and 0.90, yielding 0.7875. The gap is only 0.0075; that is a reason to examine sensitivity, not announce certainty. See the main guide's worked example for ranges and a blocked option.

## Deliverable
Show feasible options, gate exclusions, rubric anchors, weights and who supplied them, contributions to scores, sensitivity results, uncertainty, and the preferred next commitment. Explain when a qualitative trade-off discussion is more honest than another decimal place. The local scoring helper is optional and executes no recommended action.

## Working record

Use [the worksheet](templates/worksheet.md). Record assumptions and evidence explicitly; do not treat placeholders as completed work. Return to [the main Decision Skills guide](../decision-skills/SKILL.md) to choose the next bounded step. These instructions do not override the user, platform rules, or actual permissions. No remote service or action is started merely by reading them.
