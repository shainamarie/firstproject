from flask import *
from functools import wraps
import sqlite3

DATABASE = 'samontedatabase.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'shainanana'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You were logged out")
    return redirect (url_for('login'))

@app.route('/hello')
@login_required
def hello():
    g.db = connect_db()
    cur = g.db.execute('select id, fname, mname, lname, gender, course, year from stud')
    students = [dict(id=row[0], fname=row[1], mname=row[2], lname=row[3], gender=row[4], course=row[5], year=row[6] ) for row in cur.fetchall()]
    g.db.commit()
    g.db.close()
    return render_template('hello.html', students=students)



@app.route('/delete/<item_id>', methods=['GET', 'DELETE'])
@login_required
def delete(item_id):
    g.db = connect_db()
    cur = g.db.execute('''delete from stud where id= ?''', (item_id,))
    students = [dict(id=row[0], fname=row[1], mname=row[2], lname=row[3], gender=row[4], course=row[5], year=row[6] ) for row in cur.fetchall()]
    g.db.commit()
    g.db.close()
    return render_template('redirect.html', students=students)


@app.route('/addform', methods=['GET', 'POST'])
@login_required
def addform():
    return render_template('addform.html')



@app.route('/adding', methods=['POST'])
@login_required
def adding():
    if request.method == 'POST':
        try:
            id = request.form['id']
            fname = request.form['fname']
            mname = request.form['mname']
            lname = request.form['lname']
            gender = request.form['gender']
            course = request.form['course']
            year = request.form['year']

            with sqlite3.connect(app.config['DATABASE']) as g.db:
                cur = g.db.execute("INSERT INTO stud(id, fname, mname, lname, gender, course, year) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, fname, mname, lname, gender, course, year))
                g.db.commit()
                g.db.close()
                msg = "Record successfully added"

        except:
            g.db.rollback()
            msg = "Error daw"

        finally:
            return render_template('redirect.html', msg=msg)




@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form ['password'] != 'admin':
            error = 'Invalid credential. Please try again'
        else:
            session['logged_in'] = True
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)

@app.route('/editprofile')
def editprofile():
    id = request.args.get('id')
    g.db = connect_db()
    cur = g.db.execute('''select id, fname, mname, lname, gender, course, year from stud where id=?''', [id])
    rv = cur.fetchall()
    cur.close()
    person = rv[0]
    g.db.close()
    return render_template('updateform.html', person=person)


@app.route('/updateprofile')
def updateprofile():
    id = request.args.get('id')
    fname = request.args.get('fname')
    mname = request.args.get('mname')
    lname = request.args.get('lname')
    gender = request.args.get('gender')
    course = request.args.get('course')
    year = request.args.get('year')
    g.db = connect_db()
    sql = "update stud set fname=?, mname=?, lname=?, gender=?, course=?, year=? where id=?"
    g.db.execute(sql, [fname, mname, lname, gender, course, year, id])
    g.db.commit()
    g.db.close()
    return render_template('redirect.html')

@app.route('/searchpage')
def searchpage():
    return render_template('search.html')

@app.route('/studentsearch', methods=['POST', 'GET'])
def studentsearch():
    if request.method == "POST":
        try:
            searchinfo = request.form['info']

            g.db = connect_db()
            cur = g.db.execute(
                "SELECT * FROM infoComplete where id = ? or COURSE_ID = ? or COLLEGE = ? or DESCRIPTION = ? or fname = ? or mname = ? or lname = ? or gender = ? or year = ?",
                (searchinfo, searchinfo, searchinfo, searchinfo, searchinfo, searchinfo, searchinfo, searchinfo,searchinfo))
            print ("1")
            coffee = cur.fetchall()
            msg = "existed"
            '''for row in cur.fetchall():
                coffee = row
                print coffee
                msg = "existed"'''

        except:
            msg = ("error")
        finally:
            print ("coffee")
            print (" copied")
            print ("the message: " + msg)
            return render_template("result.html", msg=msg, coffee=coffee)

if __name__ == '__main__':
    app.run(debug=True)
