from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    nice: int = 0                    # CFS priority (-20 to +19)
    tickets: int = 10                # Lottery scheduling tickets
    remaining_time: int = field(init=False)
    vruntime: float = 0.0
    state: str = "NEW"               # NEW, READY, RUNNING, TERMINATED
    start_time: Optional[int] = None
    finish_time: Optional[int] = None

    def __post_init__(self) -> None:
        self.remaining_time = self.burst_time


@dataclass
class GanttSegment:
    core_id: int
    pid: str                         # "IDLE" when core has no task
    start_time: int
    end_time: int


@dataclass
class TickSnapshot:
    tick: int
    running: Dict[int, Optional[str]]  # {core_id: pid or None}
    ready_queue: List[str]             # Ordered PIDs waiting in queue
    terminated: List[str]


@dataclass
class SimulationResult:
    algorithm: str
    num_cores: int
    segments: List[GanttSegment]
    snapshots: List[TickSnapshot]
    processes: List[Process]
    metrics: Dict[str, float]
    context_switches: int