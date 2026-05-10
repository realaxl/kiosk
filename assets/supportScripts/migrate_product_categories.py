"""
Database migration script to rename imageUrl to image in productCategories table
"""
import sqlite3
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent
db_path = PROJECT_ROOT / "db" / "db.sqlite"

def migrate_database():
    print(f"Migrating productCategories table at {db_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = OFF")
    
    try:
        # Step 1: Create new productCategories table with updated schema
        print("Creating new productCategories table with updated schema...")
        cursor.execute("""
            CREATE TABLE productCategories_new (
                productCategoryId INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                image TEXT,
                note TEXT,
                active INTEGER NOT NULL DEFAULT 1
            )
        """)
        print("  [+] Created productCategories_new table")
        
        # Step 2: Copy data from old table to new table
        print("\nCopying data from productCategories to productCategories_new...")
        cursor.execute("""
            INSERT INTO productCategories_new 
                (productCategoryId, name, description, image, note, active)
            SELECT 
                productCategoryId, name, description, imageUrl, note, active
            FROM productCategories
        """)
        rows_copied = cursor.rowcount
        print(f"  [+] Copied {rows_copied} rows")
        
        # Step 3: Drop old table
        print("\nDropping old productCategories table...")
        cursor.execute("DROP TABLE productCategories")
        print("  [+] Dropped productCategories table")
        
        # Step 4: Rename new table to productCategories
        print("\nRenaming productCategories_new to productCategories...")
        cursor.execute("ALTER TABLE productCategories_new RENAME TO productCategories")
        print("  [+] Renamed productCategories_new to productCategories")
        
        # Commit changes
        conn.commit()
        print("\n[OK] Migration completed successfully!")
        print("Changes:")
        print("  - Renamed column: imageUrl -> image in productCategories")
        
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        # Re-enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        conn.close()

if __name__ == "__main__":
    migrate_database()

# Made with Bob
