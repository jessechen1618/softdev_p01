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
import datetime
from utl import user, cache
from utl.builder import builder
from utl.query import query

with open("APIkeys.json", 'r') as read_file:
    keys = json.load(read_file)
MAPQUEST_API_KEY = keys["MAPQUEST_API_KEY"]
IMAGGA_AUTH = keys["IMAGGA_AUTH"]

app = Flask(__name__)
app.secret_key = os.urandom(32)


def protected(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            # if logged in, continue with expected function
            return f(*args, **kwargs)
        else:
            # redirect to login page if not
            flash("You are not logged in", 'error')
            return redirect(url_for('login'))
    return wrapper


def missing_launch(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if MAPQUEST_API_KEY == '' and IMAGGA_AUTH == '':
            return redirect(url_for('warning', map=True, imagga=True))
        elif MAPQUEST_API_KEY == '':
            return redirect(url_for('warning', map=True, imagga=False))
        elif IMAGGA_AUTH == '':
            return redirect(url_for('warning', map=False, imagga=True))
        else:
            return f(*args, **kwargs)
    return wrapper


@app.route('/warning/<map>/<imagga>', methods=['GET'])
def warning(map=False, imagga=False):
    mapapi = True if map == 'True' else False
    imagga_header = True if imagga == 'True' else False
    return render_template(
        'warning.html',
        title="Warning",
        map=mapapi,
        imagga=imagga_header
    )


@app.route('/', methods=['GET'])
@missing_launch
def root():
    # redirects to either home or login page depending on whether or not the user is logged in
    if 'user' in session:
        flash(f"Hello {session['user']}!", 'success')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@missing_launch
def register():
    if(request.method == 'GET'):
        return render_template('register.html', title="Register")

    elif(request.method == 'POST'):
        # checks if username exists and if passwords match. if yes, create account
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


@app.route('/login', methods=['GET', 'POST'])
@missing_launch
def login():
    if(request.method == 'GET'):
        # checks session
        if 'user' in session:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', title="Login")

    elif(request.method == 'POST'):
        # checks if account esists and creates session if successful login
        if(user.get_pw(request.form['username']) == request.form['password']):
            session['userid'] = user.get_id(request.form['username'])
            session['user'] = request.form['username']
            flash("You have successfully logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials", 'error')
            return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
@missing_launch
def logout():
    # removes session when logging out
    session.pop('user', None)
    session.pop('userid', None)
    flash("You have successfully logged out", 'success')
    return redirect(url_for('login'))


@app.route('/home', methods=['GET'])
@protected
@missing_launch
def home():
    # gets and displayed cached art in homepage
    collection = dict()
    display = cache.get()
    collection['Ancient Egypt'] = list()
    collection['Ancient Greece'] = list()
    collection['Medieval and Gothic'] = list()
    collection['Renaissance'] = list()
    collection['Baroque'] = list()
    collection['Impressionism + Post-Impressionism'] = list()
    for art in display:
        collection[art[1]].append(art)
    return render_template(
        'home.html',
        title="Home",
        cache=collection,
    )


def results(searchtype, data, entered):
    # gets and returns information on artworks (based on the results found when something is searched)
    images, artTitle, name, ids = list(), list(), list(), list()
    count = 0
    for id in data:
        if count == 10:
            break
        data = query.data(
            f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}')
        toAdd = True

        # checks wheter the user searched by name, artist, or keyword (which returns all results), and returns information accordingly
        if searchtype == 'name':
            if entered.lower() in data['title'].lower():
                pass
            else:
                toAdd = False
        if searchtype == 'artist':
            if entered.lower() in data['artistDisplayName'].lower():
                pass
            else:
                toAdd = False
        if searchtype == 'saved':
            pass
        if toAdd:
            images.append(data['primaryImageSmall'])
            artTitle.append(data['title'])
            name.append(data['artistDisplayName'])
            ids.append(id)
        counter = 0
        for names in name:  # checks if artist of artwork is known
            if len(names) < 1:
                name[counter] = "Unknown Artist"
            counter += 1
        count += 1
    return images, artTitle, name, ids


@app.route('/search', methods=['GET', 'POST'])
@protected
@missing_launch
def search():
    if (request.method == 'GET'):
        return render_template('search.html', title="Search")

    elif (request.method == 'POST'):
        # displays artwork and their info from results()
        entered = request.form['search']
        search = entered.replace(' ', '+')
        link = f'https://collectionapi.metmuseum.org/public/collection/v1/search?q={urllib.parse.quote(search)}'
        data = query.data(link)['objectIDs']
        images, artTitle, name, ids = list(), list(), list(), list()
        if data == None:
            flash("No Results Found", 'error')
        else:
            images, artTitle, name, ids = results(
                request.form['searchtype'], data, entered)
            if len(images) < 1:
                flash("No Results Found", 'error')
        return render_template('search.html', title="Search", info=zip(images, artTitle, name, ids))


@app.route('/settings', methods=['GET', 'POST'])
@protected
@missing_launch
def settings():
    if (request.method == 'GET'):
        return render_template('settings.html', title="Settings")

    elif (request.method == 'POST'):
        # allows user to change password
        if(request.form['new'] == request.form['confirm']):
            if(user.get_pw(session['user']) == request.form['current']):
                if(user.set_pw(request.form['new'], session['userid'])):
                    flash("You have successfully changed your password!", 'success')
                else:
                    flash("Could not change password", 'error')
            else:
                flash("Current password is incorrect", 'error')
        else:
            flash("New passwords do not match", 'error')
        return redirect(url_for('settings'))


@app.route('/cache', methods=['GET', 'POST'])
@protected
@missing_launch
def caching():
    if(request.method == 'GET'):
        return render_template('cache.html', title="Cache")
    else:
        # allows admin account to add/remove/clear artworks in cache (to display on homepage)
        if request.form['submit'] == 'add':
            id = request.form['add']
            data = query.data(
                f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}')
            if data['artistDisplayName'] == '':
                data['artistDisplayName'] = "Unknown Artist"
            if(cache.add_image(id, request.form['collection'], data['title'], data['artistDisplayName'], data['primaryImage'])):
                flash("Successfully added art to cache", 'success')
            else:
                flash("Could not add art to cache", 'error')
        if request.form['submit'] == 'clear':
            if(cache.clear()):
                flash("Successfully cleared cache", 'success')
            else:
                flash("Could not clear cache", 'error')
        return redirect(url_for('caching'))


@app.route('/image/<id>', methods=['GET', 'POST'])
@protected
@missing_launch
def image(id):
    if(request.method == 'GET'):
        # get image of artwork
        metCol = query.data(
            f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}')
        location = [metCol['city'], metCol['state'], metCol['country']]

        # get color info on image
        imageurl = metCol['primaryImage']
        imagga = query.data(
            f'https://api.imagga.com/v2/colors?image_url={urllib.parse.quote(imageurl)}&extract_object_colors=0', headers=True, auth=IMAGGA_AUTH)
        imagga = imagga['result']['colors']['image_colors']
        colors = [image_colors['html_code'] for image_colors in imagga]

        # detects if location of art created is known
        address = ''
        for part in location:
            if part != '':
                address += part + ','

        address = urllib.parse.quote(address)
        imageurl = f'https://www.mapquestapi.com/staticmap/v5/map?key={MAPQUEST_API_KEY}&center={address}'

        # prepares comments to be displayed
        comments = []
        for comment in user.get_comments(id):
            cement = comment[3:]
            cement.append(user.get_un(comment[1]))
            comments.append(cement)

        return render_template(
            'image.html',
            id=id,
            is_saved=user.is_saved(session['userid'], id) > 0,
            image=metCol['primaryImage'],
            title=metCol['title'],
            artist=metCol['artistDisplayName'],
            moreImages=metCol['additionalImages'],
            tags=metCol['tags'],
            location=location,
            imageColors=colors,
            address=address,
            map=imageurl,
            comments=comments,
            artistDisplayBio=metCol['artistDisplayBio'],
            objectEndDate=metCol['objectEndDate'],
            medium=metCol['medium'],
            classification=metCol['classification'],
            repository=metCol['repository']
        )

    if (request.method == 'POST'):
        if 'save' in request.form:
            # allows user to save or unsave art
            if request.form['save'] == 'save':
                user.save(session['userid'], id)
                flash("Saved to your collection!", 'success')
            elif request.form['save'] == 'unsave':
                user.unsave(session['userid'], id)
                flash("Deleted from your collection!", 'success')
        elif request.form['send'] == 'com':
            # allows user to comment (while displaying username and time of comment)
            if(request.form['content'] == '' or request.form['content'].isspace()):
                flash("Please enter some text", 'error')
            else:
                if(user.comment(session['userid'], id, request.form['content'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))):
                    pass
                else:
                    flash("Could not make comment", 'error')
        return redirect(url_for('image', id=id))


@app.route('/saved_art', methods=['GET'])
@protected
@missing_launch
def saved_art():
    # displays art that is saved by the user
    artids = user.get_saved(session['userid'])
    images, artTitle, name, ids = results('saved', artids, '')
    return render_template('saved_art.html', title="Saved Art", info=zip(images, artTitle, name, ids))


if __name__ == '__main__':
    cache.init()
    user.init()
    app.debug = True
    app.run()
