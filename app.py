from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from flask_mail import Mail, Message
import re
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Atlas connection
client = MongoClient('mongodb+srv://ganistar6360_db_user:gani1939@cluster0.jg20zj7.mongodb.net/?appName=Cluster0')
db = client['geeklogin']
accounts = db['accounts']

# Email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ganistar6360@gmail.com'      # Your Gmail
app.config['MAIL_PASSWORD'] = 'ifxh fypd ysyv iqjs'          # Your 16 char app password

mail = Mail(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = accounts.find_one({'username': username, 'password': password})
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            return render_template('index.html', msg='Logged in successfully!')
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = accounts.find_one({'$or': [{'username': username}, {'email': email}]})
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            accounts.insert_one({'username': username, 'password': password, 'email': email})
            msg = 'You have successfully registered!'
    return render_template('register.html', msg=msg)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        account = accounts.find_one({'email': email})
        if account:
            token = str(uuid.uuid4())
            accounts.update_one({'email': email}, {'$set': {'reset_token': token}})
            reset_link = url_for('reset_password', token=token, _external=True)
            message = Message('Password Reset Request',
                sender='ganistar6360@gmail.com',
                recipients=[email])
            message.body = f'Click this link to reset your password: {reset_link}'
            mail.send(message)
            msg = 'Reset link sent to your email!'
        else:
            msg = 'Email not found!'
    return render_template('forgot_password.html', msg=msg)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    msg = ''
    account = accounts.find_one({'reset_token': token})
    if not account:
        return 'Invalid or expired token!'
    if request.method == 'POST':
        new_password = request.form['password']
        accounts.update_one({'reset_token': token}, {
            '$set': {'password': new_password},
            '$unset': {'reset_token': ''}
        })
        msg = 'Password reset successful! You can now login.'
        return redirect(url_for('login'))
    return render_template('reset_password.html', msg=msg, token=token)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)