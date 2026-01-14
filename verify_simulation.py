import os
import json

def verify_simulation():
    """Verify the simulation results and structure"""
    print("Starting verification...")
    
    # Check directories exist
    directories = [
        "bulk_output",
        "bulk_output/results",
        "bulk_output/simulations"
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✓ Directory exists: {directory}")
        else:
            print(f"✗ Missing directory: {directory}")
    
    # Check results file
    results_file = "bulk_output/results/bulk_results.json"
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            results = json.load(f)
            print(f"\nResults Summary:")
            print(f"- Total simulations: {len(results.get('results', []))}")
            print(f"- Successful: {sum(1 for r in results.get('results', []) if r.get('status') == 'completed')}")
            print(f"- Failed: {sum(1 for r in results.get('results', []) if r.get('status') == 'failed')}")
    else:
        print(f"✗ Missing results file: {results_file}")
    
    # Check simulation files
    sim_files = os.listdir("bulk_output/simulations")
    print(f"\nFound {len(sim_files)} simulation files")
    
    # Check log file
    if os.path.exists("bulk_simulation.log"):
        with open("bulk_simulation.log", 'r') as f:
            log_content = f.read()
            if "ERROR" in log_content:
                print("\n⚠️ Warning: Found errors in log file")
            else:
                print("\n✓ No errors found in log file")
    else:
        print("\n✗ Missing log file")

if __name__ == "__main__":
    verify_simulation()