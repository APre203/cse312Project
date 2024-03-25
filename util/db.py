from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client["cse312project"]
chat_collection = db["chat-history"]

def storeMessage(username, msg):
    chat_collection.insert_one({username: msg})


def getallmessages():
    retval = []
    for record in chat_collection.find():
        retval.append({"username":record["username"], "message":record["message"]})
    return retval

    
