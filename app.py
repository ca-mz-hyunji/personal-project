from flask import Flask, redirect, render_template, request, url_for
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
test_users = {
    "Alice": {
        "username" : "Alice",
		"password" : "HELLOALICE"
    },
    "Bob": {
        "username" : "Bob",
		"password" : "HELLOBOB"
    }
}

@app.route('/')
def home():
    message = request.args.get('message')
    return render_template('home.html', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = request.args.get('message')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        if not username or not password or not password_confirm:
            return redirect(url_for('register', message='All fields are required.'))
        if password != password_confirm:
            return redirect(url_for('register', message='Passwords do not match.'))
        if username in test_users:
            return redirect(url_for('login', message='Username already exists. Please login instead.'))
        return redirect(url_for('home', message='You are now registered.'))
    return render_template('register.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = request.args.get('message')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = test_users.get(username)
        if username in test_users and password == test_users[username]['password']:
            return redirect(url_for('home', message='You are now logged in.'))
        else:
            return redirect(url_for('login', message='Invalid username or password. Please try again.'))
    return render_template('login.html', message=message)


if __name__=='__main__':
    app.run()
    #test_db_connection = get_db_connection("SELECt * FROM users;")