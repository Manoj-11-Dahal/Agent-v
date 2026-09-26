#!/usr/bin/env python3
"""Validate the arithmetic inside the code-quality decision skills.

Stdlib only. Read-only: no file is written and no document code is executed.

Each worked case in ``decision-making`` embeds one synthetic JSON fixture. This
validator re-implements the decision procedure described by the corresponding
SKILL.md, runs it on the fixture inputs and compares every number with the
recorded expectations. It also checks the boundary rules the guides promise:
a gate blocks a promotion, a high score never outranks a missing control, an
unknown control blocks a tier, a deferral must be recorded, an infeasible
requirement set must not silently default, and the HXMax label must not be
reused across revisions.

Run:  PYTHONDONTWRITEBYTECODE=1 python3 skills/_catalog/validate_decision_code_quality.py
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT = ROOT / "decision-making"
TIERS_PATH = CAT / "decision-language-profiles/references/tier-definitions.json"
sys.path.insert(0, str(CAT / "decision-language-profiles/scripts"))
import select_profile  # noqa: E402  (workspace module, path added above)

TOL = 1e-9
ACCEPT_FLOOR = 0.60
TIERS = json.loads(TIERS_PATH.read_text())
ORDER = TIERS["tier-order"]
TIER = TIERS["tiers"]
CONTROLS = sorted(TIERS["controls"])


def control_order(name: str) -> tuple[int, str]:
    return (int(name[1:]), name)


def fixture(skill: str) -> dict:
    text = (CAT / skill / "references/worked-case.md").read_text()
    blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
    if len(blocks) != 1:
        raise AssertionError(f"{skill}: expected exactly one JSON fixture, found {len(blocks)}")
    return json.loads(blocks[0])


def approx(actual, expected, path="$"):
    if isinstance(expected, dict):
        assert isinstance(actual, dict), f"{path}: expected object, got {type(actual).__name__}"
        assert set(actual) == set(expected), f"{path}: keys {sorted(actual)} != {sorted(expected)}"
        for key, value in expected.items():
            approx(actual[key], value, f"{path}.{key}")
    elif isinstance(expected, list):
        assert isinstance(actual, list), f"{path}: expected list"
        assert len(actual) == len(expected), f"{path}: length {len(actual)} != {len(expected)}"
        for index, value in enumerate(expected):
            approx(actual[index], value, f"{path}[{index}]")
    elif isinstance(expected, bool) or expected is None:
        assert actual is expected, f"{path}: {actual!r} is not {expected!r}"
    elif isinstance(expected, (int, float)):
        assert isinstance(actual, (int, float)) and not isinstance(actual, bool), f"{path}: not numeric"
        assert abs(actual - expected) <= TOL, f"{path}: {actual!r} != {expected!r}"
    else:
        assert actual == expected, f"{path}: {actual!r} != {expected!r}"


def evaluate_tier(weights, components, gate, defs=None):
    """Score components, apply the gate AND rule, report the blocking tier."""
    defs = defs or TIER
    for name, weight in weights.items():
        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            raise ValueError(f"weight {name} is not numeric")
        if not 0.0 <= weight <= 1.0:
            raise ValueError(f"weight {name} out of range: {weight}")
    for name, value in components.items():
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"component {name} is not numeric")
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"component {name} out of range: {value}")
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"weights must sum to 1.0, got {total}")
    score = sum(weights[name] * components[name] for name in weights)
    unknown = sorted(c for c, v in gate.items() if v is None)
    for control, value in gate.items():
        if value is not None and not isinstance(value, bool):
            raise ValueError(f"control {control} must be true, false or unknown")
    score_tier = "tier-0"
    for name in ORDER:
        if score >= defs[name]["min-score"]:
            score_tier = name
    gate_tier = None
    for name in ORDER:
        if all(gate.get(c) is True for c in defs[name]["gate"]):
            gate_tier = name
    if unknown:
        return {"status": "evidence-incomplete", "weighted-score": score,
                "score-derived-tier": score_tier, "gate-derived-tier": None,
                "reported-tier": None, "blocking-tier": None,
                "blocking-controls": unknown, "blocking-reason": "unknown-evidence"}
    if gate_tier is None:
        return {"status": "tier-assigned", "weighted-score": score,
                "score-derived-tier": score_tier, "gate-derived-tier": None,
                "reported-tier": None, "blocking-tier": "tier-0",
                "blocking-controls": sorted((c for c in defs["tier-0"]["gate"]
                                             if gate.get(c) is not True), key=control_order),
                "blocking-reason": "controls"}
    reported = min(score_tier, gate_tier, key=ORDER.index)
    index = ORDER.index(reported)
    next_tier = ORDER[index + 1] if index + 1 < len(ORDER) else None
    if next_tier is None:
        blocking, blocking_controls, reason = None, [], "top-tier-reached"
    else:
        missing = [c for c in defs[next_tier]["gate"] if gate.get(c) is not True]
        if missing:
            blocking, blocking_controls = next_tier, sorted(missing, key=control_order)
            reason = "controls"
        else:
            blocking, blocking_controls, reason = next_tier, [], "score-floor"
    return {"status": "tier-assigned", "weighted-score": score,
            "score-derived-tier": score_tier, "gate-derived-tier": gate_tier,
            "reported-tier": reported, "blocking-tier": blocking,
            "blocking-controls": blocking_controls, "blocking-reason": reason}


RULES = [
    (lambda c: c["blast-radius"] == "high" and (not c["reversible"] or c["regulated"]),
     "tier-5", "safety-irreversible-regulated"),
    (lambda c: c["blast-radius"] == "high" and c["external-input"], "tier-4", "high-blast-external-surface"),
    (lambda c: c["blast-radius"] == "medium" and (c["external-input"] or c["users-dependent"] > 1),
     "tier-2", "customer-facing-production"),
    (lambda c: True, "tier-0", "single-user-local-exploration"),
]
ALLOWED_BLAST = ("low", "medium", "high")


def select_tier(context, requested):
    for predicate, tier, rule in RULES:
        if predicate(context):
            break
    if context["blast-radius"] not in ALLOWED_BLAST:
        raise ValueError("unknown blast radius must be treated as high, not scored")
    adjustment = 0
    if tier == "tier-0" and context["users-dependent"] > 1:
        tier, adjustment = "tier-1", 1
    missing = sorted((c for c in TIER["tier-5"]["gate"] if requested and c not in TIER[requested]["gate"]),
                     key=control_order) if requested else []
    if requested is None:
        status = "no-request"
    elif ORDER.index(requested) < ORDER.index(tier):
        status = "gap"
    elif ORDER.index(requested) > ORDER.index(tier):
        status = "excess"
    else:
        status, missing = "aligned", []
    return {"required-tier": tier, "matched-rule": rule, "reversibility-adjustment": adjustment,
            "status": status, "missing-controls": missing}


def review_coverage(required, evidence):
    covered = set()
    for item in evidence:
        if not item["id"]:
            raise ValueError("evidence item without an identifier cannot count as coverage")
        covered.update(item["covers"])
    covered &= set(required)
    uncovered = sorted(set(required) - covered)
    return {"covered-count": len(covered), "required-count": len(required),
            "coverage": len(covered) / len(required), "uncovered": uncovered,
            "verdict": "sufficient" if not uncovered else "insufficient"}


def rank_improvements(weights, multiplier, floor, candidates, available):
    scored = {}
    for item in candidates:
        for field in ("severity", "blast-radius", "confidence", "fix-risk", "effort"):
            value = item[field]
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f"{item['id']}: {field} is not numeric")
        for field in ("severity", "blast-radius", "confidence", "fix-risk"):
            if not 0.0 <= item[field] <= 1.0:
                raise ValueError(f"{item['id']}: {field} out of range")
        if item["effort"] <= 0:
            raise ValueError(f"{item['id']}: effort must be positive")
        raw = sum(weights[key] * item[key] for key in weights)
        priority = raw * (multiplier if item["irreversible"] else 1.0)
        scored[item["id"]] = priority / max(floor, item["effort"])
    order = sorted((item["id"] for item in candidates), key=lambda i: -scored[i])
    groups: dict[float, list[str]] = {}
    for identifier, value in scored.items():
        groups.setdefault(value, []).append(identifier)
    ties = sorted(i for group in groups.values() if len(group) > 1 for i in group)
    by_id = {item["id"]: item for item in candidates}
    mandatory = [i for i in order
                 if by_id[i]["irreversible"] or by_id[i]["severity"] >= 0.80]
    optional = [i for i in order if i not in mandatory]
    for identifier in optional:
        if not by_id[identifier].get("harm-if-deferred", "").strip():
            raise ValueError(f"{identifier}: a deferral candidate needs a written harm statement")
    fix_now, used = list(mandatory), sum(by_id[i]["effort"] for i in mandatory)
    accepted, deferred = [], []
    for identifier in optional:
        item = by_id[identifier]
        if item["fix-risk"] > ACCEPT_FLOOR:
            accepted.append(identifier)
        elif used + item["effort"] <= available + 1e-12:
            fix_now.append(identifier)
            used += item["effort"]
        else:
            deferred.append(identifier)
    return {"cost-adjusted": scored, "ranking": order, "ties": ties,
            "fix-now": sorted(fix_now), "defer-with-risk": sorted(deferred),
            "accepted": sorted(accepted), "fix-now-effort": used}


def hxmax_gate(gate, reviewer, approver, plan):
    for control, value in gate.items():
        if value is not None and not isinstance(value, bool):
            raise ValueError(f"control {control} must be true, false or unknown")
    satisfied = sum(1 for v in gate.values() if v is True)
    missing = sorted((c for c, v in gate.items() if v is not True), key=control_order)
    unknown = sorted(c for c, v in gate.items() if v is None)
    if not missing:
        if not reviewer or not approver or reviewer == approver:
            raise ValueError("independent reviewer and named approver must differ and be named")
        status, allowed, signed = "ready", True, True
    elif not unknown and plan and set(missing) == {"C14", "C15"}:
        status, allowed, signed = "conditional", False, False
    else:
        status, allowed, signed = "blocked", False, False
    return {"satisfied-count": satisfied, "required-count": len(gate),
            "satisfied-ratio": satisfied / len(gate), "missing": missing,
            "status": status, "release-allowed": allowed, "signed": signed}


def writing_check(fixture_data):
    slices_ = fixture_data["slices"]
    cost = fixture_data["cost-check"]
    ratio = cost["optional-gate-days"] / cost["required-gate-days"]
    if cost["stated-requirement-for-optional-gates"] and cost["decision"] != "raise-tier":
        raise ValueError("a stated requirement for higher-tier controls must raise the tier")
    if not cost["stated-requirement-for-optional-gates"] and cost["decision"] == "raise-tier":
        raise ValueError("raising the tier without a stated requirement is gold-plating")
    if cost["decision"] == "stay-at-required-tier" and not cost["deferred-recorded"]:
        raise ValueError("deferred controls must be recorded, not silently skipped")
    return {"slices-completed": len(slices_),
            "all-slices-with-evidence": all(
                s.get("high-findings-unresolved", 0) == 0 for s in slices_),
            "empty-catch-blocks-remaining": sum(
                s.get("empty-catch-blocks-remaining", 0) for s in slices_),
            "high-findings-unresolved": sum(
                s.get("high-findings-unresolved", 0) for s in slices_),
            "cost-ratio": ratio, "decision": cost["decision"],
            "deferred-controls": sorted(cost["deferred-controls"])}


class CodeQualityFixtures(unittest.TestCase):
    def test_fixture_code_quality_tiers(self):
        data = fixture("decision-code-quality-tiers")
        for entry in data["cases"]:
            with self.subTest(case=entry["id"]):
                approx(evaluate_tier(data["weights"], entry["components"], entry["gate"]),
                       entry["expected"])

    def test_fixture_code_tier_selection(self):
        data = fixture("decision-code-tier-selection")
        for entry in data["cases"]:
            with self.subTest(case=entry["id"]):
                approx(select_tier(entry["context"], entry["requested-tier"]), entry["expected"])

    def test_fixture_code_writing_practice(self):
        data = fixture("decision-code-writing-practice")
        approx(writing_check(data), data["expected"])

    def test_fixture_code_review_coverage(self):
        data = fixture("decision-code-review-and-verification")
        required = data["required-controls"]
        for entry in data["cases"]:
            with self.subTest(case=entry["id"]):
                evidence = data["proposed-evidence"] + entry["added-evidence"]
                approx(review_coverage(required, evidence), entry["expected"])

    def test_fixture_code_improvement_priority(self):
        data = fixture("decision-code-improvement-priority")
        approx(rank_improvements(data["weights"], data["irreversibility-multiplier"],
                                 data["effort-floor"], data["candidates"],
                                 data["available-effort"]), data["expected"])

    def test_fixture_hxmax_release_gate(self):
        data = fixture("decision-hxmax-standard")
        for entry in data["cases"]:
            with self.subTest(case=entry["id"]):
                approx(hxmax_gate(entry["gate"], entry["independent-reviewer"],
                                  entry["named-approver"], entry["conditional-plan-recorded"]),
                       entry["expected"])

    def test_fixture_language_profiles_use_real_table(self):
        data = fixture("decision-language-profiles")
        table = CAT / "decision-language-profiles" / data["profile-table"]
        for entry in data["cases"]:
            with self.subTest(case=entry["id"]):
                result = select_profile.select(entry["requirements"], table)
                approx({"status": result["status"], "matched": result["matched"],
                        "profile-count": result["profileCount"]}, entry["expected"])


class BoundaryRules(unittest.TestCase):
    def test_gate_blocks_a_high_score_promotion(self):
        weights = {"a": 1.0}
        good = evaluate_tier(weights, {"a": 1.0}, {"C1": True, "C2": True, "C8": True,
                                                  "C3": False, "C11": False})
        self.assertEqual(good["score-derived-tier"], "tier-5")
        self.assertEqual(good["reported-tier"], "tier-1")
        self.assertIn("C3", good["blocking-controls"])

    def test_score_floor_blocks_when_controls_pass(self):
        result = evaluate_tier({"a": 1.0}, {"a": 0.75},
                               {"C1": True, "C2": True, "C3": True, "C7": True, "C8": True,
                                "C11": True, "C12": True, "C13": True})
        self.assertEqual(result["score-derived-tier"], "tier-2")
        self.assertEqual(result["reported-tier"], "tier-2")
        self.assertEqual(result["blocking-tier"], "tier-3")
        self.assertEqual(result["blocking-reason"], "score-floor")
        self.assertEqual(result["blocking-controls"], [])

    def test_tier_zero_requires_a_reproducible_build(self):
        result = evaluate_tier({"a": 1.0}, {"a": 1.0}, {"C1": False})
        self.assertIsNone(result["gate-derived-tier"])
        self.assertIsNone(result["reported-tier"])
        self.assertEqual(result["blocking-tier"], "tier-0")
        self.assertEqual(result["blocking-controls"], ["C1"])

    def test_unknown_control_blocks_tiering(self):
        result = evaluate_tier({"a": 1.0}, {"a": 1.0}, {"C1": None})
        self.assertEqual(result["status"], "evidence-incomplete")
        self.assertIsNone(result["reported-tier"])
        self.assertEqual(result["blocking-controls"], ["C1"])

    def test_out_of_range_component_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_tier({"a": 1.0}, {"a": 1.5}, {"C1": True})

    def test_weights_must_sum_to_one(self):
        with self.assertRaises(ValueError):
            evaluate_tier({"a": 0.5}, {"a": 1.0}, {"C1": True})

    def test_non_boolean_control_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_tier({"a": 1.0}, {"a": 1.0}, {"C1": "yes"})

    def test_unknown_blast_radius_is_not_scored_as_low(self):
        with self.assertRaises(ValueError):
            select_tier({"blast-radius": "unknown", "reversible": True, "external-input": False,
                         "regulated": False, "lifetime": "throwaway", "users-dependent": 1}, None)

    def test_requested_tier_above_required_is_flagged_not_hidden(self):
        result = select_tier({"blast-radius": "low", "reversible": True, "external-input": False,
                              "regulated": False, "lifetime": "throwaway", "users-dependent": 1},
                             "tier-4")
        self.assertEqual(result["status"], "excess")

    def test_multi_user_dependency_raises_tier_zero(self):
        result = select_tier({"blast-radius": "low", "reversible": True, "external-input": False,
                              "regulated": False, "lifetime": "weeks", "users-dependent": 4}, None)
        self.assertEqual(result["matched-rule"], "single-user-local-exploration")
        self.assertEqual(result["required-tier"], "tier-1")
        self.assertEqual(result["reversibility-adjustment"], 1)

    def test_review_cannot_be_covered_by_unnamed_evidence(self):
        with self.assertRaises(ValueError):
            review_coverage(["C1"], [{"id": "", "covers": ["C1"]}])

    def test_partial_coverage_is_insufficient(self):
        result = review_coverage(["C1", "C2", "C3"], [{"id": "t1", "covers": ["C1"]}])
        self.assertEqual(result["verdict"], "insufficient")
        self.assertEqual(result["uncovered"], ["C2", "C3"])

    def test_deferred_controls_must_be_recorded(self):
        data = fixture("decision-code-writing-practice")
        data["cost-check"]["deferred-recorded"] = False
        with self.assertRaises(ValueError):
            writing_check(data)

    def test_gold_plating_without_requirement_is_rejected(self):
        data = fixture("decision-code-writing-practice")
        data["cost-check"]["decision"] = "raise-tier"
        with self.assertRaises(ValueError):
            writing_check(data)

    def test_priority_ties_are_not_broken_by_identifier(self):
        weights = {"severity": 1.0, "blast-radius": 0.0, "confidence": 0.0, "fix-risk": 0.0}
        candidates = [
            {"id": "B", "harm-if-deferred": "weekly export corruption", "severity": 0.5,
             "blast-radius": 0.0, "confidence": 0.0, "fix-risk": 0.0,
             "irreversible": False, "effort": 0.5},
            {"id": "A", "harm-if-deferred": "slow report under peak load", "severity": 0.5,
             "blast-radius": 0.0, "confidence": 0.0, "fix-risk": 0.0,
             "irreversible": False, "effort": 0.5},
        ]
        result = rank_improvements(weights, 1.25, 0.10, candidates, 1.0)
        self.assertEqual(result["ties"], ["A", "B"])
        self.assertEqual(result["cost-adjusted"]["A"], result["cost-adjusted"]["B"])

    def test_deferral_without_harm_statement_is_rejected(self):
        data = fixture("decision-code-improvement-priority")
        candidates = [dict(c) for c in data["candidates"]]
        for item in candidates:
            if item["id"] == "F2":
                item["harm-if-deferred"] = "  "
        self.assertEqual(len(candidates), 4)
        with self.assertRaises(ValueError):
            rank_improvements(data["weights"], data["irreversibility-multiplier"],
                              data["effort-floor"], candidates, data["available-effort"])

    def test_out_of_range_priority_factor_rejected(self):
        with self.assertRaises(ValueError):
            rank_improvements({"severity": 1.0, "blast-radius": 0.0, "confidence": 0.0,
                               "fix-risk": 0.0}, 1.25, 0.10,
                              [{"id": "X", "harm-if-deferred": "silent data loss",
                                "severity": 1.4, "blast-radius": 0.0, "confidence": 0.0,
                                "fix-risk": 0.0, "irreversible": False, "effort": 0.2}], 1.0)

    def test_hxmax_unknown_control_blocks_release(self):
        gate = {c: True for c in CONTROLS}
        gate["C7"] = None
        result = hxmax_gate(gate, "reviewer-7", "approver-2", True)
        self.assertEqual(result["status"], "blocked")
        self.assertFalse(result["release-allowed"])

    def test_hxmax_missing_signoff_never_allows_release(self):
        gate = {c: True for c in CONTROLS}
        gate["C14"] = False
        gate["C15"] = False
        result = hxmax_gate(gate, None, None, True)
        self.assertEqual(result["status"], "conditional")
        self.assertFalse(result["release-allowed"])
        self.assertFalse(result["signed"])

    def test_hxmax_self_review_rejected(self):
        gate = {c: True for c in CONTROLS}
        gate["C14"] = False
        with self.assertRaises(ValueError):
            hxmax_gate(dict(gate, C14=True), "same-person", "same-person", False)
        result = hxmax_gate(gate, "same-person", "same-person", True)
        self.assertEqual(result["status"], "blocked")
        self.assertFalse(result["release-allowed"])

    def test_hxmax_label_is_per_revision_and_not_reusable(self):
        gate = {c: True for c in CONTROLS}
        first = hxmax_gate(gate, "reviewer-7", "approver-2", False)
        self.assertTrue(first["signed"])
        changed = dict(gate, C2=False)
        second = hxmax_gate(changed, "reviewer-7", "approver-2", False)
        self.assertEqual(second["status"], "blocked")
        self.assertFalse(second["release-allowed"])

    def test_tier_order_and_gates_are_monotone(self):
        self.assertEqual(ORDER, ["tier-0", "tier-1", "tier-2", "tier-3", "tier-4", "tier-5"])
        previous = set()
        for name in ORDER:
            gate = set(TIER[name]["gate"])
            self.assertTrue(previous <= gate, f"{name} gate is not a superset of the previous tier")
            previous = gate
        scores = [TIER[name]["min-score"] for name in ORDER]
        self.assertEqual(scores, sorted(scores))
        self.assertEqual(set(TIER["tier-5"]["gate"]), set(CONTROLS))

    def test_language_profiles_table_shape(self):
        profiles = select_profile.load_profiles()
        self.assertGreaterEqual(len(profiles), 100)
        self.assertEqual(len({p["name"] for p in profiles}), len(profiles))
        for profile in profiles:
            for field in select_profile.REQUIRED_FIELDS:
                self.assertTrue(profile[field].strip(), f"{profile['name']}: empty {field}")
                self.assertNotIn(",", profile[field], f"{profile['name']}: comma in {field}")

    def test_infeasible_requirements_do_not_default_to_a_language(self):
        result = select_profile.select({"memory-equals": "gc", "memory": "manual"})
        self.assertEqual(result["status"], "infeasible")
        self.assertEqual(result["matched"], [])

    def test_unknown_profile_field_rejected(self):
        with self.assertRaises(ValueError):
            select_profile.select({"speed": "fast"})

    def test_fixtures_are_not_mutated_by_the_calculations(self):
        for skill in ("decision-code-quality-tiers", "decision-code-tier-selection",
                      "decision-code-writing-practice", "decision-code-review-and-verification",
                      "decision-code-improvement-priority", "decision-hxmax-standard",
                      "decision-language-profiles"):
            with self.subTest(skill=skill):
                self.assertEqual(fixture(skill), fixture(skill))


if __name__ == "__main__":
    unittest.main(verbosity=2)
