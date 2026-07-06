"""Automated tests for the PawPal+ logic layer."""

from pawpal_system import Owner, Pet, Task, Scheduler


def make_owner_with_pet():
    owner = Owner(name="Jordan")
    pet = Pet(name="Biscuit", species="dog")
    owner.add_pet(pet)
    return owner, pet


# --- Phase 2: Core behaviors ---


def test_mark_complete_changes_status():
    task = Task(title="Walk", category="walk", time="08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog")
    assert pet.task_count() == 0
    pet.add_task(Task(title="Walk", category="walk", time="08:00"))
    assert pet.task_count() == 1


# --- Phase 5: Algorithmic behaviors ---


def test_sort_by_time_returns_chronological_order():
    owner, pet = make_owner_with_pet()
    pet.add_task(Task(title="Evening feeding", category="feeding", time="18:00"))
    pet.add_task(Task(title="Morning walk", category="walk", time="08:00"))
    pet.add_task(Task(title="Midday check-in", category="other", time="12:00"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(owner.all_tasks())
    times = [task.time for _, task in sorted_tasks]

    assert times == ["08:00", "12:00", "18:00"]


def test_recurrence_creates_task_for_next_day():
    owner, pet = make_owner_with_pet()
    task = Task(title="Morning walk", category="walk", time="08:00", frequency="daily", date="2026-07-06")
    pet.add_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(pet, task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.date == "2026-07-07"
    assert next_task.completed is False
    assert pet.task_count() == 2


def test_recurrence_does_not_trigger_for_one_time_task():
    owner, pet = make_owner_with_pet()
    task = Task(title="Vet checkup", category="appointment", time="09:00", frequency="once")
    pet.add_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(pet, task)

    assert next_task is None
    assert pet.task_count() == 1


def test_detect_conflicts_flags_same_time_same_day():
    owner, pet = make_owner_with_pet()
    other_pet = Pet(name="Mochi", species="cat")
    owner.add_pet(other_pet)

    pet.add_task(Task(title="Morning walk", category="walk", time="08:00", date="2026-07-06"))
    other_pet.add_task(Task(title="Vet checkup", category="appointment", time="08:00", date="2026-07-06"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(owner.all_tasks())

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_filter_tasks_by_pet_name_and_completion():
    owner, pet = make_owner_with_pet()
    other_pet = Pet(name="Mochi", species="cat")
    owner.add_pet(other_pet)

    pet.add_task(Task(title="Walk", category="walk", time="08:00", completed=True))
    other_pet.add_task(Task(title="Feed", category="feeding", time="09:00", completed=False))

    scheduler = Scheduler(owner)

    biscuit_only = scheduler.filter_tasks(pet_name="Biscuit")
    assert len(biscuit_only) == 1
    assert biscuit_only[0][0].name == "Biscuit"

    incomplete_only = scheduler.filter_tasks(completed=False)
    assert len(incomplete_only) == 1
    assert incomplete_only[0][1].title == "Feed"
