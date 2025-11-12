import pandas as pd
import json
from pathlib import Path
import numpy as np
from typing import Dict

class SimulationAnalyzer:
    def __init__(self, results_dir: str):
        self.results_dir = Path(results_dir)
        self.results_data = None
        
    def load_results(self):
        """Load and parse all simulation results"""
        results_file = self.results_dir / 'results' / 'bulk_results.json'
        with open(results_file) as f:
            self.results_data = json.load(f)
            
    def generate_summary(self) -> dict:
        """Generate detailed analysis summary"""
        if not self.results_data:
            self.load_results()
            
        summary = {
            'total_simulations': len(self.results_data['results']),
            'success_rate': self.calculate_success_rate(),
            'average_users': self.calculate_average_users(),
            'performance_metrics': self.analyze_performance()
        }
        return summary
    
    def calculate_success_rate(self) -> float:
        successful = sum(1 for r in self.results_data['results'] 
                        if r['status'] == 'completed')
        return successful / len(self.results_data['results']) * 100
    
    def calculate_average_users(self) -> float:
        user_counts = [r['users'] for r in self.results_data['results'] 
                      if r['status'] == 'completed']
        return sum(user_counts) / len(user_counts) if user_counts else 0
    
    def analyze_performance(self) -> Dict:
        """Analyze performance metrics of the simulations"""
        successful_sims = [r for r in self.results_data['results'] 
                         if r['status'] == 'completed']
        
        if not successful_sims:
            return {
                'average_users': 0,
                'total_successful': 0,
                'success_rate': 0
            }
        
        metrics = {
            'average_users': np.mean([s['users'] for s in successful_sims]),
            'total_successful': len(successful_sims),
            'success_rate': (len(successful_sims) / len(self.results_data['results'])) * 100,
            'simulation_distribution': {
                'completed': len(successful_sims),
                'failed': len(self.results_data['results']) - len(successful_sims)
            }
        }
        
        return metrics