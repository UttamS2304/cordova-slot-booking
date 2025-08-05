import sqlite3

# Read SQL schema file
with open("schema.sql", "r") as f:
    schema = f.read()

# Connect to (or create) SQLite database file
conn = sqlite3.connect("cordova_publication.db")

# Create a cursor to execute commands
cursor = conn.cursor()

# Run schema to create tables
cursor.executescript(schema)

# Save and close
conn.commit()
conn.close()

print("✅ Database initialized successfully!")

