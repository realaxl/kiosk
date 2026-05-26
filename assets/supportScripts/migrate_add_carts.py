import sqlite3
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Database file path
db_path = PROJECT_ROOT / "db" / "db.sqlite"

def migrate_database():
    """Add carts table and cartId to sales table."""
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return
    
    print(f"Migrating database at {db_path}\n")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    try:
        # Check if carts table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='carts'")
        carts_exists = cursor.fetchone() is not None
        
        if not carts_exists:
            print("[1/2] Creating carts table...")
            cursor.execute("""
                CREATE TABLE carts (
                    cartId INTEGER PRIMARY KEY,
                    name TEXT,
                    timestamp INTEGER NOT NULL,
                    note TEXT,
                    active INTEGER NOT NULL DEFAULT 1
                )
            """)
            print("  [+] Created carts table")
        else:
            print("[1/2] Carts table already exists")
        
        # Check if cartId column exists in sales table
        cursor.execute("PRAGMA table_info(sales)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'cartId' not in columns:
            print("[2/2] Adding cartId column to sales table...")
            cursor.execute("ALTER TABLE sales ADD COLUMN cartId INTEGER")
            print("  [+] Added cartId column to sales table")
            
            # Note: We cannot add the foreign key constraint to an existing table in SQLite
            # without recreating the table. For now, we'll just add the column.
            print("  [!] Note: Foreign key constraint for cartId needs manual table recreation")
        else:
            print("[2/2] cartId column already exists in sales table")
        
        # Commit changes
        conn.commit()
        print("\n[OK] Migration completed successfully!")
        
    except sqlite3.Error as e:
        print(f"\n[ERROR] Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()

# Made with Bob