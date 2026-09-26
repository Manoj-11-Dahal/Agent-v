# Decision Skills

**31 decision modules: 12 foundation skills, 12 advanced methods, and 7 code-quality decision skills covering basic, good, very good, excellent, advanced and HXMax code.**

Start with [Decision Skills — Main Guide](decision-skills/SKILL.md). This is a practical framework for improving decision quality, not a promise of infallibility or autonomous permission. Use a short check for routine reversible work and deeper analysis when stakes justify it.

## Foundation modules — original 12

| Skill | Purpose |
|---|---|
| [Decision Skills — Main Guide](decision-skills/SKILL.md) | Primary decision-making workflow for consequential agent actions and strategic choices. Frames goals, verifies evidence, gates inadmissible options, compares trade-offs, tests uncertainty, and records a bounded commitment with review triggers. Routes to specialized decision skills; TypeSafe is optional. |
| [Decision Framing and Goals](decision-framing-and-goals/SKILL.md) | Turn an ambiguous request into an owned, bounded decision with measurable outcomes, explicit constraints, a status-quo baseline and a proportional analysis plan. Avoids optimizing the wrong proxy or inventing stakeholder preferences. |
| [Decision Evidence and Uncertainty](decision-evidence-and-uncertainty/SKILL.md) | Build an evidence ledger, test source relevance and independence, express uncertainty honestly, and update beliefs without double-counting observations. Separates forecast probability, model confidence, assumption quality and permission. |
| [Decision Options and Trade-offs](decision-options-and-tradeoffs/SKILL.md) | Generate meaningfully different alternatives, apply hard constraints before scoring, use anchored preference scales, and test whether rankings survive plausible changes. Supports transparent comparison without false precision or hidden value judgments. |
| [Decision Risk and Reversibility](decision-risk-and-reversibility/SKILL.md) | Assess downside, exposure, recoverability and blast radius before consequential actions. Distinguishes hard safety boundaries from uncertain performance trade-offs and defines approval, containment and rollback conditions. |
| [Decision Value of Information](decision-value-of-information/SKILL.md) | Decide whether to act, ask a question, research, run a bounded experiment or defer. Estimates how new evidence could change the choice and compares that benefit with cost, delay and exposure. |
| [Decision Routing for Agent Actions](decision-agent-action-routing/SKILL.md) | Choose the next agent action from actual capabilities, task scope, evidence and risk. Routes among deterministic work, skill lookup, model assistance, clarification and review while enforcing budgets and guarding against untrusted instructions. |
| [Decision Resource and Priority Planning](decision-resource-and-priority/SKILL.md) | Allocate scarce time, compute, money and team capacity across candidate work while accounting for dependencies, marginal value, risk and uncertainty. Avoids false precision and score-only scheduling. |
| [Decision Scenarios and Premortem](decision-scenarios-and-premortem/SKILL.md) | Stress-test a proposed decision against plausible futures, dependency failures and second-order effects. Uses independent failure generation, mitigations and leading indicators rather than claiming that consensus proves robustness. |
| [Decision Commitment and Monitoring](decision-commit-and-monitor/SKILL.md) | Convert an approved choice into a bounded execution plan with scope, ownership, checkpoints, observable success, guardrails and rollback. Prevents recommendations from silently becoming permission or unbounded agent action. |
| [Decision Review and Calibration](decision-review-and-calibration/SKILL.md) | Evaluate decision process and forecast accuracy without confusing outcomes with reasoning quality. Supports probability calibration, decision journals and measured policy updates while avoiding hindsight bias and overfitting small samples. |
| [Optional TypeSafe Decision Judgments](decision-typesafe-judgments/SKILL.md) | Use TypeSafe as an optional source of typed semantic judgments inside a broader decision process. Maps Choice, Score and Noul to narrow questions while keeping eligibility, weights, approval, validation and execution in deterministic code. |

## Advanced methods — 12 new skills

Use the smallest method that answers the actual decision question. The original 12 skill packages remain unchanged. These additions extend them rather than replacing their authority, evidence and risk checks.

| Decision question | Advanced skill | Main output |
|---|---|---|
| Will changing X actually improve Y? | [Causal Decision Analysis](decision-causal-inference/SKILL.md) | Target effect, causal assumptions and defensible study design |
| How likely is a defined event by a deadline? | [Probabilistic Forecasting and Base Rates](decision-probabilistic-forecasting/SKILL.md) | Base rate, evidence update, sensitivity and resolution rules |
| Which option holds up when future probabilities are weak? | [Robust Decisions and Minimax Regret](decision-robust-optimization/SKILL.md) | Scenario payoffs, worst cases, regret and criterion comparison |
| How do we compare conflicting objectives without arbitrary weights? | [Multi-objective Decisions and Pareto Frontiers](decision-pareto-frontiers/SKILL.md) | Dominance witnesses, frontier and explicit trade-off boundaries |
| When should an experiment stop or continue? | [Sequential Experiments and Stopping Decisions](decision-sequential-experiments/SKILL.md) | Predeclared design, sequential boundaries and inconclusive outcomes |
| Should we commit now, pilot, wait or abandon? | [Real Options and Staged Commitments](decision-real-options/SKILL.md) | Decision tree, imperfect learning, staged value and expiry |
| How should several people reach a legitimate decision? | [Group Deliberation and Decision Governance](decision-group-deliberation/SKILL.md) | Decision rights, independent input, aggregation and recorded dissent |
| Which agreement is better than walking away? | [Negotiation Design and Agreement Decisions](decision-negotiation-design/SKILL.md) | BATNA, reservation limits, joint-value packages and approval checks |
| How will other actors adapt to this policy? | [Game Theory and Incentive-aware Decisions](decision-game-theory-and-incentives/SKILL.md) | Players, best responses, incentive changes and enforcement limits |
| What delayed or nonlinear effects might this change create? | [Systems Thinking and Feedback Decisions](decision-systems-and-feedback/SKILL.md) | Stock/flow map, feedback, queue bottlenecks and bounded control |
| Who bears errors and burdens, and how can they appeal? | [Fairness, Stakeholder Impact and Contestability](decision-fairness-and-stakeholders/SKILL.md) | Stakeholder impacts, subgroup denominators, protections and recourse |
| What is the safest authorized next step under time pressure? | [Time-critical Decision Triage and Incident Command](decision-crisis-triage/SKILL.md) | Containment, verified state, feasible sequence and escalation |

### What each advanced module contains

- A detailed playbook with scope, required inputs, ordered procedure, assumptions, interpretation limits and failure modes.
- A separate worked case with transparent calculations, counterexamples and a machine-checkable JSON fixture. All example numbers are synthetic.
- A method-specific worksheet covering inputs, evidence, calculations, decision rights, sensitivity, stop conditions and handoff.
- Links to the main guide and complementary decision modules.

### Suggested paths

- **Choose an intervention:** causal analysis → appropriate experiment design → original commitment/monitoring and review modules.
- **Commit under uncertainty:** event forecast → robust scenario comparison → staged commitment or information-gathering decision.
- **Resolve competing interests:** Pareto frontier → stakeholder impacts → group governance or negotiation.
- **Change a live workflow:** incentive analysis → systems feedback → bounded commitment; use crisis triage only when genuine urgency warrants it.

Do not run every module on every task. Do not mix preference scores, forecast probabilities, significance thresholds and model confidence as if they were interchangeable. A favorable calculation does not establish authorization, causal identification, fairness or operational readiness.

## Code quality modules — 7 new skills

Judge code, choose the bar it must meet, write to that bar, verify it, and order the fixes. All seven use one shared control set and tier ladder, so a judgement in one module is checkable in another.

| Decision question | Skill | Main output |
|---|---|---|
| Is this code basic, good, very good, excellent, advanced or HXMax grade? | [Code Quality Tiers](decision-code-quality-tiers/SKILL.md) | Weighted score, gate-derived tier, reported tier and blocking gap |
| What quality bar does this task actually require? | [Code Tier Selection](decision-code-tier-selection/SKILL.md) | Required tier, matched rule, gap/excess against the requested tier |
| How do I write it so it genuinely reaches that bar? | [Code Writing Practice](decision-code-writing-practice/SKILL.md) | Contract, reviewable slices, tier-appropriate tests, recorded evidence |
| Is the review or verification plan sufficient? | [Code Review and Verification](decision-code-review-and-verification/SKILL.md) | Evidence-to-control mapping, coverage ratio, uncovered controls |
| Which known problems should I fix now? | [Code Improvement Priority](decision-code-improvement-priority/SKILL.md) | Ranked plan split into fix-now, defer-with-risk and accept |
| Does this revision meet the top assurance bar? | [HXMax v1 Standard](decision-hxmax-standard/SKILL.md) | Fifteen-control gate reporting ready, conditional or blocked |
| Which implementation language fits these requirements? | [Language Profiles](decision-language-profiles/SKILL.md) | Candidates from a 148-language profile table, or an explicit infeasible verdict |

The tier ladder is: **tier-0 basic → tier-1 good → tier-2 very good → tier-3 excellent → tier-4 advanced → tier-5 HXMax**. HXMax is this library's own documented standard — not an industry certification and not a claim that code is defect-free. The shared control set and tier definitions live in [decision-language-profiles/references/tier-definitions.json](decision-language-profiles/references/tier-definitions.json).

```bash
python3 decision-language-profiles/scripts/select_profile.py --require memory=ownership --require fuzz-not=n/a --json
```

## Included resources

- A worksheet in every skill folder.
- A full decision-record JSON template in the main skill.
- An optional local scoring helper with hard-gate checks, score ranges and one-way weight sensitivity.
- Foundation worked examples and 12 additional detailed advanced cases, all synthetic.
- Local validation: 30 foundation scoring tests, 21 advanced arithmetic/edge-case tests and 33 code-quality tests. The validators check teaching fixtures and boundary rules; they are not production decision engines.
- Optional TypeSafe integration guidance; no SDK or paid inference is required.

## Quick lookup

```bash
python3 /home/user/skills/_catalog/find.py --category decision-making --limit 30
python3 /home/user/skills/_catalog/find.py --skill decision-skills --read SKILL.md
```

## Validate locally

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /home/user/skills/_catalog/validate_decision_advanced.py
PYTHONDONTWRITEBYTECODE=1 python3 /home/user/skills/_catalog/validate_decision_code_quality.py
PYTHONDONTWRITEBYTECODE=1 python3 /home/user/skills/decision-making/decision-skills/scripts/test_score_options.py
python3 /home/user/skills/_catalog/find.py --tag code-quality --limit 20
```

No network connection, API key or installed statistical package is needed for these checks. They validate the example arithmetic and boundary rules, not the truth of real-world assumptions. Last run: 30 foundation, 21 advanced and 33 code-quality tests passed; 158 relative links inside this category resolve. The `code-quality` tag returns 15 skills — the 7 decision modules here plus 8 pre-existing tool skills that already carried that tag.

## Operating rules

Preserve the user’s goals, privacy and authority. No score or confidence estimate grants permission. Unknown mandatory conditions remain unresolved; do not fabricate evidence or overstate precision. Record concise rationales and verifiable calculations, not private internal reasoning. No agent loop, background monitor, external action or live TypeSafe integration is activated by adding this suite.
