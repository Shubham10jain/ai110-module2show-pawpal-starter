# PawPal+ Project Reflection

## 1. System Design

Core Action 
- Set Owner Availablity
- Add/View pets and their related tasks
- Viewing a organized daily task view

Objects-
- Owners
    * Name
    * List of Pets
    * Schedule

- Pets
    * Name
    * Type of Pet
    * Breed
    * List of tasks 
    * Medications

- Tasks
    * Name
    * Type (walk, feeding, etc..)
    * Duration (Time)
    * Priority
    * Description 


**a. Initial design**

My initial UML (`diagrams/uml.mmd`) has four classes:

- `Task` — represents a single care activity (title, category, time, duration, priority, frequency, completed). Owns the logic for marking itself complete and producing its next occurrence when recurring.
- `Pet` — holds identity info (name, species, breed, medications) and its own list of `Task` objects. Responsible for adding tasks and reporting how many it has.
- `Owner` — holds a list of `Pet` objects and can look one up by name or flatten all pets' tasks into one list. Doesn't know anything about scheduling logic itself.
- `Scheduler` — the "brain." Takes an `Owner` and is responsible for pulling tasks across all of an owner's pets, sorting/filtering them, detecting conflicts, and handling completion (including recurrence). Keeping this logic out of `Owner`/`Pet` keeps those classes simple data holders.

**b. Design changes**

After reviewing the skeleton with my AI coding assistant, I confirmed the `Scheduler` should not duplicate state — it should always read tasks live from `owner.all_tasks()` rather than keeping its own copy, so it never goes stale when a pet/task is added after the `Scheduler` is created. No structural classes changed, but this clarified that `Scheduler.owner` is a reference, not a snapshot.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers task `time` (for ordering), `date` (for "today's schedule" and conflict checks), `priority` (surfaced to the user but not currently used to reorder), `frequency` (for recurrence), and `completed` status (for filtering). Time and date mattered most because the core use case is "what do I need to do today, in what order" — priority and completion are secondary lenses layered on top via filtering rather than baked into the sort itself.

**b. Tradeoffs**

`Scheduler.detect_conflicts()` only flags tasks with the *exact same* `(date, time)` string — it does not account for task duration or overlapping time ranges (e.g., a 30-minute walk starting at 08:00 wouldn't be flagged against a task at 08:15, even though they'd overlap in real life). This is reasonable for this scenario because pet care tasks are typically quick, discrete events rather than long blocking appointments, and exact-match detection is simple, fast, and easy to reason about. A duration-aware overlap check would be a natural next step (see Testing section for edge cases I'd add next).

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

`tests/test_pawpal.py` covers: marking a task complete, adding a task increasing a pet's task count, sorting tasks chronologically, recurrence creating a next-day task for a daily task, recurrence *not* triggering for a one-time task, conflict detection flagging two tasks at the same date/time across different pets, and filtering by pet name and completion status. These matter because they're the exact behaviors the scheduler promises (accurate ordering, safe recurrence, non-crashing conflict warnings) — if any of them silently broke, the app would show a wrong or misleading daily plan to a pet owner.

**b. Confidence**

⭐⭐⭐⭐ (4/5). All 7 tests pass and cover the happy path plus a couple of edge cases (non-recurring task, multi-pet conflicts). With more time I'd test: a pet with zero tasks, weekly recurrence math across month boundaries, conflicts across midnight, and sorting stability when multiple tasks share the same time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
