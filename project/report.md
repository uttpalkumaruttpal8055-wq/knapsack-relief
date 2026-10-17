# PS-O3 experimental report

## Exact baseline and formulation

The official five items have optimum value 26, weight 14, one-based items [1,2,3,4]. All 32 choices are enumerated. For this fixed instance penalty 2 makes every infeasible cost strictly greater than -26; this is an exhaustively verified instance-specific choice.

The genuine QUBO uses nine bits: five selections and binary slack weights [1,2,4,8]. All 512 QUBO energies match the expanded polynomial. Minimizing over slack reproduces the squared-overflow cost for every item string. A has only five qubits: the nine-qubit circuit is not executed on A. Instead A/B use the exact five-qubit higher-order diagonal Hamiltonian, with all Pauli-Z terms retained. We do not mislabel that cost as a five-bit QUBO. B also runs the full QUBO. This is a substantive capacity limitation relative to interpreting PS-O3 as requiring the same full QUBO on both processors.

## Algorithm and verification

p=1: prepare |+> on every logical qubit, apply exp(-i gamma H), then exp(-i beta sum X). Integer energies give a gamma search period 2*pi; beta uses [0,pi]. Optimize exact expected cost with 2048 seeded starts and deterministic coordinate refinement of twelve candidates. This heuristic search is not certified globally optimal. Both encodings have separate angles; hinge angles are identical for A/B.

Independent NumPy statevectors agree with synthesized Qiskit circuits at three angle pairs for each encoding. Each routed circuit preserves logical probabilities to tolerance 1e-8 after final-layout/measurement remapping. All CX edges and basis gates are checked. QUBO degree is verified <=2; hinge higher-order terms are explicitly verified present. Raw counts total 4096 for all six runs.

## Actual measured results

| Processor / encoding | Mode | Depth | CX | SWAP | P(valid items) | P(optimal items) | Modal feasible value | Best observed value |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A/hinge | ideal | 192 | 186 | 34 | 0.7842 | 0.1401 | 26 | 26 |
| A/hinge | noisy | 192 | 186 | 34 | 0.8354 | 0.0745 | 24 | 26 |
| B/hinge | ideal | 140 | 105 | 3 | 0.7861 | 0.1394 | 26 | 26 |
| B/hinge | noisy | 140 | 105 | 3 | 0.8225 | 0.0930 | 24 | 26 |
| B/slack | ideal | 111 | 117 | 15 | 0.9504 | 0.0195 | 12 | 26 |
| B/slack | noisy | 111 | 117 | 15 | 0.9387 | 0.0249 | 8 | 26 |


The modal feasible choice is selected by frequency among feasible item strings; best observed feasible value is a different statistic. Report both and do not imply every shot finds the optimum. Item feasibility in the slack experiment marginalizes the four slack bits; equality-valid probability is also exported separately. A solution can have feasible items but incorrect measured slack.

## Architecture interpretation

A is a 4-link chain (maximum degree 2). B is a 12-link perimeter/center graph (maximum degree 4). In this controlled hinge experiment B reduces CX count by 43.5% and depth by 27.1%. Routing SWAPs decrease from 34 to 3. Extra connectivity reduces parity-routing costs in this circuit; the trade-off is more couplers, greater degree and possible crosstalk absent from this synthetic model. B/slack is a different circuit and cannot isolate connectivity effects against A/hinge.

Routing SWAP count is the maximum explicit SWAP count captured in transpiler pass callbacks before basis translation, not final count_ops()['swap']; final SWAP count is zero because basis gates exclude SWAP. CX counts include decomposed routing. Depth includes final measurements. SABRE layout/routing, optimization 1 and seed 42 are fixed. Basis is rz/sx/x/cx. Both synthetic models use depolarizing .001 on each one-qubit basis gate, .005 on CX, readout .01. Aer uses seed 42 and 4096 shots.

## Limits and statistical interpretation

Shallow p=1 QAOA does not guarantee optimal sampling, especially in the larger slack space. The full QUBO's modal feasible value is substantially below the optimum even though optimal strings were sampled; that weakness is retained in the results. Higher P(valid) under noise is not automatically improvement: noise can shift weight toward lower-value feasible strings. Compare P(optimal), expected value and expected penalized cost together. Single-shot-run binomial error bars reflect sampling only; one seed is not a multi-seed noise robustness study. No quantum advantage is claimed against a 32-choice classical enumeration.

Experiments use local simulation, not IBM hardware. No idle relaxation, correlated faults, hardware calibration or real emergency data is modeled. The disaster-management website is an additional classical application demo, and no live alerts or verified flood forecasts are claimed by this quantum package.

## Reproduce and sources

Run `python run_experiment.py` or all notebook cells. Environment versions are recorded and pinned. Raw counts, classical data, angle traces and figures are included. Phase 1 scope/coupling freedom follows the supplied Master Guide and organizer clarification. Archived documents differ on D and fixed topology; no D is included.

## Added reproducibility and robustness evidence

Same-seed independent replay matched all six raw-count JSON tables exactly in the pinned environment. `reproduce.py` also recomputes metrics from raw counts and verifies stored angle probabilities. Source/configuration/data SHA-256 hashes are recorded in manifest.json.

Three additional simulator seeds (7,123,2026) retain optimized angles and transpiler seed 42. This explores sampling/noise variation, not optimizer/layout robustness.

| Processor/encoding | Mean noisy P(optimal) | Sample standard deviation | Mean noisy P(valid) |
|---|---:|---:|---:|
| A/hinge | 0.07357 | 0.00263 | 0.83626 |
| B/hinge | 0.09033 | 0.00384 | 0.82015 |
| B/slack | 0.02458 | 0.00014 | 0.93799 |

Exact penalty analysis yields strict safety condition P>1 for this fixed data; P=1 ties an infeasible choice with the optimum. P=2 excludes it. This is a ground-state safety check, not evidence of quantum sampling quality. 95% Wilson intervals and graph density, degree, diameter and average path length are exported.

The website evidence viewer uses these fixed exported measurements. Its item and penalty controls perform classical local calculations. Front-end control logic and authenticated asset serving were checked without a browser; visual preview was unavailable due to local-file browser policy. Upload the website update ZIP and redeploy the existing Render service to publish the changes.
