from flask import render_template, request, redirect
from data import airportdict

def flight():
    return render_template("flight.html", airports=airportdict)

def searchflight():
    if request.method == "POST":
        fro = request.form['from']
        to = request.form['to']
        d = request.form['date'].split("-")
        dat = d[2] + "/" + d[1] + "/" + d[0]
        adult = request.form['adult']
        child = request.form['child']
        clas = request.form['class']
        url = f"https://www.makemytrip.com/flight/search?itinerary={fro}-{to}-{dat}&tripType=O&paxType=A-{adult}_C-{child}_I-0&intl=false&cabinClass={clas}&ccde=IN&lang=eng"
        return redirect(url)
    return render_template("flight.html", airports=airportdict)