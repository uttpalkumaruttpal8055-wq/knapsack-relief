def compile_circuit(circuit, config):
    from qiskit import transpile
    from qiskit.transpiler import CouplingMap
    coupling = CouplingMap(config['coupling_map'])
    swaps = []
    def capture(**kwargs):
        dag = kwargs['dag']
        swaps.append(int(dag.count_ops().get('swap',0)))
    compiled = transpile(circuit, basis_gates=config['basis_gates'], coupling_map=coupling,
        optimization_level=1, seed_transpiler=42, layout_method='sabre', routing_method='sabre', callback=capture)
    return compiled, max(swaps,default=0)
