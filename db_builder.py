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

#enter code here to build a database

#===============================================

db.commit()
db.close()