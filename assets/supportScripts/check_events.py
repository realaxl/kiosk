import sqlite3

conn = sqlite3.connect('db/db.sqlite')
conn.row_factory = sqlite3.Row
events = conn.execute('SELECT * FROM events').fetchall()

print('All events in database:')
for e in events:
    print(f'  ID: {e["eventId"]}, Name: {e["name"]}, Active: {e["active"]}')

conn.close()

# Made with Bob
