import sqlite3
import uuid
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Database file path
db_path = PROJECT_ROOT / "db" / "db.sqlite"

# List of all tables that need uuid column
TABLES = [
    "events",
    "productCategories",
    "products",
    "stocks",
    "carts",
    "sales",
    "tags",
    "productRelations"
]

def add_uuid_column_to_table(cursor, table_name):
    """Add uuid column to a table if it doesn't exist"""
    # Check if uuid column already exists
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'uuid' in columns:
        print(f"  [SKIP] Table '{table_name}' already has uuid column")
        return False
    
    # Add uuid column
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN uuid TEXT")
    print(f"  [+] Added uuid column to table '{table_name}'")
    return True

def populate_uuid_for_table(cursor, table_name, primary_key):
    """Populate uuid column with unique UUIDs for existing records"""
    # Get all records without uuid
    cursor.execute(f"SELECT {primary_key} FROM {table_name} WHERE uuid IS NULL")
    records = cursor.fetchall()
    
    if not records:
        print(f"  [OK] No records to update in '{table_name}'")
        return
    
    # Update each record with a unique UUID
    for record in records:
        pk_value = record[0]
        new_uuid = str(uuid.uuid4())
        cursor.execute(f"UPDATE {table_name} SET uuid = ? WHERE {primary_key} = ?", (new_uuid, pk_value))
    
    print(f"  [+] Populated {len(records)} records with UUIDs in '{table_name}'")

def main():
    print("=== UUID Migration Script ===\n")
    
    # Check if database exists
    if not db_path.exists():
        print(f"[ERROR] Database not found at {db_path}")
        print("Please run create_database.py first")
        return
    
    # Connect to database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Table to primary key mapping
    table_pk_map = {
        "events": "eventId",
        "productCategories": "productCategoryId",
        "products": "productId",
        "stocks": "stockId",
        "carts": "cartId",
        "sales": "saleId",
        "tags": "tagId",
        "productRelations": "productRelationId"
    }
    
    print("Step 1: Adding uuid column to all tables\n")
    for table_name in TABLES:
        add_uuid_column_to_table(cursor, table_name)
    
    print("\nStep 2: Populating uuid column with unique UUIDs\n")
    for table_name in TABLES:
        if table_name in table_pk_map:
            populate_uuid_for_table(cursor, table_name, table_pk_map[table_name])
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("\n=== Migration Complete ===")
    print("All tables now have uuid column with unique UUIDs")

if __name__ == "__main__":
    main()

# Made with Bob