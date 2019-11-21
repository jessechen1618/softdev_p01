import sqlite3 

DB_FILE = "../data/artpi.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

