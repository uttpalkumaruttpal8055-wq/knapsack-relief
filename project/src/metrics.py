import numpy as np
from .problem import describe, brute_force, bits, WEIGHTS, CAPACITY

def distribution_metrics(probability, encoding):
    p = np.asarray(probability,dtype=float)
    n = int(np.log2(len(p)))
    marginal = p.reshape(-1,32).sum(axis=0)
    feasible = [i for i in range(32) if describe(i)['feasible']]
    best = max(feasible,key=lambda i:(marginal[i],describe(i)['value']))
    opt = brute_force()['optimal_value']
    exact = [i for i in feasible if describe(i)['value']==opt]
    valid = float(marginal[feasible].sum())
    result = dict(selected=describe(best), selected_index=best, selection_rule='most probable feasible item string',
        selected_value_pct_optimum=100*describe(best)['value']/opt,
        probability_valid=valid, probability_optimal=float(marginal[exact].sum()),
        expected_feasible_value_unconditional=float(sum(marginal[i]*describe(i)['value'] for i in feasible)),
        expected_feasible_value_conditional=float(sum(marginal[i]*describe(i)['value'] for i in feasible)/valid) if valid else 0,
        most_probable_raw_index=int(np.argmax(p)))
    if encoding == 'slack':
        result['probability_equality_valid'] = float(sum(p[i] for i in range(len(p))
            if bits(i,n)[:5]@WEIGHTS + bits(i,n)[5:]@np.array([1,2,4,8]) == CAPACITY))
    return result

def circuit_metrics(qc, swaps):
    return dict(depth=qc.depth(),cx_count=int(qc.count_ops().get('cx',0)),routing_swaps=swaps,
        physical_qubits=qc.num_qubits,total_gates=qc.size(),ops=dict(qc.count_ops()))
