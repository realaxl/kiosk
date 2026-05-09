import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
db_path = PROJECT_ROOT / 'db' / 'db.sqlite'

conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all active products
products = cursor.execute('SELECT * FROM products WHERE active = 1').fetchall()

print("Testing product data structure:\n")

# Get tags for each product
for product in products[:3]:  # Just test first 3
    product_dict = dict(product)
    
    # Fetch tags for this product
    tags = cursor.execute('''
        SELECT name, value FROM tags 
        WHERE productId = ? AND active = 1
    ''', (product['productId'],)).fetchall()
    
    product_dict['tags'] = [dict(tag) for tag in tags]
    
    print(f"Product: {product_dict['name']}")
    print(f"  productId: {product_dict['productId']}")
    print(f"  tags: {product_dict['tags']}")
    print()

conn.close()

# Made with Bob
