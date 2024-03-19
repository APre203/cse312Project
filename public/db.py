from pymongo import MongoClient

client= MongoClient("mongodb+srv://test:test@312chat1.5f8u0gy.mongodb.net/")

chat_db=client.get_database("ChatDB")
users_collection=chat_db.get_collection("chat history")

