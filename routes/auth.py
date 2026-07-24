from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from forms.register_form import RegisterForm
from forms.login_form import LoginForm

from services.auth_service import AuthService

from constants.roles import UserRole

auth = Blueprint("auth", __name__)


# ===================================================
# REGISTER
# ===================================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        success, message = AuthService.register(form)

        if success:
            flash(message, "success")
            return redirect(url_for("auth.login"))

        flash(message, "danger")
        return redirect(url_for("auth.register"))

    return render_template(
        "auth/register.html",
        form=form
    )


# ===================================================
# LOGIN
# ===================================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        success, message, role = AuthService.login(form)

        print("\n================ ROUTE DEBUG ================")
        print("Returned Role:", role)
        print("ADMIN:", UserRole.ADMIN)
        print("STAFF:", UserRole.STAFF)
        print("ENGINEER:", UserRole.ENGINEER)
        print("SUPERVISOR:", UserRole.SUPERVISOR)
        print("=============================================\n")

        if success:

            flash(message, "success")

            if role == UserRole.ADMIN:

                print(">>> Redirecting to ADMIN dashboard")

                return redirect(url_for("admin.dashboard"))

            elif role == UserRole.STAFF:

                print(">>> Redirecting to STAFF dashboard")

                return redirect(url_for("staff.dashboard"))

            elif role == UserRole.ENGINEER:

                print(">>> Redirecting to ENGINEER dashboard")

                return redirect(url_for("staff.dashboard"))

            elif role == UserRole.SUPERVISOR:

                print(">>> Redirecting to SUPERVISOR dashboard")

                return redirect(url_for("staff.dashboard"))

            else:

                print(">>> Redirecting to CUSTOMER dashboard")

                return redirect(url_for("customer.dashboard"))

        flash(message, "danger")

    return render_template(
        "auth/login.html",
        form=form
    )


# ===================================================
# LOGOUT
# ===================================================

@auth.route("/logout")
def logout():

    AuthService.logout()

    flash(
        "You have successfully logged out.",
        "info"
    )

    return redirect(url_for("home"))