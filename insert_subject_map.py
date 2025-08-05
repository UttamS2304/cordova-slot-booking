import sqlite3

DB_FILE = "booking.db"

subject_mappings = [
    ("Hindi", "Bharti", ""),  # No fallback
    ("Mathematics", "Vivek", ""),
    ("GK", "Dakshika", "Ishita"),
    ("SST", "Ishita", "Shivangi"),
    ("Science", "Kalpana", "Payal,Sneha"),
    ("English", "Aparajita", "Deepanshi,Megha"),
    ("Pre Primary", "Yaindrila", ""),
    ("EVS", "Yaindrila", "Kalpana"),
    ("Computer", "Arpit", "Geetanjali")
]

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Insert records
for subject, main, fallbacks in subject_mappings:
    cursor.execute("INSERT INTO subject_map (subject, main, fallbacks) VALUES (?, ?, ?)",
                   (subject, main, fallbacks))

conn.commit()
conn.close()

print("✅ Subject-teacher mappings inserted successfully.")
