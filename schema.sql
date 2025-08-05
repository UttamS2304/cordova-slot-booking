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
CREATE TABLE IF NOT EXISTS teacher_unavailability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher TEXT NOT NULL,
    date TEXT NOT NULL,
    slot TEXT  -- If NULL, teacher is absent for the full day
);
