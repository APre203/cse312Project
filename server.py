from flask import Flask, render_template, request, redirect, send_from_directory
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@socketio.on("message")
def handle_message(message):
    if message != 'User Connected!':
        send(message, broadcast=True)


@socketio.on('connect')
def test_connect():
    print("User Connected!")



@app.route('/')
def playPage():
    return send_from_directory('public', 'playPage.html')

@app.route('/styles.css')
def style():
    return send_from_directory('public', 'styles.css')

def main():
    host = "0.0.0.0"
    port = 8080

    print("Listening on port " + str(port))

    app.run(host=host, port=port)

    
if __name__ == "__main__":
    main()