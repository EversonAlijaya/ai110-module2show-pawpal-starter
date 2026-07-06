"""PawPal+ CLI demo.

Builds a small household (one owner, two pets, several tasks) and walks
through the scheduler's features: sorting, filtering, recurring tasks,
conflict detection, and the daily plan. Run with: python main.py
"""

from pawpal_system import Owner, Pet, Scheduler, Task

WIDTH = 56


def pet_name_for(task: Task, owner: Owner) -> str:
    """Find which of the owner's pets a task belongs to."""
    for pet in owner.pets:
        if task in pet.tasks:
            return pet.name
    return "?"


def print_task_row(task: Task, owner: Owner, extra: str = "") -> None:
    """Print one task as an aligned schedule row."""
    when = task.due_time if task.due_time else "anytime"
    print(f"  {when:>7}  {task.description:<22} {pet_name_for(task, owner):<8} {task.duration:>3} min  [{task.priority}]{extra}")


def header(title: str) -> None:
    print()
    print(f"--- {title} " + "-" * max(0, WIDTH - len(title) - 5))


def main() -> None:
    owner = Owner("Jordan", available_minutes=80)
    mochi = Pet("Mochi", "dog", "Golden Retriever")
    biscuit = Pet("Biscuit", "cat", "Tabby")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    mochi.add_task(Task("Fetch practice", duration=25, due_time="17:00", priority="low"))
    biscuit.add_task(Task("Litter box cleaning", duration=15, due_time="19:30", priority="medium", frequency="daily"))
    mochi.add_task(Task("Morning walk", duration=30, due_time="08:00", priority="high", frequency="daily"))
    biscuit.add_task(Task("Brush fur", duration=20, priority="low"))
    biscuit.add_task(Task("Give medication", duration=5, due_time="08:00", priority="high", frequency="daily"))
    mochi.add_task(Task("Feeding", duration=10, due_time="08:45", priority="high", frequency="daily"))
    biscuit.add_task(Task("Feeding", duration=10, due_time="09:00", priority="high", frequency="daily"))

    scheduler = Scheduler(owner)

    print("=" * WIDTH)
    print(f"  PawPal+ — {owner.name}'s day")
    print(f"  Pets: {', '.join(pet.describe() for pet in owner.pets)}")
    print(f"  Time available: {owner.available_minutes} minutes")
    print("=" * WIDTH)

    header("All tasks, sorted by time (added out of order)")
    for task in scheduler.sort_by_time(scheduler.get_all_tasks()):
        print_task_row(task, owner)

    header("Filter: only Mochi's tasks")
    for task in scheduler.filter_by_pet("Mochi"):
        print_task_row(task, owner)

    header("Conflict check")
    conflicts = scheduler.find_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  ⚠ {warning}")
    else:
        print("  No conflicts found.")

    header("Recurring: completing 'Morning walk' (daily)")
    walk = next(t for t in scheduler.filter_by_pet("Mochi") if t.description == "Morning walk")
    follow_up = mochi.complete_task(walk)
    print(f"  Completed: {walk.description} — done today")
    print(f"  Auto-created next occurrence: {follow_up.description} on {follow_up.due_date} at {follow_up.due_time}")

    header("Filter: completed vs pending")
    print(f"  Completed: {len(scheduler.filter_by_status(True))} task(s)")
    print(f"  Pending:   {len(scheduler.filter_by_status(False))} task(s)")

    header("Today's schedule")
    plan = scheduler.generate_plan()
    total = 0
    for task in plan:
        print_task_row(task, owner)
        total += task.duration

    print("-" * WIDTH)
    print(f"  Scheduled: {len(plan)} tasks, {total} of {owner.available_minutes} min used")

    minutes_left = owner.available_minutes - total
    skipped = [t for t in scheduler.filter_by_status(False) if t not in plan and not t.due_date]
    if skipped:
        print(f"  Skipped (only {minutes_left} min left in the day):")
    for task in skipped:
        print_task_row(task, owner, extra=f"  needs {task.duration - minutes_left} more min")
    print("=" * WIDTH)


if __name__ == "__main__":
    main()
