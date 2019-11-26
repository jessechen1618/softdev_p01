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
from utl import user, cache
from utl.builder import builder
from utl.query import query
from opencage.geocoder import OpenCageGeocode # for finding longitude and latitude

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

def protected(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session: return f(*args, **kwargs) # if logged in, continue with expected function
        else:
            flash("You are not logged in", 'error')
            return redirect(url_for('login'))
    return wrapper

@app.route('/', methods=['GET'])
def root():
    if 'user' in session:
        flash(f"Hello {session['user']}!", 'success')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if(request.method == 'GET'): return render_template('register.html', title = "Register")

    elif(request.method == 'POST'):
        if(request.form['username'] == '' or request.form['username'].isspace()):
            flash("Fill out username", 'error')
        elif(request.form['password'] == '' or request.form['password'].isspace()):
            flash("Fill out password", 'error')
        elif(request.form['password'] != request.form['confirm']):
            flash("Passwords do not match", 'error')
        elif(user.create(request.form['username'], request.form['password'])):
            flash("You have successfully registered", 'success')
            return redirect(url_for('login'))
        else:
            flash("Username already exists", 'error')
        return redirect(url_for('register'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(request.method == 'GET'):
        if 'user' in session: return redirect(url_for('home'))
        else: return render_template("login.html", title = "Login" )

    elif(request.method == 'POST'):
        if(user.get_pw(request.form['username']) == request.form['password']):
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
def home(): return render_template("home.html", title = "Home", cache = cache.get())

@app.route("/saved_art", methods=['GET'])
@protected
def saved_art(): return render_template("saved_art.html", title = "Saved Art")

def results(searchtype, data, entered):
    images, artTitle, name, ids = list(), list(), list(), list()
    count = 0
    for id in data:
        if count == 10: break # displaying less results for now 
        data = query.data(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}")
        toAdd = True 
        if searchtype == 'name': 
            if entered.lower() in data['title'].lower(): pass
            else: toAdd = False  
        if searchtype == 'artist': 
            if entered.lower() in data['artistDisplayName'].lower(): pass
            else: toAdd = False  
        if toAdd:
            images.append(data['primaryImageSmall'])
            artTitle.append(data['title'])
            name.append(data['artistDisplayName'])
            ids.append(id)
        counter = 0
        for names in name:
            if len(names) < 1: name[counter] = 'Unknown Artist'
            counter += 1
        count += 1
    return images, artTitle, name, ids
    
@app.route("/search", methods=['GET', 'POST'])
@protected
def search():
    if (request.method == 'GET'): return render_template("search.html", title = "Search")

    elif (request.method == 'POST'):
        entered = request.form['search']
        search = entered.replace(" ", "+")
        link = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={search}"
        data = query.data(link)['objectIDs']
        images, artTitle, name, ids = list(), list(), list(), list()
        if data == None: flash("No Results Found", 'error')
        else:
            images, artTitle, name, ids = results(request.form['searchtype'], data, entered)
            if len(images) < 1: flash("No Results Found", 'error')
        return render_template("search.html", title="Search", info=zip(images,artTitle,name,ids))

@app.route("/settings", methods=['GET', 'POST'])
@protected
def settings():
    if (request.method == 'GET'): return render_template("settings.html", title = "Settings")

    elif (request.method == 'POST'):
        if(request.form['new'] == request.form['confirm']):
            if(user.get_pw(session['user']) == request.form['current']):
                if(user.set_pw(request.form['new'], session['userid'])):
                    flash('You have successfully changed your password!', "success")
                else:
                    flash('Could not change password', "error")
            else:
                flash('Current password is incorrect', "error")
        else:
            flash('New passwords do not match', "error")
        return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))

@app.route("/image/<id>", methods=['GET', 'POST'])
@protected
def image(id):
    if(request.method == 'GET'):
        # get image of artwork
        metCol = query.data(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}")
        location=[metCol["city"],metCol["state"],metCol["country"]]
        '''
        #get color info on image
        imageurl = metCol["primaryImage"]
        print(imageurl)
        imagga = query.data(f"https://api.imagga.com/v2/colors?image_url={imageurl}&extract_object_colors=0", headers=True)
        imagga = imagga['result']['colors']["image_colors"]
        colors = [image_colors['html_code'] for image_colors in imagga]
        '''
        # get longitude and latitude
        key = '9104fa024a004ae2866cf65a080b75fb'
        geocoder = OpenCageGeocode(key)
        address = ""
        for part in location:
            address += part + ","
        geocoded = geocoder.geocode(address)
        
        return render_template(
            "image.html",
            image=metCol["primaryImage"],
            title=metCol["title"],
            artist=metCol["artistDisplayName"],
            moreImages=metCol["additionalImages"],
            tags=metCol["tags"],
            location=location,
            #imageColors=colors,
            longlat = geocoded
            )

if __name__ == "__main__":
    # cache.build()
    user.init()
    app.debug = True
    app.run()
