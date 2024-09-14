from flask import render_template, redirect, request, session, url_for
from bson import ObjectId
import pymongo
import certifi
from data import conn_str

def tourbuddy():
    return render_template("tour_buddy.html")

def pairup():
    if request.method == "POST":
        if session.get("username"):
            email = session['username']
            client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
            db = client['Tour']
            collection = db['Customers']
            user = collection.find_one({"email": email})
            if not user == None:                
                name = (user['name']).lower()
                dat = request.form['date']
                mob = request.form['mobile']
                fro = request.form['from'].lower()
                travel = request.form['travel'].lower()
                col = db['Pairup_request']
                col.insert_one({
                    "UserID": email,
                    "travel": travel,
                    "Mobile": mob,
                    "Name": name,
                    "start": fro,
                    "date": dat
                })
                return redirect(url_for("dash"))
        return redirect(url_for("login"))
    return redirect(url_for("login"))


def pairrequests():
    if session.get("username"):
        email = session['username']
        client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
        db = client['Tour']
        collection = db['match_found']
        results = collection.find({"$or" : [{'User1': email}, {'User2': email}]})
        to_show = []
        cus = db['Customers']
        for r in results:
            if r['User1'] == email and r['ac1'] == 0:
                per = cus.find_one({"email": r["User2"]})
                to_show.append({
                    "name": per['name'],
                    "age" : per['age'],
                    "gender" : per["gender"],
                    'martial': per['maritalstatus'],
                    'travel' : r['travel'],
                    'city' : per['city'],
                    "date" : r['date'],
                    "id" : r['_id']
                })
            elif r['ac2'] == 0:
                per = cus.find_one({"email": r["User1"]})
                to_show.append({
                    "name": per['name'],
                    "age" : per['age'],
                    "gender" : per["gender"],
                    'martial': per['maritalstatus'],
                    'travel' : r['travel'],
                    "start" : r['start'],
                    'city' : per['city'],
                    "date" : r['date'],
                    "id" : r['_id']
                })
        si = len(to_show)
        return render_template("budreq.html", lis = to_show, s =si)
    return redirect(url_for("login"))

def accept():
    if request.method == 'POST':
        if session.get("username"):
            email = session['username']
            travel = request.form['travel']
            start = request.form['start']
            dat = request.form['date']
            id = ObjectId(request.form['id'])
            client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
            db = client['Tour']
            collection = db['match_found']
            to_add = collection.find_one({"_id": id})
            collection.delete_many({"$and" : [{"travel" : travel}, {"start": start}, {"date": dat}, {"$or": [{"User1":email}, {"User2": email}]}, {"_id" : {"$ne": id}}]})
            if to_add["User1"] == email:
                collection.update_one({"_id": id}, {"$inc": { 'ac1' : 1}})
            else:
                collection.update_one({"_id": id}, {"$inc": { 'ac2' : 1}})
            return redirect(url_for("dash"))
    return redirect(url_for("login"))

def reject():
    if request.method == 'POST':
        if session.get("username"):
            id = ObjectId(request.form['id'])
            email = session['username']
            client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
            db = client['Tour']
            collection = db['match_found']
            to_edit = collection.find_one({"_id": id})
            print(to_edit)
            collection.delete_one({"_id": id})
            if not to_edit == None:
                if to_edit["User1"] == email and to_edit["ac2"] == 1:
                    tab = db['Pairup_request']
                    tab.insert_one({
                        "UserID": to_edit["User2"],
                        "travel": to_edit["travel"],
                        "date" : to_edit["date"],
                        "start" : to_edit["start"],
                        "Mobile" : to_edit["mob2"]
                    })
                elif to_edit["User2"] == email and to_edit["ac1"] == 1:
                    tab = db['Pairup_request']
                    tab.insert_one({
                        "UserID": to_edit["User1"],
                        "travel": to_edit["travel"],
                        "date" : to_edit["date"],
                        "start" : to_edit["start"],
                        "Mobile" : to_edit["mob1"]
                    })
            return redirect(url_for("pairrequests"))
    return redirect(url_for("login"))