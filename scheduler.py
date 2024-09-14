from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, redirect, render_template, request, request_tearing_down, sessions, url_for,session, json
import linecache
import pandas as pd
import csv
import math
from datetime import date
# from flask_mysqldb import MySQL
from flask_mail import Mail,Message
from random import *
import datetime
from pymysql import NULL
import pytz
import pymongo
import certifi
import smtplib

sender='g17miniproject@gmail.com'
passwd='Myminiprojectpswd17'


smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
smtpObj.connect("smtp.gmail.com", 587)
smtpObj.starttls()
smtpObj.login(sender, passwd)
conn_str = "mongodb+srv://rkr2137:Rahul%402137@cluster0.dtzxv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

def matchup():
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000,  tlsCAFile=certifi.where())
    db = client['Tour']
    collection = db['Pairup_request']
    re = collection.find()
    final = []
    for r in re:
        final.append(r)
    f2 = []
    for i in range(0,len(final)):
        for j in range(i+1, len(final)):
            if final[i]['date'] == final[j]['date'] and final[i]['travel'] == final[j]['travel'] and final[i]['start'] == final[j]['start']:
                if final[i]['UserID'] == final[j]['UserID']:
                    if not final[i]["_id"] in f2:
                        f2.append(final[i]["_id"])
                else:
                    ma = db['match_found']
                    ma.insert_one({
                        "User1" : final[i]["UserID"],
                        "User2" : final[j]['UserID'],
                        "date" : final[i]['date'],
                        'travel' : final[i]['travel'],
                        'start' : final[i]['start'],
                        "mob1" : final[i]["Mobile"],
                        "mob2" : final[j]['Mobile'],
                        "ac1" : 0,
                        "ac2" : 0
                    })
                    if not final[i]["_id"] in f2:
                        f2.append(final[i]["_id"])
                    if not final[j]["_id"] in f2:
                        f2.append(final[j]["_id"])
    for i in range(0, len(f2)):
        collection.delete_one({"_id" : f2[i]})

    mat_f = db["match_found"]
    to_mail = mat_f.find({"ac1" : 1, "ac2" : 1})
    for m in to_mail:
        email1 = m['User1']
        email2 = m["User2"]
        mob1 = m["mob1"]
        mob2 = m["mob2"]
        travel = m["travel"]
        dat = m["date"]
        start = m["start"]
        message = f'''
        Dear User,
        Below is the contact number of your Travel Buddy
        Mobile Number: {mob2}
        Here are your other details of travel:
        Travelling to: {travel}
        Travelling from : {start}
        Travelling On: {dat}
        Yours sincerely,
        Tourbuddy team.'''
        smtpObj.sendmail(sender, email1, message)
        # msg2 = Message(subject="Hey, You have been paired!", sender="g17miniproject@gmail.com", recipients=[email2])
        # msg.html=(f'''
        # <h1>Here's the details of your tour Buddy</h1>
        # <h2>Mobile Number: {mob1}</h2></br>
        # <p>Here are your other details of travel:</p>
        # <ul><li>Travelling to: {travel}</li>
        # <li>Travelling from : {start}</li>
        # <li>Travelling On: {dat}</li>''')
        message = f'''
        Dear User,
        Below is the contact number of your Travel Buddy
        Mobile Number: {mob1}
        Here are your other details of travel:
        Travelling to: {travel}
        Travelling from : {start}
        Travelling On: {dat}
        Yours sincerely,
        Tourbuddy team.'''
        smtpObj.sendmail(sender, email2, message)
        mat_f.delete_one({"_id": m["_id"]})
    # print("done")

matching = BackgroundScheduler(daemon=True)
matching.add_job(matchup,'interval',minutes=1)
