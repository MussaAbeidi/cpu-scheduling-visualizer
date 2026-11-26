from src.models import GanttSegment, Process
from src.metrics import compute_metrics

p1 = Process("P1", arrival_time=0, burst_time=4)
p2 = Process("P2", arrival_time=1, burst_time=2)
p1.finish_time = 4
p2.finish_time = 6

segments = [
    GanttSegment(core_id=0, pid="P1", start_time=0, end_time=4),
    GanttSegment(core_id=0, pid="P2", start_time=4, end_time=6),
]

print(compute_metrics([p1, p2], segments, num_cores=1, context_switches=1))