"""PawPal+ core classes.

Generated from the UML draft in diagrams/uml.mmd, then implemented in Phase 2.

Data flows Owner -> Pet -> Task: an Owner manages multiple Pets, each Pet
owns its list of Tasks, and the Scheduler retrieves tasks by walking that
chain through the Owner rather than holding its own separate task list.
"""

from dataclasses import dataclass, field

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """Represents a single care activity to be scheduled."""

    description: str
    duration: int
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def edit(self, description: str = None, duration: int = None, priority: str = None) -> None:
        """Modify the task's details, leaving unspecified fields unchanged."""
        if description is not None:
            self.description = description
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority

    def is_high_priority(self) -> bool:
        """Return whether this task is high priority."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not yet completed."""
        self.completed = False


@dataclass
class Pet:
    """Represents a pet being cared for, along with its care tasks."""

    name: str
    species: str
    breed: str = ""
    notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def describe(self) -> str:
        """Return a short human-readable description of the pet."""
        breed_part = f", {self.breed}" if self.breed else ""
        return f"{self.name} ({self.species}{breed_part})"

    def update_notes(self, notes: str) -> None:
        """Update the pet's care notes."""
        self.notes = notes

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks


class Owner:
    """Represents the pet owner, their pets, and their daily constraints."""

    def __init__(self, name: str, available_minutes: int, preferences: dict | None = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences if preferences is not None else {}
        self.pets: list[Pet] = []

    def update_availability(self, minutes: int) -> None:
        """Change the owner's daily time budget."""
        self.available_minutes = minutes

    def set_preference(self, key: str, value) -> None:
        """Record an owner preference."""
        self.preferences[key] = value

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's care."""
        self.pets.remove(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves tasks from an Owner's pets, organizes them, and builds a plan."""

    def __init__(self, owner: Owner):
        self.owner = owner
        self.plan: list[Task] = []

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks across the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (high first), then by shorter duration."""
        return sorted(tasks, key=lambda task: (PRIORITY_ORDER.get(task.priority, 1), task.duration))

    def generate_plan(self) -> list[Task]:
        """Fit incomplete tasks into available time and produce the daily plan."""
        candidates = [task for task in self.get_all_tasks() if not task.completed]
        ordered = self.sort_tasks(candidates)

        plan = []
        minutes_left = self.owner.available_minutes
        for task in ordered:
            if task.duration <= minutes_left:
                plan.append(task)
                minutes_left -= task.duration

        self.plan = plan
        return self.plan

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why the plan was chosen."""
        if not self.plan:
            return "No tasks fit into today's plan."

        lines = [f"Today's plan ({self.owner.available_minutes} minutes available):"]
        for task in self.plan:
            lines.append(f"- {task.description} ({task.duration} min, {task.priority} priority)")
        return "\n".join(lines)
