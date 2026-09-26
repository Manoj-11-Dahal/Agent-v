#!/usr/bin/env python3
"""Read a local JSON matrix and emit advisory scores. Stdlib only; no execution/network."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

MAX_INPUT_BYTES = 2_000_000
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_-]{0,63}$")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mapping(value, required, optional, where):
    require(isinstance(value, dict), f"{where}: expected an object")
    require(set(required) <= set(value), f"{where}: missing keys {sorted(set(required) - set(value))}")
    require(not (set(value) - set(required) - set(optional)), f"{where}: unknown keys {sorted(set(value) - set(required) - set(optional))}")
    return value


def text(value, where):
    require(isinstance(value, str) and bool(value.strip()), f"{where}: expected nonempty text")
    return value


def ident(value, where):
    text(value, where)
    require(bool(ID_PATTERN.fullmatch(value)), f"{where}: use a lowercase ID, at most 64 characters")
    return value


def unit(value, where):
    require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{where}: expected a number, not a boolean")
    try:
        value = float(value)
    except (OverflowError, ValueError):
        raise ValueError(f"{where}: number is not finite") from None
    require(math.isfinite(value) and 0 <= value <= 1, f"{where}: expected a finite number in [0, 1]")
    return value


def unique(items, where):
    ids = [item['id'] for item in items]
    require(len(set(ids)) == len(ids), f"{where}: duplicate IDs")


def parse(data):
    mapping(data, ['schemaVersion', 'title', 'criteria', 'gateDefinitions', 'options'], ['tieTolerance', 'sensitivityDelta'], 'root')
    require(type(data['schemaVersion']) is int and data['schemaVersion'] == 1, 'schemaVersion must be integer 1')
    text(data['title'], 'title')
    tolerance = unit(data.get('tieTolerance', 0.01), 'tieTolerance')
    delta = unit(data.get('sensitivityDelta', 0.10), 'sensitivityDelta')
    require(delta > 0, 'sensitivityDelta must be greater than zero')
    criteria, gates, options = data['criteria'], data['gateDefinitions'], data['options']
    require(isinstance(criteria, list) and 1 <= len(criteria) <= 50, 'criteria: expected 1 to 50 entries')
    require(isinstance(gates, list) and 1 <= len(gates) <= 50, 'gateDefinitions: expected 1 to 50 entries, including authority/scope as appropriate')
    require(isinstance(options, list) and 1 <= len(options) <= 200, 'options: expected 1 to 200 entries')
    for c in criteria:
        mapping(c, ['id', 'label', 'weight', 'anchors'], [], 'criterion')
        ident(c['id'], 'criterion.id'); text(c['label'], 'criterion.label')
        unit(c['weight'], 'criterion.weight')
        mapping(c['anchors'], ['low', 'high'], [], 'criterion.anchors')
        text(c['anchors']['low'], 'anchor.low'); text(c['anchors']['high'], 'anchor.high')
    unique(criteria, 'criteria')
    weights = {c['id']: float(c['weight']) for c in criteria}
    total = math.fsum(weights.values())
    require(total > 0, 'at least one criterion weight must be positive')
    weights = {key: value / total for key, value in weights.items()}
    for gate in gates:
        mapping(gate, ['id', 'description'], [], 'gate definition')
        ident(gate['id'], 'gate.id'); text(gate['description'], 'gate.description')
    unique(gates, 'gateDefinitions')
    gate_ids = {g['id'] for g in gates}; criterion_ids = set(weights)
    eligible, blocked = [], []
    for option in options:
        mapping(option, ['id', 'name', 'gates'], ['scores'], 'option')
        ident(option['id'], 'option.id'); text(option['name'], 'option.name')
        require(isinstance(option['gates'], dict) and set(option['gates']) == gate_ids, f"{option['id']}: gates must exactly match gateDefinitions")
        failed, unknown = [], []
        for gid, assertion in option['gates'].items():
            mapping(assertion, ['status'], ['evidence'], f'{option["id"]}.{gid}')
            status = assertion['status']
            require(isinstance(status, str) and status in ('pass', 'fail', 'unknown'), 'gate status must be pass, fail or unknown')
            if status == 'pass':
                text(assertion.get('evidence'), f'{option["id"]}.{gid}.evidence')
            elif assertion.get('evidence') is not None:
                text(assertion['evidence'], f'{option["id"]}.{gid}.evidence')
            if status == 'fail': failed.append(gid)
            if status == 'unknown': unknown.append(gid)
        scores = option.get('scores', {})
        require(isinstance(scores, dict) and not (set(scores) - criterion_ids), f"{option['id']}: invalid score keys")
        parsed_scores = {}
        for cid, estimate in scores.items():
            mapping(estimate, ['low', 'estimate', 'high', 'evidence'], [], f'{option["id"]}.{cid}')
            low = unit(estimate['low'], 'score.low'); mid = unit(estimate['estimate'], 'score.estimate'); high = unit(estimate['high'], 'score.high')
            require(low <= mid <= high, 'scores must satisfy low <= estimate <= high')
            text(estimate['evidence'], 'score.evidence')
            parsed_scores[cid] = {'low': low, 'estimate': mid, 'high': high, 'evidence': estimate['evidence']}
        if failed or unknown:
            blocked.append({'id': option['id'], 'name': option['name'], 'disposition': 'excluded' if failed else 'hold', 'failedGates': failed, 'unknownGates': unknown, 'gateAssertions': option['gates']})
        else:
            require(set(scores) == criterion_ids, f"{option['id']}: eligible options require every criterion score; missing is not zero")
            eligible.append({'id': option['id'], 'name': option['name'], 'scores': parsed_scores, 'gateAssertions': option['gates']})
    unique(options, 'options')
    return weights, eligible, blocked, tolerance, delta


def rank(options, weights):
    rows = []
    for option in options:
        sums = {field: math.fsum(weights[cid] * option['scores'][cid][field] for cid in weights) for field in ('low', 'estimate', 'high')}
        rows.append({'id': option['id'], 'name': option['name'], **sums,
                     'contributions': {cid: weights[cid] * option['scores'][cid]['estimate'] for cid in weights}})
    return sorted(rows, key=lambda row: (-row['estimate'], row['id']))


def leaders(rows, tolerance):
    if not rows:
        return []
    top = rows[0]['estimate']
    return sorted(row['id'] for row in rows if top - row['estimate'] <= tolerance + 1e-12)


def score(data):
    weights, options, blocked, tolerance, delta = parse(data)
    rows = rank(options, weights)
    top_ids = leaders(rows, tolerance)
    trials, skipped = [], []
    if len(rows) >= 2:
        for cid, old_weight in weights.items():
            for direction in (-1, 1):
                new_weight = max(0.0, min(1.0, old_weight + direction * delta))
                label = {'criterion': cid, 'direction': 'down' if direction < 0 else 'up'}
                other_total = math.fsum(w for key, w in weights.items() if key != cid)
                if new_weight == old_weight or other_total == 0:
                    skipped.append({**label, 'reason': 'No weight change, or no nonzero other weights to redistribute proportionally.'})
                    continue
                alternative = {key: (new_weight if key == cid else weight / other_total * (1 - new_weight)) for key, weight in weights.items()}
                trial_rows = rank(options, alternative)
                trials.append({**label, 'weights': alternative, 'pointLeadersWithinTolerance': leaders(trial_rows, tolerance),
                               'pointScores': {row['id']: row['estimate'] for row in trial_rows}})
    dominant = [row['id'] for row in rows if len(rows) >= 2 and all(row['id'] == other['id'] or row['low'] > other['high'] + tolerance for other in rows)]
    stable = all(trial['pointLeadersWithinTolerance'] == top_ids for trial in trials) if trials else None
    if not rows:
        status = 'no_eligible_options'
    elif len(rows) == 1:
        status = 'single_eligible_option'
    elif len(top_ids) > 1:
        status = 'near_tie_requires_judgment'
    elif dominant == top_ids and stable is True:
        status = 'leader_survives_provided_checks'
    else:
        status = 'uncertain_under_ranges_or_weights'
    return {
        'schemaVersion': 1, 'title': data['title'], 'advisoryOnly': True,
        'warning': 'Inputs and evidence assertions are not independently verified. No score grants approval or triggers execution. Intervals are supplied bounds, not confidence intervals.',
        'status': status, 'normalizedWeights': weights, 'tieTolerance': tolerance,
        'eligibleCount': len(rows), 'ranking': rows, 'ineligibleOptions': blocked,
        'pointLeadersWithinTolerance': top_ids, 'intervalDominantIds': dominant,
        'oneWayLeaderSetStable': stable, 'sensitivityDelta': delta,
        'sensitivityTrials': trials, 'sensitivitySkipped': skipped,
        'limitations': ['Weighted additive preferences can hide criterion interactions and depend on valid anchors.',
                       'Independent bounding-box intervals are conservative extrema, not a probability model.',
                       'One-way weight checks do not cover joint changes, all possible weights, or shifting evidence.',
                       'Human authority, actual feasibility and evidence relevance require separate verification.'],
    }


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'nonstandard JSON number: {value}')


def read_input(path):
    with Path(path).open('rb') as stream:
        raw = stream.read(MAX_INPUT_BYTES + 1)
    require(len(raw) <= MAX_INPUT_BYTES, f'input exceeds {MAX_INPUT_BYTES} bytes')
    data = json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicates, parse_constant=reject_constant)
    return data, hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Local UTF-8 JSON input; see ../examples/options.json')
    args = parser.parse_args()
    try:
        data, digest = read_input(args.input)
        result = score(data)
        result['inputSha256'] = digest
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError, RecursionError) as exc:
        print(f'Input error: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
