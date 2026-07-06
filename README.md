# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Owner & Pet management** — add multiple pets per owner, each with species/breed and its own list of care tasks.
- **Task tracking** — represent walks, feedings, medications, and appointments with a time, category, priority, and recurrence frequency.
- **Sorting by time** — `Scheduler.sort_by_time()` always shows today's tasks in chronological order.
- **Filtering** — `Scheduler.filter_tasks()` narrows the view down to one pet's tasks and/or only incomplete tasks.
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags two tasks scheduled at the same time instead of silently double-booking.
- **Daily/weekly recurrence** — completing a recurring task via `Scheduler.mark_task_complete()` automatically schedules its next occurrence.
- **Streamlit UI** — add pets/tasks and generate a live daily schedule with success/warning banners, backed by `st.session_state` so data persists across reruns.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
=== Today's Schedule (sorted by time) ===
  [ ] 08:00 - Morning walk (walk) for Biscuit | priority=high | freq=daily
  [ ] 08:00 - Vet checkup (appointment) for Mochi | priority=high | freq=once
  [ ] 09:00 - Flea medication (medication) for Mochi | priority=medium | freq=weekly
  [ ] 18:00 - Evening feeding (feeding) for Biscuit | priority=high | freq=daily

=== Conflict Warnings ===
  WARNING: Conflict at 08:00 on 2026-07-06: 'Morning walk' (Biscuit) overlaps with 'Vet checkup' (Mochi)

=== Filtered: Biscuit's tasks only ===
  [ ] 08:00 - Morning walk (walk) for Biscuit | priority=high | freq=daily
  [ ] 18:00 - Evening feeding (feeding) for Biscuit | priority=high | freq=daily

=== After completing Biscuit's morning walk ===
  Next occurrence scheduled for 2026-07-07 at 08:00

=== Filtered: Incomplete tasks only ===
  [ ] 18:00 - Evening feeding (feeding) for Biscuit | priority=high | freq=daily
  [ ] 08:00 - Morning walk (walk) for Biscuit | priority=high | freq=daily
  [ ] 09:00 - Flea medication (medication) for Mochi | priority=medium | freq=weekly
  [ ] 08:00 - Vet checkup (appointment) for Mochi | priority=high | freq=once
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.9, pytest-9.0.3, pluggy-1.6.0
collected 7 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 14%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 28%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 42%]
tests/test_pawpal.py::test_recurrence_creates_task_for_next_day PASSED   [ 57%]
tests/test_pawpal.py::test_recurrence_does_not_trigger_for_one_time_task PASSED [ 71%]
tests/test_pawpal.py::test_detect_conflicts_flags_same_time_same_day PASSED [ 85%]
tests/test_pawpal.py::test_filter_tasks_by_pet_name_and_completion PASSED [100%]

============================== 7 passed in 0.02s ===============================
```

**Confidence Level:** ⭐⭐⭐⭐ (4/5) — Core behaviors (completion, task counts, sorting, recurrence, conflict detection, filtering) are all covered and passing. I'd want to add more edge cases (pet with zero tasks, tasks at midnight/end-of-day boundaries, weekly recurrence math) before calling it 5/5.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts `(pet, task)` pairs chronologically using `task.time` ("HH:MM") as the sort key. |
| Filtering | `Scheduler.filter_tasks(pet_name=..., completed=...)` | Filters by pet name and/or completion status; either can be applied alone or together. |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags any two tasks that share the same `(date, time)` and returns human-readable warning strings instead of raising an error. |
| Recurring tasks | `Task.next_occurrence()` + `Scheduler.mark_task_complete()` | Completing a `daily`/`weekly` task automatically creates and schedules its next occurrence (`+1` or `+7` days) via `datetime.timedelta`. |

## 📸 Demo Walkthrough

**Main UI features:** On launch, the app shows an "Add a Pet" form, an "Add a Task" form (once at least one pet exists), and a "Generate schedule" button that displays today's tasks as a table with conflict warnings.

**Example workflow:**

1. Enter a pet name (e.g., "Biscuit"), pick a species, and click **Add pet**. The pet now appears in the "Current pets" list.
2. Select the pet from the "Add a Task" dropdown, fill in a title, time ("08:00"), priority, category, and frequency, then click **Add task**. Repeat for a second task at the same or a different time.
3. Click **Generate schedule**. The app calls `Scheduler.get_today_schedule()`, which internally sorts today's tasks by time (`Scheduler.sort_by_time()`) and displays them in a table with columns for time, pet, task, category, priority, frequency, and completion status.
4. If two tasks share the same time, `Scheduler.detect_conflicts()` runs against the displayed schedule and an `st.warning()` banner appears below the table naming both conflicting tasks and pets.
5. If there are no conflicts, an `st.success()` banner confirms the schedule is conflict-free.
6. Because the `Owner` object lives in `st.session_state`, pets and tasks persist as you keep adding more and re-generating the schedule, instead of resetting on every rerun.

**Key Scheduler behaviors shown:** chronological sorting, live conflict detection, and multi-pet task aggregation via `Owner.all_tasks()`.

**Sample CLI output** (from `python main.py`, which also exercises filtering and recurrence — see the [Sample Output](#️-sample-output) section above for the full run):

```
=== Today's Schedule (sorted by time) ===
  [ ] 08:00 - Morning walk (walk) for Biscuit | priority=high | freq=daily
  [ ] 08:00 - Vet checkup (appointment) for Mochi | priority=high | freq=once
  [ ] 09:00 - Flea medication (medication) for Mochi | priority=medium | freq=weekly
  [ ] 18:00 - Evening feeding (feeding) for Biscuit | priority=high | freq=daily

=== Conflict Warnings ===
  WARNING: Conflict at 08:00 on 2026-07-06: 'Morning walk' (Biscuit) overlaps with 'Vet checkup' (Mochi)
```

**Screenshot or video** *(optional)*: not included — the text walkthrough and CLI output above cover the gradable demo requirements.
