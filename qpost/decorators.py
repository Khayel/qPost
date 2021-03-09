from functools import wraps
from flask import redirect, session, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("LOGIN REQUIRED CHECK")
        if 'username' not in session or 'user_id' not in session:
            print(session)
            return redirect(url_for('views.login'))
        return(f(*args, **kwargs))
    return decorated_function
