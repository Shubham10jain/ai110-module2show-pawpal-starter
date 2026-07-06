"""CLI demo/testing ground for the PawPal+ logic layer (pawpal_system.py)."""

from datetime import datetime

from pawpal_system import Owner, Pet, Task, Scheduler

TODAY = datetime.now().strftime("%Y-%m-%d")


def print_schedule(title, pet_tasks):
    print(f"\n=== {title} ===")
    if not pet_tasks:
        print("  (no tasks)")
        return
    for pet, task in pet_tasks:
        status = "[x]" if task.completed else "[ ]"
        print(
            f"  {status} {task.time} - {task.title} ({task.category}) "
            f"for {pet.name} | priority={task.priority} | freq={task.frequency}"
        )


def main():
    owner = Owner(name="Jordan")

    biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever")
    mochi = Pet(name="Mochi", species="cat", breed="Tabby")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    biscuit.add_task(Task(title="Morning walk", category="walk", time="08:00", priority="high", frequency="daily", date=TODAY))
    biscuit.add_task(Task(title="Evening feeding", category="feeding", time="18:00", priority="high", frequency="daily", date=TODAY))
    mochi.add_task(Task(title="Flea medication", category="medication", time="09:00", priority="medium", frequency="weekly", date=TODAY))
    # Two tasks at the same time to demonstrate conflict detection.
    mochi.add_task(Task(title="Vet checkup", category="appointment", time="08:00", priority="high", frequency="once", date=TODAY))

    scheduler = Scheduler(owner)

    print_schedule("Today's Schedule (sorted by time)", scheduler.get_today_schedule())

    conflicts = scheduler.detect_conflicts(scheduler.get_today_schedule())
    print("\n=== Conflict Warnings ===")
    if conflicts:
        for warning in conflicts:
            print(f"  WARNING: {warning}")
    else:
        print("  (no conflicts)")

    print_schedule(
        "Filtered: Biscuit's tasks only",
        scheduler.filter_tasks(pet_name="Biscuit"),
    )

    # Demonstrate recurrence: completing a daily task schedules its next occurrence.
    walk_pet, walk_task = scheduler.get_today_schedule()[0]
    next_task = scheduler.mark_task_complete(walk_pet, walk_task)
    print("\n=== After completing Biscuit's morning walk ===")
    print(f"  Next occurrence scheduled for {next_task.date} at {next_task.time}")

    print_schedule(
        "Filtered: Incomplete tasks only",
        scheduler.filter_tasks(completed=False),
    )


if __name__ == "__main__":
    main()
