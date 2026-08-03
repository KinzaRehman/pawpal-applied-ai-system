from pawpal_ai.agent import PawPalPlanningAgent
from pawpal_ai.models import Pet, Task


def test_medication_is_elevated_and_first(tmp_path):
    result = PawPalPlanningAgent(str(tmp_path / "trace.md")).build_schedule(
        [Pet("Milo", "cat", 4)],
        [
            Task("Play", "Milo", 20, "urgent", 12, "play"),
            Task("Medicine", "Milo", 10, "low", 10, "medication"),
        ],
        8,
        12,
    )
    assert result.status == "success"
    assert result.scheduled[0].category == "medication"
    assert result.scheduled[0].priority == "high"


def test_unknown_pet_is_blocked(tmp_path):
    result = PawPalPlanningAgent(str(tmp_path / "trace.md")).build_schedule(
        [Pet("Milo", "cat", 4)],
        [Task("Walk", "Luna", 20, "high", 10, "walk")],
        8,
        12,
    )
    assert result.status == "blocked"
    assert result.confidence == 0.0


def test_overflow_is_reported(tmp_path):
    result = PawPalPlanningAgent(str(tmp_path / "trace.md")).build_schedule(
        [Pet("Milo", "cat", 4)],
        [
            Task("Medicine", "Milo", 30, "high", 9, "medication"),
            Task("Grooming", "Milo", 120, "medium", 12, "grooming"),
        ],
        8,
        9,
    )
    assert result.status == "partial"
    assert "Grooming" in result.unscheduled
