"""PawPal+ core classes (skeleton).

Generated from the UML draft in diagrams/uml_draft.mmd.
These are stubs only — attributes and empty method bodies. No scheduling
logic yet; that gets implemented in a later phase.

Pet and Task use dataclasses to keep the data objects clean.
"""

from dataclasses import dataclass, field


@dataclass
class Pet:
    """Represents the pet being cared for."""

    name: str
    species: str
    breed: str = ""
    notes: str = ""

    def describe(self) -> str:
        """Return a short human-readable description of the pet."""
        raise NotImplementedError

    def update_notes(self, notes: str) -> None:
        """Update the pet's care notes."""
        raise NotImplementedError


@dataclass
class Task:
    """Represents a single care task to be scheduled."""

    name: str
    duration: int
    priority: str
    recurring: bool = False

    def edit(self, name: str, duration: int, priority: str) -> None:
        """Modify the task's details."""
        raise NotImplementedError

    def is_high_priority(self) -> bool:
        """Return whether this task is high priority."""
        raise NotImplementedError


class Owner:
    """Represents the pet owner and their daily constraints."""

    def __init__(self, name: str, available_minutes: int, preferences: dict | None = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences if preferences is not None else {}

    def update_availability(self, minutes: int) -> None:
        """Change the owner's daily time budget."""
        raise NotImplementedError

    def set_preference(self, key: str, value) -> None:
        """Record an owner preference."""
        raise NotImplementedError


class Scheduler:
    """Builds the daily plan from tasks and constraints, and explains it."""

    def __init__(self, owner: Owner, tasks: list[Task] | None = None):
        self.owner = owner
        self.tasks: list[Task] = tasks if tasks is not None else []
        self.plan: list = []

    def add_task(self, task: Task) -> None:
        """Add a task to the pool."""
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pool."""
        raise NotImplementedError

    def sort_tasks(self) -> None:
        """Order tasks by priority (with duration as a tiebreaker)."""
        raise NotImplementedError

    def generate_plan(self) -> list:
        """Fit tasks into available time and produce the daily plan."""
        raise NotImplementedError

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why the plan was chosen."""
        raise NotImplementedError
