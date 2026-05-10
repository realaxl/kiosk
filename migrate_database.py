"""
Database migration script to:
1. Rename imageUrl to image in products table
2. Add url column to products table
"""
import sqlite3
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent
db_path = PROJECT_ROOT / "db" / "db.sqlite"

def migrate_database():
    print(f"Migrating database at {db_path}\n")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = OFF")
    
    try:
        # Step 1: Create new products table with updated schema
        print("Creating new products table with updated schema...")
        cursor.execute("""
            CREATE TABLE products_new (
                productId INTEGER PRIMARY KEY,
                productCategoryId INTEGER,
                name TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                purchasePrice REAL NOT NULL,
                description TEXT,
                image TEXT,
                url TEXT,
                manualUrl TEXT,
                note TEXT,
                active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (productCategoryId) REFERENCES productCategories(productCategoryId)
            )
        """)
        print("  [+] Created products_new table")
        
        # Step 2: Copy data from old table to new table
        print("\nCopying data from products to products_new...")
        cursor.execute("""
            INSERT INTO products_new 
                (productId, productCategoryId, name, timestamp, purchasePrice, 
                 description, image, manualUrl, note, active)
            SELECT 
                productId, productCategoryId, name, timestamp, purchasePrice,
                description, imageUrl, manualUrl, note, active
            FROM products
        """)
        rows_copied = cursor.rowcount
        print(f"  [+] Copied {rows_copied} rows")
        
        # Step 3: Drop old table
        print("\nDropping old products table...")
        cursor.execute("DROP TABLE products")
        print("  [+] Dropped products table")
        
        # Step 4: Rename new table to products
        print("\nRenaming products_new to products...")
        cursor.execute("ALTER TABLE products_new RENAME TO products")
        print("  [+] Renamed products_new to products")
        
        # Commit changes
        conn.commit()
        print("\n[OK] Migration completed successfully!")
        print("Changes:")
        print("  - Renamed column: imageUrl → image")
        print("  - Added column: url (TEXT)")
        
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
