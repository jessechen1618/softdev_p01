'''
put me to REST - Jesse "McCree" Chen, Kelvin Ng, Eric "Morty" Lau, David Xiedeng
SoftDev1 pd1
P1 ArRESTed Development
'''

import sqlite3 
from .builder import builder 

# initializes new users table 
@builder.execute(err_type = sqlite3.Error,
    command = '''CREATE TABLE IF NOT EXISTS users ( 
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE CHECK (length(username) > 0),
                password TEXT CHECK (length(password) > 0));''')
def init(): pass

@builder.execute(err_type = sqlite3.Error, command = 'INSERT INTO users(username, password) VALUES (?,?);')
def create(un, pw): pass

@builder.execute(err_type = sqlite3.Error, command = 'UPDATE users SET password=? WHERE userid=?;')
def set_pw(npw, userid): pass

@builder.execute(err_type = IndexError, command = 'SELECT userid FROM users WHERE username=?;')
def get_id(un): pass

@builder.execute(err_type = IndexError, command = 'SELECT password FROM users WHERE username=?;')
def get_pw(un): pass