import sqlite3
import functools


def execute(err_type, command):
    def decorator(f):
        # allows for several methods to have this decorator
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                db = sqlite3.connect('./data/artpi.db')
                # turn all user args into a format that command takes
                select = db.execute(command, tuple(args))
                db.commit()
                if(err_type != IndexError):  # getter methods have index error exception
                    return True  # should not return a boolean if method is a getter
                else:
                    # correctly retrieves data from select cursor
                    return [item for item in select][0][0]
            except err_type as error:
                print(error)
                if(err_type != IndexError):
                    return False
            finally:
                db.close()  # close after everything is finished
        return wrapper
    return decorator
