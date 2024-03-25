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
client = MongoClient("mongo")
db = client['cse312project']
chat_collection = db['chat-history']
def savechattod(username, message):
    chat_collection.insert_one({'username': username, 'message': message})
    
    
    
def getallmessages():
    retval = []
    for record in chat_collection.find():
        retval.append({"username":record["username"], "message":record["message"]})
    return retval