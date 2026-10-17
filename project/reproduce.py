"""Verify shipped evidence, or independently replay quantum experiments.

python reproduce.py                # raw-data/formulation checks
python reproduce.py --replay       # identical seed replay in separate directory
python reproduce.py --robustness   # additional simulator seeds; layout/angles fixed
"""
import argparse
import json
import hashlib
from pathlib import Path
import numpy as np
from src.problem import validate,energies
from src.qaoa import probabilities
from src.metrics import distribution_metrics
from run_experiment import benchmark,check_quantum_implementation,write_json

ROOT=Path(__file__).resolve().parent

def verify():
    checks=validate()
    rows=json.loads((ROOT/'results/tables/benchmark.json').read_text())
    reference=json.loads((ROOT/'results/tables/reference.json').read_text())
    for encoding,r in reference.items():
        a=r['angles']
        p=probabilities(a['gamma'],a['beta'],encoding)
        assert np.allclose(p,r['probabilities'],atol=1e-12)
        assert abs(p@energies(encoding)-a['expected_energy'])<1e-8
    for row in rows:
        name=f"counts_{row['processor']}_{row['encoding']}_{row['mode']}.json"
        counts=json.loads((ROOT/'results/tables'/name).read_text())
        assert sum(counts.values())==row['shots']
        p=np.zeros(1<<row['logical_qubits'])
        for key,count in counts.items():p[int(key.replace(' ',''),2)]=count/row['shots']
        metrics=distribution_metrics(p,row['encoding'])
        for key in ['probability_valid','probability_optimal','selected_value_pct_optimum']:
            assert abs(metrics[key]-row[key])<1e-12,(name,key)
        assert metrics['selected']==row['selected']
        assert abs(p@energies(row['encoding'])-row['expected_energy'])<1e-10
    checks.update(raw_count_tables_verified=len(rows),saved_angles_verified=2)
    manifest=ROOT/'results/tables/manifest.json'
    if manifest.exists():
        entries=json.loads(manifest.read_text())
        for relative,digest in entries.items():
            assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==digest,relative
        checks['sha256_files_verified']=len(entries)
    return checks

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    parser.add_argument('--robustness',action='store_true')
    args=parser.parse_args()
    checks=verify()
    if args.replay or args.robustness:
        check_quantum_implementation()
        reference=json.loads((ROOT/'results/tables/reference.json').read_text())
        seeds=[42] if args.replay else [7,123,2026]
        all_rows=[]
        for seed in seeds:
            directory=ROOT/'results'/('replay' if args.replay else 'robustness')/f'seed_{seed}'
            for name,encoding in [('A','hinge'),('B','hinge'),('B','slack')]:
                all_rows+=benchmark(name,encoding,reference[encoding]['angles'],4096,seed,directory)
        if args.replay:
            matched=[]
            for row in all_rows:
                name=f"counts_{row['processor']}_{row['encoding']}_{row['mode']}.json"
                shipped=json.loads((ROOT/'results/tables'/name).read_text())
                rerun=json.loads((ROOT/'results/replay/seed_42/tables'/name).read_text())
                matched.append(dict(file=name,exact_counts_match=shipped==rerun))
            checks['replay']=matched
            checks['all_counts_exactly_reproduced']=all(x['exact_counts_match'] for x in matched)
        else:
            summaries=[]
            for name,encoding in [('A','hinge'),('B','hinge'),('B','slack')]:
                selected=[r for r in all_rows if r['processor']==name and r['encoding']==encoding and r['mode']=='noisy']
                summaries.append(dict(processor=name,encoding=encoding,seeds=seeds,
                    mean_probability_optimal=float(np.mean([r['probability_optimal'] for r in selected])),
                    sample_std_probability_optimal=float(np.std([r['probability_optimal'] for r in selected],ddof=1)),
                    mean_probability_valid=float(np.mean([r['probability_valid'] for r in selected]))))
            write_json(ROOT/'results/tables/robustness_summary.json',dict(rows=all_rows,summary=summaries,
                scope='Simulator sampling/noise seeds only; transpiler seed and optimized angles fixed.'))
            checks['additional_simulator_seeds']=seeds
    filename='replay_verification.json' if args.replay else 'robustness_verification.json' if args.robustness else 'reproducibility_verification.json'
    write_json(ROOT/'results/tables'/filename,checks)
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
