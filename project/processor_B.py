"""Convenience entry point for 5-qubit diagnostic and 9-qubit slack QUBO."""
import sys
from run_experiment import main
if __name__ == '__main__':
    sys.argv.extend(['--processor','B'])
    main()
