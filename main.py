import sys
import argparse
import json
import time
from typing import Dict
from pathlib import Path

from config import BulkSimulationConfig
from bulk_manager import BulkSimulationManager
from analysis import SimulationAnalyzer
from visualization import SimulationVisualizer
from optimization import PerformanceOptimizer

def parse_arguments() -> Dict:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run enhanced bulk simulations')
    
    parser.add_argument(
        '--num-simulations',
        type=int,
        default=10,
        help='Number of simulations to run (default: 10)'
    )
    
    parser.add_argument(
        '--users-per-simulation',
        type=int,
        default=3,
        help='Number of users per simulation (default: 3)'
    )
    
    parser.add_argument(
        '--steps-per-phase',
        type=int,
        default=3,
        help='Number of steps per phase (default: 3)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='bulk_output',
        help='Output directory for results (default: bulk_output)'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Perform detailed analysis'
    )
    
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Create visualization plots'
    )
    
    parser.add_argument(
        '--optimize',
        action='store_true',
        help='Enable performance optimization'
    )

    return vars(parser.parse_args())

def run_analysis(output_dir: str):
    """Run detailed analysis on simulation results"""
    print("\n📊 Running detailed analysis...")
    analyzer = SimulationAnalyzer(output_dir)
    summary = analyzer.generate_summary()
    
    # Save analysis results
    analysis_file = Path(output_dir) / 'results' / 'analysis_summary.json'
    with open(analysis_file, 'w') as f:
        json.dump(summary, f, indent=4)
    
    print("\nAnalysis Summary:")
    print(f"Total Simulations: {summary['total_simulations']}")
    print(f"Success Rate: {summary['success_rate']:.2f}%")
    print(f"Average Users per Simulation: {summary['average_users']:.2f}")
    
    return analyzer

def create_visualizations(analyzer: SimulationAnalyzer):
    """Create visualization plots"""
    print("\n📈 Generating visualization plots...")
    visualizer = SimulationVisualizer(analyzer)
    visualizer.create_summary_plots()
    print("Plots saved in: visualization_output/")

def print_summary(summary: Dict):
    """Print formatted summary of simulation results"""
    print("\n" + "="*50)
    print("BULK SIMULATION SUMMARY")
    print("="*50)
    print(f"Total Simulations: {summary['total_simulations']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {(summary['successful']/summary['total_simulations'])*100:.2f}%")
    print(f"\nResults saved in: {summary['output_directory']}")
    print("="*50 + "\n")

def main():
    """Enhanced main execution function"""
    start_time = time.time()
    
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Initialize performance optimizer if requested
        optimizer = None
        if args['optimize']:
            print("\n⚡ Enabling performance optimization...")
            optimizer = PerformanceOptimizer()
            optimizer.start_profiling()
        
        # Configure bulk simulation
        config = BulkSimulationConfig(
            num_simulations=args['num_simulations'],
            users_per_simulation=args['users_per_simulation'],
            steps_per_phase=args['steps_per_phase'],
            output_directory=args['output_dir']
        )

        # Create and run bulk simulation manager
        print("\n🚀 Starting bulk simulation...")
        bulk_manager = BulkSimulationManager(config)
        
        try:
            bulk_manager.run_bulk_simulations()
            print("\n✅ Bulk simulation completed successfully!")
            
            # Get and print summary
            summary = bulk_manager.get_summary()
            print_summary(summary)
            
            # Run analysis if requested
            analyzer = None
            if args['analyze']:
                analyzer = run_analysis(args['output_dir'])
            
            # Create visualizations if requested
            if args['visualize']:
                if analyzer is None:
                    analyzer = run_analysis(args['output_dir'])
                create_visualizations(analyzer)
            
            # End profiling if enabled
            if optimizer:
                optimizer.end_profiling('performance_stats.prof')
                print("\n📊 Performance profile saved to: performance_stats.prof")
            
            # Print execution time
            execution_time = time.time() - start_time
            print(f"\n⏱️ Total execution time: {execution_time:.2f} seconds")
            
            return 0  # Success exit code
            
        except Exception as e:
            print(f"\n❌ Bulk simulation failed: {str(e)}")
            return 1  # Error exit code
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Simulation interrupted by user")
        return 2  # Interrupted exit code
    
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        return 1  # Error exit code

if __name__ == "__main__":
    sys.exit(main())