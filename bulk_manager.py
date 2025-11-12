import os
import logging
from typing import Dict
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from simulation import UserFeedbackSimulation  # Updated import
from config import BulkSimulationConfig

class BulkSimulationManager:
    def __init__(self, config: BulkSimulationConfig):
        """Initialize the bulk simulation manager"""
        self.config = config
        self.results = []
        self.setup_logging()
        self.setup_directories()

    def setup_logging(self):
        """Configure logging for bulk operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bulk_simulation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_directories(self):
        """Create necessary directories for output"""
        os.makedirs(self.config.output_directory, exist_ok=True)
        os.makedirs(os.path.join(self.config.output_directory, 'simulations'), exist_ok=True)
        os.makedirs(os.path.join(self.config.output_directory, 'results'), exist_ok=True)

    def run_single_simulation(self, sim_id: int) -> Dict:
        """Run a single simulation instance"""
        try:
            # Create simulation instance with unique ID
            simulation = UserFeedbackSimulation()
            output_file = f"simulation_{sim_id}.json"
            
            # Initialize simulation
            simulation.initialize_simulation()
            
            # Run simulation phases
            simulation.run_simulation()
            
            # Save simulation results
            output_path = os.path.join(self.config.output_directory, 'simulations', output_file)
            simulation.save_results(output_path)
            
            # Collect results
            results = {
                'simulation_id': sim_id,
                'status': 'completed',
                'users': len(simulation.users),
                'output_file': output_file
            }
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in simulation {sim_id}: {str(e)}")
            return {
                'simulation_id': sim_id,
                'status': 'failed',
                'error': str(e)
            }

    def run_bulk_simulations(self):
        """Run multiple simulations in parallel"""
        self.logger.info(f"Starting bulk simulation with {self.config.num_simulations} instances")
        
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = []
            
            # Create progress bar
            with tqdm(total=self.config.num_simulations) as pbar:
                # Submit all simulation jobs
                for sim_id in range(self.config.num_simulations):
                    future = executor.submit(self.run_single_simulation, sim_id)
                    future.add_done_callback(lambda p: pbar.update(1))
                    futures.append(future)
                
                # Collect results
                for future in futures:
                    result = future.result()
                    self.results.append(result)

        self.save_bulk_results()

    def save_bulk_results(self):
        """Save aggregated results"""
        import json
        results_file = os.path.join(self.config.output_directory, 'results', 'bulk_results.json')
        
        with open(results_file, 'w') as f:
            json.dump({
                'config': self.config.__dict__,
                'results': self.results
            }, f, indent=4)

    def get_summary(self) -> Dict:
        """Get summary of simulation results"""
        successful = sum(1 for r in self.results if r['status'] == 'completed')
        failed = sum(1 for r in self.results if r['status'] == 'failed')
        
        return {
            'total_simulations': self.config.num_simulations,
            'successful': successful,
            'failed': failed,
            'output_directory': self.config.output_directory
        }