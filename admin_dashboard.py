import streamlit as st
from backend import (
    get_all_bookings, delete_booking,
    mark_teacher_unavailable, delete_teacher_unavailability,
    get_teacher_unavailability
)

# All valid teacher names for dropdown
TEACHERS = [
    "Bharti Ma'am", "Vivek Sir", "Dakshika", "Ishita", "Shivangi",
    "Kalpana Ma'am", "Payal", "Sneha", "Aparajita",
    "Deepanshi", "Megha", "Yaindrila Ma'am", "Arpit", "Geetanjali"
]

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("📊 Cordova Admin Dashboard")

tabs = st.tabs([
    "📅 View Bookings", 
    "🗑️ Delete Booking", 
    "⛔ Mark Teacher Unavailable", 
    "✅ Unmark Teacher Unavailable", 
    "📈 Analytics (Coming Soon)"
])

# ------------------- Tab 1: View Bookings ------------------- #
with tabs[0]:
    st.subheader("📅 All Bookings Overview")
    all_bookings = get_all_bookings()
    if all_bookings:
        st.dataframe(all_bookings, use_container_width=True)
    else:
        st.info("No bookings found.")

# ------------------- Tab 2: Delete Booking ------------------- #
with tabs[1]:
    st.subheader("🗑️ Delete Booking")
    all_bookings = get_all_bookings()
    if not all_bookings:
        st.warning("No bookings available to delete.")
    else:
        selected = st.selectbox("Select a booking to delete", all_bookings)
        if st.button("Delete Booking", type="primary"):
            delete_booking(selected)
            st.success("✅ Booking deleted and emails sent.")

# ------------------- Tab 3: Mark Teacher Unavailable ------------------- #
with tabs[2]:
    st.subheader("⛔ Mark Teacher Unavailable")
    teacher = st.selectbox("Select Teacher", TEACHERS)
    date = st.date_input("Unavailable Date")
    slot = st.text_input("Time Slot (optional, leave blank for full day)")
    if st.button("Mark Unavailable"):
        slot_value = slot.strip() if slot.strip() else None
        mark_teacher_unavailable(teacher, str(date), slot_value)
        st.success(f"✅ Marked {teacher} unavailable on {date}" + (f" during {slot}" if slot_value else " for full day."))

# ------------------- Tab 4: Unmark Teacher Unavailability ------------------- #
with tabs[3]:
    st.subheader("✅ Unmark Teacher Unavailability")
    absences = get_teacher_unavailability()
    if not absences:
        st.info("No teachers marked as unavailable.")
    else:
        selected = st.selectbox("Select an absence to remove", absences)
        if st.button("Remove Unavailability"):
            delete_teacher_unavailability(
                selected["teacher"], selected["date"], selected["slot"]
            )
            st.success(f"✅ Removed unavailability for {selected['teacher']} on {selected['date']}")

# ------------------- Tab 5: Analytics (Placeholder) ------------------- #
with tabs[4]:
    st.subheader("📈 Analytics (Coming Soon)")
    st.info("This section will include charts and booking insights in future.")
