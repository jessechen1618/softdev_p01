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

imageurl ="https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg"
url = f"https://api.imagga.com/v2/colors?image_url={imageurl}&extract_object_colors=0"
req = urllib.request.Request(url)
req.add_header("Authorization", "Basic YWNjXzE2YWNmNWJlODE0Yzk0ODo1NzM2YzRiMmQ4NzU1NzYwNmM5MjJlMjcyYWUxOGU4Ng==")
res = urllib.request.urlopen(req)
response = res.read()
data = json.loads(response)

app = Flask(__name__)
@app.route("/")
def root():
    # TODO: if not logged in 
    return redirect(url_for('login'))
    # TODO: if logged in
    return redirect(url_for('home'))

@app.route("/login")
def login():
    return render_template(
        "login.html",
        title = "Login",
        register = url_for('register')
    )

@app.route("/register")
def register():
    return render_template(
        "register.html",
        title = "Register",
        login = url_for('login')
    )

@app.route("/home")
def home():
    return render_template(
        "home.html",
        title = "Home"
    )

@app.route("/saved_art")
def saved_art():
    return render_template(
        "saved_art.html",
        title = "Saved Art"
    )

@app.route("/search")
def search():
    return render_template(
        "search.html",
        title = "Search"
    )

@app.route("/settings")
def settings():
    return render_template(
        "settings.html",
        title = "Settings"
    )

@app.route("/logout")
def logout():
    return 0
    
if __name__ == "__main__":
    app.debug = True
    app.run()