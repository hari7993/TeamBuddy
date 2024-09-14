from flask import render_template, redirect, url_for, session
import pymongo
import certifi
from data import conn_str

def index():
    return render_template("index.html")

def home():
    return render_template("index.html")

def temps(m):
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
    db = client['Tour']
    collection = db['Places']
    monu = collection.find_one({"Name": m})
    return render_template("temp.html", monu = monu)