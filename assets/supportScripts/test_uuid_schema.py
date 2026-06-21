# -*- coding: utf-8 -*-
import sys
import os

# Set environment variable to ensure UTF-8 encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import sqlite3
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Database file path
db_path = PROJECT_ROOT / "db" / "db.sqlite"

def test_uuid_columns():
    """Test that all tables have uuid column"""
    print("=== Testing UUID Schema ===\n")
    
    if not db_path.exists():
        print(f"[ERROR] Database not found at {db_path}")
        return False
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # List of all tables that should have uuid column
    tables = [
        "events",
        "productCategories",
        "products",
        "stocks",
        "carts",
        "sales",
        "tags",
        "productRelations"
    ]
    
    all_passed = True
    
    for table_name in tables:
        # Get table info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'uuid' in columns:
            # Check if any records have uuid values
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total_count = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE uuid IS NOT NULL")
            uuid_count = cursor.fetchone()[0]
            
            print(f"[OK] {table_name:20} - uuid column exists ({uuid_count}/{total_count} records have UUIDs)")
        else:
            print(f"[ERROR] {table_name:20} - uuid column MISSING")
            all_passed = False
    
    conn.close()
    
    if all_passed:
        print("\n[SUCCESS] All tables have uuid column!")
    else:
        print("\n[FAILED] Some tables are missing uuid column")
    
    return all_passed

if __name__ == "__main__":
    test_uuid_columns()

# Made with Bob