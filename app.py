'''
put me to REST - Jesse "McCree" Chen, Kelvin Ng, Eric "Morty" Lau, David Xiedeng
SoftDev1 pd1
P1 ArRESTed Development
2019-11-17
'''

from flask import Flask, request, redirect, session, render_template, url_for, flash
import urllib.request
import os
import json
from db_builder import *

imageurl ="https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg"
url = f"https://api.imagga.com/v2/colors?image_url={imageurl}&extract_object_colors=0"
req = urllib.request.Request(url)
req.add_header("Authorization", "Basic YWNjXzE2YWNmNWJlODE0Yzk0ODo1NzM2YzRiMmQ4NzU1NzYwNmM5MjJlMjcyYWUxOGU4Ng==")
res = urllib.request.urlopen(req)
response = res.read()
data = json.loads(response)

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/", methods=['GET'])
def root():
    # TODO: if logged in
    return redirect(url_for('home'))
    # TODO: else
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    # flash('Username does not exist', "error")
    # flash('Incorrect password', "error")
    # flash('You have successfully logged in', "success")
    return render_template(
        "login.html",
        title = "Login",
    )

@app.route("/register", methods=['GET', 'POST'])
def register():
    # flash('Passwords do not match', "error")
    # flash('Username is taken', "error")
    # flash('Fill out all fields', "error")
    # flash('You have successfully registered', "success")
    return render_template(
        "register.html",
        title = "Register",
    )

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # TODO session work
    flash('You have successfully logged out', "success")
    return redirect(url_for('login'))

@app.route("/home", methods=['GET'])
def home():
    return render_template(
        "home.html",
        title = "Home"
    )

@app.route("/saved_art", methods=['GET'])
def saved_art():
    return render_template(
        "saved_art.html",
        title = "Saved Art"
    )

@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template(
        "search.html",
        title = "Search"
    )

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    return render_template(
        "settings.html",
        title = "Settings"
    )

buildTable("Users", {"user":"TEXT", "password":"TEXT", "saved_art":"TEXT"})
buildTable("Comments", {"artID":"INTEGER", "comment":"TEXT", "user":"TEXT", "timestamp":"BLOB"})

if __name__ == "__main__":
    app.debug = True
    app.run()
