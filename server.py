from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, make_response, send_from_directory, jsonify, abort
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import datetime
from util.auth import *
from util.db import *
import html
from flask_sock import Sock
import time
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

sock = Sock(app)

def getUsername(request):
    username = "Guest"
    if "auth_token" in request.cookies:
        cookie_value = request.cookies.get('auth_token')
        username = find_user(cookie_value)
    return username

@sock.route('/gamews')
def test_ws(socket):
    print("I AM CONNECTED")
    print(socket)
    username = getUsername(request)
    while True:
        raw_data = socket.receive(timeout=0)
        try:
            data_to_send = {"Username":username, "message":"server message"}
            send_data = json.dumps(data_to_send)
            socket.send(send_data)

            print("RAW DATA: ", raw_data)
            # recieved_data = json.loads(raw_data)
            print("DATA", json.loads(raw_data))
            
            print("Here")
        except:
            pass
        
        time.sleep(5)



@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
 
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/playstyles.css')
def playstyle():
    return send_from_directory('static', 'playstyles.css')


@app.route('/styles.css')
def style():
    return send_from_directory('static', 'styles.css')


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
            salt = user['salt']
            hashed_password = hash_password(password, salt)
            if hashed_password == user['password']:
                token = generate_token()
                hashed_token = hash_token(token)
                tokens_collection.delete_one({'username': username})
                tokens_collection.insert_one({'username': username, 'token': hashed_token})
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
            token = generate_token()
            hashed_token = hash_token(token)
            tokens_collection.insert_one({'username': username, 'token': hashed_token})
            salt = generate_salt()
            hashed_password = hash_password(password, salt)
            users_collection.insert_one({'username': username, 'password': hashed_password, 'salt': salt})
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('auth_token', token, httponly=True, expires=datetime.datetime.now() + datetime.timedelta(hours=1))
            return response
        else:
            flash('Username already taken. Please choose another username.', 'danger')
            return redirect(url_for('index'))

@app.route('/play_as_guest', methods=['POST'])
def play_as_guest():
    flash('Playing as Guest!', 'info')
    username = getUsername(request)
    return render_template('playPage.html', name=username)



@app.route('/game')
def dashboard():
    username = getUsername(request)
    return render_template('playPage.html', name=username)


@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('auth_token', '', expires=0)  # Remove the auth_token cookie
    return response

@app.route('/api/chat',  methods=['GET', 'POST'])
def add_chat_message():
    username = "Guest"
    if "auth_token" in request.cookies:
        cookie_value = request.cookies.get('auth_token')
        username = find_user(cookie_value)
    if request.method == "GET":
        # GET TOTAL FROM DATABASE
        return jsonify(getallmessages(username))#[{"username": "test", "message": "something","id":1},{"username": "test2", "message": "something2","id":2}]), 200
    data = request.json
    # print("data:",data)

    message = data.get('message')
  #  print(message)
    
    if message:
        id = storeMessage(username, message)
        #chat_collection.insert_one({'username': username, 'message': message})
        return jsonify({"username": username, "message": message,"id":id, "count":0}), 201
    else:
        return jsonify({'error': 'Username and message are required'}), 400
    
@app.route('/api/like', methods=['POST'])
def add_like_data():
    if "auth_token" in request.cookies:
        cookie_value = request.cookies.get('auth_token')
        data = request.json
        id = data["id"]

        username = find_user(cookie_value)
        message = getSingleMessage(id)
        notLiked = True
        if username in  message["likes"]:
            notLiked = False
        color, count = updateLikeCount(id, username, notLiked)
        return jsonify({"color": color, "count":count}), 201
    else:
        abort(403)

def main():
    host = "0.0.0.0"
    port = 8080

    print("Listening on port " + str(port))
    
    app.run(host=host, port=port)
    # socketio.run(app, host=host, port=port, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    main()
