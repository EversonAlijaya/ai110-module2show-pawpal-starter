"""Basic tests for the PawPal+ core classes."""

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() flips the task's completion status."""
    task = Task("Morning walk", duration=30, due_time="08:00", priority="high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet increases that pet's task count."""
    pet = Pet("Mochi", "dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Feeding", duration=10, due_time="08:45", priority="high"))

    assert len(pet.get_tasks()) == 1


def test_scheduler_skips_completed_tasks_across_pets():
    """The plan pulls tasks from every pet but leaves out completed ones."""
    owner = Owner("Jordan", available_minutes=120)
    mochi = Pet("Mochi", "dog")
    biscuit = Pet("Biscuit", "cat")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    walk = Task("Morning walk", duration=30, due_time="08:00", priority="high")
    feed = Task("Feeding", duration=10, due_time="09:00", priority="high")
    done = Task("Brush fur", duration=20, priority="low", completed=True)
    mochi.add_task(walk)
    biscuit.add_task(feed)
    biscuit.add_task(done)

    plan = Scheduler(owner).generate_plan()

    assert walk in plan and feed in plan  # tasks from both pets made it in
    assert done not in plan  # already-finished task was left out


def _household():
    owner = Owner("Jordan", available_minutes=120)
    mochi = Pet("Mochi", "dog")
    biscuit = Pet("Biscuit", "cat")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)
    return owner, mochi, biscuit


def test_sort_by_time_orders_tasks_and_puts_untimed_last():
    """Tasks come out earliest-first, with no-time tasks at the end."""
    owner, mochi, biscuit = _household()
    late = Task("Evening walk", duration=20, due_time="19:00")
    anytime = Task("Brush fur", duration=10)
    early = Task("Feeding", duration=10, due_time="07:30")
    mochi.add_task(late)
    mochi.add_task(anytime)
    biscuit.add_task(early)

    scheduler = Scheduler(owner)
    ordered = scheduler.sort_by_time(scheduler.get_all_tasks())

    assert ordered == [early, late, anytime]


def test_filter_by_pet_returns_only_that_pets_tasks():
    """Filtering by pet name only returns tasks belonging to that pet."""
    owner, mochi, biscuit = _household()
    walk = Task("Walk", duration=30, due_time="08:00")
    feed = Task("Feeding", duration=10, due_time="09:00")
    mochi.add_task(walk)
    biscuit.add_task(feed)

    scheduler = Scheduler(owner)

    assert scheduler.filter_by_pet("Mochi") == [walk]
    assert scheduler.filter_by_pet("Biscuit") == [feed]
    assert scheduler.filter_by_pet("Nonexistent") == []


def test_completing_daily_task_spawns_next_day_occurrence():
    """Completing a daily task auto-creates an incomplete copy due the next day."""
    owner, mochi, _ = _household()
    walk = Task("Walk", duration=30, due_time="08:00", frequency="daily", due_date="2026-07-06")
    mochi.add_task(walk)

    follow_up = mochi.complete_task(walk)

    assert walk.completed is True
    assert follow_up in mochi.tasks
    assert follow_up.completed is False
    assert follow_up.due_date == "2026-07-07"
    assert follow_up.due_time == "08:00"


def test_completing_one_time_task_spawns_nothing():
    """Completing a non-recurring task does not create a follow-up."""
    owner, mochi, _ = _household()
    brush = Task("Brush fur", duration=10)
    mochi.add_task(brush)

    assert mochi.complete_task(brush) is None
    assert len(mochi.tasks) == 1


def test_find_conflicts_flags_same_time_tasks_across_pets():
    """Two incomplete tasks at the same date and time produce one warning."""
    owner, mochi, biscuit = _household()
    mochi.add_task(Task("Walk", duration=30, due_time="08:00"))
    biscuit.add_task(Task("Medication", duration=5, due_time="08:00"))
    biscuit.add_task(Task("Feeding", duration=10, due_time="09:00"))

    warnings = Scheduler(owner).find_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Walk" in warnings[0] and "Medication" in warnings[0]


def test_no_conflict_for_same_time_on_different_days():
    """Same clock time on different dates is not a conflict."""
    owner, mochi, biscuit = _household()
    mochi.add_task(Task("Walk", duration=30, due_time="08:00", due_date="2026-07-06"))
    biscuit.add_task(Task("Medication", duration=5, due_time="08:00", due_date="2026-07-07"))

    assert Scheduler(owner).find_conflicts() == []
