'''
put me to REST - Jesse "McCree" Chen, Kelvin Ng, Eric "Morty" Lau, David Xiedeng
SoftDev1 pd1
P1 ArRESTed Development 
2019-11-17
'''

import sqlite3	#enable control of an sqlite database
import csv

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

buildTable("Users", {"user":"TEXT", "password":"TEXT", "saved_art":"TEXT"})
buildTable("Comments", {"artID":"INTEGER", "comment":"TEXT", "user":"TEXT", "timestamp":"BLOB"})

#addRow("Users", ("testUser0", "pword0", []))

#===============================================

db.commit()
db.close()