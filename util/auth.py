from pymongo import MongoClient
import hashlib
import secrets

mongo_client = MongoClient("mongo")

db = mongo_client['cse312project']
users_collection = db['users']
tokens_collection = db['tokens']
# chat_collection = db['chat-history']


def hash_password(password, salt):
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password

def generate_salt():
    return secrets.token_hex(16)

def hash_token(token):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    return hashed_token

def generate_token():
    return secrets.token_hex(32)
