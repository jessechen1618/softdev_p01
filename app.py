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
from utl import user

imageurl ="https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg"
url = f"https://api.imagga.com/v2/colors?image_url={imageurl}&extract_object_colors=0"
req = urllib.request.Request(url)
req.add_header("Authorization", "Basic YWNjXzE2YWNmNWJlODE0Yzk0ODo1NzM2YzRiMmQ4NzU1NzYwNmM5MjJlMjcyYWUxOGU4Ng==")
res = urllib.request.urlopen(req)
response = res.read()
data = json.loads(response)

app = Flask(__name__)
app.secret_key = os.urandom(32)

def check(): # checks if user is logged before allowing access to that page
    if not 'user' in session:
        return redirect(url_for('login'))

@app.route("/", methods=['GET'])
def root():
    if 'user' in session:
        flash(f"Hello {session['user']}!", "success")
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if(request.method == 'GET'): 
        return render_template(
            "register.html",
            title = "Register",
        )
    elif(request.method == 'POST'):
        if(request.form['username'] == '' or request.form['username'].isspace()):
            flash('Fill out username', "error")
            return redirect(url_for('register'))
        elif(request.form['password'] == '' or request.form['password'].isspace()):
            flash('Fill out password', "error")
            return redirect(url_for('register'))
        elif(request.form['password'] != request.form['confirm']):
            flash('Passwords do not match', "error")
            return redirect(url_for('register'))
        elif(user.create_acc(request.form['username'], request.form['password'])):
            flash('You have successfully registered', "success")
            return redirect(url_for('login'))
        else:
            flash('Username already exists', "error")
            return redirect(url_for('register'))

@app.route("/login", methods=['GET', 'POST'])
def login():     
    if(request.method == 'GET'):
        if 'user' in session:
            return redirect(url_for('home'))
        else:
            return render_template(
                "login.html",
                title = "Login",
            )
    elif(request.method == 'POST'):
        if(user.login(request.form['username'], request.form['password'])):
            session['userid'] = user.get_id(request.form['username'])
            session['user'] = request.form['username']
            flash('You have successfully logged in!', "success")
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', "error")
            return redirect(url_for('login'))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    session.pop('userid', None)
    flash('You have successfully logged out', "success")
    return redirect(url_for('login'))

@app.route("/home", methods=['GET'])
def home():
    check()
    return render_template(
        "home.html",
        title = "Home"
    )

@app.route("/saved_art", methods=['GET'])
def saved_art():
    check()
    return render_template(
        "saved_art.html",
        title = "Saved Art"
    )

@app.route("/search", methods=['GET', 'POST'])
def search():
    check()
    if (request.method == 'GET'):
        return render_template(
            "search.html",
            title = "Search"
        )
    elif (request.method == 'POST'):
        return 0

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    check()
    # flash('You have successfully changed your password', "success")
    # flash('New passwords do not match', "error")
    # flash('Current password is incorrect', "error")
    if (request.method == 'GET'):
        return render_template(
            "settings.html",
            title = "Settings"
        )
    elif (request.method == 'POST'):
        return 0

if __name__ == "__main__":
    user.init()
    app.debug = True
    app.run()
