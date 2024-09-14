from flask import render_template, session, redirect, url_for, request
import pymongo
import certifi
from data import conn_str

def login():
    return render_template("login.html", usf = False, wrng = False)

def logout():
    session.pop('username',None)
    return redirect(url_for("login"))

def check():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
        db = client['Tour']
        collection = db['Customers']
        user = collection.find_one({"email": username})
        if user == None:
            return render_template("login.html", usf = True, wrng = False)
        if user['password'] == password:
            session['username'] = username
            if user['set'] == 0:
                return redirect(url_for("register"))
            return redirect(url_for("dash"))
        return render_template("login.html", usf = False, wrng = True)
    return redirect(url_for("login"))

def recommendations(username):
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
    db = client['Tour']
    collection = db['Customers']
    user = collection.find_one({"email": username})
    sorted_dict = dict( sorted(user["mostfrequent"].items(),
                           key=lambda item: item[1],
                           reverse=True))
    def getList(dict):
        list = []
        for key in dict.keys():
            list.append(key)
            
        return list
    sorted_list=getList(sorted_dict)
    suggest_list=sorted_list[0:3]
    print(suggest_list)
    return suggest_list

def dash():
    if session.get("username"):
        email = session['username']
        client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
        db = client['Tour']
        collection = db['Customers']
        user = collection.find_one({"email": email})
        if user["set"] == 1:
            keys=recommendations(email)
            s=keys[0]
            col = db['match_found']
            f = col.find({"$and": [{"User1": email}, {"ac1": 0}]})
            n = len(list(f))
            g = col.find({"$and": [{"User2": email}, {"ac2": 0}]})
            n += len(list(g))
            for i in range(1,len(keys)):
                s=s+"+"+keys[i]
            return render_template("userindex.html",s=s, n = n)
        return redirect(url_for("register"), code = 307)
    return redirect(url_for("login"))

def forget():
    return render_template("Forget_Password.html")