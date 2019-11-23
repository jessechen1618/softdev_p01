'''
put me to REST - Jesse "McCree" Chen, Kelvin Ng, Eric "Morty" Lau, David Xiedeng
SoftDev1 pd1
P1 ArRESTed Development
2019-11-17
'''

import sqlite3	#enable control of an sqlite database
import csv
import urllib.request
import json

DB_FILE = "data/artpi.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

#===============================================

#@ create table and remove table if exists
#@ takes in a table name (string) and the keys(dict)
def buildTable(name, kc):
    # formulates order to create a table
    # ie: "CREATE TABLE if not exists test ("hello":"TEXT")"
    toBuild = "CREATE TABLE if not exists \"" + name + "\"("
    for el in kc:
        toBuild = toBuild + "\"{}\" {}, ".format(el, kc[el])
    toBuild = toBuild[:-2] + ")"
    # executes the command string toBuild
    db = sqlite3.connect("data/artpi.db") #open if file exists, otherwise create
    c = db.cursor()
    c.execute(toBuild)
    output = c.fetchall()
    db.commit()
    db.close()

#@ adds data to table, whole row insertion
#@ takes string table, and list val
def addRow(table, val):
    toDo = "INSERT INTO \"{}\" VALUES (".format(table)
    for el in val:
        if type(el) == str:
            toDo = toDo + "\'" + el + "\'" + ", "
        else:
            toDo = toDo + "\'" + str(el) + "\'" + ", "
    toDo = toDo[:-2] + ")"
    # executes the command string toBuild
    db = sqlite3.connect("data/artpi.db") #open if file exists, otherwise create
    c = db.cursor()
    c.execute(toDo)
    output = c.fetchall()
    db.commit()
    db.close()

#===============================================

# use if columns have been change for all tables
def drop(table):
    db = sqlite3.connect("data/artpi.db")
    c = db.cursor()
    c.execute("DROP TABLE {}".format(table))
    output = c.fetchall()
    db.commit()
    db.close()

#===============================================

def buildGalleryCache():
    #build table
    info = {"objectID":"INTEGER", "title":"TEXT", "artist":"TEXT", "image":"TEXT"}
    buildTable("cache", info)
    clearTables()
    #get list of objects
    link = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
    request = urllib.request.urlopen(link)
    response = request.read()
    data = json.loads(response)['objectIDs']
    #get object info and input into database
    x = 0;
    for object in data:
        if x > 99:
            break
        req = urllib.request.urlopen("https://collectionapi.metmuseum.org/public/collection/v1/objects/{}".format(object))
        res = req.read()
        info = json.loads(res)
        if (len(info["title"]) < 1 or len(info["artistDisplayName"]) < 1 or len(info["primaryImage"]) < 1):
            continue
        try:
            addRow("cache", (object, info["title"], info["artistDisplayName"], info["primaryImage"]))
        except:
            print((object, info["title"], info["artistDisplayName"], info["primaryImage"]))

#===============================================

db.commit()
db.close()
