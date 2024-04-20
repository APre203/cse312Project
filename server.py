from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, make_response, send_from_directory, jsonify, abort
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import datetime
from util.auth import *
from util.db import *
import html
from flask_sock import Sock
import time
import json
from util.gameBoard import GameBoard
from util.player import Player

app = Flask(__name__)
app.secret_key = 'your_secret_key'

sock = Sock(app)

def getUsername(request):
    username = "Guest"
    if "auth_token" in request.cookies:
        cookie_value = request.cookies.get('auth_token')
        username = find_user(cookie_value)
    return username

gameBoard = GameBoard()
@sock.route('/gamews')
def test_ws(socket):
    username = getUsername(request)
    if username != "Guest":
        gameBoard.addPlayer(Player(socket, username, 50, 50, 10))
    while True:
        raw_data = socket.receive(timeout=0)
        try:
            send_data = gameBoard.playersDict()
            sockets = gameBoard.getSockets()
            data_to_send = {"id":username, "server_data":send_data}
            print("DataToSend",data_to_send)
            send_data = json.dumps(data_to_send)
            socket.send(send_data)
            # for s in sockets:
            #     print()
            #     s.send(send_data)

            print("RAW DATA: ", raw_data)
            # recieved_data = json.loads(raw_data)
            print("DATA", json.loads(raw_data))
            
        except Exception as e:
            print("EXCEPTION:",e)
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
    @after_this_request
    def add_header(response):
        response.headers['X-Content-Type-Options'] = 'text/css'
        return response
    return send_from_directory("public", "styles.css")

def main():
    host = "0.0.0.0"
    port = 8080

    print("Listening on port " + str(port))
    
    app.run(host=host, port=port)
    # socketio.run(app, host=host, port=port, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    main()
