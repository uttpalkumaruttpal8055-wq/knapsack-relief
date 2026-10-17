"""Convenience entry point; JSON schema is participant-defined, not organizer-provided."""
import sys
from run_experiment import main
if __name__ == '__main__':
    sys.argv.extend(['--processor','A'])
    main()
