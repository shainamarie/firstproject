import sqlite3 as lite
import sys


students = (
    ('0', 'Shaina Marie', 'Samonte', '20152567', 'cutiesshaina98@gmail.com', 'nanana' ),
    ('1', 'James', 'Lavilla', '20150444', 'jacob', 'jems'),
    ('2', 'Karyl', 'Sabulbero', '20150001', 'carla', 'luhhh')
)

con = lite.connect('samontedatabase.db')

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS stud")
    cur.execute("CREATE TABLE stud(id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, idno INT, email TEXT, password TEXT )")
    cur.executemany("INSERT INTO stud VALUES(?, ?, ?, ?, ?, ?)", students)