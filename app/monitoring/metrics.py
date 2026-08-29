from dataclasses import dataclass, field
from typing import Dict, Any
import time

@dataclass
class PipelineMetrics:
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    total_duration_seconds: float = 0.0
    custom_counters: Dict[str, int] = field(default_factory=dict)

    def record_run(self, duration: float, success: bool):
        self.total_runs += 1
        if success:
            self.successful_runs += 1
        else:
            self.failed_runs += 1
        self.total_duration_seconds += duration

    def increment_counter(self, metric_name: str, count: int = 1):
        self.custom_counters[metric_name] = self.custom_counters.get(metric_name, 0) + count

    def get_summary(self) -> Dict[str, Any]:
        avg_duration = (self.total_duration_seconds / self.total_runs) if self.total_runs > 0 else 0.0
        return {
            "total_runs": self.total_runs,
            "successful_runs": self.successful_runs,
            "failed_runs": self.failed_runs,
            "avg_duration_seconds": round(avg_duration, 4),
            "counters": self.custom_counters
        }

metrics_collector = PipelineMetrics()
