import sqlite3
from pathlib import Path

# Get the project root directory (parent of src directory)
PROJECT_ROOT = Path(__file__).parent.parent

# Create db directory if it doesn't exist
db_dir = PROJECT_ROOT / "db"
db_dir.mkdir(exist_ok=True)

# Database file path
db_path = db_dir / "db.sqlite"

# Define the expected schema based on db.mmd
SCHEMA = {
    "events": {
        "columns": {
            "eventId": "INTEGER PRIMARY KEY",
            "name": "TEXT NOT NULL",
            "timestamp": "INTEGER NOT NULL",
            "description": "TEXT",
            "note": "TEXT",
            "active": "INTEGER NOT NULL DEFAULT 1"
        }
    },
    "productCategories": {
        "columns": {
            "productCategoryId": "INTEGER PRIMARY KEY",
            "name": "TEXT NOT NULL",
            "description": "TEXT",
            "image": "TEXT",
            "note": "TEXT",
            "active": "INTEGER NOT NULL DEFAULT 1"
        }
    },
    "products": {
        "columns": {
            "productId": "INTEGER PRIMARY KEY",
            "productCategoryId": "INTEGER",
            "name": "TEXT NOT NULL",
            "timestamp": "INTEGER NOT NULL",
            "purchasePrice": "REAL NOT NULL",
            "description": "TEXT",
            "image": "TEXT",
            "url": "TEXT",
            "manualUrl": "TEXT",
            "note": "TEXT",
            "active": "INTEGER NOT NULL DEFAULT 1"
        },
        "foreign_keys": [
            "FOREIGN KEY (productCategoryId) REFERENCES productCategories(productCategoryId)"
        ]
    },
    "stocks": {
        "columns": {
            "stockId": "INTEGER PRIMARY KEY",
            "eventId": "INTEGER NOT NULL",
            "productId": "INTEGER NOT NULL",
            "initialNumberInStock": "INTEGER NOT NULL",
            "currentNumberInStock": "INTEGER NOT NULL",
            "salePrice": "REAL NOT NULL",
            "note": "TEXT",
            "favorite": "INTEGER",
            "active": "INTEGER NOT NULL DEFAULT 1"
        },
        "foreign_keys": [
            "FOREIGN KEY (eventId) REFERENCES events(eventId)",
            "FOREIGN KEY (productId) REFERENCES products(productId)"
        ]
    },
    "carts": {
        "columns": {
            "cartId": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "timestamp": "INTEGER NOT NULL",
            "note": "TEXT",
            "active": "INTEGER NOT NULL DEFAULT 1"
        }
    },
    "sales": {
        "columns": {
            "saleId": "INTEGER PRIMARY KEY",
            "cartId": "INTEGER",
            "stockId": "INTEGER NOT NULL",
            "numberItemsSold": "INTEGER NOT NULL",
            "timestamp": "INTEGER NOT NULL",
            "note": "TEXT"
        },
        "foreign_keys": [
            "FOREIGN KEY (cartId) REFERENCES carts(cartId)",
            "FOREIGN KEY (stockId) REFERENCES stocks(stockId)"
        ]
    },
    "tags": {
        "columns": {
            "tagId": "INTEGER PRIMARY KEY",
            "productId": "INTEGER NOT NULL",
            "name": "TEXT NOT NULL",
            "value": "TEXT",
            "note": "TEXT",
            "active": "INTEGER NOT NULL DEFAULT 1"
        },
        "foreign_keys": [
            "FOREIGN KEY (productId) REFERENCES products(productId)"
        ]
    }
}


def get_existing_tables(cursor):
    """Get list of existing tables in the database."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return {row[0] for row in cursor.fetchall()}


def get_table_columns(cursor, table_name):
    """Get list of columns in a table."""
    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}


def create_table(cursor, table_name, table_schema):
    """Create a new table with the given schema."""
    columns = []
    for col_name, col_def in table_schema["columns"].items():
        columns.append(f"{col_name} {col_def}")
    
    # Add foreign keys if present
    if "foreign_keys" in table_schema:
        columns.extend(table_schema["foreign_keys"])
    
    columns_str = ",\n    ".join(columns)
    create_sql = f"CREATE TABLE {table_name} (\n    {columns_str}\n)"
    cursor.execute(create_sql)
    print(f"  [+] Created table: {table_name}")


def add_missing_columns(cursor, table_name, table_schema):
    """Add missing columns to an existing table."""
    existing_columns = get_table_columns(cursor, table_name)
    expected_columns = set(table_schema["columns"].keys())
    missing_columns = expected_columns - existing_columns
    
    if missing_columns:
        for col_name in missing_columns:
            col_def = table_schema["columns"][col_name]
            # Remove PRIMARY KEY constraint for ALTER TABLE
            col_def_alter = col_def.replace(" PRIMARY KEY", "")
            try:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_def_alter}")
                print(f"  [+] Added column '{col_name}' to table '{table_name}'")
            except sqlite3.OperationalError as e:
                print(f"  [!] Could not add column '{col_name}' to '{table_name}': {e}")
    else:
        print(f"  [OK] Table '{table_name}' is up to date")


def main():
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    db_exists = db_path.exists() and db_path.stat().st_size > 0
    
    if db_exists:
        print(f"Database exists at {db_path}")
        print("Checking schema against db.mmd...\n")
        
        # Get existing tables
        existing_tables = get_existing_tables(cursor)
        expected_tables = set(SCHEMA.keys())
        
        # Create missing tables
        missing_tables = expected_tables - existing_tables
        if missing_tables:
            print("Creating missing tables:")
            for table_name in missing_tables:
                create_table(cursor, table_name, SCHEMA[table_name])
            print()
        
        # Check and update existing tables
        print("Checking existing tables for missing columns:")
        for table_name in expected_tables:
            if table_name in existing_tables:
                add_missing_columns(cursor, table_name, SCHEMA[table_name])
        
        print("\n[OK] Database schema updated successfully")
    else:
        print(f"Creating new database at {db_path}\n")
        
        # Create all tables
        for table_name, table_schema in SCHEMA.items():
            create_table(cursor, table_name, table_schema)
        
        print(f"\n[OK] Database created successfully")
        print("Tables created: events, productCategories, products, stocks, carts, sales, tags")
        print("Foreign key constraints enabled")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()

# Made with Bob