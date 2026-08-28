import psutil
import random

class TelemetryService:
    """
    Gathers system and pipeline metrics for real-time monitoring.
    """
    @staticmethod
    def get_system_metrics():
        # CPU and Memory using psutil
        cpu_usage = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        
        # Simulated pipeline metrics (In production, query Redis State Manager)
        active_pipelines = random.randint(10, 15)
        records_per_sec = random.randint(500, 2000)
        
        return {
            'cpu_percent': cpu_usage,
            'memory_percent': memory.percent,
            'memory_used_gb': round(memory.used / (1024**3), 2),
            'active_pipelines': active_pipelines,
            'records_per_second': records_per_sec
        }
