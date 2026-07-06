"""PawPal+ logic layer: Owner, Pet, Task, and Scheduler classes."""

from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    category: str
    time: str
    duration_minutes: int = 15
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self):
        pass

    def next_occurrence(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    medications: list = field(default_factory=list)
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def task_count(self) -> int:
        pass


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def get_pet(self, name: str):
        pass

    def all_tasks(self):
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_today_schedule(self):
        pass

    def sort_by_time(self, tasks):
        pass

    def filter_tasks(self, pet_name=None, completed=None):
        pass

    def detect_conflicts(self, tasks):
        pass

    def mark_task_complete(self, pet: Pet, task: Task):
        pass
