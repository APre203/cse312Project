import uuid
from flask import Flask, render_template, request, redirect, send_file, url_for, flash, get_flashed_messages, make_response, send_from_directory, jsonify, abort
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import datetime
from util.auth import *
from util.db import *
import json
from util.DBuploads import getImage, storeImage
from util.gameBoard import GameBoard
from util.player import Player
import threading
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'
ssl_context = ('/etc/letsencrypt/live/heapoverflow312.me/fullchain.pem', '/etc/letsencrypt/live/heapoverflow312.me/privkey.pem')

timer_duration = 30
start_time = None

socketio = SocketIO(app, cors_allowed_origins="*")#, transports=['websocket'])
# sock = Sock(app)
app.config['UPLOAD_FOLDER'] = 'static/images'

gameBoard = GameBoard(100)

def getUsername(request):
    username = "Guest"
    if "auth_token" in request.cookies:
        cookie_value = request.cookies.get('auth_token')
        username = find_user(cookie_value)
    return username

@socketio.on("connect")
def handle_connection():
    socket = request.sid
    username = getUsername(request)
    if username != "Guest":
        gameBoard.addPlayer(Player(username))
    # gameState = gameBoard.gameState()
    gameState = gameBoard.gameState()
    # print("Actual GameState",gameBoard.gameState())
    socketio.emit('new-gamestate',gameState)
    print("User Connected -- ",username,  "-- Socket: ", socket)

@socketio.on("disconnect")
def handle_disconnect():
    username = getUsername(request)
    gameBoard.removePlayer(username)
    gameState = gameBoard.gameState()
    # print("Actual GameState",gameBoard.gameState())

    socketio.emit('new-gamestate',gameState)
    # if len(gameBoard.players) == 0:
    #     gameBoard = GameBoard()
    print("User Disconnect -- ", username)

@socketio.on("request-game-state")
def handle_request_state():
    gameState = gameBoard.gameState()
    # print("Actual GameState",gameBoard.gameState())

    socketio.emit('new-gamestate',gameState)

@socketio.on("handle_update_game_state")
def handle_update_game_state(userUpdate):
    try:
        userUpdate = json.loads(userUpdate)
        # print("USER-Update -- ",userUpdate)
        username = userUpdate["username"]["username"]
        player = gameBoard.findPlayer(username)
        if userUpdate["username"]["location"][0] != 0 or userUpdate["username"]["location"][1] != 0 or userUpdate["username"]["score"] != 0:
            player.top = userUpdate["username"]["location"][0]
            player.left = userUpdate["username"]["location"][1]
            player.updateScore(userUpdate["username"]["score"])

            if len(userUpdate["balls"]) > 0:
                for balls in userUpdate["balls"]:
                    gameBoard.removeBall(top=balls[0], left=balls[1])

            gameState = gameBoard.gameState()
            # print("Actual GameState",gameBoard.gameState())

            socketio.emit('new-gamestate',gameState)
    except Exception as e:
        print(e)
        return


@socketio.on("message")
def handle_message(message, b):
    # print("IN MESSAGE: ", message)
    if message == "request-game-state":
        handle_request_state()
    elif message == "update-game-state":
        handle_update_game_state(b)
    # print("Message: ", message)
    # {"username":username, username: {"location":[player.style.top,player.style.left], "width":10}}

@socketio.on('start_timer')
def start_timer():
    print("\n\nTEST\n\n")
    gamestate = gameBoard.restartGameboard()
    socketio.emit('new-gamestate', gamestate)
    global start_time
    print("THIS", start_time)
    if start_time is None:
        start_time = time.time()
        print(start_time)
        countdown_thread = threading.Thread(target=countdown_timer)
        countdown_thread.start()
        socketio.emit('timer_started')

def countdown_timer():
    global start_time
    
    print("test2")
    while time.time() - start_time < timer_duration:
        print(timer_duration, time.time() - start_time)
        print("test3")
        remaining_time = int(timer_duration - (time.time() - start_time))
        socketio.emit('update_timer', {'time': remaining_time})
        time.sleep(1)
    old_state = gameBoard.gameState()
    board = gameBoard.restartGameboard()

    socketio.emit('timer_end', [board, old_state])
    start_time = None
    #return redirect(url_for('dashboard'))

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
                # have them redirect to an upload image page
                #response = make_response(redirect(url_for('dashboard')))
                response = make_response(redirect(url_for('handle_upload')))
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
            # have them redirect to a upload image page
            response = make_response(redirect(url_for('handle_upload')))
            #response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('auth_token', token, httponly=True, expires=datetime.datetime.now() + datetime.timedelta(hours=1))
            return response
        else:
            flash('Username already taken. Please choose another username.', 'danger')
            return redirect(url_for('index'))

@app.route('/play_as_guest', methods=['POST'])
def play_as_guest():
    flash('Playing as Guest!', 'info')
    username = getUsername(request)
    response = make_response(render_template('playPage.html', name="Guest", left=50, top=50))
    #response = make_response(redirect(url_for('dashboard')))
    response.set_cookie('auth_token', "none", httponly=True, expires=0)
    return response # render_template('playPage.html', name="Guest", left=50, top=50)



@app.route('/game')
def dashboard():
    username = getUsername(request)
    player = gameBoard.findPlayer(username)
    if not player:
        return render_template('playPage.html', name="Guest", left=50, top=50)

    left = player.left
    top = player.top
    return render_template('playPage.html', name=username, left=left, top=top)

# this function is responsible for handling POST requests from the client
# when the client uploads a photo, it will be sent as a post request on this path
@app.route("/upload", methods=["GET", "POST"])
def handle_upload():
    username = getUsername(request)
    return render_template('upload.html', name=username)
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
        username = getUsername(request)
        
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
        return jsonify({"username": username, "message": message,"id":id, "count":0}), 201 #"filename":id[1]
    else:
        return jsonify({'error': 'Username and message are required'}), 400
    
@app.route('/api/like', methods=['POST'])
def add_like_data():
    if "auth_token" in request.cookies:
        cookie_value = request.cookies.get('auth_token')
        data = request.json
        id = data["id"]

        username = getUsername(request)
        message = getSingleMessage(id)
        notLiked = True
        if username in  message["likes"]:
            notLiked = False
        color, count = updateLikeCount(id, username, notLiked)
        return jsonify({"color": color, "count":count}), 201
    else:
        abort(403)
@app.route("/upload-image", methods=['POST'])
def handle_image_upload():
    # This method is called when an image is uploaded
    # I will get bytes for the image which I need to read from the request
    # Check if the user is authorized
    flash_messages = get_flashed_messages(with_categories=False, category_filter=['danger'])

    for message in flash_messages:
        flash(message, 'danger')

    username = getUsername(request)
    if username != "Guest":
        unique_name = str(uuid.uuid4())
        path_of_image = app.config["UPLOAD_FOLDER"] + f'{unique_name}.jpg'
        path_of_image = app.config["UPLOAD_FOLDER"] + f'/{username}.jpg'
        # print(path_of_image)
        # print(len(request.files.getlist("upload")))
        # print(request.files.get("upload", None).filename)
        if request.files.get("upload", None).filename == '':
            print("entered here")
            flash("Please upload an image",'danger')
            return redirect(url_for('handle_upload'))
        
        request.files["upload"].save(path_of_image)
        storeImage(request, path_of_image)
    return redirect("/upload")
@app.route("/images", methods=["GET"])
def get_images():
    if "auth_token" in request.cookies:
        data = getImage(request)
        return data

@app.route("/static/images/<string:image_id>", methods=["GET"])
def handle_picture_req(image_id):
    file_path = f"static/images/{image_id}"
    try:
        with open(file_path, 'rb') as file:
            file=file.read()
    except:
        with open('static/images/Guest.jpg', 'rb') as file:
            file=file.read()
    return file, 200
def main():
    host = "0.0.0.0"
    port = 8080

    print("Listening on port " + str(port))
    
    socketio.run(app, host=host, port=port, allow_unsafe_werkzeug=True) #ssl_context=ssl_context,
    # socketio.run(app, host=host, port=port, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    main()