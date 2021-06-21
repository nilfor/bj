import sqlite3 as sql

connection = sql.connect("db.db", check_same_thread=False)
q = connection.cursor()
