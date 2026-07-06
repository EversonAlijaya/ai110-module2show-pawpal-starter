from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def pet_name_for(task, owner):
    for pet in owner.pets:
        if task in pet.tasks:
            return pet.name
    return "?"

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", available_minutes=90)
owner = st.session_state.owner

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant.

Set up your day below: tell us who you are and how much time you have,
add your pets, give them care tasks, and generate today's schedule.
"""
)

with st.expander("How to use", expanded=False):
    st.markdown(
        """
1. **Owner** — enter your name and how many minutes you have for pet care today.
2. **Pets** — add each of your pets (name, species, and optionally breed).
3. **Tasks** — pick a pet, describe a care task (walk, feeding, meds…), and set
   its duration, due time, and priority. Repeat for as many tasks as you like.
4. **Today's Schedule** — click *Generate schedule* to build your day.
"""
    )

with st.expander("How scheduling works", expanded=False):
    st.markdown(
        """
- High-priority tasks are placed first, then medium, then low.
- Tasks only make the plan if they fit in your remaining time.
- The plan is shown in time order, like a daily agenda.
- Tasks that don't fit are listed as skipped, along with how many
  more minutes you would need to fit them in.
- Completed tasks are left out automatically.
"""
    )

st.divider()

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.update_availability(
    int(st.number_input("Time available today (minutes)", min_value=10, max_value=600, value=owner.available_minutes))
)

st.subheader("Pets")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed (optional)", value="")

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species, breed))

if owner.pets:
    st.write("Current pets: " + ", ".join(pet.describe() for pet in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.subheader("Tasks")
if owner.pets:
    col1, col2 = st.columns(2)
    with col1:
        task_pet = st.selectbox("Pet", [pet.name for pet in owner.pets])
    with col2:
        description = st.text_input("Task", value="Morning walk")
    col3, col4, col5 = st.columns(3)
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        due = st.time_input("Due time", value=time(8, 0))
    with col5:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == task_pet)
        pet.add_task(Task(description, int(duration), due.strftime("%H:%M"), priority))

    rows = [
        {
            "Pet": pet.name,
            "Task": t.description,
            "Due": t.due_time,
            "Minutes": t.duration,
            "Priority": t.priority,
            "Done": t.completed,
        }
        for pet in owner.pets
        for t in pet.tasks
    ]
    if rows:
        st.table(rows)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.caption("Add a pet first, then you can give it tasks.")

st.divider()

st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()
    if plan:
        st.table(
            [
                {
                    "When": t.due_time if t.due_time else "anytime",
                    "Task": t.description,
                    "Pet": pet_name_for(t, owner),
                    "Minutes": t.duration,
                    "Priority": t.priority,
                }
                for t in plan
            ]
        )
        used = sum(t.duration for t in plan)
        st.caption(
            f"Scheduled {len(plan)} of {len(owner.get_all_tasks())} tasks — {used} of {owner.available_minutes} minutes used."
        )
        minutes_left = owner.available_minutes - used
        for t in owner.get_all_tasks():
            if not t.completed and t not in plan:
                st.warning(
                    f"Skipped: {t.description} ({pet_name_for(t, owner)}, {t.duration} min, {t.priority} priority) — needs {t.duration - minutes_left} more min."
                )
    else:
        st.info("Nothing to schedule yet — add some tasks first.")
