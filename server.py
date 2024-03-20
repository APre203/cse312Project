from flask import Flask, send_from_directory, render_template, request, redirect, url_for, flash, get_flashed_messages
app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def index():
    # return send_from_directory('templates', 'login.html')
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
    return render_template('playPage.html')

def main():
    host = "0.0.0.0"
    port = 8080

    print("Listening on port " + str(port))

    app.run(host=host, port=port, debug=True)

    
if __name__ == "__main__":
    main()