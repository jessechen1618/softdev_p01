import sqlite3 
import os 

DB_FILE = "./data/artpi.db"

def init():
    db = sqlite3.connect(DB_FILE)
    db.execute('''CREATE TABLE IF NOT EXISTS users (
                    userid INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL);''')
    db.commit()
    db.close()

def create_acc(un, pw):
    db = sqlite3.connect(DB_FILE)
    try:
        db.execute('''INSERT INTO users(username, password) 
                        VALUES (?,?);''', (un, pw,))
        db.commit()
        db.close()
        return True
    except sqlite3.Error as error:
        print(error)
        return False  

def login(un, pw):
    db = sqlite3.connect(DB_FILE)
    try:
        password = db.execute('''SELECT password FROM users
                                    WHERE username=?;''', (un,))
        password = [item for item in password][0][0]
        return password == pw
    except IndexError as error:
        print(error)
        return False 

def get_id(un):
    db = sqlite3.connect(DB_FILE)
    try:
        id = db.execute('SELECT userid FROM users WHERE username=?;', (un,))
        return [item for item in id][0][0]
    except IndexError as error:
        print(error)