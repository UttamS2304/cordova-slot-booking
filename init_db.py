import sqlite3

def initialize_database():
    conn = sqlite3.connect("cordova_publication.db")
    cursor = conn.cursor()

    # Create bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_type TEXT,
            school_name TEXT,
            title_used TEXT,
            grade TEXT,
            curriculum TEXT,
            subject TEXT,
            slot TEXT,
            date TEXT,
            topic TEXT,
            teacher TEXT,
            salesperson TEXT,
            email TEXT
        )
    """)

    # Create teacher_unavailability table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teacher_unavailability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher TEXT,
            date TEXT,
            slot TEXT
        )
    """)

    # Create subject_teacher_map table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject_teacher_map (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            main_teacher TEXT,
            fallback1 TEXT,
            fallback2 TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ All required tables created successfully in cordova_publication.db.")

# Run initialization
if __name__ == "__main__":
    initialize_database()
