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
    cur = g.db.execute('select id, fname, lname, idno, email from stud')
    students = [dict(id=row[0], fname=row[1], lname=row[2],  idno=row[3],  email=row[4]) for row in cur.fetchall()]
    g.db.commit()
    g.db.close()
    return render_template('hello.html', students=students)



@app.route('/delete/<item_id>', methods=['GET', 'DELETE'])
@login_required
def delete(item_id):
    g.db = connect_db()
    cur = g.db.execute('''delete from stud where id= ?''', (item_id,))
    students = [dict(id=row[0], fname=row[1], lname=row[2], idno=row[3], email=row[4]) for row in cur.fetchall()]
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
            fname = request.form['fname']
            lname = request.form['lname']
            idno = request.form['idno']
            email = request.form['email']
            password = request.form['password']

            with sqlite3.connect(app.config['DATABASE']) as g.db:
                cur = g.db.execute("INSERT INTO stud(fname, lname, idno, email, password) VALUES (?, ?, ?, ?, ?)", (fname, lname, idno, email, password))
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
    cur = g.db.execute('''select id, fname, lname, idno, email, password from stud where id=?''', [id])
    rv = cur.fetchall()
    cur.close()
    person = rv[0]
    g.db.close()
    return render_template('updateform.html', person=person)


@app.route('/updateprofile')
def updateprofile():
    id = request.args.get('id')
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    idno = request.args.get('idno')
    email = request.args.get('email')
    password = request.args.get('password')
    g.db = connect_db()
    sql = "update stud set fname=?, lname=?, idno=?, email=?, password=? where id=?"
    g.db.execute(sql, [fname, lname, idno, email, password, id])
    g.db.commit()
    g.db.close()
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)