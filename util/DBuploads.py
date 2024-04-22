import json
from pymongo import MongoClient

from util.auth import find_user

mongo_client = MongoClient("mongo")
db = mongo_client["cse312project"]
image_uploads = db["uploads"]
def storeImage(request:str, filename: str):
    if 'auth_token' in request.cookies:
        username = find_user(request.cookies["auth_token"])
        auth_token = request.cookies["auth_token"]
        image_filename = image_uploads.find_one({"username": username, "token": request.cookies["auth_token"]})
        if image_filename:
            image_uploads.update_one({"username": username, "token": auth_token},{"$set":{"filename":filename}})
        # image = image_uploads.find_one({"username":username, "token": auth_token})
        # print(image)
        # if image:
        #     print("there is more than one image with this username")
        #     print(image)
        else:
            image_uploads.insert_one({"username": username, "token": auth_token, "filename": filename})

def getImage(request:str):
    if 'auth_token' in request.cookies:
        username = find_user(request.cookies["auth_token"])
        image_filename = image_uploads.find({"username": username, "token": request.cookies["auth_token"]})
        list_of_all_images = []
        if image_filename:
            for image in image_filename:
                print("lalalallalalallalalallala")
                print(image)
                print("lalalallalalallalalallala")
                image.pop("_id")
                print(image)
                list_of_all_images.append(image)
            return json.dumps(list_of_all_images)
        else:
            return json.dumps([])
        
    else:
        return json.dumps([])

