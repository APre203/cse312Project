from flask import Flask, send_from_directory, render_template, request, redirect, url_for, flash, get_flashed_messages, jsonify
from util.db import *
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/styles.css')
def style():
    return send_from_directory('static', 'styles.css')

@app.route('/playstyles.css')
def playstyle():
    return send_from_directory('static', 'playstyles.css')


users = {'username': 'password'}

@app.route('/login_or_create', methods=['POST'])
def login_or_create():

  flash_messages = get_flashed_messages(with_categories=False, category_filter=['danger'])

  for message in flash_messages:
      flash(message, 'danger')

  username = request.form['username']
  password = request.form['password']
  action = request.form['action']

  if action == 'login':
      if username in users and users[username] == password:
          return redirect(url_for('dashboard',name=username))
      else:
          flash('Login failed. Please check your username and password.', 'danger')
          return redirect(url_for('index'))
        
  elif action == 'create_account':
      if username not in users.keys():
          users[username] = password
          return redirect(url_for('dashboard',name=username))
      else:
          flash('Username already taken. Please choose another username.', 'danger')
          return redirect(url_for('index'))

@app.route('/play_as_guest', methods=['POST'])
def play_as_guest():
    flash('Playing as Guest!', 'info')
    return redirect(url_for('dashboard'))

@app.route('/game')
@app.route('/game/<name>')
def dashboard(name=None):
    return render_template('playPage.html', name=name)


@app.route('/chat/api',  methods=['GET', 'POST'])
def add_chat_message():
    if request.method == "GET":
        # GET TOTAL FROM DATABASE
        return jsonify(getallmessages())#[{"username": "test", "message": "something","id":1},{"username": "test2", "message": "something2","id":2}]), 200
    data = request.json
    print("data:",data)
    username = "Guest"
    auth = False
    if auth:
        username = "new_username"

    message = data.get('message')
  #  print(message)
    
    if message:
        savechattod(username, message)
        #chat_collection.insert_one({'username': username, 'message': message})
        return jsonify({"username": username, "message": message,"id":1}), 201
    else:
        return jsonify({'error': 'Username and message are required'}), 400

# NOW WE HAVE TO SEND ALL MESSAGES FROM MONGO WHEN WE RECEIVE THEM

def main():
    host = "0.0.0.0"
    port = 8080

    print("Listening on port " + str(port))

    app.run(host=host, port=port, debug=True)

    
if __name__ == "__main__":
    main()