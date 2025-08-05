import streamlit as st
import datetime
import pandas as pd
from backend import attempt_booking, get_all_bookings

st.set_page_config(page_title="CORDOVA PUBLICATIONS | LIVE CLASSES AND PRODUCT TRAINING BOOKING", layout="wide")
st.title("📚 Cordova | Salesperson (Live Class) Portal")

# ----------------------
# Session Management
# ----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "salesperson_name" not in st.session_state:
    st.session_state.salesperson_name = ""
if "salesperson_number" not in st.session_state:
    st.session_state.salesperson_number = ""

# ----------------------
# Login Page
# ----------------------
if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    with st.form("login_form"):
        name = st.text_input("Your Name")
        number = st.text_input("Mobile Number")
        login = st.form_submit_button("Login")

    if login:
        if name.strip() and number.strip():
            st.session_state.logged_in = True
            st.session_state.salesperson_name = name.strip()
            st.session_state.salesperson_number = number.strip()
            st.rerun()
        else:
            st.error("Please enter both your name and mobile number to login.")

# ----------------------
# Dashboard + Booking Form
# ----------------------
if st.session_state.logged_in:

    col1, col2 = st.columns([5, 1])
    with col1:
        st.success(f"✅ Logged in as: {st.session_state.salesperson_name} ({st.session_state.salesperson_number})")
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.salesperson_name = ""
            st.session_state.salesperson_number = ""
            st.rerun()

    tab = st.radio("Select Action", ["📊 View Bookings Dashboard", "📝 Book a Session"])

    # ----------------------
    # Bookings Dashboard
    # ----------------------
    if tab == "📊 View Bookings Dashboard":
        bookings = get_all_bookings()
        df = pd.DataFrame(bookings)

        if df.empty:
            st.warning("No bookings found.")
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["date"] = pd.to_datetime(df["date"])

            df = df[
                (df["salesperson_name"].str.lower() == st.session_state.salesperson_name.lower()) &
                (df["salesperson_number"] == st.session_state.salesperson_number)
            ]

            if df.empty:
                st.info("You have not made any bookings yet.")
            else:
                with st.expander("🔍 Filter Bookings"):
                    subject_filter = st.selectbox("Subject", ["All"] + sorted(df["subject"].unique()))
                    date_filter = st.date_input("Filter by Date", value=None)

                    if subject_filter != "All":
                        df = df[df["subject"] == subject_filter]
                    if date_filter:
                        df = df[df["date"].dt.date == date_filter]

                df = df.sort_values(by=["date", "slot"])
                st.markdown(f"### 🗂️ Your Bookings ({len(df)})")
                st.dataframe(df[[
                    "booking_type", "school_name", "title_used", "grade", "curriculum",
                    "subject", "date", "slot", "topic", "teacher", "timestamp"
                ]].rename(columns={
                    "booking_type": "Type",
                    "school_name": "School",
                    "title_used": "Title Used",
                    "grade": "Grade",
                    "curriculum": "Curriculum",
                    "subject": "Subject",
                    "date": "Date",
                    "slot": "Slot",
                    "topic": "Topic",
                    "teacher": "Teacher",
                    "timestamp": "Booked On"
                }), use_container_width=True)

    # ----------------------
    # Book a Session Form
    # ----------------------
    if tab == "📝 Book a Session":
        st.subheader("📝 Fill the Form Below")

        booking_type = st.radio("Booking Type", ["Live Class", "Product Training Session"])

        with st.form("booking_form"):
            school_name = st.text_input("School Name")
            title_used = st.text_input("Title Name Used by School")
            curriculum = st.selectbox("Curriculum", ["Select", "CBSE", "ICSE", "State Board", "Other"])
            subject = st.selectbox("Subject", [
                "Select", "Hindi", "Mathematics", "GK", "SST", "Science",
                "English", "Pre Primary", "EVS", "Computer"
            ])
            slot = st.selectbox("Preferred Slot", [
                "Select",
                "10:00 AM - 10:40 AM", "10:40 AM - 11:20 AM", "11:20 AM - 12:00 PM",
                "12:00 PM - 12:40 PM", "12:40 PM - 1:20 PM", "1:20 PM - 2:00 PM",
                "2:00 PM - 2:40 PM", "2:40 PM - 3:20 PM", "3:20 PM - 4:00 PM"
            ])
            date = st.date_input("Session Date", min_value=datetime.date.today())
            grade = ""
            if booking_type == "Live Class":
                grade = st.selectbox("Grade", ["Select", "Nursery", "LKG", "UKG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            topic = st.text_input("Topic (Optional)")
            email = st.text_input("Your Email (for confirmation)")

            submit = st.form_submit_button("📩 Book Now")

        if submit:
            if (
                not school_name.strip() or not title_used.strip() or
                curriculum == "Select" or subject == "Select" or slot == "Select" or
                not email.strip() or (booking_type == "Live Class" and grade == "Select")
            ):
                st.error("❌ Please fill all required fields correctly.")
            else:
                form_data = {
                    "booking_type": booking_type,
                    "school_name": school_name.strip(),
                    "title_used": title_used.strip(),
                    "grade": grade if booking_type == "Live Class" else "",
                    "curriculum": curriculum,
                    "subject": subject,
                    "slot": slot,
                    "date": str(date),
                    "topic": topic.strip(),
                    "salesperson_name": st.session_state.salesperson_name,
                    "salesperson_number": st.session_state.salesperson_number,
                    "email": email.strip()
                }

                success, message = attempt_booking(form_data)

                if success:
                    st.success(message)
                else:
                    st.error(message)
