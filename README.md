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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
