import sqlite3

conn = sqlite3.connect("resume_analysis.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score REAL,
    missing_skills TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")