from flask import session
import pymongo
import certifi
from data import conn_str


def finds(s):
    print(s)
    keys = s.split("+")
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
    db = client['Tour']
    collection = db['Places']
    found = {}
    i = 0
    for k in keys:
        print(k)
        if session.get("username"):
            collectionuser = db['Customers']
            # user = collectionuser.find_one({"email": session['username']})
            collectionuser.update_one(
            { "email": session['username'] },
            { "$inc": { 'mostfrequent.'+k : 1}}
            )
        monuments = collection.find({"Key": k})
        for monu in monuments:
            new_dict = {
                "Name" : monu["Name"],
                "img" : monu["img"]
            }
            found[monu["Name"]] = new_dict
            i = i+1
    return found

def recos(s):
    keys = s.split("+")
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
    db = client['Tour']
    collection = db['Places']
    found = {}
    for k in keys:
        monuments = collection.find({"Key": k})
        for monu in monuments:
            new_dict = {
                "Name" : monu["Name"],
                "img" : monu["img"]
            }
            found[monu["Name"]] = new_dict
    return found