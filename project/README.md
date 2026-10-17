# Knapsack Relief — PS-O3 Quantum Optimization

Qiskit Fall Fest 2026 Phase 1 submission: five-item 0/1 knapsack, QAOA p=1, classical verification, participant-designed Processor A/B, and ideal/noisy routing benchmarks.

**Additional disaster-management website:** https://knapsack-relief.onrender.com/auth

The website is a separate classical planning demonstration. The Python experiments here implement QAOA on local quantum simulators. No quantum hardware execution or quantum speedup is claimed.

## Run

Use Python 3.12 or newer. Tested versions are recorded in `requirements-lock.txt` and `results/tables/environment.json`.

```powershell
py -m pip install -r requirements-lock.txt
py run_experiment.py
```

Alternatively, open `main.ipynb` in Jupyter or Google Colab and run every cell from the repository root. Install requirements in the notebook environment first. No IBM API key is required. `processor_A.py` and `processor_B.py` are convenience wrappers; running both individually overwrites the combined table, so use `run_experiment.py` for the complete submission.

If Qiskit is unavailable, `py run_experiment.py --reference-only` verifies the formulation and exact NumPy QAOA statevector. That command does **not** produce new Qiskit routing/noise results.

## Problem and exact baseline

Values `[10,4,7,5,8]`, weights `[5,3,4,2,6]`, capacity 15. Enumerate all 32 choices. The unique classical optimum selects one-based items **1,2,3,4**, total weight **14**, total value **26**.

The disaster-relief interpretation is choosing indivisible supply bundles under a vehicle payload limit. Values are illustrative utility scores, not measured lives saved; the official benchmark data is unchanged.

## Two explicitly distinguished encodings

1. **True QUBO, 9 logical qubits:** five item bits and four slack bits, `s=y0+2*y1+4*y2+8*y3`. Minimize `-sum(v_i*x_i)+2*(sum(w_i*x_i)+s-15)^2`. Expansion is quadratic; all 512 assignments are checked. Run on B. **This encoding exceeds A's five-qubit capacity.** No items are deleted to force it onto A.
2. **Five-qubit comparison:** eliminate slack by exact minimization to obtain `-sum(v_i*x_i)+2*max(0,sum(w_i*x_i)-15)^2`. This is a **higher-order diagonal Hamiltonian, not a five-variable QUBO**. Its complete Walsh/Pauli-Z expansion implements the exact cost unitary. Run the identical circuit and angles on A and B to isolate routing effects.

Penalty 2 is validated for this particular instance: every infeasible item's penalized cost is strictly above the optimum -26. It is not a safe universal penalty for arbitrary future datasets. This capacity/encoding distinction is a limitation judges should assess against the PS-O3 requirements.

## Processor designs and execution

- A: five-qubit chain, four bidirectional physical links, maximum degree 2.
- B: nine-qubit perimeter ring with four central links, twelve bidirectional physical links, maximum degree 4. Additional links and degree have physical engineering costs.
- Both: basis `rz,sx,x,cx`; one-qubit depolarizing 0.001, CX depolarizing 0.005, symmetric readout error 0.01.
- SABRE layout/routing, optimization level 1, transpiler seed 42, 4096 shots, simulator seed 42.
- Seeded 2048-start angle search and local coordinate refinement minimize exact expected cost. The same hinge angles are reused on A/B; noisy runs are not separately tuned.

All experiments are local simulations. Synthetic noise does not include idle-time relaxation, correlated faults or hardware calibration. See `report.md` for measured results and limitations.

## Evidence and verification

### Added reproducibility and analysis tools

```powershell
py reproduce.py
py reproduce.py --replay
py reproduce.py --robustness
py analyze.py
```

`reproduce.py` recomputes exported metrics from raw counts and verifies saved angles, exact QUBO energies and the SHA-256 manifest. `--replay` reruns all six experiments with seed 42 in a separate directory: the shipped replay matched all six raw-count tables exactly in the tested environment. Across library versions and platforms, exact random samples may change; preserve the lockfile and compare distributions if necessary.

`--robustness` adds simulator seeds 7, 123 and 2026 with unchanged optimized angles and layout seed. Results are exported separately and do not overwrite baseline evidence. This assesses sampling/noise variation, not optimizer or compiler robustness.

`analyze.py` exports 95% Wilson intervals, graph density/degree/diameter and an exact penalty-safety sweep. For this fixed instance, penalty must be strictly greater than 1 to exclude infeasible ground-state ties; selected P=2 satisfies this. The sweep is not a quantum accuracy sweep.

The additional website's **Qiskit results** panel displays this fixed measured evidence, supports encoding/noise filters, CSV/evidence downloads, and a local five-item/penalty explorer. Website controls do not execute Qiskit or change the submitted experiment data. The separate website update ZIP must be uploaded and the existing Render service redeployed before the hosted panel appears.

- `results/tables/classical.json`: all 32 classical choices.
- `data/processed/qubo.json`: full linear/quadratic QUBO coefficients.
- `results/tables/reference.json`: optimized angles and exact probabilities.
- `results/tables/benchmark.csv` and `.json`: actual Qiskit ideal/noisy measurements.
- `results/tables/counts_*.json`: complete raw shot counts.
- `results/figures/`: coupling graphs, cost landscape, routing comparison.
- `results/circuits/`: transpiled circuit text.
- Verification checks NumPy versus Qiskit statevectors, routed logical probabilities, all physical CX edges and allowed basis gates. Feasibility probability is reported before postselection; selected value must not be confused with average performance.

## Rules and submission

Scope follows the Phase 1 Master Guide and organizer clarification: A/B only; participant-designed coupling maps; no C/D benchmark. JSON uses a documented participant-defined schema, not an organizer-provided template. The archive documents contain conflicting topology/D rules; organizer clarification resolves those points.

Submit the **public GitHub repository URL** at https://qffsrmap2026.com/learning/hackathon before the confirmed deadline. Upload the contents of this directory at the repository root so `main.ipynb`, `src/`, `processors/` and `results/` are directly visible. Existing website folders can remain alongside these files. Do not upload passwords, account databases or `.env` files. Judge access to the website uses a separate demo registration.

## References

- Organizer-provided QFF Phase 1 Master Guide; PS-O3 in Problem Statement Details and Updated Challenge Kit.
- [Qiskit transpilation stages](https://quantum.cloud.ibm.com/docs/en/guides/transpiler-stages).
- [Qiskit transpile API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/compiler).

Team members and affiliation: add your actual team details before final submission.
