#!/usr/bin/env python3
"""Local regression tests. No services, SDKs or paid calls; temporary files are removed."""
import copy
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_options import score, read_input, MAX_INPUT_BYTES

BASE = Path(__file__).resolve().parents[1]
SCRIPT = BASE / 'scripts/score_options.py'
EXAMPLE = BASE / 'examples/options.json'


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(EXAMPLE.read_text())

    def reject(self):
        with self.assertRaises(ValueError):
            score(self.data)

    def test_worked_arithmetic(self):
        result = score(self.data)
        a, b = result['ranking']
        self.assertEqual([a['id'], b['id']], ['a', 'b'])
        for actual, expected in [(a['estimate'], .795), (b['estimate'], .7875), (a['low'], .695), (a['high'], .8725), (b['low'], .665), (b['high'], .8825)]:
            self.assertAlmostEqual(actual, expected)
        self.assertEqual(result['status'], 'near_tie_requires_judgment')
        self.assertEqual(result['pointLeadersWithinTolerance'], ['a', 'b'])
        self.assertEqual(result['intervalDominantIds'], [])
        self.assertIs(result['advisoryOnly'], True)

    def test_failed_gate_beats_perfect_scores(self):
        result = score(self.data)
        blocked = {row['id']: row for row in result['ineligibleOptions']}
        self.assertEqual(blocked['c']['disposition'], 'excluded')
        self.assertEqual(blocked['c']['failedGates'], ['privacy'])
        self.assertNotIn('c', [r['id'] for r in result['ranking']])

    def test_unknown_gate_is_held(self):
        blocked = {row['id']: row for row in score(self.data)['ineligibleOptions']}
        self.assertEqual(blocked['d']['disposition'], 'hold')
        self.assertEqual(blocked['d']['unknownGates'], ['authority'])

    def test_failed_and_unknown_both_reported(self):
        self.data['options'][2]['gates']['authority']['status'] = 'unknown'
        row = next(r for r in score(self.data)['ineligibleOptions'] if r['id'] == 'c')
        self.assertEqual(row['disposition'], 'excluded')
        self.assertEqual(row['unknownGates'], ['authority'])

    def test_no_eligible_options(self):
        self.data['options'] = self.data['options'][2:]
        result = score(self.data)
        self.assertEqual(result['status'], 'no_eligible_options')
        self.assertEqual(result['ranking'], [])
        self.assertIsNone(result['oneWayLeaderSetStable'])

    def test_one_eligible_is_not_dominant(self):
        self.data['options'] = [self.data['options'][0]]
        result = score(self.data)
        self.assertEqual(result['status'], 'single_eligible_option')
        self.assertEqual(result['intervalDominantIds'], [])

    def test_weight_renormalization(self):
        expected = score(self.data)['ranking']
        for c in self.data['criteria']: c['weight'] /= 2
        actual = score(self.data)['ranking']
        for a, b in zip(expected, actual): self.assertAlmostEqual(a['estimate'], b['estimate'])

    def test_weight_reversal(self):
        result = score(self.data)
        self.assertEqual(len(result['sensitivityTrials']), 6)
        self.assertFalse(result['oneWayLeaderSetStable'])
        trial = next(t for t in result['sensitivityTrials'] if t['criterion'] == 'reliability' and t['direction'] == 'down')
        self.assertEqual(trial['pointLeadersWithinTolerance'], ['b'])
        self.assertAlmostEqual(trial['pointScores']['a'], .7759090909090909)
        self.assertAlmostEqual(trial['pointScores']['b'], .8125)
        for trial in result['sensitivityTrials']:
            self.assertAlmostEqual(math.fsum(trial['weights'].values()), 1)
            self.assertTrue(all(0 <= v <= 1 for v in trial['weights'].values()))

    def test_exact_tie_has_no_hidden_tiebreak(self):
        self.data['options'][1]['scores'] = copy.deepcopy(self.data['options'][0]['scores'])
        self.data['tieTolerance'] = 0
        self.assertEqual(score(self.data)['pointLeadersWithinTolerance'], ['a', 'b'])

    def test_interval_dominance_and_stable_leader(self):
        for option, value in zip(self.data['options'][:2], [.9, .2]):
            for estimate in option['scores'].values():
                estimate.update(low=value, estimate=value, high=value)
        result = score(self.data)
        self.assertEqual(result['status'], 'leader_survives_provided_checks')
        self.assertEqual(result['intervalDominantIds'], ['a'])
        self.assertTrue(result['oneWayLeaderSetStable'])

    def test_unique_point_leader_can_remain_uncertain(self):
        self.data['tieTolerance'] = .001
        self.assertEqual(score(self.data)['status'], 'uncertain_under_ranges_or_weights')

    def test_zero_other_weights_skip_redistribution(self):
        for c in self.data['criteria']: c['weight'] = 1 if c['id'] == 'delivery' else 0
        result = score(self.data)
        self.assertTrue(result['sensitivitySkipped'])
        self.assertTrue(all(math.isfinite(row['estimate']) for row in result['ranking']))

    def test_reject_zero_weight_total(self):
        for c in self.data['criteria']: c['weight'] = 0
        self.reject()

    def test_reject_nonfinite_bool_or_out_of_range_numbers(self):
        for value in [float('nan'), float('inf'), -float('inf'), True, False, -0.1, 1.1, '0.5', None, 10**400]:
            with self.subTest(value=repr(value)):
                self.data['criteria'][0]['weight'] = value
                self.reject()

    def test_reject_reversed_bounds(self):
        self.data['options'][0]['scores']['delivery']['low'] = .95
        self.reject()

    def test_reject_missing_score(self):
        del self.data['options'][0]['scores']['delivery']
        self.reject()

    def test_reject_missing_pass_evidence(self):
        del self.data['options'][0]['gates']['authority']['evidence']
        self.reject()

    def test_reject_blank_score_evidence(self):
        self.data['options'][0]['scores']['delivery']['evidence'] = '  '
        self.reject()

    def test_reject_missing_gate(self):
        del self.data['options'][0]['gates']['authority']
        self.reject()

    def test_reject_unknown_gate_status(self):
        self.data['options'][0]['gates']['authority']['status'] = 'approved'
        self.reject()

    def test_reject_unknown_fields(self):
        self.data['tieTolerence'] = .01
        self.reject()

    def test_reject_duplicate_ids(self):
        for collection in ['criteria', 'gateDefinitions', 'options']:
            with self.subTest(collection=collection):
                self.setUp()
                self.data[collection][1]['id'] = self.data[collection][0]['id']
                self.reject()

    def test_reject_bad_shape_and_version(self):
        for field, value in [('schemaVersion', True), ('schemaVersion', 2), ('criteria', []), ('criteria', None), ('options', []), ('gateDefinitions', []), ('sensitivityDelta', 0)]:
            with self.subTest(field=field, value=value):
                self.setUp(); self.data[field] = value
                self.reject()

    def test_blocked_scores_still_validated(self):
        self.data['options'][2]['scores']['delivery']['estimate'] = 2
        self.reject()

    def test_input_not_mutated(self):
        before = copy.deepcopy(self.data)
        score(self.data)
        self.assertEqual(before, self.data)

    def test_deterministic_interval_properties(self):
        rng = random.Random(17)
        for _ in range(50):
            for c in self.data['criteria']: c['weight'] = rng.random()
            for option in self.data['options'][:2]:
                for estimate in option['scores'].values():
                    low, mid, high = sorted(rng.random() for _ in range(3))
                    estimate.update(low=low, estimate=mid, high=high)
            result = score(self.data)
            self.assertAlmostEqual(math.fsum(result['normalizedWeights'].values()), 1)
            for row in result['ranking']:
                self.assertTrue(0 <= row['low'] <= row['estimate'] <= row['high'] <= 1)
                self.assertAlmostEqual(row['estimate'], math.fsum(row['contributions'].values()))

    def test_strict_json_duplicate_keys_and_constants(self):
        with tempfile.TemporaryDirectory(prefix='decision-tests-') as tmp:
            path = Path(tmp) / 'input.json'
            for payload in ['{"a": 1, "a": 2}', '{"x": NaN}', '{"x": Infinity}', '{']:
                with self.subTest(payload=payload):
                    path.write_text(payload)
                    with self.assertRaises(ValueError): read_input(path)

    def test_input_size_cap(self):
        with tempfile.TemporaryDirectory(prefix='decision-tests-') as tmp:
            path = Path(tmp) / 'input.json'; path.write_bytes(b' ' * (MAX_INPUT_BYTES + 1))
            with self.assertRaises(ValueError): read_input(path)

    def test_cli_success_and_input_digest(self):
        completed = subprocess.run([sys.executable, str(SCRIPT), str(EXAMPLE)], capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result['eligibleCount'], 2)
        self.assertEqual(len(result['inputSha256']), 64)
        self.assertEqual(completed.stderr, '')

    def test_cli_error_is_not_false_success(self):
        with tempfile.TemporaryDirectory(prefix='decision-tests-') as tmp:
            path = Path(tmp) / 'invalid.json'; path.write_text('{"schemaVersion": 1}')
            completed = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 2)
            self.assertIn('Input error:', completed.stderr)
            self.assertNotIn('Traceback', completed.stderr)
            self.assertEqual(completed.stdout, '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
