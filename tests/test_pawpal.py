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
