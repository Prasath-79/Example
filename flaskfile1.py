from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(_name_)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'prasathdb'
app.config['MYSQL_DB'] = 'StudentDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(name, age, grade) VALUES(%s, %s, %s)", (name, age, grade))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home'))

if (_name== 'main_'):
    app.run(debug=True)