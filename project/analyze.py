"""Bonus analyses: penalty safety, topology resources and confidence intervals."""
import json,math,csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.problem import describe,brute_force
from src.processors import load
from run_experiment import write_json
ROOT=Path(__file__).resolve().parent

def wilson(p,n,z=1.96):
    denominator=1+z*z/n
    center=(p+z*z/(2*n))/denominator
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/denominator
    return [max(0,center-half),min(1,center+half)]

def main():
    optimum=brute_force()['optimal_value']
    sweep=[]
    for penalty in [0,.25,.5,1,1.1,1.5,2,4,8,35]:
        cost=[-describe(i)['value']+penalty*max(0,describe(i)['weight']-15)**2 for i in range(32)]
        ground=[i for i,e in enumerate(cost) if abs(e-min(cost))<1e-10]
        sweep.append(dict(penalty=penalty,ground_energy=min(cost),ground_item_sets=[describe(i) for i in ground],
            all_ground_states_valid_and_optimal=all(describe(i)['feasible'] and describe(i)['value']==optimum for i in ground)))
    threshold=max((describe(i)['value']-optimum)/(describe(i)['weight']-15)**2 for i in range(32) if not describe(i)['feasible'])
    write_json(ROOT/'results/tables/penalty_sweep.json',dict(strict_safety_threshold=threshold,selected_penalty=2,
        statement='For this instance P must be strictly greater than threshold to exclude infeasible ground-state ties.',rows=sweep))
    topology=[]
    for name in ['A','B']:
        cfg=load(name);n=cfg['num_qubits'];distance=np.full((n,n),np.inf);np.fill_diagonal(distance,0)
        degrees=[0]*n
        for a,b in cfg['undirected_edges']:distance[a,b]=distance[b,a]=1;degrees[a]+=1;degrees[b]+=1
        for k in range(n):distance=np.minimum(distance,distance[:,k,None]+distance[None,k,:])
        topology.append(dict(processor=name,qubits=n,links=len(cfg['undirected_edges']),maximum_degree=max(degrees),
            graph_density=2*len(cfg['undirected_edges'])/(n*(n-1)),diameter=int(distance.max()),
            average_shortest_path=float(distance[np.triu_indices(n,1)].mean())))
    write_json(ROOT/'results/tables/topology_analysis.json',topology)
    rows=json.loads((ROOT/'results/tables/benchmark.json').read_text())
    uncertainty=[]
    for r in rows:uncertainty.append(dict(processor=r['processor'],encoding=r['encoding'],mode=r['mode'],shots=r['shots'],
        valid_95pct_wilson=wilson(r['probability_valid'],r['shots']),optimal_95pct_wilson=wilson(r['probability_optimal'],r['shots'])))
    write_json(ROOT/'results/tables/confidence_intervals.json',uncertainty)
    fig,ax=plt.subplots(figsize=(8,4))
    ax.plot([r['penalty'] for r in sweep],[r['ground_energy'] for r in sweep],marker='o')
    ax.axvline(threshold,color='#bd5544',linestyle='--',label=f'Strict safety boundary P>{threshold:g}')
    ax.axvline(2,color='#2c8c7b',linestyle=':',label='Chosen P=2')
    ax.set(xlabel='Penalty strength',ylabel='Ground-state cost',title='Penalty safety: exact enumeration, not a QAOA performance sweep')
    ax.legend();fig.tight_layout()
    for ext in ['png','svg']:fig.savefig(ROOT/f'results/figures/penalty_safety.{ext}')
    plt.close(fig)
    print('Penalty, topology and 95% Wilson interval analyses saved. Strict penalty threshold:',threshold)

if __name__=='__main__':main()
