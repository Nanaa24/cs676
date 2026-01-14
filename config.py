from dataclasses import dataclass
from typing import Optional, Dict
import json
import os

@dataclass
class BulkSimulationConfig:
    """Configuration for bulk simulation runs"""
    num_simulations: int
    users_per_simulation: int
    steps_per_phase: int
    output_directory: str
    max_workers: Optional[int] = None
    verbose: bool = False
    
    @classmethod
    def from_json(cls, json_file: str) -> 'BulkSimulationConfig':
        """Create configuration from JSON file"""
        with open(json_file, 'r') as f:
            data = json.load(f)
        return cls(**data)
    
    def to_json(self, json_file: str) -> None:
        """Save configuration to JSON file"""
        with open(json_file, 'w') as f:
            json.dump(self.__dict__, f, indent=4)
    
    def validate(self) -> bool:
        """Validate configuration parameters"""
        if self.num_simulations <= 0:
            raise ValueError("num_simulations must be positive")
        if self.users_per_simulation <= 0:
            raise ValueError("users_per_simulation must be positive")
        if self.steps_per_phase <= 0:
            raise ValueError("steps_per_phase must be positive")
        if not self.output_directory:
            raise ValueError("output_directory cannot be empty")
        return True

class SimulationPaths:
    """Helper class to manage simulation paths"""
    def __init__(self, base_directory: str):
        self.base_directory = base_directory
        self.simulations_dir = os.path.join(base_directory, 'simulations')
        self.results_dir = os.path.join(base_directory, 'results')
        self.logs_dir = os.path.join(base_directory, 'logs')
        
    def create_directories(self):
        """Create all necessary directories"""
        os.makedirs(self.base_directory, exist_ok=True)
        os.makedirs(self.simulations_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
    def get_simulation_path(self, sim_id: int) -> str:
        """Get path for specific simulation results"""
        return os.path.join(self.simulations_dir, f"simulation_{sim_id}.json")
    
    def get_results_path(self) -> str:
        """Get path for bulk results"""
        return os.path.join(self.results_dir, "bulk_results.json")

# Default configuration settings
DEFAULT_CONFIG = {
    "num_simulations": 10,
    "users_per_simulation": 3,
    "steps_per_phase": 3,
    "output_directory": "bulk_output",
    "max_workers": None,
    "verbose": False
}

def create_default_config(output_file: str = "default_config.json") -> None:
    """Create a default configuration file"""
    config = BulkSimulationConfig(**DEFAULT_CONFIG)
    config.to_json(output_file)
    return config

def load_config(config_file: str) -> BulkSimulationConfig:
    """Load configuration from file"""
    try:
        return BulkSimulationConfig.from_json(config_file)
    except FileNotFoundError:
        print(f"Config file {config_file} not found. Using default configuration.")
        return BulkSimulationConfig(**DEFAULT_CONFIG)
    except json.JSONDecodeError:
        print(f"Invalid JSON in {config_file}. Using default configuration.")
        return BulkSimulationConfig(**DEFAULT_CONFIG)

# Example usage:
if __name__ == "__main__":
    # Create default configuration file
    create_default_config()
    
    # Example of loading and validating configuration
    config = load_config("default_config.json")
    try:
        config.validate()
        print("Configuration is valid!")
        print(f"Will run {config.num_simulations} simulations")
    except ValueError as e:
        print(f"Invalid configuration: {e}")
class ConfigurationManager:
    """Manages configuration settings and their validation"""
    def __init__(self):
        self.settings = {}
    
    def load_settings(self, settings_file: str) -> None:
        """Load settings from a file"""
        import json
        with open(settings_file, 'r') as f:
            self.settings = json.load(f)
    
    def save_settings(self, settings_file: str) -> None:
        """Save current settings to a file"""
        import json
        with open(settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get_setting(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value) -> None:
        """Set a setting value"""
        self.settings[key] = value