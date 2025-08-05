import sqlite3

schema = """
DROP TABLE IF EXISTS bookings;

CREATE TABLE bookings (
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
    salesperson_name TEXT,
    salesperson_number TEXT,
    email TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

conn = sqlite3.connect("booking.db")
cursor = conn.cursor()
cursor.executescript(schema)
conn.commit()
conn.close()

print("✅ bookings table reset successfully.")
