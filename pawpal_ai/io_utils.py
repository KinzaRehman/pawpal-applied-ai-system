import json
from pathlib import Path
from typing import List, Tuple
from .models import Pet, Task, ScheduleResult


def load_scenario(path: str) -> Tuple[List[Pet], List[Task], int, int]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    pets = [Pet(**item) for item in data["pets"]]
    tasks = [Task(**item) for item in data["tasks"]]
    availability = data.get("availability", {"start_hour": 8, "end_hour": 20})
    return (
        pets,
        tasks,
        int(availability["start_hour"]),
        int(availability["end_hour"]),
    )


def format_result(result: ScheduleResult) -> str:
    lines = [
        "=" * 60,
        "PAWPAL AI SCHEDULE",
        "=" * 60,
        f"Status: {result.status.upper()}",
        f"Confidence: {result.confidence:.2f}",
        "",
    ]

    if result.scheduled:
        lines.append("Recommended schedule:")
        for item in result.scheduled:
            lines.append(
                f"- {item.start_time}–{item.end_time}: {item.name} "
                f"for {item.pet_name} [{item.priority}/{item.category}]"
            )
            lines.append(f"  Why: {item.reason}")
    else:
        lines.append("No tasks were scheduled.")

    if result.unscheduled:
        lines.append("\nUnscheduled tasks:")
        lines.extend(f"- {name}" for name in result.unscheduled)

    if result.warnings:
        lines.append("\nHuman-review warnings:")
        lines.extend(f"- {warning}" for warning in result.warnings)

    lines.append("\nDecision trace:")
    lines.extend(f"- {step}" for step in result.trace)
    return "\n".join(lines)
