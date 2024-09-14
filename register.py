from flask import request, render_template, redirect, url_for, session
import pymongo
import certifi
from data import conn_str

def signup():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
        db = client['Tour']
        collection = db['Customers']
        found = collection.find_one({"email" : email})
        if found is None:
            obj = {
                "email" : email,
                "password": password,
                "set": 0
            }
            collection.insert_one(obj)
            return render_template("login.html")
        else:
            return "User Already Exists! Kindly login."
    return redirect(url_for("login"))

def register():
    if session.get("username"):
        return render_template("register.html", email = session['username'])
    return redirect(url_for("login"))

def registering():
    if request.method == 'POST':
        name = request.form["name"]
        mobile = request.form["mobile"]
        age = request.form['age']
        gender = request.form["inlineRadioOptions"]
        married = request.form["married"]
        city = request.form["city"]
        state = request.form["state"]
        address = request.form["address"]
        email = session['username']
        obj = {"$set":{
        "name":name,
        "Mobile":mobile,
        "age":age,
        "gender":gender,
        "address": address,
        "maritalstatus": married,
        "city":city,
        "state":state,
        "set": 1,
        "mostfrequent":{
            "hillstation" : 0,
            "sightseeing" : 0,
            "adventure" : 0,
            "couple" : 0,
            "monument" : 0,
            "beach" : 0,
            "wildlife" : 0,
            },
        }}
        client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
        db = client['Tour']
        collection = db['Customers']
        collection.update_one({"email": email}, obj)
        return redirect(url_for("dash"))
    return redirect(url_for("login"))
