"""Exact p=1 statevector and Qiskit synthesis of the same cost unitary."""
import numpy as np
from .problem import energies, walsh

def probabilities(gamma, beta, encoding='hinge'):
    e = energies(encoding)
    n = int(np.log2(len(e)))
    state = np.exp(-1j * gamma * e) / np.sqrt(len(e))
    for i in range(n):
        h = 1 << i
        view = state.reshape(-1, 2*h)
        a, b = view[:, :h].copy(), view[:, h:].copy()
        view[:, :h] = np.cos(beta)*a - 1j*np.sin(beta)*b
        view[:, h:] = np.cos(beta)*b - 1j*np.sin(beta)*a
    return np.abs(state)**2

def optimize(encoding='hinge', seed=42, samples=2048):
    """Seeded multistart search followed by deterministic coordinate refinement."""
    rng = np.random.default_rng(seed)
    e = energies(encoding)
    candidates = []
    for g,b in rng.uniform([0,0],[2*np.pi,np.pi], size=(samples,2)):
        candidates.append((float(probabilities(g,b,encoding) @ e),float(g),float(b)))
    best = min(candidates)
    trace = [best[0]]
    for start in sorted(candidates)[:12]:
        loss,g,b = start
        step = 0.04
        for _ in range(28):
            options = [(float(probabilities(gg,bb,encoding) @ e),gg,bb)
                for gg,bb in [(g,b),(g+step,b),(g-step,b),(g,b+step),(g,b-step)]]
            new = min(options)
            if new[0] < loss:
                loss,g,b = new
            else:
                step *= 0.5
        if loss < best[0]:
            best = (loss,g,b)
        trace.append(best[0])
    return dict(expected_energy=best[0],gamma=best[1],beta=best[2],seed=seed,
                random_starts=samples,refinement_trace=trace)

def circuit(gamma, beta, encoding='hinge'):
    from qiskit import QuantumCircuit
    coefficients = walsh(energies(encoding))
    n = int(np.log2(len(coefficients)))
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for mask, coefficient in enumerate(coefficients):
        if mask == 0 or abs(coefficient) < 1e-10:
            continue  # identity adds only global phase
        support = [i for i in range(n) if mask & (1 << i)]
        target = support[-1]
        for control in support[:-1]:
            qc.cx(control, target)
        qc.rz(2*gamma*coefficient, target)
        for control in reversed(support[:-1]):
            qc.cx(control, target)
    qc.rx(2*beta, range(n))
    return qc
