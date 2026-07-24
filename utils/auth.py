from functools import wraps

from flask import session
from flask import redirect
from flask import url_for
from flask import flash

from constants.roles import UserRole


# ===================================================
# LOGIN REQUIRED DECORATOR
# ===================================================

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login first.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        return function(*args, **kwargs)

    return wrapper


# ===================================================
# ADMIN REQUIRED DECORATOR
# ===================================================

def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if session.get("role") != UserRole.ADMIN:

            flash(
                "Administrator access required.",
                "danger"
            )

            return redirect(
                url_for("home")
            )

        return function(*args, **kwargs)

    return wrapper


# ===================================================
# STAFF REQUIRED DECORATOR
# ===================================================

def staff_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        role = session.get("role")

        if role not in [UserRole.STAFF, UserRole.ENGINEER]:

            flash(
                "Staff access required.",
                "danger"
            )

            return redirect(
                url_for("home")
            )

        return function(*args, **kwargs)

    return wrapper


# ===================================================
# CUSTOMER REQUIRED DECORATOR
# ===================================================

def customer_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if session.get("role") != UserRole.CUSTOMER:

            flash(
                "Customer access required.",
                "danger"
            )

            return redirect(
                url_for("home")
            )

        return function(*args, **kwargs)

    return wrapper