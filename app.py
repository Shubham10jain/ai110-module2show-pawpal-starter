import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, your pet care planning assistant. Add your pets and their
care tasks below, then generate a smart daily schedule.
"""
)

# --- Session state: keep one Owner alive across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.divider()

# --- Add a pet ---
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="", key="new_pet_name")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")
with col3:
    breed = st.text_input("Breed (optional)", value="", key="new_pet_breed")

if st.button("Add pet"):
    if pet_name.strip():
        owner.add_pet(Pet(name=pet_name.strip(), species=species, breed=breed.strip()))
        st.success(f"Added {pet_name}!")
    else:
        st.warning("Please enter a pet name.")

if owner.pets:
    st.write("Current pets:", ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task ---
st.subheader("Add a Task")

if owner.pets:
    task_pet_name = st.selectbox("Pet", [p.name for p in owner.pets], key="task_pet_name")
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title")
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00", key="task_time")
    with col3:
        task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")

    col4, col5 = st.columns(2)
    with col4:
        task_category = st.selectbox(
            "Category", ["walk", "feeding", "medication", "appointment", "other"], key="task_category"
        )
    with col5:
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], key="task_frequency")

    if st.button("Add task"):
        pet = owner.get_pet(task_pet_name)
        pet.add_task(
            Task(
                title=task_title,
                category=task_category,
                time=task_time,
                priority=task_priority,
                frequency=task_frequency,
            )
        )
        st.success(f"Added '{task_title}' for {task_pet_name} at {task_time}.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# --- Generate schedule ---
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    schedule = scheduler.get_today_schedule()

    if not schedule:
        st.info("No tasks scheduled for today yet.")
    else:
        st.table(
            [
                {
                    "Time": task.time,
                    "Pet": pet.name,
                    "Task": task.title,
                    "Category": task.category,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Done": "✅" if task.completed else "⬜",
                }
                for pet, task in schedule
            ]
        )

        conflicts = scheduler.detect_conflicts(schedule)
        if conflicts:
            for warning in conflicts:
                st.warning(f"⚠️ {warning}")
        else:
            st.success("No scheduling conflicts detected.")
