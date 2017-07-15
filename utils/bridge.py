from bson.objectid import ObjectId
from pymongo import MongoClient

username = 'techteam'
password = 'AGjllOpG5w'

client = MongoClient('127.0.0.1') # edit later

db = client.dataBase

#return the users info as a python dictionary
def getUserData(index):
    return db.Account.find_one({'_id': ObjectId(index)})
#finds the users ObjectId by looking for username identifier
def getPostData(index):
    return db.posts.find_one({'_id' : ObjectId(index)})
#createUser creates the user based off a python dictionary imported
def createUser(dictionary):
    db.Account.insert(dictionary)
    return True

def createPost(dictionary):
    return db.posts.insert(dictionary)['_id']

#update a uers info based off a dictionary
def updateUser(user, dict):
    db.Account.update_one({'_id' : ObjectId(user)}, {'$set' : {'_id' : dict}})

def filterUser(dictionary):
    db.Account.find(dictionary)
    
