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
        # image = image_uploads.find_one({"username":username, "token": auth_token})
        # print(image)
        # if image:
        #     print("there is more than one image with this username")
        #     print(image)
        image_uploads.insert_one({"username": username, "token": auth_token, "filename": filename})

def getImage(request:str):
    if 'auth_token' in request.cookies:
        username = find_user(request.cookies["auth_token"])
        image_filename = image_uploads.find({"username": username, "token": request.cookies["auth_token"]})
        list_of_all_images = []
        for image in image_filename:
            image.pop("_id")
            print(image)
            list_of_all_images.append(image)
        return json.dumps(list_of_all_images)

