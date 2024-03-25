from pymongo import MongoClient

mongo_client = MongoClient("mongo")

def savechattod(username, message):
    db = mongo_client['ChatDB']
    chat_collection = db['chat history']
    chat_collection.insert_one({'username': username, 'message': message})

def getallmessages():
    db = mongo_client['ChatDB']
    chat_collection = db['chat history']
    retval = []
    for record in chat_collection.find():
        retval.append({"username":record["username"], "message":record["message"]})
    return retval

def addUserLike(message_id, user_id):
    # ADD THE USER TO THE LIKE
    return