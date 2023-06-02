import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/skillednursing")
def skillednursing():
    return render_template("skillednursing.html")


@app.route("/respitecare")
def respitecare():
    return render_template("respitecare.html")


@app.route("/physicaltherapy")
def physicaltherapy():
    return render_template("physicaltherapy.html")


@app.route("/personalcare")
def personalcare():
    return render_template("personalcare.html")



@app.route("/mission")
def mission():
    return render_template("mission.html")

@app.route("/vision")
def vision():
    return render_template("vision.html")


@app.route("/dementiacare")
def dementiacare():
    return render_template("dementiacare.html")


@app.route("/companioncare")
def companioncare():
    return render_template("companioncare.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 