from flask import *
from functools import wraps
from ...config import Config


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.admin_login"))
        return f(*args, **kwargs)

    return decorated_function


def authenticate_admin(username, password):
    print(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
    return username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD
