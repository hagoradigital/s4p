import sqlite3

conn = sqlite3.connect('instance/sgp.db')
cursor = conn.cursor()

cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    if table[0] is not None:
        print(table[0])
        print("\n" + "-" * 80 + "\n")

conn.close()