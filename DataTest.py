import sqlite3 as sql

conn = sql.connect("C:\\SQLITE\\testtest.db")
cur = conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS names(first TEXT, last TEXT)''')

testData = [("Faith", "Connors"),
            ("Sam", "Fisher"),
            ("Sol", "Badguy"),
            ("Evie", "Frye"),
            ("Jesse", "Faden")]

try:
    cur.executemany('''INSERT INTO names(first, last) VALUES (?, ?)''', testData)
    conn.commit()
    print("Operation Successful")
except sql.Error:
    print("Operation Failed")

cur.close()
conn.close()
