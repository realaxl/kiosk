"""
Migration script to add the config table to the database
"""
import sys
import os

# Fix UTF-8 issues on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import sqlite3
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
db_path = PROJECT_ROOT / 'db' / 'db.sqlite'

def main():
    print("=" * 60)
    print("Adding config table to database")
    print("=" * 60)
    print()
    
    if not db_path.exists():
        print("❌ Database does not exist at:", db_path)
        print("Please run create_database.py first.")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Check if table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='config'")
    if cursor.fetchone():
        print("ℹ Config table already exists")
        conn.close()
        return
    
    print("Creating config table...")
    
    # Create the config table
    cursor.execute('''
        CREATE TABLE config (
            configId INTEGER PRIMARY KEY,
            uuid TEXT,
            key TEXT NOT NULL,
            value TEXT,
            note TEXT,
            active INTEGER NOT NULL DEFAULT 1
        )
    ''')
    
    conn.commit()
    print("✓ Config table created successfully")
    
    # Verify the table was created
    cursor.execute("PRAGMA table_info(config)")
    columns = cursor.fetchall()
    
    print("\nTable schema:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ Migration completed successfully!")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()

# Made with Bob
