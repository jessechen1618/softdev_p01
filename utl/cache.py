'''
put me to REST - Jesse "McCree" Chen, Kelvin Ng, Eric "Morty" Lau, David Xiedeng
SoftDev1 pd1
P1 ArRESTed Development
'''

import sqlite3	#enable control of an sqlite database
from .builder import builder 
from .query import query

# initializes new cache table
@builder.execute(err_type=sqlite3.Error,
    command='''CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE CHECK (length(title) > 0),
                artist TEXT CHECK (length(artist) > 0), 
                image TEXT UNIQUE CHECK(length(image) > 0)
                );''')
def init(): pass

# clears the cache table 
@builder.execute(err_type=sqlite3.Error, command='DELETE FROM cache;')
def clear(): pass

@builder.execute(err_type=sqlite3.Error, command = 'INSERT INTO cache(id, title, artist, image) VALUES(?,?,?,?);')
def add_image(id, title, artist, image): pass

@builder.execute(err_type=IndexError, command = 'SELECT COUNT(*) FROM cache;')
def size(): pass

def build():
    init()
    clear()
    #get list of objects
    objects = query.data('https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q=van+gogh')['objectIDs']
    #get object info and input into database
    checked = 0 
    while size() < 20 and checked < len(objects):
        print("Caching...")
        info = query.data(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{objects[checked]}")
        add_image(objects[checked], info['title'], info['artistDisplayName'], info['primaryImage'])
        checked += 1

def get():
    try:
        db = sqlite3.connect("data/artpi.db")
        c = db.cursor()
        c.execute("SELECT * FROM cache")
        output = [list(c.fetchmany()[0]) for image in range(0, size())]
        db.close()
        return output
    except: return None
