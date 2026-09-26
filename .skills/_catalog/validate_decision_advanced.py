#!/usr/bin/env python3
"""Validate advanced decision teaching fixtures. Not a production decision engine.
Stdlib only; reads local Markdown, executes no document code, writes no files.
"""
from pathlib import Path
import copy
import json
import math
import re
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'decision-making'
MODULES = {
    'causal-standardization': 'causal-inference',
    'forecasting': 'probabilistic-forecasting',
    'robust': 'robust-optimization',
    'pareto': 'pareto-frontiers',
    'sequential': 'sequential-experiments',
    'real-options': 'real-options',
    'group': 'group-deliberation',
    'negotiation': 'negotiation-design',
    'game': 'game-theory-and-incentives',
    'queue': 'systems-and-feedback',
    'fairness': 'fairness-and-stakeholders',
    'crisis': 'crisis-triage',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(x):
    require(type(x) in (int, float) and math.isfinite(x), 'Expected finite number, not boolean')
    return x


def probability(x):
    require(0 <= number(x) <= 1, 'Probability out of bounds')
    return x


def divide(n, d):
    require(d > 0, 'Undefined denominator')
    return n / d


def distribution(values):
    require(bool(values), 'Empty distribution')
    for v in values: probability(v)
    require(math.isclose(sum(values), 1, abs_tol=1e-12), 'Distribution must sum to one')
    return values


def unique_best(values, maximize=True):
    best = (max if maximize else min)(values.values())
    winners = [k for k, v in values.items() if math.isclose(v, best, abs_tol=1e-12)]
    require(len(winners) == 1, 'Fixture has no unique winner; do not break substantive ties by ID')
    return winners[0]


def calculate(d):
    method = d['method']
    if method == 'causal-standardization':
        weights = distribution(d['targetWeights']); result = {}
        for key, groups in d['groups'].items():
            require(len(groups) == len(weights), 'Group/weight length mismatch')
            for successes, total in groups:
                require(type(successes) is int and type(total) is int and 0 <= successes <= total and total > 0, 'Invalid counts')
            result['aggregate' + key.upper()] = sum(g[0] for g in groups) / sum(g[1] for g in groups)
            result['standardized' + key.upper()] = sum(w * s / n for w, (s, n) in zip(weights, groups))
        return result
    if method == 'forecasting':
        sens = probability(d['sensitivity']); fpr = probability(d['falsePositiveRate'])
        def update(p):
            probability(p)
            return divide(p * sens, p * sens + (1-p) * fpr)
        a, b = d['betaPrior']; s, f = d['eventCounts']
        require(number(a) > 0 and number(b) > 0 and type(s) is int and type(f) is int and s >= 0 and f >= 0, 'Invalid Beta update')
        return {'posterior': update(d['prior']), 'alternativePosterior': update(d['alternativePrior']), 'betaPosteriorMean': (a+s)/(a+b+s+f)}
    if method == 'robust':
        u = d['utilities']; p = distribution(d['probabilities']); q = distribution(d['alternativeProbabilities'])
        require(len(p) == len(q) and all(len(row) == len(p) for row in u.values()), 'Scenario lengths differ')
        for row in u.values():
            for v in row: number(v)
        best = [max(row[i] for row in u.values()) for i in range(len(p))]
        regret = {key: max(b-x for b, x in zip(best, row)) for key, row in u.items()}
        return {'worstRegret': regret, 'minimaxRegret': unique_best(regret, False), 'maximin': unique_best({k: min(v) for k, v in u.items()}), 'expectedUtilities': {k: sum(a*b for a,b in zip(row,p)) for k,row in u.items()}, 'alternativeUtilities': {k: sum(a*b for a,b in zip(row,q)) for k,row in u.items()}}
    if method == 'pareto':
        points = d['points']
        for row in points.values():
            require(len(row) == 2, 'Expected two minimized objectives')
            for x in row: number(x)
        def dominates(a, b): return all(x <= y for x,y in zip(a,b)) and any(x < y for x,y in zip(a,b))
        return {'frontier': sorted(k for k,v in points.items() if not any(j != k and dominates(w,v) for j,w in points.items())), 'costOnly': sorted(k for k,v in points.items() if v[1] <= d['costCeiling']), 'latencyOnly': sorted(k for k,v in points.items() if v[0] <= d['latencyCeiling']), 'both': sorted(k for k,v in points.items() if v[0] <= d['latencyCeiling'] and v[1] <= d['costCeiling'])}
    if method == 'sequential':
        p0, p1, alpha, beta = (probability(d[k]) for k in ('p0','p1','alpha','beta'))
        require(0 < p0 < p1 < 1 and alpha > 0 and beta > 0 and alpha+beta < 1, 'Invalid simple-hypothesis design')
        upper = math.log((1-beta)/alpha); lower = math.log(beta/(1-alpha)); logs=[]; crossings=[]
        for path in d['paths']:
            require(bool(path) and all(c in 'SF' for c in path), 'Invalid binary path')
            lr=0; first=None
            for i, outcome in enumerate(path,1):
                lr += math.log(p1/p0) if outcome == 'S' else math.log((1-p1)/(1-p0))
                if first is None and (lr >= upper or lr <= lower): first=i
            logs.append(lr); crossings.append(first)
        return {'upper':upper,'lower':lower,'finalLogLR':logs,'firstCrossing':crossings}
    if method == 'real-options':
        p = probability(d['probabilityGood']); sens=probability(d['sensitivity']); fpr=probability(d['falsePositiveRate'])
        good=number(d['goodPayoff']); bad=number(d['badPayoff']); cost=number(d['pilotCost']); require(cost>=0,'Negative pilot cost')
        positive=p*sens+(1-p)*fpr; pp=divide(p*sens,positive); pn=divide(p*(1-sens),1-positive)
        immediate=p*good+(1-p)*bad
        value=positive*max(0,pp*good+(1-pp)*bad)+(1-positive)*max(0,pn*good+(1-pn)*bad)-cost
        return {'immediate':immediate,'perfectSignalPolicy':p*max(0,good)+(1-p)*max(0,bad)-cost,'positiveProbability':positive,'posteriorPositive':pp,'posteriorNegative':pn,'imperfectSignalPolicy':value,'incrementalValue':value-max(0,immediate)}
    if method == 'group':
        ballots=d['ballots']; require(bool(ballots),'No ballots'); candidates=set(ballots[0]); plurality={k:0 for k in candidates}; borda=dict(plurality)
        for ballot in ballots:
            require(len(ballot)==len(candidates) and set(ballot)==candidates,'Incomplete or repeated ranking')
            plurality[ballot[0]]+=1
            for i,k in enumerate(ballot): borda[k]+=len(candidates)-1-i
        a=sum(b.index('a') < b.index('b') for b in ballots)
        return {'plurality':plurality,'borda':borda,'pluralityWinner':unique_best(plurality),'bordaWinner':unique_best(borda),'aVersusB':[a,len(ballots)-a]}
    if method == 'negotiation':
        b,s,p,v,c,q=(number(d[k]) for k in ('buyerMaximum','sellerMinimum','basePrice','addOnBuyerValue','addOnSellerCost','packagePrice'))
        return {'baseRange':b-s,'baseSurpluses':[b-p,p-s],'packageRange':b+v-s-c,'packageSurpluses':[b+v-q,q-s-c],'jointGain':v-c}
    if method == 'game':
        pay=d['payoffs']; cost=number(d['skipExpectedCost'])
        require(len(pay)==2 and all(len(row)==2 and all(len(x)==2 for x in row) for row in pay),'Expected 2x2 game')
        for row in pay:
            for cell in row:
                for x in cell:number(x)
        def equilibria(table):
            return [[i,j] for i in range(2) for j in range(2) if table[i][j][0]>=max(table[k][j][0] for k in range(2)) and table[i][j][1]>=max(table[i][k][1] for k in range(2))]
        revised=[[[pay[i][j][0]-(cost if i==1 else 0),pay[i][j][1]-(cost if j==1 else 0)] for j in range(2)] for i in range(2)]
        return {'baselinePureEquilibria':equilibria(pay),'revisedPureEquilibria':equilibria(revised)}
    if method == 'queue':
        mu=number(d['serviceRate']); require(mu>0,'Nonpositive service rate'); arrivals=d['arrivalRates']
        for v in arrivals: require(0<=number(v)<mu,'No stable finite M/M/1 mean at or above capacity')
        return {'utilization':[v/mu for v in arrivals],'systemMinutes':[60/(mu-v) for v in arrivals],'meanPopulation':[v/(mu-v) for v in arrivals]}
    if method == 'fairness':
        result={}
        for name,g in d['groups'].items():
            for n in g.values():require(type(n) is int and n>=0,'Invalid confusion counts')
            tp,fn,fp,tn=(g[k] for k in ('tp','fn','fp','tn'))
            result[name]={'tpr':divide(tp,tp+fn),'fpr':divide(fp,fp+tn),'ppv':divide(tp,tp+fp),'prevalence':divide(tp+fn,tp+fn+fp+tn)}
        return result
    if method == 'crisis':
        jobs=d['jobs'];times=[];late=[]
        for g in jobs.values(): require(number(g['duration'])>0 and number(g['deadline'])>=0,'Invalid job timing')
        for order in d['orders']:
            require(len(order)==len(jobs) and set(order)==set(jobs),'Order must include each task once')
            t=0;row={};miss=[]
            for key in order:
                t+=jobs[key]['duration'];row[key]=t
                if t>jobs[key]['deadline']:miss.append(key)
            times.append(row);late.append(miss)
        return {'latestStarts':{k:g['deadline']-g['duration'] for k,g in jobs.items()},'completionTimes':times,'lateJobs':late}
    raise ValueError('Unknown teaching method')


def fixture(method):
    path=ROOT/('decision-'+MODULES[method])/'references/worked-case.md'
    blocks=re.findall(r'```json\s*\n(.*?)\n```',path.read_text(),re.S)
    require(len(blocks)==1,'Expected one fixture per worked case')
    data=json.loads(blocks[0]);require(data['method']==method,'Wrong method fixture')
    return data


class AdvancedExamples(unittest.TestCase):
    def compare(self, actual, expected):
        if isinstance(expected,dict):
            self.assertEqual(set(actual),set(expected))
            for key in expected:self.compare(actual[key],expected[key])
        elif isinstance(expected,list):
            self.assertEqual(len(actual),len(expected))
            for a,b in zip(actual,expected):self.compare(a,b)
        elif type(expected) in (int,float):
            self.assertTrue(math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-10),(actual,expected))
        else:self.assertEqual(actual,expected)

    def test_reject_unstable_queue(self):
        d=fixture('queue')
        for arrival in [100,101,-1]:
            with self.subTest(arrival=arrival):
                d['arrivalRates']=[arrival]
                with self.assertRaises(ValueError):calculate(d)

    def test_reject_impossible_observed_signal(self):
        d=fixture('forecasting');d['sensitivity']=0;d['falsePositiveRate']=0
        with self.assertRaises(ValueError):calculate(d)

    def test_reject_invalid_probabilities(self):
        for bad in [True,-0.1,1.1,float('nan'),float('inf')]:
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):probability(bad)

    def test_reject_undefined_fairness_rate(self):
        d=fixture('fairness');d['groups']['a'].update(tp=0,fn=0)
        with self.assertRaises(ValueError):calculate(d)

    def test_reject_duplicate_ballot_choice(self):
        d=fixture('group');d['ballots'][1]=['a','a','b']
        with self.assertRaises(ValueError):calculate(d)

    def test_substantive_tie_not_broken_by_id(self):
        with self.assertRaises(ValueError):unique_best({'a':1,'b':1})

    def test_pareto_equal_vectors_do_not_dominate_each_other(self):
        d=fixture('pareto');d['points']={'a':[1,1],'b':[1,1]}
        self.assertEqual(calculate(d)['frontier'],['a','b'])

    def test_sequential_first_crossing_is_not_final_count(self):
        d=fixture('sequential');d['paths']=['FFFFSSFF']
        self.assertEqual(calculate(d)['firstCrossing'],[4])

    def test_calculations_do_not_mutate_fixtures(self):
        for method in MODULES:
            d=fixture(method);before=copy.deepcopy(d);calculate(d);self.assertEqual(d,before)


for method in MODULES:
    def make_test(key):
        def check(self):
            data=fixture(key);self.compare(calculate(data),data['expected'])
        return check
    setattr(AdvancedExamples,'test_fixture_'+method.replace('-','_'),make_test(method))

if __name__=='__main__':
    unittest.main(verbosity=2)
