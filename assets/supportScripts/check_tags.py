import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
db_path = PROJECT_ROOT / "db" / "db.sqlite"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("All active tags by product:")
cursor.execute('SELECT productId, name, value FROM tags WHERE active = 1 ORDER BY productId, name')
results = cursor.fetchall()
for row in results:
    print(f'  Product {row[0]}: {row[1]} = {row[2]}')

print("\nUnique tag combinations:")
cursor.execute('SELECT DISTINCT name, value FROM tags WHERE active = 1 ORDER BY name, value')
results = cursor.fetchall()
for i, row in enumerate(results, 1):
    print(f'  {i}. {row[0]}: {row[1]}')

print("\nTest query for product 1:")
cursor.execute('''
    SELECT DISTINCT name, value
    FROM tags
    WHERE active = 1
    AND (name || ':' || value) NOT IN (
        SELECT name || ':' || value
        FROM tags
        WHERE productId = 1 AND active = 1
    )
    ORDER BY name, value
''')
results = cursor.fetchall()
print(f"  Available combinations for product 1: {len(results)}")
for row in results:
    print(f'    - {row[0]}: {row[1]}')

conn.close()

# Made with Bob
