# जल्दी submission करें

1. ZIP extract करें। `qff-submission` के अंदर की files/folders GitHub repository के root में upload करें। केवल ZIP upload न करें।
2. README, main.ipynb, requirements.txt, processors, src, data, results और report.md दिखने चाहिए। पुराने website folders रहने दें।
3. README के अंत में अपना team name, members और college जोड़ें।
4. Repository Settings में visibility Public करें। पहले passwords, .env और account database नहीं होने की जाँच करें।
5. यह repository URL official portal पर submit करें: https://qffsrmap2026.com/learning/hackathon
6. Submission confirmation सुरक्षित रखें। Website URL अतिरिक्त demo है; मुख्य link GitHub का देना है।

## अपने laptop पर दोबारा चलाएँ

```powershell
cd 'C:\Users\uttpa\Documents\Codex\2026-10-10\w\outputs\qff-submission'
py -3.14 run_experiment.py
```

## Judges को समझाएँ

“हमारा problem payload-limited relief bundles चुनना है। Official five-item benchmark में classical optimum 26 है। हमने p=1 QAOA, exact classical comparison, अपने A/B coupling maps और equal-noise benchmarks बनाए हैं। Full QUBO में slack सहित 9 qubits लगते हैं, इसलिए वह B पर चलता है। Same-circuit A/B comparison के लिए exact five-qubit higher-order cost अलग दिया है। हमने depth, CX, routing SWAPs और unconditional probabilities report किए हैं। Website इसी disaster-management application का अतिरिक्त demo है।”

Full QUBO को 5-qubit QUBO न बोलें। Simulator को real quantum hardware और observed optimum को quantum advantage न बोलें।

## Extra features और repeatable checks

`py reproduce.py` से raw counts और saved results verify करें। `py reproduce.py --replay` से वही 6 runs दोबारा चलेंगे; `--robustness` तीन additional simulator seeds चलाता है। `py analyze.py` penalty, topology और confidence intervals तैयार करता है।

Website update ZIP में `knapsack/` और `knapsack-server/` की बदली हुई files हैं। इन्हें existing repository के उसी folder में upload/replace करें। Render redeploy पूरा होने पर sidebar में **Qiskit results** खुलेगा। Website के selectors केवल saved Qiskit results दिखाते हैं; browser में नया Qiskit execution नहीं होता।
