'''
put me to REST - Jesse "McCree" Chen, Kelvin Ng, Eric "Morty" Lau, David Xiedeng
SoftDev1 pd1
P1 ArRESTed Development
'''

import sqlite3
import datetime
from .builder import builder


@builder.execute(err_type=sqlite3.Error,
                 command='''CREATE TABLE IF NOT EXISTS users (
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE CHECK (length(username) > 0),
                password TEXT CHECK (length(password) > 0));''')
def inituser(): pass


@builder.execute(err_type=sqlite3.Error, command='CREATE TABLE IF NOT EXISTS art (userid INTEGER, artid INTEGER);')
def initart(): pass


@builder.execute(err_type=sqlite3.Error, command='''CREATE TABLE IF NOT EXISTS comments(
    commentid INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER, artid INTEGER,
    content TEXT CHECK (length(content) > 0),
    timestamp BLOB);''')
def initcomment(): pass


@builder.execute(err_type=sqlite3.Error, command='INSERT INTO users(username, password) VALUES (?,?);')
def create(un, pw): pass


@builder.execute(err_type=IndexError, command='SELECT userid FROM users WHERE username=?;')
def get_id(un): pass


@builder.execute(err_type=IndexError, command='SELECT username FROM users WHERE userid=?;')
def get_un(userid): pass


@builder.execute(err_type=IndexError, command='SELECT password FROM users WHERE username=?;')
def get_pw(un): pass


@builder.execute(err_type=IndexError, command='SELECT COUNT(*) FROM comments where artid=?;')
def num_comments(artid): pass


@builder.execute(err_type=IndexError, command='SELECT COUNT(1) FROM art WHERE userid=? AND artid=?;')
def is_saved(userid, artid): pass


@builder.execute(err_type=sqlite3.Error, command='DELETE FROM art WHERE userid=? AND artid=?;')
def unsave(userid, artid): pass


def get_saved(userid):
    try:
        artids = list()
        db = sqlite3.connect("data/artpi.db")
        c = db.cursor()
        c.execute(f"SELECT * FROM art WHERE userid=?", (userid,))
        fetched = c.fetchall()
        artids = [art[1] for art in fetched]
        return artids
    except sqlite3.Error as error:
        print(error)
        return None


def get_comments(artid):
    try:
        comments = list()
        db = sqlite3.connect("data/artpi.db")
        c = db.cursor()
        num = num_comments(artid)
        if(num > 0):
            c.execute("SELECT * FROM comments where artid=?", (artid,))
            comments = [list(c.fetchmany()[0]) for comment in range(0, num)]
        db.close()
        return comments
    except sqlite3.Error as error:
        print(error)
        return None


@builder.execute(err_type=sqlite3.Error, command='INSERT INTO comments(userid, artid, content, timestamp) VALUES (?,?,?,?);')
def comment(userid, artid, content, datetime): pass


@builder.execute(err_type=sqlite3.Error, command='UPDATE users SET password=? WHERE userid=?;')
def set_pw(npw, userid): pass


@builder.execute(err_type=sqlite3.Error, command='INSERT INTO art(userid, artid) VALUES (?,?);')
def save(userid, artid): pass


def init():
    inituser()
    initart()
    initcomment()
