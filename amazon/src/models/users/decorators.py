from functools import wraps
from flask import session, url_for, redirect, request


def requires_login(func):
    @wraps(func)
    def decorated_function(*args,**kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args,**kwargs)
    return decorated_function


# @requires_login
# def my_function():
#     print("Hello world!")
#     return "Hi!"

#
# @requires_login
# def my_function(x,y,z):
#     return x + y + z
#


# print(my_function(1,2,3))




