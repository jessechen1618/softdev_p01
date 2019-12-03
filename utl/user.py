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
def inituser():
    """
    Create table for users in database.

    Returns:
        bool: A boolean signifying the success of the sql command.
    """
    pass


@builder.execute(err_type=sqlite3.Error, command='CREATE TABLE IF NOT EXISTS art (userid INTEGER, artid INTEGER);')
def initart():
    """
    Create table for saved art in database.

    Returns:
        bool: A boolean signifying the success of the sql command.
    """
    pass


@builder.execute(err_type=sqlite3.Error, command='''CREATE TABLE IF NOT EXISTS comments(
    commentid INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER, artid INTEGER,
    content TEXT CHECK (length(content) > 0),
    timestamp BLOB);''')
def initcomment():
    """
    Create table for comments in database.

    Returns:
        bool: A boolean signifying the success of the sql command.
    """
    pass


@builder.execute(err_type=sqlite3.Error, command='INSERT INTO users(username, password) VALUES (?,?);')
def create(un, pw):
    """
    Insert a new user into the users table.

    Parameters:
        un (str): A string of the user's username.
        pw (str): A string of the user's password.

    Returns:
        bool: A boolean signifying the success of the sql command.
    """
    pass


@builder.execute(err_type=IndexError, command='SELECT userid FROM users WHERE username=?;')
def get_id(un):
    """
    Retrieve the user id attached to the username.

    Parameters:
        un (str): A string of the user's username.

    Returns:
        int: An integer representing the user's id.
    """
    pass


@builder.execute(err_type=IndexError, command='SELECT username FROM users WHERE userid=?;')
def get_un(userid):
    """
    Retrieve the username attached to the userid.

    Parameters:
        userid (int): An integer represeting the user's userid.

    Returns:
        str: A string of the user's username.
    """
    pass


@builder.execute(err_type=IndexError, command='SELECT password FROM users WHERE username=?;')
def get_pw(un):
    """
    Retrieve the password attached to the username.

    Parameters:
        un (str): A string of the user's username.

    Returns:
        str: A string of the user's password.
    """
    pass


@builder.execute(err_type=IndexError, command='SELECT COUNT(*) FROM comments where artid=?;')
def num_comments(artid):
    """
    Retrieve the number of comments for an artwork.

    Parameters:
        artid (int): An integer representing the artwork's id.

    Returns:
        int: An integer of the number of comments an artwork has.
    """
    pass


@builder.execute(err_type=IndexError, command='SELECT COUNT(1) FROM art WHERE userid=? AND artid=?;')
def is_saved(userid, artid):
    """
    Signal whether a user has already saved a piece of art.

    Parameters:
        userid (int): An integer representing the user's id.
        artid (int): An integer representing the artwork's id.

    Returns:
        bool: A boolean signifying whether the user has already saved an artwork with the provided artid.
    """
    pass


def get_saved(userid):
    """
    Retrieve artwork ids that a user has saved.

    Parameters:
        userid (int): An integer representing the user's id.

    Returns:
        list: A list of all artids that a user has saved.
    """
    try:
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
    """
    Retrieve comments belonging to an artwork.

    Parameters:
        artid (int): An integer representing the artwork's id.

    Returns:
        list: A list of all comments belonging to an artwork.
    """
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
def comment(userid, artid, content, datetime):
    """
    Insert a new comment with all related information.

    Parameters:
        userid (int): An integer representing the user's id.
        artid (int): An integer representing the artwork's id.
        content (str): A string representing the content of the comment.
        datetime (datetime): A datetime representing when the comment was made.

    Returns:
        bool: A boolean signifying the success of the sql command.
    """
    pass

# updates password
@builder.execute(err_type=sqlite3.Error, command='UPDATE users SET password=? WHERE userid=?;')
def set_pw(npw, userid):
    """
    Update a user's password with a new password.

    Parameters:
        userid (int): An integer representing the user's id.
        npw (str): A string representing the user's new password.

    Returns:
        bool: A boolean signifying the success of the sql command.
    """
    pass

# saves artwork
@builder.execute(err_type=sqlite3.Error, command='INSERT INTO art(userid, artid) VALUES (?,?);')
def save(userid, artid):
    """
    Save a new artwork for the user.

    Parameters:
        userid (int): An integer representing the user's id.
        artid (int): An integer representing the artwork's id.

    Returns:
        bool: A boolean signifying the success of the sql command.
    """
    pass

# removes saved art
@builder.execute(err_type=sqlite3.Error, command='DELETE FROM art WHERE userid=? AND artid=?;')
def unsave(userid, artid):
    """
    Unsave a new artwork for the user.

    Parameters:
        userid (int): An integer representing the user's id.
        artid (int): An integer representing the artwork's id.

    Returns:
        bool: A boolean signifying the success of the sql command.
    """
    pass


def init():
    """Intialize the user, saved art, and comment tables in the database"""
    inituser()
    initart()
    initcomment()
