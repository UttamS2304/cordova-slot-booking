# backend.py

import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import ssl
from teacher_mapping import get_teacher_for_subject
from init_db import initialize_database

# --------------------------
# Initialize DB and load env
# --------------------------
initialize_database()
os.environ["STREAMLIT_CLOUD"] = "1"
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


# --------------------------
# Connect DB (single source of truth)
# --------------------------
def connect_db():
    return sqlite3.connect("cordova_publication.db")


# --------------------------
# Get teacher email
# --------------------------
def get_teacher_email(name):
    env_key = f"TEACHER_EMAIL_{name.upper().replace(' ', '')}"
    return os.getenv(env_key, "default@school.com")


# --------------------------
# Check teacher availability
# --------------------------
def is_teacher_available(teacher, date, slot):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM teacher_unavailability
        WHERE teacher=? AND date=? AND (slot IS NULL OR slot=?)
    """, (teacher, date, slot))
    result = cursor.fetchone()[0]
    conn.close()
    return result == 0


# --------------------------
# Attempt booking
# --------------------------
def attempt_booking(form_data):
    teacher = get_teacher_for_subject(form_data["subject"], form_data["date"])
    if not teacher:
        return False, "No teacher available for this subject on that date."

    if not is_teacher_available(teacher, form_data["date"], form_data["slot"]):
        return False, f"{teacher} is unavailable on {form_data['date']} during {form_data['slot']}."

    form_data["teacher"] = teacher
    record_booking(form_data)
    send_email_notification("confirmation", form_data)
    return True, "✅ Session successfully booked!"


# --------------------------
# Record booking
# --------------------------
def record_booking(data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (
            booking_type, school_name, title_used, grade, curriculum,
            subject, slot, date, topic, salesperson_name, salesperson_number,
            teacher, email, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["booking_type"], data["school_name"], data["title_used"],
        data["grade"], data["curriculum"], data["subject"], data["slot"],
        data["date"], data["topic"], data["salesperson_name"], data["salesperson_number"],
        data["teacher"], data["email"], datetime.now()
    ))
    conn.commit()
    conn.close()


# --------------------------
# Get all bookings
# --------------------------
def get_all_bookings():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    cols = [desc[0] for desc in cursor.description]
    results = [dict(zip(cols, row)) for row in cursor.fetchall()]
    conn.close()
    return results


# --------------------------
# Delete booking
# --------------------------
def delete_booking(row_data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM bookings
        WHERE school_name=? AND grade=? AND subject=? AND slot=? AND date=?
        AND salesperson_name=? AND teacher=?
    """, (
        row_data["school_name"], row_data["grade"], row_data["subject"],
        row_data["slot"], row_data["date"], row_data["salesperson_name"],
        row_data["teacher"]
    ))
    conn.commit()
    conn.close()
    send_email_notification("cancellation", row_data)


# --------------------------
# Send emails
# --------------------------
def send_email_notification(email_type, form_data):
    msg = EmailMessage()
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            if email_type == "confirmation":
                # Salesperson
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = form_data["email"]
                msg["Subject"] = "✅ Your Cordova Class is Confirmed"
                msg.set_content(f"""Dear {form_data['salesperson_name']},

Your class has been successfully booked.

School: {form_data['school_name']}
Grade: {form_data['grade']}
Subject: {form_data['subject']}
Date: {form_data['date']}
Slot: {form_data['slot']}
Type: {form_data['booking_type']}
Topic: {form_data['topic'] or 'N/A'}
""")
                server.send_message(msg)
                msg.clear()

                # Teacher
                msg["To"] = get_teacher_email(form_data["teacher"])
                msg["Subject"] = "✅ New Cordova Session Assigned"
                msg.set_content(f"""You have a new session to conduct.

Subject: {form_data['subject']}
Date: {form_data['date']}
Slot: {form_data['slot']}
School: {form_data['school_name']}
Grade: {form_data['grade']}
Curriculum: {form_data['curriculum']}
Type: {form_data['booking_type']}
Topic: {form_data['topic'] or 'N/A'}
""")
                server.send_message(msg)
                msg.clear()

                # Admin
                msg["To"] = ADMIN_EMAIL
                msg["Subject"] = "📢 New Cordova Booking Created"
                msg.set_content(f"""A new booking has been created:

School: {form_data['school_name']}
Grade: {form_data['grade']}
Subject: {form_data['subject']}
Date: {form_data['date']}
Slot: {form_data['slot']}
Type: {form_data['booking_type']}
Topic: {form_data['topic'] or 'N/A'}
Teacher: {form_data['teacher']}
Salesperson: {form_data['salesperson_name']} ({form_data['salesperson_number']})
""")
                server.send_message(msg)

            elif email_type == "cancellation":
                # Salesperson
                msg["To"] = form_data["email"]
                msg["Subject"] = "❌ Cordova Class Cancelled"
                msg.set_content(f"""Dear {form_data['salesperson_name']},

Your scheduled class has been cancelled.

School: {form_data['school_name']}
Grade: {form_data['grade']}
Subject: {form_data['subject']}
Date: {form_data['date']}
Slot: {form_data['slot']}
""")
                server.send_message(msg)
                msg.clear()

                # Teacher
                msg["To"] = get_teacher_email(form_data["teacher"])
                msg["Subject"] = "❌ Cordova Session Cancelled"
                msg.set_content(f"""Your assigned session has been cancelled.

Subject: {form_data['subject']}
Date: {form_data['date']}
Slot: {form_data['slot']}
School: {form_data['school_name']}
Grade: {form_data['grade']}
""")
                server.send_message(msg)

    except Exception as e:
        print(f"❌ Email Error: {e}")


# --------------------------
# Mark Teacher Unavailable
# --------------------------
def mark_teacher_unavailable(teacher, date, slot=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO teacher_unavailability (teacher, date, slot)
        VALUES (?, ?, ?)
    """, (teacher, date, slot))
    conn.commit()
    conn.close()


# --------------------------
# Remove Teacher Unavailability
# --------------------------
def delete_teacher_unavailability(teacher, date, slot=None):
    conn = connect_db()
    cursor = conn.cursor()
    if slot:
        cursor.execute("DELETE FROM teacher_unavailability WHERE teacher=? AND date=? AND slot=?", (teacher, date, slot))
    else:
        cursor.execute("DELETE FROM teacher_unavailability WHERE teacher=? AND date=? AND slot IS NULL", (teacher, date))
    conn.commit()
    conn.close()


# --------------------------
# Get All Teacher Unavailability
# --------------------------
def get_teacher_unavailability():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teacher_unavailability")
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(cols, row)) for row in rows]
