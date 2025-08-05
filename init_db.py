<<<<<<< HEAD
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
=======
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
>>>>>>> e8f1dd0c8cde3c0d31c3ac3867a4decb1e56d7f7
