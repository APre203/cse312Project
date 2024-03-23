from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
chat_collection = db["chat"]

def storeMessage(username, msg):
    print(chat_collection.insert_one({username: msg}))
    
