"""PawPal+ CLI demo.

Builds a small household (one owner, two pets, several tasks) and prints
today's schedule to the terminal. Run with: python main.py
"""

from pawpal_system import Owner, Pet, Scheduler, Task


def pet_name_for(task: Task, owner: Owner) -> str:
    """Find which of the owner's pets a task belongs to."""
    for pet in owner.pets:
        if task in pet.tasks:
            return pet.name
    return "?"


def main() -> None:
    # 1. Set up the owner and their pets
    owner = Owner("Jordan", available_minutes=90)
    mochi = Pet("Mochi", "dog", "Golden Retriever")
    biscuit = Pet("Biscuit", "cat", "Tabby")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    # 2. Add care tasks with different times of day
    mochi.add_task(Task("Morning walk", duration=30, due_time="08:00", priority="high", frequency="daily"))
    mochi.add_task(Task("Feeding", duration=10, due_time="08:45", priority="high", frequency="daily"))
    mochi.add_task(Task("Fetch practice", duration=25, due_time="17:00", priority="low"))
    biscuit.add_task(Task("Feeding", duration=10, due_time="09:00", priority="high", frequency="daily"))
    biscuit.add_task(Task("Litter box cleaning", duration=15, due_time="19:30", priority="medium", frequency="daily"))
    biscuit.add_task(Task("Brush fur", duration=20, priority="low"))

    # 3. Let the scheduler build today's plan
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    # 4. Print a readable schedule
    print("=" * 52)
    print(f"  PawPal+ — Today's Schedule for {owner.name}")
    print(f"  Pets: {', '.join(pet.describe() for pet in owner.pets)}")
    print(f"  Time available: {owner.available_minutes} minutes")
    print("=" * 52)

    total = 0
    for task in plan:
        when = task.due_time if task.due_time else "anytime"
        pet_name = pet_name_for(task, owner)
        print(f"  {when:>7}  {task.description:<22} {pet_name:<8} {task.duration:>3} min  [{task.priority}]")
        total += task.duration

    print("-" * 52)
    print(f"  Scheduled: {len(plan)} of {len(owner.get_all_tasks())} tasks, {total} min used")

    skipped = [t for t in owner.get_all_tasks() if t not in plan]
    for task in skipped:
        print(f"  Skipped:   {task.description} ({pet_name_for(task, owner)}) — not enough time left")
    print("=" * 52)


if __name__ == "__main__":
    main()
