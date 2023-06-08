import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from forms import ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    form = ContactForm()
    return render_template("index.html", form=form)


@app.route("/skillednursing")
def skillednursing():
    form = ContactForm()
    return render_template("skillednursing.html", form=form)


@app.route("/respitecare")
def respitecare():
    form = ContactForm()
    return render_template("respitecare.html", form=form)


@app.route("/physicaltherapy")
def physicaltherapy():
    form = ContactForm()
    return render_template("physicaltherapy.html", form=form)


@app.route("/personalcare")
def personalcare():
    form = ContactForm()
    return render_template("personalcare.html", form=form)



@app.route("/mission")
def mission():
    form = ContactForm()
    return render_template("mission.html", form=form)


@app.route("/vision")
def vision():
    form = ContactForm()
    return render_template("vision.html", form=form)


@app.route("/dementiacare")
def dementiacare():
    form = ContactForm()
    return render_template("dementiacare.html", form=form)


@app.route("/companioncare")
def companioncare():
    form = ContactForm()
    return render_template("companioncare.html", form=form)


@app.route("/aboutus")
def aboutus():
    form = ContactForm()
    return render_template("aboutus.html", form=form)

@app.route("/contacts")
def contacts():
    form = ContactForm()
    return render_template("contacts.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 