import csv
import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()
with open('books.csv', 'rt') as fin:
	dr = csv.DictReader(fin)
	to_db = [(i, val['isbn'], val['title'], val['author'], val['year']) 
				for i, val in enumerate(dr, 1)]

cur.executemany("INSERT INTO books (id, isbn, title, author, year) \
					VALUES (?, ?, ?, ?, ?);", to_db)
conn.commit()
conn.close()