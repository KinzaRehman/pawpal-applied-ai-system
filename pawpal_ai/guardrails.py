from typing import Iterable, List
from .models import Pet, Task


ALLOWED_PRIORITIES = {"low", "medium", "high", "urgent"}
ALLOWED_CATEGORIES = {
    "feeding", "medication", "walk", "grooming",
    "cleaning", "play", "appointment", "general"
}


class ValidationError(ValueError):
    """Raised when input cannot safely be scheduled."""


def validate_inputs(
    pets: Iterable[Pet],
    tasks: Iterable[Task],
    available_start_hour: int,
    available_end_hour: int,
) -> List[str]:
    warnings: List[str] = []
    pets = list(pets)
    tasks = list(tasks)

    if not pets:
        raise ValidationError("At least one pet is required.")
    if not tasks:
        raise ValidationError("At least one task is required.")
    if not 0 <= available_start_hour <= 23 or not 1 <= available_end_hour <= 24:
        raise ValidationError("Availability hours must be between 0 and 24.")
    if available_start_hour >= available_end_hour:
        raise ValidationError("Start hour must be earlier than end hour.")

    pet_names = {pet.name.lower() for pet in pets}
    if len(pet_names) != len(pets):
        raise ValidationError("Pet names must be unique.")

    for pet in pets:
        if not pet.name.strip():
            raise ValidationError("Pet name cannot be empty.")
        if pet.age < 0:
            raise ValidationError(f"Age cannot be negative for {pet.name}.")

    seen_tasks = set()
    for task in tasks:
        if not task.name.strip():
            raise ValidationError("Task name cannot be empty.")
        if task.pet_name.lower() not in pet_names:
            raise ValidationError(
                f"Task '{task.name}' references unknown pet '{task.pet_name}'."
            )
        if not 5 <= task.duration_minutes <= 240:
            raise ValidationError(
                f"Task '{task.name}' duration must be between 5 and 240 minutes."
            )
        if task.priority.lower() not in ALLOWED_PRIORITIES:
            raise ValidationError(
                f"Task '{task.name}' has invalid priority '{task.priority}'."
            )
        if task.category.lower() not in ALLOWED_CATEGORIES:
            warnings.append(
                f"Task '{task.name}' uses uncommon category '{task.category}'; "
                "treated as general."
            )
        if not 0 <= task.due_hour <= 23:
            raise ValidationError(
                f"Task '{task.name}' due hour must be between 0 and 23."
            )

        key = (task.name.lower(), task.pet_name.lower())
        if key in seen_tasks:
            warnings.append(
                f"Possible duplicate task: '{task.name}' for {task.pet_name}."
            )
        seen_tasks.add(key)

        if task.category.lower() == "medication" and task.priority.lower() in {"low", "medium"}:
            warnings.append(
                f"Medication task '{task.name}' was elevated to high priority."
            )

    return warnings
