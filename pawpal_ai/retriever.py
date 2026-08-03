from pathlib import Path
from typing import Dict, Iterable, List

from .models import Pet, Task


class PetCareRetriever:
    """
    Retrieves relevant pet-care guidance from local Markdown documents.

    The retrieved guidance is used by the planning agent before it creates
    the schedule.
    """

    def __init__(self, knowledge_directory: str = "knowledge") -> None:
        self.knowledge_directory = Path(knowledge_directory)

    def retrieve(
        self,
        pets: Iterable[Pet],
        tasks: Iterable[Task],
    ) -> Dict[str, List[str]]:
        pets = list(pets)
        tasks = list(tasks)

        species = {pet.species.lower().strip() for pet in pets}
        categories = {task.category.lower().strip() for task in tasks}

        retrieved: Dict[str, List[str]] = {}

        for pet_species in species:
            document_path = self.knowledge_directory / f"{pet_species}_care.md"

            if not document_path.exists():
                retrieved[pet_species] = [
                    f"No custom guidance document was found for {pet_species}."
                ]
                continue

            document = document_path.read_text(encoding="utf-8")
            sections = self._split_sections(document)

            relevant_sections: List[str] = []

            for category in categories:
                matching_section = sections.get(category)

                if matching_section:
                    relevant_sections.append(
                        f"{category.title()}: {matching_section}"
                    )

            safety_section = sections.get("safety")

            if safety_section:
                relevant_sections.append(f"Safety: {safety_section}")

            if not relevant_sections:
                relevant_sections.append(
                    "The knowledge document was loaded, but no task-specific "
                    "section matched the submitted categories."
                )

            retrieved[pet_species] = relevant_sections

        return retrieved

    def _split_sections(self, document: str) -> Dict[str, str]:
        sections: Dict[str, str] = {}
        current_heading = None
        current_lines: List[str] = []

        for raw_line in document.splitlines():
            line = raw_line.strip()

            if line.startswith("## "):
                if current_heading:
                    sections[current_heading] = " ".join(current_lines).strip()

                current_heading = line[3:].strip().lower()
                current_lines = []
            elif current_heading and line:
                current_lines.append(line.lstrip("- ").strip())

        if current_heading:
            sections[current_heading] = " ".join(current_lines).strip()

        return sections