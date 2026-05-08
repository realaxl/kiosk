import sqlite3
from pathlib import Path

# Create db directory if it doesn't exist
db_dir = Path("../db")
db_dir.mkdir(exist_ok=True)

# Database file path
db_path = db_dir / "db.sqlite"

# Check if database already exists
if db_path.exists():
    print(f"Database already exists at {db_path}")
    exit(0)

# Create database and tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON")

# Create events table
cursor.execute("""
CREATE TABLE events (
    eventId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    description TEXT,
    note TEXT,
    active INTEGER NOT NULL DEFAULT 1
)
""")

# Create products table
cursor.execute("""
CREATE TABLE products (
    productId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    purchasePrice REAL NOT NULL,
    description TEXT,
    imageUrl TEXT,
    manualUrl TEXT,
    note TEXT,
    active INTEGER NOT NULL DEFAULT 1
)
""")

# Create stocks table with foreign keys
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

# Create sales table with foreign key
cursor.execute("""
CREATE TABLE sales (
    saleId INTEGER PRIMARY KEY,
    stockId INTEGER NOT NULL,
    numberItemsSold INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    note TEXT,
    FOREIGN KEY (stockId) REFERENCES stocks(stockId)
)
""")

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Database created successfully at {db_path}")
print("Tables created: events, products, stocks, sales")
print("Foreign key constraints enabled")

# Made with Bob