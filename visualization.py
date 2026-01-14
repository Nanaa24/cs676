import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class SimulationVisualizer:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.output_dir = Path('visualization_output')
        self.output_dir.mkdir(exist_ok=True)
        
    def create_summary_plots(self):
        """Generate summary visualization plots"""
        # Success rate pie chart
        plt.figure(figsize=(10, 6))
        success_rate = self.analyzer.calculate_success_rate()
        plt.pie([success_rate, 100-success_rate], 
                labels=['Success', 'Failure'],
                autopct='%1.1f%%')
        plt.title('Simulation Success Rate')
        plt.savefig(self.output_dir / 'success_rate.png')
        plt.close()
        
        # User distribution
        plt.figure(figsize=(10, 6))
        user_counts = [r['users'] for r in self.analyzer.results_data['results']
                      if r['status'] == 'completed']
        sns.histplot(user_counts)
        plt.title('Distribution of Users per Simulation')
        plt.savefig(self.output_dir / 'user_distribution.png')
        plt.close()