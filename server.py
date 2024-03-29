from flask import Flask, send_from_directory, send_file, request, jsonify
#from pymongo import MongoClient
from util.auth import *
app = Flask(__name__)

# client = MongoClient("mongodb+srv://test:test@312chat1.5f8u0gy.mongodb.net/")
# db = client['ChatDB']
# chat_collection = db['chat history']

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/',  methods=['GET', 'POST'])
def playPage():
    return send_from_directory('public', 'playPage.html')

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
        return jsonify({"username": username, "message": message, "likes":"0","id":1}), 201
    else:
        return jsonify({'error': 'Username and message are required'}), 400

@app.route('/chat/getlikes', methods=['POST'])
def getlikes():
    data=request.json
    inclikes(data.get('message'))
    return jsonify({'status': 'success'})
    
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