'''
put me to REST - Jesse "McCree" Chen, Kelvin Ng, Eric "Morty" Lau, David Xiedeng
SoftDev1 pd1
P1 ArRESTed Development
2019-11-17
'''

from flask import Flask, request, redirect, session, render_template, url_for, flash
import sqlite3
import urllib.request
import urllib.parse
import functools
import os
import json
from utl import user

# imageurl = "https://www.mapquestapi.com/staticmap/v5/map?key=GN6wCdut6eE2QkB8ATz12lMHJV8tvVD5&center=San+Francisco,CA&zoom=10&type=hyb&size=600,400@2x"
# print(imageurl)
# url = f"https://api.imagga.com/v2/colors?image_url={imageurl}&extract_object_colors=0"
# req = urllib.request.Request(url)
# req.add_header("Authorization", "Basic YWNjXzE2YWNmNWJlODE0Yzk0ODo1NzM2YzRiMmQ4NzU1NzYwNmM5MjJlMjcyYWUxOGU4Ng==")
# res = urllib.request.urlopen(req)
# response = res.read()
# data = json.loads(response)

# mapquest GN6wCdut6eE2QkB8ATz12lMHJV8tvVD5
# bitly 49758fd83aca5ad4f773441471c853dec4461543

app = Flask(__name__)
app.secret_key = os.urandom(32)

def querydata(link):
    url = urllib.request.urlopen(link)
    response = url.read()
    data = json.loads(response)
    return data

def protected(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash("You are not logged in", "error")
            return redirect(url_for('login'))
    return wrapper

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
        elif(request.form['password'] == '' or request.form['password'].isspace()):
            flash('Fill out password', "error")
        elif(request.form['password'] != request.form['confirm']):
            flash('Passwords do not match', "error")
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
@protected
def home():
    db = sqlite3.connect("data/artpi.db")
    c = db.cursor()
    c.execute("SELECT * FROM cache")
    x = 0
    output = []
    while x < 100:
        x += 1
        temp = list(c.fetchmany()[0])
        output.append(temp)
    db.commit()
    db.close()
    return render_template(
        "home.html",
        title = "Home",
        src = "https://images.metmuseum.org/CRDImages/ep/web-large/DT1567.jpg",
        output = output
    )

@app.route("/saved_art", methods=['GET'])
@protected
def saved_art():
    return render_template(
        "saved_art.html",
        title = "Saved Art"
    )

@app.route("/search", methods=['GET', 'POST'])
@protected
def search():
    if (request.method == 'GET'):
        return render_template(
            "search.html",
            title = "Search"
        )
    elif (request.method == 'POST'):
        search = request.form['search']
        search = search.replace(" ", "+")
        link = "https://collectionapi.metmuseum.org/public/collection/v1/search?q={}".format(search)
        data = querydata(link)['objectIDs']
        if request.form['searchtype'] == 'keyword':
            images = list()
            artTitle = list()
            name = list()
            count = 0
            for ids in data:
                count += 1
                if count == 10: #displaying less results for now
                    break
                link = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{}".format(ids)
                print(link)
                images.append(querydata(link)['primaryImageSmall'])
                artTitle.append(querydata(link)['title'])
                name.append(querydata(link)['artistDisplayName'])
                counter = 0
                for names in name:
                    if len(names) < 1:
                        name[counter] = 'Unknown Artist'
                    counter += 1
            return render_template("search.html", info=zip(images,artTitle,name))

@app.route("/settings", methods=['GET', 'POST'])
@protected
def settings():
    if (request.method == 'GET'):
        return render_template(
            "settings.html",
            title = "Settings"
        )
    elif (request.method == 'POST'):
        if(request.form['new'] == request.form['confirm']):
            if(user.get_pw(session['userid']) == request.form['current']):
                if(user.set_pw(session['userid'], request.form['new'])):
                    flash('You have successfully changed your password!', "success")
                else:
                    flash('Current password is incorrect', "error")
            else:
                flash('New passwords do not match', "error")
            return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))

@app.route("/image", methods=['GET', 'POST'])
@protected
def image():
    if(request.method == 'GET'):
        #temporary object for page creation
        objectID = request.args['id']
        req = urllib.request.urlopen("https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(objectID))
        response = req.read()
        metCol = json.loads(response)
        #get color info on image
        '''
        imageurl = metCol["primaryImage"]
        url = f"https://api.imagga.com/v2/colors?image_url={imageurl}&extract_object_colors=0"
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Basic YWNjXzE2YWNmNWJlODE0Yzk0ODo1NzM2YzRiMmQ4NzU1NzYwNmM5MjJlMjcyYWUxOGU4Ng==")
        res = urllib.request.urlopen(req)
        response = res.read()
        imagga = json.loads(response)['result']['colors']
        '''
        return render_template(
            "image.html",
            image=metCol["primaryImage"],
            title=metCol["title"],
            artist=metCol["artistDisplayName"],
            moreImages=metCol["additionalImages"],
            tags=metCol["tags"],
            #testjson=imagga
            )

if __name__ == "__main__":
    user.init()
    app.debug = True
    app.run()
