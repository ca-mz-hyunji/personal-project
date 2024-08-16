from flask import Flask, redirect, render_template, request, url_for
import pymysql
from pymysql.cursors import DictCursor
import os

UPLOAD_FOLDER = 'C:\\Users\\Kim\\Desktop\\GitHub\\personal-project\\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'web_app',
    'port': 3306
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    message = request.args.get('message')
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home', message='File successfully uploaded.'))
        else:
            return redirect(url_for('home', message='File type not allowed.'))
    return render_template('upload.html', message=message)


def get_db_connection():
    return pymysql.connect(**DB_CONFIG, cursorclass=DictCursor)
        
def get_user_data(username, password):
    search_sql = "SELECT * FROM auth_data WHERE username=%s AND password=%s;"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(search_sql, (username, password))
            rows = cursor.fetchall()
            if rows:
                user_data = rows[0]
                return user_data
            else:
                return {}

def check_username(username):
    search_sql = "SELECT * FROM auth_data WHERE username=%s;"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(search_sql, (username))
            rows = cursor.fetchall()
            if rows:
                return True
            else:
                return False

def add_new_user(username, password):
    write_sql = "INSERT INTO auth_data (username, password) VALUES (%s, %s)"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(write_sql, (username, password))
            connection.commit()
        

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
        # check if the username already exists
        user_exist = check_username(username)

        if not username or not password or not password_confirm:
            return redirect(url_for('register', message='All fields are required.'))
        if password != password_confirm:
            return redirect(url_for('register', message='Passwords do not match.'))
        if user_exist == True:
            return redirect(url_for('login', message='Username already exists. Please login instead.'))
        
        add_new_user(username, password)
        return redirect(url_for('home', message='You are now successfully registered.'))
    
    return render_template('register.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = request.args.get('message')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # get the data from the DB
        user_data = get_user_data(username, password)
        if user_data and username == user_data['username'] and password == user_data['password']:
            return redirect(url_for('home', message='You are now successfully logged in.'))
        else:
            return redirect(url_for('login', message='Invalid username or password. Please try again.'))
        
    return render_template('login.html', message=message)


if __name__=='__main__':
    app.run()