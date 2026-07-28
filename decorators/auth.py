from functools import wraps

from flask import flash
from flask import redirect
from flask import session
from flask import url_for

from constants.roles import UserRole


# ==========================================================
# LOGIN REQUIRED
# ==========================================================

def login_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login first.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        return view(*args, **kwargs)

    return wrapped


# ==========================================================
# ROLE REQUIRED
# ==========================================================

def role_required(*roles):

    def decorator(view):

        @wraps(view)
        def wrapped(*args, **kwargs):

            if "user_id" not in session:

                flash(
                    "Authentication required.",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
                )

            current_role = session.get("role")

            if current_role not in roles:

                flash(
                    "You are not authorized to access this page.",
                    "danger"
                )

                return redirect(
                    url_for("auth.login")
                )

            return view(*args, **kwargs)

        return wrapped

    return decorator


# ==========================================================
# ADMIN
# ==========================================================

def admin_required(view):

    return role_required(
        UserRole.ADMIN
    )(view)


# ==========================================================
# STAFF
#
# Staff dashboard is temporarily shared with
# Staff, Engineer and Supervisor until their
# dedicated modules are completed.
# ==========================================================

def staff_required(view):

    return role_required(
        UserRole.STAFF,
        UserRole.ENGINEER,
        UserRole.SUPERVISOR
    )(view)


# ==========================================================
# ENGINEER
# ==========================================================

def engineer_required(view):

    return role_required(
        UserRole.ENGINEER
    )(view)


# ==========================================================
# SUPERVISOR
# ==========================================================

def supervisor_required(view):

    return role_required(
        UserRole.SUPERVISOR
    )(view)


# ==========================================================
# CUSTOMER
# ==========================================================

def customer_required(view):

    return role_required(
        UserRole.CUSTOMER
    )(view)