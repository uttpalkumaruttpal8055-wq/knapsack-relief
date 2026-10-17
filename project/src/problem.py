"""Exact inequality encoding and genuine slack-variable QUBO.

Little endian: bit i selects item i; reported item numbers are one-based.
"""
import itertools
import numpy as np

VALUES = np.array([10, 4, 7, 5, 8], dtype=int)
WEIGHTS = np.array([5, 3, 4, 2, 6], dtype=int)
CAPACITY = 15
PENALTY = 2  # Instance-specific; exhaustive checks below prove optimum preservation.

def bits(index, n):
    return np.array([(index >> i) & 1 for i in range(n)], dtype=int)

def describe(index):
    x = bits(index, 5)
    return dict(items=[i + 1 for i in range(5) if x[i]], weight=int(x @ WEIGHTS),
                value=int(x @ VALUES), feasible=bool(x @ WEIGHTS <= CAPACITY))

def brute_force():
    rows = [dict(index=i, **describe(i)) for i in range(32)]
    best = max(r['value'] for r in rows if r['feasible'])
    return dict(optimal_value=best, solutions=[r for r in rows if r['feasible'] and r['value'] == best], rows=rows)

def energies(encoding='hinge'):
    n = 5 if encoding == 'hinge' else 9
    result = []
    for i in range(1 << n):
        x = bits(i, n)
        weight = int(x[:5] @ WEIGHTS)
        violation = max(0, weight - CAPACITY) if encoding == 'hinge' else weight + int(x[5:] @ np.array([1, 2, 4, 8])) - CAPACITY
        result.append(-int(x[:5] @ VALUES) + PENALTY * violation ** 2)
    return np.array(result, dtype=float)

def walsh(values):
    a = np.asarray(values, dtype=float).copy()
    h = 1
    while h < len(a):
        view = a.reshape(-1, 2 * h)
        left, right = view[:, :h].copy(), view[:, h:].copy()
        view[:, :h], view[:, h:] = left + right, left - right
        h *= 2
    return a / len(a)

def qubo():
    """E = constant + sum linear[i]*x_i + sum quadratic[i,j]*x_i*x_j."""
    a = np.concatenate([WEIGHTS, [1, 2, 4, 8]])
    v = np.concatenate([VALUES, [0, 0, 0, 0]])
    return dict(constant=PENALTY * CAPACITY ** 2,
        linear=(PENALTY * (a*a - 2*CAPACITY*a) - v).tolist(),
        quadratic={f'{i},{j}': int(2*PENALTY*a[i]*a[j]) for i,j in itertools.combinations(range(9),2)})

def validate():
    q = qubo()
    for i, expected in enumerate(energies('slack')):
        x = bits(i, 9)
        actual = q['constant'] + np.dot(q['linear'], x)
        actual += sum(c*x[int(k.split(',')[0])]*x[int(k.split(',')[1])] for k,c in q['quadratic'].items())
        assert actual == expected
    reduced = energies('slack').reshape(16, 32).min(axis=0)
    assert np.array_equal(reduced, energies('hinge'))
    assert brute_force()['optimal_value'] == 26
    ground = np.where(energies('hinge') == energies('hinge').min())[0]
    assert all(describe(int(i))['feasible'] and describe(int(i))['value']==26 for i in ground)
    assert all(e > -26 for i,e in enumerate(energies('hinge')) if not describe(i)['feasible'])
    return {'qubo_states_verified':512, 'slack_reduction_states_verified':32, 'optimal_value':26}
