# Knapsack Relief — Phase 1

**Team:** Hollow Knights

**University:** SRM University AP

**Team members:**
- कार्तिक शर्मा
- कृष्णा अग्रवाल
- दिव्यान्स सिंह
- Ben ND
- Uthpal Kumar

**Quantum experiment:** [project/README.md](project/README.md)  
**Executed notebook:** [project/main.ipynb](project/main.ipynb)  
**Report:** [project/report.md](project/report.md)  
**Demo website:** https://knapsack-relief.onrender.com/

The required Phase 1 submission is in `project/`. The existing `knapsack/`, `knapsack-server/` and `Dockerfile` at the repository root run the separate disaster-management website on Render.

## Run the experiment

```sh
cd project
python -m pip install -r requirements-lock.txt
python reproduce.py
```

Open `project/main.ipynb` with `project/` as the working directory to inspect the executed notebook. For fresh Qiskit simulation results, run `python run_experiment.py` from that same directory. No IBM account or quantum hardware credentials are needed.

The archived evidence and source are preserved from the existing experiment package; restructuring does not create new experimental results. Local QAOA simulations compare participant-defined processors A/B. The website uses a separate classical optimizer and simulated disaster data. No quantum hardware execution or quantum advantage is claimed.

## Submission structure

```text
project/
  README.md
  main.ipynb
  requirements.txt
  data/raw/
  data/processed/
  processors/processor_A.json
  processors/processor_B.json
  src/__init__.py
  src/problem.py
  src/processors.py
  src/routing.py
  src/metrics.py
  src/visualization.py
  src/qaoa.py
  results/tables/
  results/figures/
  results/circuits/
  results/replay/
  results/robustness/
  report.md
  assets/qff-phase1_latex_images/
```

Additional reproduction scripts and the pinned requirements lockfile remain in `project/`.

## Key encoding limitation

The true slack-variable QUBO uses nine logical qubits and fits Processor B, not five-qubit Processor A. The A/B comparison uses an exactly reduced five-qubit higher-order diagonal cost, **not a five-variable QUBO**. See the report for this distinction and the measured results.


