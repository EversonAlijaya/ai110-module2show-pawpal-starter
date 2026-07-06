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

The suite covers task completion (`mark_complete` flips the status), task management (adding a task to a pet grows its task list), scheduling (the plan includes tasks from multiple pets and skips completed ones), sorting correctness (earliest first, untimed last), filtering by pet, recurring tasks (completing a daily task spawns a next-day copy; one-time tasks don't), and conflict detection (same time flagged, different days not flagged).

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
collected 9 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 11%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 22%]
tests/test_pawpal.py::test_scheduler_skips_completed_tasks_across_pets PASSED [ 33%]
tests/test_pawpal.py::test_sort_by_time_orders_tasks_and_puts_untimed_last PASSED [ 44%]
tests/test_pawpal.py::test_filter_by_pet_returns_only_that_pets_tasks PASSED [ 55%]
tests/test_pawpal.py::test_completing_daily_task_spawns_next_day_occurrence PASSED [ 66%]
tests/test_pawpal.py::test_completing_one_time_task_spawns_nothing PASSED [ 77%]
tests/test_pawpal.py::test_find_conflicts_flags_same_time_tasks_across_pets PASSED [ 88%]
tests/test_pawpal.py::test_no_conflict_for_same_time_on_different_days PASSED [100%]

============================== 9 passed in 0.01s ===============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_tasks()` | `sort_by_time` orders tasks by "HH:MM" due time (untimed tasks go last); `sort_tasks` orders by priority (high → low) with duration as tiebreaker |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Filter all tasks across pets by pet name, or by completed/pending status |
| Conflict handling | `Scheduler.find_conflicts()` | Flags incomplete tasks scheduled at the same date + time (across any pets) and returns human-readable warnings instead of crashing |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a "daily"/"weekly" task auto-creates a fresh copy due one day/week later (via `timedelta`); one-time tasks spawn nothing |

The daily plan itself (`Scheduler.generate_plan()`) combines these: it filters out completed and future-dated tasks, sorts by priority, fits what it can into the owner's available minutes, and presents the result in time order.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
