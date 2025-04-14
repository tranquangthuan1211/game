# search/metrics.py - Search performance metrics

import time
import psutil
import os

class SearchMetrics:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.search_time = 0
        self.expanded_nodes = 0
        self.memory_usage_start = 0
        self.memory_usage_end = 0
        self.memory_used = 0
        
    def start_tracking(self):
        self.start_time = time.time()
        self.memory_usage_start = self.get_memory_usage()
        self.expanded_nodes = 0
    
    def end_tracking(self):
        self.end_time = time.time()
        self.memory_usage_end = self.get_memory_usage()
        self.search_time = self.end_time - self.start_time
        self.memory_used = self.memory_usage_end - self.memory_usage_start
    
    def increment_expanded_nodes(self):
        self.expanded_nodes += 1
    
    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024  # in KB
    
    def get_results(self):
        return {
            "search_time": self.search_time,
            "expanded_nodes": self.expanded_nodes,
            "memory_used": self.memory_used
        }