"""PawPal+ logic layer: Owner, Pet, Task, and Scheduler classes."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta

VALID_FREQUENCIES = {"once", "daily", "weekly"}


@dataclass
class Task:
    """A single pet care activity (walk, feeding, medication, appointment)."""

    title: str
    category: str
    time: str  # "HH:MM" 24-hour format
    duration_minutes: int = 15
    priority: str = "medium"  # "low" | "medium" | "high"
    frequency: str = "once"  # "once" | "daily" | "weekly"
    completed: bool = False
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

    def mark_complete(self):
        """Flip this task's completed flag to True."""
        self.completed = True

    def next_occurrence(self):
        """Return a new Task for the next occurrence, or None if not recurring."""
        if self.frequency not in ("daily", "weekly"):
            return None
        days_ahead = 1 if self.frequency == "daily" else 7
        current_date = datetime.strptime(self.date, "%Y-%m-%d")
        next_date = current_date + timedelta(days=days_ahead)
        return Task(
            title=self.title,
            category=self.category,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            completed=False,
            date=next_date.strftime("%Y-%m-%d"),
        )


@dataclass
class Pet:
    """A pet owned by an Owner, with its own care tasks."""

    name: str
    species: str
    breed: str = ""
    medications: list = field(default_factory=list)
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Attach a Task to this pet."""
        self.tasks.append(task)

    def task_count(self) -> int:
        """Return how many tasks this pet has."""
        return len(self.tasks)


@dataclass
class Owner:
    """A pet owner who manages one or more Pets."""

    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a Pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_pet(self, name: str):
        """Look up a pet by name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def all_tasks(self):
        """Flatten and return every task across all of this owner's pets, tagged with the pet name."""
        tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                tasks.append((pet, task))
        return tasks


class Scheduler:
    """The 'brain' that retrieves, organizes, and manages tasks across an Owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_today_schedule(self):
        """Return today's tasks (pet, task pairs), sorted by time."""
        today = datetime.now().strftime("%Y-%m-%d")
        todays = [pt for pt in self.owner.all_tasks() if pt[1].date == today]
        return self.sort_by_time(todays)

    def sort_by_time(self, pet_tasks):
        """Sort a list of (pet, task) pairs chronologically by task.time (HH:MM)."""
        return sorted(pet_tasks, key=lambda pt: pt[1].time)

    def filter_tasks(self, pet_tasks=None, pet_name=None, completed=None):
        """Filter (pet, task) pairs by pet name and/or completion status."""
        if pet_tasks is None:
            pet_tasks = self.owner.all_tasks()
        result = pet_tasks
        if pet_name is not None:
            result = [pt for pt in result if pt[0].name == pet_name]
        if completed is not None:
            result = [pt for pt in result if pt[1].completed == completed]
        return result

    def detect_conflicts(self, pet_tasks=None):
        """Return a list of warning strings for tasks scheduled at the same date/time."""
        if pet_tasks is None:
            pet_tasks = self.owner.all_tasks()
        warnings = []
        seen = {}
        for pet, task in pet_tasks:
            key = (task.date, task.time)
            if key in seen:
                other_pet, other_task = seen[key]
                warnings.append(
                    f"Conflict at {task.time} on {task.date}: "
                    f"'{other_task.title}' ({other_pet.name}) overlaps with "
                    f"'{task.title}' ({pet.name})"
                )
            else:
                seen[key] = (pet, task)
        return warnings

    def mark_task_complete(self, pet: Pet, task: Task):
        """Mark a task complete; if it recurs, schedule its next occurrence."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            pet.add_task(next_task)
        return next_task
