import sqlite3
from pathlib import Path
import time
import os

# Check if database exists
db_path = Path("../db/db.sqlite")
if not db_path.exists():
    print(f"Database does not exist at {db_path}")
    print("Please run create_database.py first")
    exit(1)

# Get image files from images folder
images_dir = Path("../images")
if not images_dir.exists():
    print(f"Images directory does not exist")
    exit(1)

# Get all image files (excluding cache directory)
image_files = []
for file in images_dir.iterdir():
    if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        image_files.append(file.name)

if not image_files:
    print("No image files found in images directory")
    exit(0)

print(f"Found {len(image_files)} image files")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Current timestamp
current_timestamp = int(time.time())

# Process each image file
for image_file in image_files:
    # Extract product name from filename
    # Remove file extension and dimensions suffix (e.g., _1920x1920)
    product_name = image_file.rsplit('.', 1)[0]  # Remove extension
    
    # Remove dimension suffix if present (pattern: _NNNNxNNNN)
    if '_' in product_name:
        parts = product_name.rsplit('_', 1)
        if 'x' in parts[-1] and parts[-1].replace('x', '').isdigit():
            product_name = parts[0]
    
    # Replace underscores and hyphens with spaces for better readability
    product_name = product_name.replace('_', ' ').replace('-', ' ')
    
    # Insert product into database
    cursor.execute("""
        INSERT INTO products (name, timestamp, purchasePrice, description, imageUrl, note, active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        product_name,
        current_timestamp,
        0.0,  # Default purchase price
        "auto-generated dummy",
        image_file,
        "auto-generated dummy",
        1  # Active
    ))
    
    print(f"Added product: {product_name} (image: {image_file})")

# Commit changes and close connection
conn.commit()
conn.close()

print(f"\nSuccessfully added {len(image_files)} products to the database")

# Made with Bob