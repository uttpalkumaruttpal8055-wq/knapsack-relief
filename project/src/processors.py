import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    config = json.loads((ROOT / 'processors' / f'processor_{name}.json').read_text())
    n = config['num_qubits']
    seen = {0}
    for _ in range(n):
        for a,b in config['coupling_map']:
            assert 0 <= a < n and 0 <= b < n and a != b
            if a in seen or b in seen:
                seen.update([a,b])
    assert len(seen) == n, 'Disconnected graph'
    return config

def noise_model(config):
    from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
    noise = NoiseModel()
    rates = config['noise']
    noise.add_all_qubit_quantum_error(depolarizing_error(rates['one_qubit'],1), ['rz','sx','x'])
    noise.add_all_qubit_quantum_error(depolarizing_error(rates['cx'],2), ['cx'])
    p = rates['readout']
    noise.add_all_qubit_readout_error(ReadoutError([[1-p,p],[p,1-p]]))
    return noise
