<<<<<<< HEAD
# teacher_mapping.py

import sqlite3

teacher_map = {
    "Hindi": ["Bharti Ma'am"],
    "Mathematics": ["Vivek Sir"],
    "GK": ["Dakshika", "Ishita"],
    "SST": ["Ishita", "Shivangi"],
    "Science": ["Kalpana Ma'am", "Payal", "Sneha"],
    "English": ["Aparajita", "Deepanshi", "Megha"],
    "Pre Primary": ["Yaindrila Ma'am"],
    "EVS": ["Yaindrila Ma'am", "Kalpana Ma'am"],
    "Computer": ["Arpit", "Geetanjali"]
}

daily_class_limit = {
    "Bharti Ma'am": 2,
    "Vivek Sir": 2,
    "Dakshika": 2,
    "Ishita": 2,
    "Shivangi": 2,
    "Kalpana Ma'am": 2,
    "Payal": 2,
    "Sneha": 2,
    "Aparajita": 1,
    "Deepanshi": 1,
    "Megha": 1,
    "Yaindrila Ma'am": 2,
    "Arpit": 2,
    "Geetanjali": 2
}

# Helper function to check if teacher is available
def is_teacher_available(teacher, date):
    conn = sqlite3.connect("cordova_publication.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM teacher_unavailability
        WHERE teacher = ? AND date = ? AND slot IS NULL
    """, (teacher, date))
    result = cursor.fetchone()[0]
    conn.close()
    return result == 0

# Main fallback logic with absence check
def get_teacher_for_subject(subject, date):
    conn = sqlite3.connect("cordova_publication.db")
    cursor = conn.cursor()

    if subject not in teacher_map:
        return None

    for teacher in teacher_map[subject]:
        # Check if teacher is absent
        if not is_teacher_available(teacher, date):
            continue

        # Check if class limit is exceeded
        cursor.execute("""
            SELECT COUNT(*) FROM bookings
            WHERE teacher = ? AND date = ?
        """, (teacher, date))
        count = cursor.fetchone()[0]
        if count < daily_class_limit[teacher]:
            return teacher

    conn.close()
    return None
=======
# teacher_mapping.py

import sqlite3

teacher_map = {
    "Hindi": ["Bharti Ma'am"],
    "Mathematics": ["Vivek Sir"],
    "GK": ["Dakshika", "Ishita"],
    "SST": ["Ishita", "Shivangi"],
    "Science": ["Kalpana Ma'am", "Payal", "Sneha"],
    "English": ["Aparajita", "Deepanshi", "Megha"],
    "Pre Primary": ["Yaindrila Ma'am"],
    "EVS": ["Yaindrila Ma'am", "Kalpana Ma'am"],
    "Computer": ["Arpit", "Geetanjali"]
}

daily_class_limit = {
    "Bharti Ma'am": 2,
    "Vivek Sir": 2,
    "Dakshika": 2,
    "Ishita": 2,
    "Shivangi": 2,
    "Kalpana Ma'am": 2,
    "Payal": 2,
    "Sneha": 2,
    "Aparajita": 1,
    "Deepanshi": 1,
    "Megha": 1,
    "Yaindrila Ma'am": 2,
    "Arpit": 2,
    "Geetanjali": 2
}

# Helper function to check if teacher is available
def is_teacher_available(teacher, date):
    conn = sqlite3.connect("cordova_publication.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM teacher_unavailability
        WHERE teacher = ? AND date = ? AND slot IS NULL
    """, (teacher, date))
    result = cursor.fetchone()[0]
    conn.close()
    return result == 0

# Main fallback logic with absence check
def get_teacher_for_subject(subject, date):
    conn = sqlite3.connect("cordova_publication.db")
    cursor = conn.cursor()

    if subject not in teacher_map:
        return None

    for teacher in teacher_map[subject]:
        # Check if teacher is absent
        if not is_teacher_available(teacher, date):
            continue

        # Check if class limit is exceeded
        cursor.execute("""
            SELECT COUNT(*) FROM bookings
            WHERE teacher = ? AND date = ?
        """, (teacher, date))
        count = cursor.fetchone()[0]
        if count < daily_class_limit[teacher]:
            return teacher

    conn.close()
    return None
>>>>>>> e8f1dd0c8cde3c0d31c3ac3867a4decb1e56d7f7
