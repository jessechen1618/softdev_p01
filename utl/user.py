import sqlite3 
import os 
import functools

def execute(err_type, command):
    def decorator(f):
        @functools.wraps(f) #allows for several methods to have this decorator
        def wrapper(*args, **kwargs):
            try:
                db = sqlite3.connect('./data/artpi.db')
                select = db.execute(command, tuple(args)) # turn all user args into a format that command takes 
                db.commit()
                if(err_type != IndexError): # getter methods have index error exception
                    return True # should not return a boolean if method is a getter 
                else: return [item for item in select][0][0] # correctly retrieves data from select cursor
            except err_type as error:
                print(error)
                if(err_type != IndexError): return False
            finally: db.close() # close after everything is finished
        return wrapper
    return decorator

# initializes new users table 
@execute(err_type = sqlite3.Error,
    command = '''CREATE TABLE IF NOT EXISTS users ( userid INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    username TEXT UNIQUE CHECK (length(username) > 0),
                                                    password TEXT CHECK (length(password) > 0));''')
def init(): pass

@execute(err_type = sqlite3.Error, command = 'INSERT INTO users(username, password) VALUES (?,?);')
def create(un, pw): pass

@execute(err_type = sqlite3.Error, command = 'UPDATE users SET password=? WHERE userid=?;')
def set_pw(npw, userid): pass

@execute(err_type = IndexError, command = 'SELECT userid FROM users WHERE username=?;')
def get_id(un): pass

@execute(err_type = IndexError, command = 'SELECT password FROM users WHERE username=?;')
def get_pw(un): pass