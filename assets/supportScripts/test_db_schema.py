import sqlite3

conn = sqlite3.connect('db/db.sqlite')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print("Tables in database:", tables)
print()

# Check each table's columns
for table in tables:
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    print(f"{table}:")
    for col in columns:
        print(f"  - {col[1]}: {col[2]}")
    print()

conn.close()

# Made with Bob
