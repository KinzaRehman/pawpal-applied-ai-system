from dataclasses import dataclass
from typing import Callable, List

from pawpal_ai.agent import PawPalPlanningAgent
from pawpal_ai.models import Pet, Task, ScheduleResult


@dataclass
class EvaluationCase:
    name: str
    runner: Callable[[], ScheduleResult]
    check: Callable[[ScheduleResult], bool]
    expected: str


def normal_case() -> ScheduleResult:
    return PawPalPlanningAgent("logs/evaluation_trace.md").build_schedule(
        [Pet("Milo", "cat", 4)],
        [
            Task("Morning medicine", "Milo", 10, "medium", 9, "medication"),
            Task("Breakfast", "Milo", 15, "high", 10, "feeding"),
            Task("Play session", "Milo", 20, "low", 18, "play"),
        ],
        8,
        12,
    )


def invalid_pet_case() -> ScheduleResult:
    return PawPalPlanningAgent("logs/evaluation_trace.md").build_schedule(
        [Pet("Milo", "cat", 4)],
        [Task("Walk", "Luna", 20, "high", 12, "walk")],
        8,
        12,
    )


def capacity_case() -> ScheduleResult:
    return PawPalPlanningAgent("logs/evaluation_trace.md").build_schedule(
        [Pet("Milo", "cat", 4)],
        [
            Task("Medicine", "Milo", 30, "high", 9, "medication"),
            Task("Deep grooming", "Milo", 120, "medium", 12, "grooming"),
            Task("Play", "Milo", 60, "low", 15, "play"),
        ],
        8,
        10,
    )


def duplicate_case() -> ScheduleResult:
    return PawPalPlanningAgent("logs/evaluation_trace.md").build_schedule(
        [Pet("Milo", "cat", 4)],
        [
            Task("Breakfast", "Milo", 15, "high", 9, "feeding"),
            Task("Breakfast", "Milo", 15, "high", 9, "feeding"),
        ],
        8,
        10,
    )


CASES: List[EvaluationCase] = [
    EvaluationCase(
        "Medication specialization",
        normal_case,
        lambda r: (
            r.status == "success"
            and r.scheduled
            and r.scheduled[0].category == "medication"
            and r.scheduled[0].priority == "high"
        ),
        "Medication is elevated and scheduled first.",
    ),
    EvaluationCase(
        "Unknown pet guardrail",
        invalid_pet_case,
        lambda r: r.status == "blocked" and r.confidence == 0.0,
        "Invalid pet reference is blocked.",
    ),
    EvaluationCase(
        "Capacity handling",
        capacity_case,
        lambda r: r.status == "partial" and len(r.unscheduled) >= 1,
        "Overflow is reported instead of silently dropped.",
    ),
    EvaluationCase(
        "Duplicate warning",
        duplicate_case,
        lambda r: any("duplicate" in x.lower() for x in r.warnings),
        "Duplicate task triggers a warning.",
    ),
]


def main() -> int:
    passed = 0
    print("PawPal AI Evaluation Harness")
    print("=" * 60)
    for case in CASES:
        result = case.runner()
        ok = case.check(result)
        passed += int(ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {case.name}")
        print(f"  Expected: {case.expected}")
        print(f"  Status: {result.status}; confidence={result.confidence:.2f}")
    total = len(CASES)
    print("-" * 60)
    print(f"Summary: {passed}/{total} tests passed ({passed / total:.0%})")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
