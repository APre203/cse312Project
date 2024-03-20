from pymongo import MongoClient
# import html
# import uuid
# from werkzeug.security import generate_password_hash
# client= MongoClient("mongodb+srv://test:test@312chat1.5f8u0gy.mongodb.net/")

# chat_db=client.get_database("ChatDB")
# users_collection=chat_db.get_collection("chat history")


# def savechattod(username, message, pwd):
#     phash=generate_password_hash(pwd)
#     users_collection.insert_one({"_id":username, "message":message, "password":phash})
client = MongoClient("mongodb+srv://test:test@312chat1.5f8u0gy.mongodb.net/")
db = client['ChatDB']
chat_collection = db['chat history']
def savechattod(username, message):
    chat_collection.insert_one({'username': username, 'message': message})