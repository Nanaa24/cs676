"""
Bulk Simulation Package
A package for running multiple simulations in parallel.
"""

from .config import (
    BulkSimulationConfig,
    SimulationPaths,
    create_default_config,
    load_config
)
from .bulk_manager import BulkSimulationManager

# Package metadata
__version__ = '1.0.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'
__all__ = [
    'BulkSimulationConfig',
    'BulkSimulationManager',
    'SimulationPaths',
    'create_default_config',
    'load_config',
]

# Package-level configuration
DEFAULT_CONFIG_PATH = 'config.json'
DEFAULT_OUTPUT_DIR = 'bulk_output'

# Optional: Helper function to quickly set up a simulation
def quick_setup(num_simulations=10, output_dir=DEFAULT_OUTPUT_DIR):
    """
    Quick setup helper for common use cases.
    
    Args:
        num_simulations (int): Number of simulations to run
        output_dir (str): Output directory path
    
    Returns:
        BulkSimulationManager: Configured simulation manager
    """
    config = BulkSimulationConfig(
        num_simulations=num_simulations,
        users_per_simulation=3,
        steps_per_phase=3,
        output_directory=output_dir
    )
    return BulkSimulationManager(config)

# Optional: Package initialization code
def initialize_package():
    """Initialize package resources if needed."""
    import logging
    logging.getLogger(__name__).addHandler(logging.NullHandler())

initialize_package()
