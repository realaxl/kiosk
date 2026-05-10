import sqlite3
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
db_path = PROJECT_ROOT / 'db' / 'db.sqlite'

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get all product IDs
cursor.execute('SELECT productId, name FROM products')
products = cursor.fetchall()

# Check existing tags to avoid duplicates
cursor.execute('SELECT productId FROM tags WHERE name = "Schwierigkeit"')
existing_tags = {row[0] for row in cursor.fetchall()}

difficulty_levels = ["leicht", "mittel"]
added_count = 0
skipped_count = 0

print("Adding difficulty tags...\n")

for product_id, product_name in products:
    if product_id in existing_tags:
        print(f"[SKIP] {product_name} (already has difficulty tag)")
        skipped_count += 1
        continue
    
    # Randomly assign difficulty
    difficulty = random.choice(difficulty_levels)
    
    cursor.execute('''
        INSERT INTO tags (productId, name, value, note, active)
        VALUES (?, ?, ?, ?, ?)
    ''', (product_id, "Schwierigkeit", difficulty, None, 1))
    
    print(f"[+] {product_name}: {difficulty}")
    added_count += 1

conn.commit()
conn.close()

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Added: {added_count} tags")
print(f"  Skipped: {skipped_count} tags (already existed)")
print(f"{'='*60}")

# Made with Bob
