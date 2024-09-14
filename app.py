from flask import Flask, json
from scheduler import matching
from data import airportdict
from login import login, logout, check, dash, forget
from flight import flight, searchflight
from register import signup, register, registering
from search import finds, recos
from tourbuddy import tourbuddy, pairup, pairrequests, accept, reject
from views import index, home, temps

matching.start()

app = Flask(__name__)

app.secret_key="@342$62455asdw"


app.add_url_rule("/", view_func=index)
app.add_url_rule("/home", view_func=home)
app.add_url_rule('/dashboard', view_func=dash)


app.add_url_rule("/login", view_func=login)
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/check", view_func=check, methods=["GET", "POST"])
app.add_url_rule("/forgetpass", view_func=forget)


app.add_url_rule("/flight", view_func= flight)
app.add_url_rule("/checkflight", view_func= searchflight, methods=["GET", "POST"])


app.add_url_rule('/signup', view_func=signup, methods=["POST", "GET"])
app.add_url_rule('/register', view_func=register, methods=["GET", "POST"])
app.add_url_rule('/registering', view_func=registering, methods=["POST", "GET"])


app.add_url_rule('/tourbuddy', view_func=tourbuddy)
app.add_url_rule('/pairup', view_func=pairup, methods=["GET", "POST"])
app.add_url_rule('/pairrequests', view_func=pairrequests)
app.add_url_rule('/accept',view_func=accept, methods=["POST", "GET"])
app.add_url_rule('/reject',view_func=reject, methods=["POST", "GET"])

app.add_url_rule('/places/<m>', view_func=temps)


@app.route('/result/<s>', methods=["GET"])
def find(s):
    found = finds(s)
    response = app.response_class(
        status=200,
        response=json.dumps(found),
        mimetype='application/json'
    )
    return response

@app.route('/recco/<s>', methods=["GET"])
def reco(s):
    found = recos(s)
    response = app.response_class(
        status=200,
        response=json.dumps(found),
        mimetype='application/json'
    )
    return response

if __name__ =="__main__":
    app.run(debug=True)