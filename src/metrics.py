from statistics import mean
from typing import Dict, List

from src.models import GanttSegment, Process


def compute_metrics(
    processes: List[Process],
    segments: List[GanttSegment],
    num_cores: int,
    context_switches: int,
) -> Dict[str, float]:
    
    # check the inputs are valid
    if num_cores < 1:
         raise ValueError("num_cores must be at least 1")
    
    if not processes:
        raise ValueError("processes list cannot be empty")
    
    for p in processes:
        if p.burst_time < 1:
            raise ValueError(f"Process {p.pid} has invalid burst_time {p.burst_time}")
        if p.finish_time is None:
            raise ValueError(f"Process {p.pid} never finished")
        
    # 2. for each process: turnaround, wait, prop. fairness
    turnarounds = []
    waits = []
    fairness = []

    for p in processes:
        turnaround = p.finish_time - p.arrival_time
        wait = turnaround - p.burst_time
        prop = turnaround / p.burst_time

        turnarounds.append(turnaround)
        waits.append(wait)  
        fairness.append(prop)

    # 3. from the segments: total time, busy time
        total_time = 0
        busy_time = 0

    for s in segments:
        total_time = max(total_time, s.end_time)
        if s.pid != "IDLE":
            busy_time += (s.end_time - s.start_time)

    if total_time == 0:
        raise ValueError("Total time is zero.")
    
    cpu_use = busy_time / (num_cores * total_time)
    throughput = len(processes) / total_time
        

    # 4. return the results
    return {
        "avg_wait": mean(waits),
        "avg_turnaround": mean(turnarounds),
        "avg_prop_fairness": mean(fairness),
        "max_prop_fairness": max(fairness),
        "cpu_utilization": cpu_use,
        "throughput": throughput,
        "context_switches": float(context_switches),
    }