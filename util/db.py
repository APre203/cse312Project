from pymongo import MongoClient

mongo_client = MongoClient("mongo")
db = mongo_client["cse312project"]
chat_collection = db["chat-history"]
image_uploads = db["uploads"]
def storeMessage(username, msg):
    id = chat_collection.count_documents({})
    image_filename = image_uploads.find_one({"username": username})
    x=image_filename["filename"]
    if username=="Guest":
        chat_collection.insert_one({"username": username,"message": msg, "id":id, "likes":[], "count":0, "filename":f'<img src="/static/images/GuestProfilePic.jpg" alt="Post image">'})
        return [id, '<img src="/static/images/GuestProfilePic.jpg" alt="Post image">']
    
    x3=f'<img src="/static/images/{x}" alt="Post image">'
    chat_collection.insert_one({"username": username,"message": msg, "id":id, "likes":[], "count":0, "filename":f'<img src="/static/images/{x}" alt="Post image">'})
    return [id, x3]

def getallmessages(currentUser):
    retval = []
    if currentUser== "Guest":
        for record in chat_collection.find():
            print(record["filename"])
            retval.append({"username":record["username"], "message":record["message"], "filename":record["filename"], "id":record["id"],"count":record["count"], "color":"none"})
    else:
        for record in chat_collection.find():
            color = "transparent"
            if currentUser in  record["likes"]:
                color = "green"
            print(record["filename"])
            retval.append({"username":record["username"], "message":record["message"], "filename":record["filename"], "id":record["id"],"count":record["count"], "color":color})
    return retval

def getSingleMessage(id):
    result = chat_collection.find_one({"id":id})
    return result

def updateLikeCount(id, username, isAdd=True):
    if isAdd:
        chat_collection.update_one({"id":id}, {"$addToSet": {"likes": username},  # Add the username to the likes array
            "$inc": {"count": 1}})
        chat = chat_collection.find_one({"id":id})
        return 'green', chat["count"]
    else:
        chat_collection.update_one({"id":id}, {"$pull": {"likes": username},  # Add the username to the likes array
            "$inc": {"count": -1}})
        chat = chat_collection.find_one({"id":id})
        return 'transparent', chat["count"]