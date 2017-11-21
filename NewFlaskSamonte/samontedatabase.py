import sqlite3 as lite
import sys


students = (
    ('2015-2567', 'Shaina Marie', 'Anim', 'Samonte', 'F', 'BSCS','3' ),
    ('2015-0444', 'James', 'Villa', 'Lavilla', 'M', 'BSIT', '3'),
    ('2015-2356', 'Karyl', 'Lambayong', 'Sabulbero', 'F', 'BSCS', '3')
)

con = lite.connect('samontedatabase.db')

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS stud")
    cur.execute("CREATE TABLE stud(id TEXT PRIMARY KEY, fname TEXT, mname TEXT, lname TEXT, gender INT, course TEXT, year TEXT )")
    cur.executemany("INSERT INTO stud VALUES(?, ?, ?, ?, ?, ?, ?)", students)

    cur.execute(
        'CREATE TABLE IF NOT EXISTS studcourses(COURSE_ID TEXT PRIMARY KEY, DESCRIPTION TEXT, COLLEGE TEXT)')
    cur.execute(
        "INSERT OR IGNORE INTO studcourses(COURSE_ID, DESCRIPTION, COLLEGE) VALUES ('BSCS', 'Bachelor of Science in Computer Science', 'SCS')")
    cur.execute(
        "INSERT OR IGNORE INTO studcourses(COURSE_ID, DESCRIPTION, COLLEGE) VALUES ('BSIT', 'Bachelor of Science in Information Technology', 'SCS')")
    cur.execute(
        "INSERT OR IGNORE INTO studcourses(COURSE_ID, DESCRIPTION, COLLEGE) VALUES ('BSECT', 'Bachelor of Science in Electronics and Computer Technology', 'SCS')")
    cur.execute(
        "INSERT OR IGNORE INTO studcourses(COURSE_ID, DESCRIPTION, COLLEGE) VALUES ('ECET', 'Electronics Engineering Technology', 'SCS')")

    cur.execute(
        "CREATE VIEW IF NOT EXISTS courseRecord AS SELECT COURSE_ID, lname, fname, DESCRIPTION, COLLEGE, year FROM stud CROSS JOIN studcourses WHERE studcourses.COURSE_ID = stud.course")
    cur.execute(
        "CREATE VIEW IF NOT EXISTS infoComplete AS SELECT  id, COURSE_ID, DESCRIPTION, COLLEGE, lname, fname, mname, gender, year FROM stud CROSS JOIN studcourses WHERE studcourses.COURSE_ID = stud.course")
