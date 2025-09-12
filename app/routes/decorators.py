from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Acceso restringido ⚠️", "danger")
            return redirect(url_for("auth.login_classic"))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "user":
            flash("Acceso restringido ⚠️", "danger")
            return redirect(url_for("auth.login_classic"))
        return f(*args, **kwargs)
    return decorated_function

def farmacia_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "farmacia":
            flash("Acceso restringido ⚠️", "danger")
            return redirect(url_for("auth.login_classic"))
        return f(*args, **kwargs)
    return decorated_function
