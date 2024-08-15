from flask import Flask, flash, redirect, render_template, request, url_for
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)
'''
DB_CONFIG = {
    'host': '172.17.0.2',
    'user': 'root',
    'password': 'password',
    'database': 'authdata',
    'port': 3306
}

def get_db_connection(sql):
    connection = pymysql.connect(**DB_CONFIG, cursorclass=DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()
'''
account = {
    1: {
        "username" : "Alice",
		"password" : "HELLOALICE",
		"city" : "New York"
    },
    2: {
        "username" : "Bob",
		"password" : "HELLOBOB",
		"city" : "San Francisco"
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'Alice' and password == 'HELLOALICE':
            flash('You are now logged in.', 'success')
            return redirect(url_for('home'))
        elif username == 'Bob' and password == 'HELLOBOB':
            flash('You are now logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

"""
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'city' in request.form:
        if request.form:
            username = request.form['username']
            password = request.form['password']
            city = request.form['city']
            msg = 'You have successfully registered'
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('login.html')
"""

if __name__=='__main__':
    app.run()
    #test_db_connection = get_db_connection("SELECt * FROM users;")