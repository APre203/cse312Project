from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client["cse312project"]
chat_collection = db["chat-history"]

def storeMessage(username, msg):
    chat_collection.insert_one({username: msg})

    
