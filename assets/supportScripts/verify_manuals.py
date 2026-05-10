import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
db_path = PROJECT_ROOT / 'db' / 'db.sqlite'

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

cursor.execute('SELECT name, manualUrl FROM products ORDER BY name')
products = cursor.fetchall()

print("Products with manual URLs:\n")
for name, manual_url in products:
    status = "[OK]" if manual_url else "[NO]"
    url_display = manual_url if manual_url else "(no manual)"
    print(f"{status} {name}")
    if manual_url:
        print(f"  {url_display}")

conn.close()

# Made with Bob
