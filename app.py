from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from pymongo import MongoClient
import hashlib
import secrets


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# This will obviously need to be changed to use a database

client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
users_collection = db['users']
tokens_collection = db['tokens']

def hash_password(password, salt):
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password

def generate_salt():
    return secrets.token_hex(16)

def hash_token(token):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    return hashed_token

def generate_token():
    # Generate a random 32-byte token
    return secrets.token_hex(32)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login_or_create', methods=['POST'])
def login_or_create():

    flash_messages = get_flashed_messages(with_categories=False, category_filter=['danger'])

    for message in flash_messages:
        flash(message, 'danger')

    username = request.form['username']
    password = request.form['password']
    action = request.form['action']
    confirm_password = request.form['confirm_password']

    if action == 'login':
        user = users_collection.find_one({'username': username})
        if user:
            # Get salt from the user document
            salt = user['salt']
            # Hash the provided password with the retrieved salt
            hashed_password = hash_password(password, salt)
            # Check if the hashed password matches the one stored in the database
            if hashed_password == user['password']:
                token = generate_token()
                # Hash the token
                hashed_token = hash_token(token)
                # Store the hashed token in the database
                tokens_collection.insert_one({'username': username, 'token': hashed_token})
                # Set the token as a cookie with HttpOnly directive and expiration time
                response = make_response(redirect(url_for('dashboard')))
                response.set_cookie('auth_token', token, httponly=True, expires=datetime.datetime.now() + datetime.timedelta(hours=1))
                return response
        flash('Login failed. Please check your username and password.', 'danger')
        return redirect(url_for('index'))
        
    elif action == 'create_account':
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('index'))
        
        user = users_collection.find_one({'username': username})
        if not user:
            salt = generate_salt()
            hashed_password = hash_password(password, salt)
            users_collection.insert_one({'username': username, 'password': hashed_password, 'salt': salt})
            return redirect(url_for('dashboard'))
        else:
            flash('Username already taken. Please choose another username.', 'danger')
            return redirect(url_for('index'))

@app.route('/play_as_guest', methods=['POST'])
def play_as_guest():
    flash('Playing as Guest!', 'info')
    return redirect(url_for('dashboard'))

@app.route('/game')
def dashboard():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)
