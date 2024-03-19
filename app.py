from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# This will obviously need to be changed to use a database

users = {'username': 'password'}

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

  if action == 'login':
      if username in users and users[username] == password:
          return redirect(url_for('dashboard'))
      else:
          flash('Login failed. Please check your username and password.', 'danger')
          return redirect(url_for('index'))
        
  elif action == 'create_account':
      if username not in users.keys():
          users[username] = password
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
