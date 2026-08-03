from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0


@dataclass
class Task:
    name: str
    pet_name: str
    duration_minutes: int
    priority: str = "medium"
    due_hour: int = 18
    category: str = "general"
    notes: str = ""


@dataclass
class ScheduledTask:
    name: str
    pet_name: str
    start_minute: int
    end_minute: int
    priority: str
    category: str
    reason: str

    @property
    def start_time(self) -> str:
        return minutes_to_time(self.start_minute)

    @property
    def end_time(self) -> str:
        return minutes_to_time(self.end_minute)


@dataclass
class ScheduleResult:
    status: str
    scheduled: List[ScheduledTask] = field(default_factory=list)
    unscheduled: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    confidence: float = 0.0
    trace: List[str] = field(default_factory=list)


def minutes_to_time(total_minutes: int) -> str:
    hour = (total_minutes // 60) % 24
    minute = total_minutes % 60
    suffix = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12
    return f"{display_hour}:{minute:02d} {suffix}"
