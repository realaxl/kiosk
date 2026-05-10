import sqlite3
import os
import shutil
from pathlib import Path

# Backup the existing database
db_path = Path("db/db.sqlite")
backup_path = Path("db/db.sqlite.backup")

if db_path.exists():
    shutil.copy(db_path, backup_path)
    print(f"[+] Backed up database to {backup_path}")

# Test 1: Remove a column (simulate missing column scenario)
print("\n=== Test 1: Simulating missing 'favorite' column in stocks table ===")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop and recreate stocks table without 'favorite' column
cursor.execute("DROP TABLE IF EXISTS stocks_backup")
cursor.execute("CREATE TABLE stocks_backup AS SELECT * FROM stocks")
cursor.execute("DROP TABLE stocks")
cursor.execute("""
CREATE TABLE stocks (
    stockId INTEGER PRIMARY KEY,
    eventId INTEGER NOT NULL,
    productId INTEGER NOT NULL,
    numberInStock INTEGER NOT NULL,
    salePrice REAL NOT NULL,
    note TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (eventId) REFERENCES events(eventId),
    FOREIGN KEY (productId) REFERENCES products(productId)
)
""")
cursor.execute("INSERT INTO stocks SELECT stockId, eventId, productId, numberInStock, salePrice, note, active FROM stocks_backup")
cursor.execute("DROP TABLE stocks_backup")
conn.commit()
conn.close()

print("[+] Removed 'favorite' column from stocks table")

# Check current schema
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(stocks)")
columns = [row[1] for row in cursor.fetchall()]
print(f"[+] Current stocks columns: {columns}")
conn.close()

# Run the create_database script
print("\n[+] Running create_database.py...")
os.system("python src/create_database.py")

# Verify the column was added
print("\n=== Verification ===")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(stocks)")
columns = [row[1] for row in cursor.fetchall()]
print(f"[+] Updated stocks columns: {columns}")

if 'favorite' in columns:
    print("[OK] SUCCESS: 'favorite' column was added!")
else:
    print("[!] FAILED: 'favorite' column was not added")

conn.close()

# Restore the backup
if backup_path.exists():
    shutil.copy(backup_path, db_path)
    backup_path.unlink()
    print(f"\n[+] Restored database from backup")

# Made with Bob
