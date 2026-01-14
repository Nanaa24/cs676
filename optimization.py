import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import cProfile
import pstats

class PerformanceOptimizer:
    def __init__(self):
        self.cpu_count = multiprocessing.cpu_count()
        self.profiler = None
        
    def optimize_workers(self, data_size: int) -> int:
        """Calculate optimal number of workers"""
        return min(self.cpu_count, max(1, data_size // 2))
        
    def start_profiling(self):
        """Start performance profiling"""
        self.profiler = cProfile.Profile()
        self.profiler.enable()
        
    def end_profiling(self, output_file: str):
        """End profiling and save results"""
        self.profiler.disable()
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative')
        stats.dump_stats(output_file)
