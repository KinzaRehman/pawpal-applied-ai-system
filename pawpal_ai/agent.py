from dataclasses import replace
from pathlib import Path
from datetime import datetime
from typing import Iterable, List, Tuple

from .models import Pet, Task, ScheduledTask, ScheduleResult
from .guardrails import validate_inputs, ValidationError


PRIORITY_SCORE = {"urgent": 4, "high": 3, "medium": 2, "low": 1}
CATEGORY_SCORE = {
    "medication": 4,
    "feeding": 3,
    "appointment": 3,
    "walk": 2,
    "cleaning": 2,
    "grooming": 1,
    "play": 1,
    "general": 1,
}


class PawPalPlanningAgent:
    """
    Specialized planning agent:
    plan -> validate -> rank -> schedule -> critique -> revise -> report.
    It is deterministic and does not require an external model or API key.
    """

    def __init__(self, log_path: str = "logs/agent_trace.md") -> None:
        self.log_path = Path(log_path)

    def build_schedule(
        self,
        pets: Iterable[Pet],
        tasks: Iterable[Task],
        available_start_hour: int = 8,
        available_end_hour: int = 20,
    ) -> ScheduleResult:
        pets = list(pets)
        tasks = list(tasks)
        trace: List[str] = [
            "PLAN: Validate inputs, specialize task priorities, rank tasks, "
            "construct a schedule, critique it, and revise if needed."
        ]

        try:
            warnings = validate_inputs(
                pets, tasks, available_start_hour, available_end_hour
            )
        except ValidationError as exc:
            result = ScheduleResult(
                status="blocked",
                warnings=[str(exc)],
                confidence=0.0,
                trace=trace + [f"GUARDRAIL: Blocked invalid input — {exc}"],
            )
            self._save_trace(result)
            return result

        trace.append(f"ANALYZE: Accepted {len(pets)} pet(s) and {len(tasks)} task(s).")

        specialized = [self._specialize_task(task, trace) for task in tasks]
        ranked = sorted(specialized, key=self._rank_key)
        trace.append(
            "ACT: Ranked tasks by safety category, priority, due time, and duration."
        )

        start = available_start_hour * 60
        end = available_end_hour * 60
        current = start
        scheduled: List[ScheduledTask] = []
        unscheduled: List[str] = []

        for task in ranked:
            task_end = current + task.duration_minutes
            due_minute = task.due_hour * 60

            if task_end > end:
                unscheduled.append(task.name)
                trace.append(
                    f"ACT: Could not place '{task.name}' because the availability "
                    "window was full."
                )
                continue

            reason = (
                f"{task.category.title()} task; {task.priority} priority; "
                f"due by {self._hour_label(task.due_hour)}."
            )
            scheduled.append(
                ScheduledTask(
                    name=task.name,
                    pet_name=task.pet_name,
                    start_minute=current,
                    end_minute=task_end,
                    priority=task.priority,
                    category=task.category,
                    reason=reason,
                )
            )
            if task_end > due_minute:
                warnings.append(
                    f"'{task.name}' is scheduled after its requested due hour."
                )
            current = task_end + 10  # transition buffer

        trace.append("TEST: Checked capacity, due times, and medication placement.")
        critique = self._critique(scheduled, specialized, warnings)
        trace.extend(critique)

        scheduled, revisions = self._revise(scheduled)
        trace.extend(revisions)

        confidence = self._confidence(
            total_tasks=len(tasks),
            scheduled_count=len(scheduled),
            warnings=warnings,
            unscheduled=unscheduled,
        )

        status = "success" if not unscheduled else "partial"
        trace.append(
            f"REFLECT: Final status={status}; confidence={confidence:.2f}; "
            f"scheduled={len(scheduled)}/{len(tasks)}."
        )

        result = ScheduleResult(
            status=status,
            scheduled=scheduled,
            unscheduled=unscheduled,
            warnings=warnings,
            confidence=confidence,
            trace=trace,
        )
        self._save_trace(result)
        return result

    def _specialize_task(self, task: Task, trace: List[str]) -> Task:
        category = task.category.lower()
        priority = task.priority.lower()

        if category not in CATEGORY_SCORE:
            category = "general"

        if category == "medication" and PRIORITY_SCORE[priority] < PRIORITY_SCORE["high"]:
            trace.append(
                f"SPECIALIZE: Elevated medication task '{task.name}' "
                f"from {priority} to high."
            )
            priority = "high"

        return replace(task, category=category, priority=priority)

    def _rank_key(self, task: Task) -> Tuple[int, int, int, int, str]:
        return (
            -CATEGORY_SCORE.get(task.category, 1),
            -PRIORITY_SCORE[task.priority],
            task.due_hour,
            task.duration_minutes,
            task.name.lower(),
        )

    def _critique(
        self,
        scheduled: List[ScheduledTask],
        tasks: List[Task],
        warnings: List[str],
    ) -> List[str]:
        notes = []
        med_names = {t.name for t in tasks if t.category == "medication"}
        if med_names:
            first_non_med = next(
                (i for i, item in enumerate(scheduled) if item.name not in med_names),
                len(scheduled),
            )
            misplaced_med = [
                item.name
                for item in scheduled[first_non_med:]
                if item.name in med_names
            ]
            if misplaced_med:
                notes.append(
                    "CRITIQUE: Medication was not placed first: "
                    + ", ".join(misplaced_med)
                )
            else:
                notes.append("CRITIQUE: Medication safety ordering passed.")

        if warnings:
            notes.append(f"CRITIQUE: Found {len(warnings)} warning(s) for human review.")
        else:
            notes.append("CRITIQUE: No timing or validation warnings detected.")
        return notes

    def _revise(
        self, scheduled: List[ScheduledTask]
    ) -> Tuple[List[ScheduledTask], List[str]]:
        medication = [x for x in scheduled if x.category == "medication"]
        other = [x for x in scheduled if x.category != "medication"]
        reordered = medication + other

        if reordered == scheduled:
            return scheduled, ["REVISE: No revision was necessary."]

        cursor = scheduled[0].start_minute if scheduled else 0
        revised = []
        for item in reordered:
            duration = item.end_minute - item.start_minute
            revised.append(
                ScheduledTask(
                    name=item.name,
                    pet_name=item.pet_name,
                    start_minute=cursor,
                    end_minute=cursor + duration,
                    priority=item.priority,
                    category=item.category,
                    reason=item.reason,
                )
            )
            cursor += duration + 10
        return revised, ["REVISE: Moved medication tasks ahead of non-medical tasks."]

    def _confidence(
        self,
        total_tasks: int,
        scheduled_count: int,
        warnings: List[str],
        unscheduled: List[str],
    ) -> float:
        if total_tasks == 0:
            return 0.0
        completion = scheduled_count / total_tasks
        score = 0.60 + (0.35 * completion)
        score -= min(0.20, len(warnings) * 0.04)
        score -= min(0.25, len(unscheduled) * 0.08)
        return max(0.0, min(0.99, round(score, 2)))

    def _save_trace(self, result: ScheduleResult) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().isoformat(timespec="seconds")
        lines = [
            f"\n## Agent Run — {timestamp}",
            f"- Status: {result.status}",
            f"- Confidence: {result.confidence:.2f}",
            "",
        ]
        lines.extend(f"1. {line}" for line in result.trace)
        lines.append("")
        with self.log_path.open("a", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")

    @staticmethod
    def _hour_label(hour: int) -> str:
        suffix = "AM" if hour < 12 else "PM"
        display_hour = hour % 12 or 12
        return f"{display_hour}:00 {suffix}"
