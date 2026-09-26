# Group Deliberation and Decision Governance — worked case

**Synthetic teaching example.** All values, parties, permissions and outcomes below are hypothetical. No real experiment, negotiation, incident response or deployment is performed.

## Five hypothetical participants
Suppose all three options pass the same mandatory gates. Three participants rank A > B > C; two rank B > C > A. These are illustrative preferences, not real votes or evidence of stakeholder consent.

Under plurality, A receives three first-choice votes and B receives two, so A wins. Under Borda scoring with 2 points for first, 1 for second and 0 for third:
- A receives 3×2 + 2×0 = 6.
- B receives 3×1 + 2×2 = 7.
- C receives 3×0 + 2×1 = 2.

B wins Borda even though A has a majority of first preferences. A also beats B in a direct pairwise comparison, 3 to 2. This demonstrates that methods embody different aggregation properties; it does not prove that Borda, plurality or majority comparison is always the right governance rule.

## Practical governance lesson
Choose the rule before collecting final rankings and explain what it is intended to capture. If an owner selects B after consultation, record an owner decision informed by the process—not “unanimous agreement.” If the rule requires approval from a data owner who did not participate, no vote establishes that approval.

## Group evidence versus social pressure
Request initial assessments before showing senior preferences where practical. Ask which evidence would change each view. Separate a disagreement about performance evidence from a disagreement about whose cost matters more. A quiet participant can hold decisive evidence; a confident majority can share the same mistaken source.

## Handoff
Record the actual participants and their roles, process chosen in advance, aggregation result, material objections, authorized owner's decision and review triggers. If stakeholder representation is incomplete, state that limitation. Do not fabricate signatures, votes or independent expert opinions to make a decision look more legitimate.

## Machine-checkable arithmetic fixture

This block is input to the local example validator, not a live API request or an executable action plan. Its expected values check the illustration only; they do not validate real-world assumptions.

```json
{
  "method": "group",
  "ballots": [
    [
      "a",
      "b",
      "c"
    ],
    [
      "a",
      "b",
      "c"
    ],
    [
      "a",
      "b",
      "c"
    ],
    [
      "b",
      "c",
      "a"
    ],
    [
      "b",
      "c",
      "a"
    ]
  ],
  "expected": {
    "plurality": {
      "a": 3,
      "b": 2,
      "c": 0
    },
    "borda": {
      "a": 6,
      "b": 7,
      "c": 2
    },
    "pluralityWinner": "a",
    "bordaWinner": "b",
    "aVersusB": [
      3,
      2
    ]
  }
}
```
