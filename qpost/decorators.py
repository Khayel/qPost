from functools import wraps
from flask import redirect, session, url_for


def login_required(f):
    """
    Decorator function to verify login session of a user
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("LOGIN REQUIRED CHECK")
        if 'username' not in session or 'user_id' not in session:
            print(session)
            return redirect(url_for('views.login'))
        return(f(*args, **kwargs))
    return decorated_function


def teacher_required(f):
    """
    Decorator function to verify user is a teacher
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("TEACHER REQUIRED CHECK")
        if 'is_teacher' in session and session['is_teacher'] == False:
            print(session)
            return redirect(url_for('views.index'))
        return(f(*args, **kwargs))
    return decorated_function
