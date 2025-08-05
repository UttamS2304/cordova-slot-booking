import streamlit as st
from backend import (
    get_all_bookings, delete_booking,
    mark_teacher_unavailable, delete_teacher_unavailability,
    get_teacher_unavailability
)

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

# ------------------ View All Bookings ------------------ #
with tabs[0]:
    st.subheader("📅 All Bookings Overview")
    bookings = get_all_bookings()
    if bookings:
        st.dataframe(bookings, use_container_width=True)
    else:
        st.info("No bookings found.")

# ------------------ Delete Booking ------------------ #
with tabs[1]:
    st.subheader("🗑️ Delete Booking")
    bookings = get_all_bookings()
    if bookings:
        selected = st.selectbox("Select a booking to delete", bookings)
        if st.button("Delete Booking", type="primary"):
            delete_booking(selected)
            st.success("✅ Booking deleted and emails sent.")
    else:
        st.warning("No bookings available to delete.")

# ------------------ Mark Teacher Unavailable ------------------ #
with tabs[2]:
    st.subheader("⛔ Mark Teacher Unavailable")
    teacher = st.selectbox("Select Teacher", TEACHERS)
    date = st.date_input("Unavailable Date")
    slot = st.text_input("Time Slot (leave blank for full day)")
    if st.button("Mark Unavailable"):
        final_slot = slot.strip() if slot.strip() else None
        mark_teacher_unavailable(teacher, str(date), final_slot)
        st.success(f"✅ Marked {teacher} unavailable on {date}" + (f" during {slot}" if final_slot else " for full day."))

# ------------------ Unmark Teacher Unavailable ------------------ #
with tabs[3]:
    st.subheader("✅ Unmark Teacher Unavailability")
    absences = get_teacher_unavailability()
    if absences:
        selected = st.selectbox("Select absence to remove", absences)
        if st.button("Remove Unavailability"):
            delete_teacher_unavailability(
                selected["teacher"], selected["date"], selected["slot"]
            )
            st.success(f"✅ Removed unavailability for {selected['teacher']} on {selected['date']}")
    else:
        st.info("No teachers marked as unavailable.")

# ------------------ Analytics Placeholder ------------------ #
with tabs[4]:
    st.subheader("📈 Analytics (Coming Soon)")
    st.info("This section will show booking insights and charts.")
