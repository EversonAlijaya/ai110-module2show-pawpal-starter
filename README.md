# PawPal+ (Module 2 Project)

**PawPal+** is a pet care planning assistant. A busy pet owner tells it how much time they have, what pets they care for, and what tasks each pet needs. PawPal+ builds a realistic daily schedule: high-priority tasks first, everything fitted to the available time, presented in time order, with clear warnings for anything that could not fit or that clashes.

It ships as two front ends over one logic layer: a Streamlit web app (`app.py`) and a CLI demo script (`main.py`), both powered by the classes in `pawpal_system.py`.

## ✨ Features

- **Daily plan generation**: fits tasks into the owner's available minutes, choosing by priority (high, then medium, then low) with shorter tasks winning ties.
- **Sorting by time**: any task list can be displayed in chronological order, with "anytime" tasks at the end.
- **Filtering**: view tasks for a single pet, or by completed/pending status, across the whole household.
- **Conflict warnings**: two tasks booked at the same date and time produce a readable warning instead of a silent double-booking.
- **Daily and weekly recurrence**: completing a recurring task automatically creates the next occurrence (tomorrow or next week) with the same details.
- **Skipped-task explanations**: anything that did not fit is listed with its full details plus exactly how many more minutes it would have needed.

## 🧱 System Design

The logic layer is four classes (see `diagrams/uml_final.mmd` for the full UML):

| Class | Responsibility |
|-------|----------------|
| `Task` | One care activity: description, duration, due time/date, priority, how often it repeats, and completion status. Knows how to spawn its own next occurrence. |
| `Pet` | A pet's identity plus its list of tasks, with methods to add, remove, and complete them. |
| `Owner` | The human: name, minutes available today, preferences, and the list of pets. Aggregates every task across all pets. |
| `Scheduler` | The brain. Reads tasks through the Owner and provides sorting, filtering, conflict detection, and daily plan generation. |

`diagrams/uml.mmd` is the original Phase 1 draft, kept for comparison with the final design.

## 🚀 Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run it

```bash
# Web app:
streamlit run app.py

# CLI demo (prints the full feature walkthrough shown below):
python main.py

# Tests:
python -m pytest
```

## 🖥️ Sample Output

Output from running `python main.py` (the CLI demo script):

```
========================================================
  PawPal+ — Jordan's day
  Pets: Mochi (dog, Golden Retriever), Biscuit (cat, Tabby)
  Time available: 80 minutes
========================================================

--- All tasks, sorted by time (added out of order) -----
    08:00  Morning walk           Mochi     30 min  [high]
    08:00  Give medication        Biscuit    5 min  [high]
    08:45  Feeding                Mochi     10 min  [high]
    09:00  Feeding                Biscuit   10 min  [high]
    17:00  Fetch practice         Mochi     25 min  [low]
    19:30  Litter box cleaning    Biscuit   15 min  [medium]
  anytime  Brush fur              Biscuit   20 min  [low]

--- Filter: only Mochi's tasks -------------------------
    17:00  Fetch practice         Mochi     25 min  [low]
    08:00  Morning walk           Mochi     30 min  [high]
    08:45  Feeding                Mochi     10 min  [high]

--- Conflict check -------------------------------------
  ⚠ Conflict at 08:00: 'Morning walk' (Mochi) and 'Give medication' (Biscuit) are scheduled at the same time.

--- Recurring: completing 'Morning walk' (daily) -------
  Completed: Morning walk — done today
  Auto-created next occurrence: Morning walk on 2026-07-07 at 08:00

--- Filter: completed vs pending -----------------------
  Completed: 1 task(s)
  Pending:   7 task(s)

--- Today's schedule -----------------------------------
    08:00  Give medication        Biscuit    5 min  [high]
    08:45  Feeding                Mochi     10 min  [high]
    09:00  Feeding                Biscuit   10 min  [high]
    19:30  Litter box cleaning    Biscuit   15 min  [medium]
  anytime  Brush fur              Biscuit   20 min  [low]
--------------------------------------------------------
  Scheduled: 5 tasks, 60 of 80 min used
  Skipped (only 20 min left in the day):
    17:00  Fetch practice         Mochi     25 min  [low]  needs 5 more min
========================================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

The suite covers both happy paths and edge cases:

- **Task behavior** — `mark_complete` flips the status; adding a task to a pet grows its task list.
- **Sorting correctness** — tasks come out in chronological order, with untimed tasks last.
- **Filtering** — by pet name (unknown pets return an empty list, not an error).
- **Recurring tasks** — completing a daily task auto-creates a copy due the next day; one-time tasks don't.
- **Conflict detection** — two tasks at the same time are flagged; the same time on different days is not.
- **Edge cases** — an owner with no pets, a pet with no tasks, a task longer than the entire time budget, and priority winning over duration when only one task fits.

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
collected 13 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  7%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 15%]
tests/test_pawpal.py::test_scheduler_skips_completed_tasks_across_pets PASSED [ 23%]
tests/test_pawpal.py::test_sort_by_time_orders_tasks_and_puts_untimed_last PASSED [ 30%]
tests/test_pawpal.py::test_filter_by_pet_returns_only_that_pets_tasks PASSED [ 38%]
tests/test_pawpal.py::test_completing_daily_task_spawns_next_day_occurrence PASSED [ 46%]
tests/test_pawpal.py::test_completing_one_time_task_spawns_nothing PASSED [ 53%]
tests/test_pawpal.py::test_find_conflicts_flags_same_time_tasks_across_pets PASSED [ 61%]
tests/test_pawpal.py::test_no_conflict_for_same_time_on_different_days PASSED [ 69%]
tests/test_pawpal.py::test_owner_with_no_pets_produces_empty_plan_without_crashing PASSED [ 76%]
tests/test_pawpal.py::test_pet_with_no_tasks_is_handled PASSED           [ 84%]
tests/test_pawpal.py::test_task_longer_than_budget_is_skipped PASSED     [ 92%]
tests/test_pawpal.py::test_high_priority_wins_over_low_when_time_is_tight PASSED [100%]

============================== 13 passed in 0.02s ==============================
```

**Confidence level: ★★★★☆ (4/5).** The core behaviors (sorting, filtering, recurrence, conflict detection, and time-budget planning) are each locked in by at least one test, including the empty and boundary cases. The missing star is for what the suite deliberately doesn't cover: conflict detection only checks exact start-time matches, not duration overlaps, and time inputs are trusted to be valid "HH:MM" strings since the UI constrains them. With more time, overlap detection and malformed-input handling would be the next tests to add.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_tasks()` | `sort_by_time` orders tasks by "HH:MM" due time (untimed tasks go last); `sort_tasks` orders by priority (high → low) with duration as tiebreaker |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Filter all tasks across pets by pet name, or by completed/pending status |
| Conflict handling | `Scheduler.find_conflicts()` | Flags incomplete tasks scheduled at the same date + time (across any pets) and returns human-readable warnings instead of crashing |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a "daily"/"weekly" task auto-creates a fresh copy due one day/week later (via `timedelta`); one-time tasks spawn nothing |

The daily plan itself (`Scheduler.generate_plan()`) combines these: it filters out completed and future-dated tasks, sorts by priority, fits what it can into the owner's available minutes, and presents the result in time order.

## 📸 Demo Walkthrough

Launch the app with `streamlit run app.py` and follow this workflow:

1. **Set up the owner.** Enter your name and how many minutes you have for pet care today. The scheduler treats this as a hard budget: change it and the next generated plan adapts.
2. **Add pets.** Give each pet a name, species, and optionally a breed, then click *Add pet*. The app supports any number of pets, and every feature below works across all of them.
3. **Add tasks.** Pick which pet the task is for, describe it (walk, feeding, medication), and set its duration, due time, priority, and whether it repeats (once, daily, or weekly). Click *Add task*.
4. **Browse the task table.** Tasks display in time order (the `sort_by_time` feature). Use the two dropdowns to filter by pet or by pending/done status: the same `filter_by_pet` and `filter_by_status` methods the tests verify.
5. **Complete tasks as you do them.** Select a task and click *Complete*. If it was daily or weekly, a green message confirms the next occurrence was auto-created, and it appears in the table with tomorrow's (or next week's) date.
6. **Generate the schedule.** Click *Generate schedule*. The plan appears as a time-ordered table showing when each task happens, for which pet, and its priority. Above it, yellow warnings flag any two tasks booked at the same time (conflict detection). Below it, each task that did not fit is listed with how many more minutes it would have needed.

The same workflow runs end to end in the terminal via `python main.py`; its full output is the fenced code block in the **Sample Output** section above, demonstrating sorting, filtering, recurrence, conflict detection, and the generated plan with a skipped task.
