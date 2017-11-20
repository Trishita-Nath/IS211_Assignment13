from flask import Flask, render_template, redirect, request, session, g
import  sqlite3
from sqlite3 import Error
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

def create_connection(db):
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)
    return None


@app.route("/")
def index():
    
    return redirect("/login")

@app.route("/login", methods = ["POST", "GET"])
def login():           
    error = ""
    if request.method == "POST":
        session.pop('user', None)
        if request.form['uname'] != 'admin' or request.form['pwd'] != 'password':            
            error = "Invalid Credentials. Please try again"
            return render_template("login.html", error = error)            
        else:
            session['user'] = request.form['uname']
            return redirect('/dashboard')
    return render_template("login.html", error = error)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route("/logout")
def dropsession():
    session.pop('user', None)
    return render_template("login.html")    
        
@app.route("/dashboard", methods = ["GET"])
def dashboard():
    dbdata_students = ""
    dbdata_quizzes = ""
    error_mgs = ""
    try:
        conn = create_connection("hw13.db")
        cur = conn.cursor()
        cur.execute('Select * FROM students')        
        dbdata_students = cur.fetchall()
        cur.execute('Select * FROM quizzes')
        dbdata_quizzes = cur.fetchall()
    except Error as e:
        error_mgs = e
        print(e)
        conn.close
        
    if g.user:        
        return render_template("dashboard.html", dbdata_students = dbdata_students, dbdata_quizzes = dbdata_quizzes, error_msg = error_mgs)
        conn.close
    return render_template("login.html")

@app.route("/student/add", methods = ["POST", "GET"])
def addstudent():
    error_mgs = ""
    try:
        conn = create_connection("hw13.db")
        cur = conn.cursor()       
        if request.method == "POST":            
            cur.execute('insert into students (first_name, last_name) values (?,?)', (request.form['sfname'], request.form['slname']))
            conn.commit()           
            
            return redirect("/dashboard")
            
    except Error as e:
        error_mgs = e
        return render_template("addstudent.html", error_mgs = error_mgs)
        print(e)        
        conn.close
        
    if g.user:        
        return render_template("addstudent.html", error_mgs = error_mgs)
        conn.close
    return render_template("login.html")

@app.route("/quiz/add", methods = ["POST", "GET"])
def addquiz():
    error_mgs = ""
    try:
        conn = create_connection("hw13.db")
        cur = conn.cursor()
        if request.method == "POST":            
            cur.execute('insert into quizzes (subject, question_count, quiz_date) values (?,?,?)', (request.form['subject'], request.form['count'],
                                                                                                    request.form['date']))
            conn.commit()
            return redirect("/dashboard")
            
    except Error as e:
        error_mgs = e
        return render_template("addquiz.html", error_mgs = error_mgs)
        print(e)        
        conn.close    
    
    if g.user:        
        return render_template("addquiz.html", error_mgs = error_mgs)
        conn.close
    return render_template("login.html")

@app.route("/results/add", methods = ["POST", "GET"])
def addresult():
    error_mgs = ""
    add_score = ""
    add_score_msg = ""
    try:
        conn = create_connection("hw13.db")
        cur = conn.cursor()
        cur.execute('Select * FROM students')        
        dbdata_students = cur.fetchall()
        cur.execute('Select * FROM quizzes')
        dbdata_quizzes = cur.fetchall()
        
        if request.method == "POST":
            add_score = request.form['score']
            if 0 <= int(add_score) <= 100:
                
                add_student = request.form.get('select_student')
                add_quiz = request.form.get('select_quiz')
                add_score = request.form['score']
                conn = create_connection("hw13.db")
                cur = conn.cursor()
                cur.execute('Insert into results (student_id, quiz_id, quiz_score) values(?,?,?)', (request.form.get('select_student'), request.form.get('select_quiz'),
                                                                                                request.form['score']))
                conn.commit()
                return redirect("/dashboard")
            else:
                
                add_score_msg = "Invalid Score. Please re-enter data"
                return render_template("addresult.html", dbdata_students = dbdata_students, dbdata_quizzes = dbdata_quizzes, add_score_msg = add_score_msg)
       
    except Error as e:
        error_mgs = e
        return render_template("addresult.html", error_mgs = error_mgs)
        print(e)
        conn.close

    if g.user:
        return render_template("addresult.html", dbdata_students = dbdata_students, dbdata_quizzes = dbdata_quizzes, error_mgs = error_mgs)
        conn.close
    return render_template("login.html")

@app.route("/student/<studentid>", methods = ["POST", "GET"])
def quizresult(studentid):
    quiz_results = ""    
    error_mgs = ""
    quiz_results_mgs = ""
    try:
        conn = create_connection("hw13.db")
        cur = conn.cursor()
        cur.execute('Select students.first_name, students.last_name, '+
                    'quizzes.subject, results.quiz_score, quizzes.quiz_date From results Join students On results.student_id = students.id '+
                    'Join quizzes On results.quiz_id = quizzes.id Where students.id =' + str(studentid))
                    
        quiz_results = cur.fetchall()
    except Error as e:
        error_mgs = e
        print(e)
        conn.close
        
    if g.user:
        if not quiz_results:
            quiz_results_mgs = "No Results"
        return render_template("viewresult.html", error_mgs = error_mgs, quiz_results = quiz_results, quiz_results_mgs = quiz_results_mgs)
        conn.close
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)
    #app.run()   
