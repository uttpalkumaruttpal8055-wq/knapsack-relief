"""Run: python run_experiment.py [--reference-only] [--processor A|B]."""
import argparse
import csv
import json
import sys
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
import numpy as np
from src.problem import brute_force, validate, energies, qubo, walsh
from src.qaoa import optimize, probabilities, circuit
from src.processors import load, noise_model
from src.routing import compile_circuit
from src.metrics import distribution_metrics, circuit_metrics
from src.visualization import topology, landscape, comparison

ROOT=Path(__file__).resolve().parent

def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2),encoding='utf-8')

def check_quantum_implementation():
    from qiskit.quantum_info import Statevector
    for encoding in ['hinge','slack']:
        for g,b in [(0,0),(.127,.39),(.93,.12)]:
            actual=Statevector.from_instruction(circuit(g,b,encoding)).probabilities()
            assert np.allclose(actual,probabilities(g,b,encoding),atol=1e-10),encoding

def benchmark(name,encoding,angles,shots,seed_simulator=42,output_dir=None):
    from qiskit_aer import AerSimulator
    from qiskit.quantum_info import Statevector
    config=load(name)
    destination=Path(output_dir) if output_dir else ROOT/'results'
    (destination/'tables').mkdir(parents=True,exist_ok=True)
    logical=circuit(angles['gamma'],angles['beta'],encoding)
    if logical.num_qubits>config['num_qubits']:
        raise ValueError('Full slack QUBO requires 9 logical qubits; cannot run on 5-qubit A.')
    measured=logical.copy()
    measured.measure_all()  # classical bits remain in logical order through routing
    compiled,swaps=compile_circuit(measured,config)
    edges={tuple(e) for e in config['coupling_map']}
    for instr in compiled.data:
        if instr.operation.name=='cx':
            a,b=[compiled.find_bit(q).index for q in instr.qubits]
            assert (a,b) in edges,'Illegal physical CX edge'
    assert set(compiled.count_ops()) <= set(config['basis_gates'])|{'measure','barrier'}
    # Exact ideal marginal in classical measurement order verifies routing/layout.
    unmeasured=compiled.remove_final_measurements(inplace=False)
    physical=Statevector.from_instruction(unmeasured).probabilities()
    destinations={compiled.find_bit(instr.clbits[0]).index:compiled.find_bit(instr.qubits[0]).index
        for instr in compiled.data if instr.operation.name=='measure'}
    marginal=np.zeros(1<<logical.num_qubits)
    for i,p in enumerate(physical):
        logical_index=sum(((i>>destinations[j])&1)<<j for j in destinations)
        marginal[logical_index]+=p
    assert np.allclose(marginal,probabilities(angles['gamma'],angles['beta'],encoding),atol=1e-8)
    (destination/'circuits').mkdir(exist_ok=True)
    (destination/'circuits'/f'{name}_{encoding}.txt').write_text(str(compiled.draw(output='text')),encoding='utf-8')
    rows=[]
    for noisy in [False,True]:
        sim=AerSimulator(method='statevector',noise_model=noise_model(config) if noisy else None,
            max_parallel_threads=2)
        counts=sim.run(compiled,shots=shots,seed_simulator=seed_simulator).result().get_counts()
        p=np.zeros(1<<logical.num_qubits)
        for key,count in counts.items():
            p[int(key.replace(' ',''),2)]=count/shots
        label='noisy' if noisy else 'ideal'
        write_json(destination/'tables'/f'counts_{name}_{encoding}_{label}.json',counts)
        row=dict(processor=name,encoding=encoding,mode=label,logical_qubits=logical.num_qubits,shots=shots,seed_simulator=seed_simulator,seed_transpiler=42,
            **circuit_metrics(compiled,swaps),**distribution_metrics(p,encoding))
        row['probability_valid_standard_error']=float(np.sqrt(row['probability_valid']*(1-row['probability_valid'])/shots))
        row['expected_energy']=float(p@energies(encoding))
        from src.problem import describe
        observed=[i for i in range(32) if p.reshape(-1,32).sum(axis=0)[i]>0 and describe(i)['feasible']]
        if observed:
            best_observed=max(observed,key=lambda i:describe(i)['value'])
            row['best_observed_feasible']=describe(best_observed)
            row['best_observed_value_pct_optimum']=100*describe(best_observed)['value']/brute_force()['optimal_value']
        rows.append(row)
        print(f"{name} {encoding} {label}: depth={row['depth']} CX={row['cx_count']} swaps={swaps} valid={row['probability_valid']:.4f}",flush=True)
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--reference-only',action='store_true')
    parser.add_argument('--processor',choices=['A','B'])
    parser.add_argument('--shots',type=int,default=4096)
    args=parser.parse_args()
    for folder in ['data/raw','data/processed','results/tables','results/figures']:
        (ROOT/folder).mkdir(parents=True,exist_ok=True)
    checks=validate()
    write_json(ROOT/'results/tables/validation.json',checks)
    write_json(ROOT/'results/tables/classical.json',brute_force())
    write_json(ROOT/'data/processed/qubo.json',qubo())
    reference={}
    for encoding in ['hinge','slack']:
        angles=optimize(encoding)
        p=probabilities(angles['gamma'],angles['beta'],encoding)
        reference[encoding]=dict(angles=angles,probabilities=p.tolist(),**distribution_metrics(p,encoding))
        print(f"Exact NumPy QAOA {encoding}: {reference[encoding]['selected']}; valid={reference[encoding]['probability_valid']:.4f}",flush=True)
    write_json(ROOT/'results/tables/reference.json',reference)
    for name in ['A','B']:
        topology(load(name),ROOT/f'results/figures/topology_{name}.svg')
    write_json(ROOT/'results/tables/landscape.json',landscape(ROOT/'results/figures/qaoa_landscape.svg'))
    if args.reference_only:
        print('Reference checks completed. Qiskit routing and noisy benchmarks NOT executed.',flush=True)
        return
    check_quantum_implementation()
    rows=[]
    for name in ([args.processor] if args.processor else ['A','B']):
        rows+=benchmark(name,'hinge',reference['hinge']['angles'],args.shots)
    if args.processor != 'A':
        rows+=benchmark('B','slack',reference['slack']['angles'],args.shots)
    write_json(ROOT/'results/tables/benchmark.json',rows)
    keys=['processor','encoding','mode','logical_qubits','physical_qubits','depth','cx_count','routing_swaps','shots',
          'probability_valid','probability_optimal','selected_value_pct_optimum','best_observed_value_pct_optimum','expected_energy']
    with (ROOT/'results/tables/benchmark.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    comparison([r for r in rows if r['mode']=='ideal'],ROOT/'results/figures/routing_comparison.svg')
    packages={}
    for package in ['qiskit','qiskit-aer','numpy','scipy','matplotlib','nbformat']:
        try:packages[package]=version(package)
        except PackageNotFoundError:pass
    write_json(ROOT/'results/tables/environment.json',dict(python=sys.version,packages=packages))
    (ROOT/'requirements-lock.txt').write_text('\n'.join(f'{k}=={v}' for k,v in packages.items())+'\n',encoding='utf-8')
    print('Qiskit statevector equivalence, routed equivalence, physical-edge checks and A/B benchmarks passed.',flush=True)

if __name__=='__main__':main()
