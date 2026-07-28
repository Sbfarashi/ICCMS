from functools import wraps
from flask import session, redirect, url_for, flash


def engineer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.get("logged_in"):
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login"))

        role = session.get("role", "").lower()

        allowed_roles = [
            "engineer",
            "staff",
            "supervisor",
            "administrator",
            "admin"
        ]

        if role not in allowed_roles:
            flash("You are not authorized to access this page.", "danger")
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function