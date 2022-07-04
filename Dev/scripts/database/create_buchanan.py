#!/usr/bin/python

from connect import connect
import csv

conn = connect()
cur = conn.cursor()
cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('buchanan',))

if cur.fetchone()[0]:
    print("Buchanan table already exists \nDropping table")
    cur.execute("DROP TABLE buchanan")
    print('Table buchanan dropped')
else:
    print("Buchanan table doesn't exist\nCreate table required")
commands = (
    """
    CREATE TABLE buchanan (
        id SERIAL PRIMARY KEY,
        animal VARCHAR(2550) NOT NULL,
        race VARCHAR(255) NOT NULL,
        recumbency VARCHAr(255) NOT NULL,
        vhs REAL NOT NULL,
        precision REAL NOT NULL
    )
    """
)

cur.execute(commands)
print('Table buchanan created')
print('inserting data')

f = open('../../data/buchanan/indices.csv')
cur.copy_from(f, 'buchanan', sep=';', columns=('animal', 'race', 'recumbency', 'vhs', 'precision'))
cur.execute('SELECT count(*) FROM buchanan')

print(cur.fetchone()[0], 'rows in buchanan table')
print('Closing connection')

conn.commit()
conn.close()
