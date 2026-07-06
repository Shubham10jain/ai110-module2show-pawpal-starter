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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
