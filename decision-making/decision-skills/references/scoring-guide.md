# Local scoring helper — input contract and limits

The Python helper is a deterministic, standard-library-only comparison aid. It reads one explicitly supplied local UTF-8 JSON file, prints JSON to stdout, and performs no network requests, installations, evidence retrieval or option execution. It does not automatically pick an action for the user. Successful parsing is not an endorsement of the input.

## Run and test

```bash
python3 /home/user/skills/decision-making/decision-skills/scripts/score_options.py /home/user/skills/decision-making/decision-skills/examples/options.json
PYTHONDONTWRITEBYTECODE=1 python3 /home/user/skills/decision-making/decision-skills/scripts/test_score_options.py
```

You may redirect stdout to your own result file. There is no output-writing or execution option in the helper. Exit code 0 means a valid comparison was produced, even when no option is eligible; inspect `status`. Invalid input or an unreadable file returns code 2 and a concise stderr error. The current implementation caps input at 2,000,000 bytes, 50 criteria, 50 mandatory gates and 200 options to bound local work.

## Input schema, version 1

The [synthetic example](../examples/options.json) is a complete input. Unknown object keys are rejected so misspelled fields cannot silently disappear. IDs must start with a lowercase letter, contain only lowercase letters, digits, `_` or `-`, and be at most 64 characters. IDs are unique within their respective lists.

| Root field | Contract |
|---|---|
| `schemaVersion` | Integer `1`, not boolean |
| `title` | Nonempty descriptive text |
| `criteria` | 1–50 entries: `id`, `label`, `weight`, `anchors` |
| `gateDefinitions` | 1–50 entries: `id`, `description`; include actual mandatory scope/authority requirements where applicable |
| `options` | 1–200 entries: `id`, `name`, `gates`, optional `scores` for blocked options |
| `tieTolerance` | Optional finite number in [0,1], default 0.01; absolute difference on the final preference scale |
| `sensitivityDelta` | Optional finite number in (0,1], default 0.10; absolute change to one normalized weight |

Each criterion weight is finite and in [0,1]; at least one is positive. Weights are normalized by their sum. Anchors are an object with nonempty `low` and `high` text describing preference scores 0 and 1. These are **higher-is-better preference values**, not probabilities. For costs or error rates, define and document a fixed cost-to-preference transformation before entering values; do not enter raw lower-is-better costs.

Each option must list **exactly all declared gates**, as objects with `status` equal to `pass`, `fail` or `unknown`, plus optional `evidence`. Every `pass` requires a nonempty evidence reference. A `fail` excludes the option, an `unknown` holds it; neither is ranked. A failure takes precedence in the disposition if another gate is unknown, but both are reported. The helper checks presence and syntax, not whether evidence exists or proves the assertion. Misstating approval can still produce an eligible row; independent review is essential.

Every eligible option needs all criterion scores. Each score contains finite `low`, `estimate`, `high` in [0,1], ordered low ≤ estimate ≤ high, and a nonempty `evidence` reference. Zero is a value, not a substitute for missing data. Blocked options may omit scores or provide a partial set; any supplied scores are still validated. Unknown score keys are rejected.

Malformed JSON, duplicate object keys, boolean numeric values, nonfinite values, reversed ranges, missing gates, duplicate IDs, unknown fields, zero total weight and missing eligible scores are errors. The journal template is intentionally a different schema and is not accepted as scoring input.

## Arithmetic and interpretation

For criterion weights w summing to 1 and preference scores s, the point estimate is the sum of w × s. Low/high output values use the supplied low/high endpoints with the same nonnegative weights. They are bounding-box extrema under the supplied ranges, **not statistical confidence intervals**. They do not encode correlations, scenario probabilities or the chance of winning.

`ranking` contains only eligible options, ordered by point estimate and then ID for deterministic display. ID ordering is not substantive preference. `pointLeadersWithinTolerance` includes all options within the declared absolute tolerance of the highest point estimate. The calculation allows a 1e-12 floating-point comparison margin. An option is interval-dominant only if its low bound exceeds every rival's high bound plus the tolerance, under the baseline weights; a lone eligible option is not labelled dominant.

One-way sensitivity changes each normalized weight up/down by the delta, clamped to [0,1], and proportionally rescales the other weights to keep their sum at 1. Scores remain at their point estimates. Trials with no change, or no nonzero other weights to redistribute, are skipped and reported. `oneWayLeaderSetStable` compares each trial's leader set within tolerance with the baseline set; it is null if no trial ran. Stability is not proof of robustness to joint changes, omitted alternatives or different evidence.

## Output statuses

- `no_eligible_options`: all options failed or have unresolved gates; revise the frame or obtain required evidence/authority.
- `single_eligible_option`: one option passed; this does not establish superiority to missing alternatives.
- `near_tie_requires_judgment`: several point estimates are within the input tolerance.
- `uncertain_under_ranges_or_weights`: no near tie, but the provided range/sensitivity checks do not support a stable, interval-separated leader.
- `leader_survives_provided_checks`: a unique leader remains interval-separated under baseline weights and its leader set survives the sampled one-way weight changes. This is a narrow arithmetic statement, **not approval or a calibrated confidence claim**.

Output includes normalized weights, score contributions, blocked-gate assertions, interval checks, sensitivity trials/skips, limitations and a SHA-256 of the exact CLI input bytes for reproducibility. It does not authenticate the decision owner or fetch evidence. Review the actual sources, interactions, unmodeled downside and stakeholder values before committing.

## Choosing the method

Use qualitative trade-offs when anchors or preference weights would be misleading. Use a richer scenario or utility model when nonlinear interactions, distributions, hard tail-risk limits or time-dependent effects matter. Do not extrapolate the helper into financial optimization, clinical recommendation, legal advice or autonomous action selection without the appropriate expertise and controls.
