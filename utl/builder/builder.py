import sqlite3 
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