from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.change_password_form import ChangePasswordForm

from services.auth_service import AuthService
from services.login_history_service import LoginHistoryService
from services.activity_log_service import ActivityLogService

from models.user import User

from constants.roles import UserRole

from decorators.auth import login_required


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

            return redirect(
                url_for("auth.login")
            )

        flash(message, "danger")

        return redirect(
            url_for("auth.register")
        )

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

        if success:

            # ============================================
            # Record Login History
            # ============================================

            user = User.query.filter_by(
                id=session["user_id"]
            ).first()

            if user:

                LoginHistoryService.record_login(user)

                ActivityLogService.log(
                    user_id=user.id,
                    activity="Logged into the system",
                    module="Authentication"
                )

            flash(message, "success")

            if role == UserRole.ADMIN:

                return redirect(
                    url_for("admin.dashboard")
                )

            elif role == UserRole.ENGINEER:

                return redirect(
                    url_for("engineer.dashboard")
                )

            elif role == UserRole.STAFF:

                return redirect(
                    url_for("staff.dashboard")
                )

            elif role == UserRole.SUPERVISOR:

                return redirect(
                    url_for("staff.dashboard")
                )

            elif role == UserRole.CUSTOMER:

                return redirect(
                    url_for("customer.dashboard")
                )

            flash(
                "Unknown user role.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        flash(message, "danger")

    return render_template(
        "auth/login.html",
        form=form
    )


# ===================================================
# CHANGE PASSWORD
# ===================================================

@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        success, message = AuthService.change_password(
            session["user_id"],
            form
        )

        if success:

            ActivityLogService.log(
                user_id=session["user_id"],
                activity="Changed account password",
                module="Account"
            )

            flash(
                message,
                "success"
            )

            role = session.get("role")

            if role == UserRole.ADMIN:

                return redirect(
                    url_for("admin.dashboard")
                )

            elif role == UserRole.ENGINEER:

                return redirect(
                    url_for("engineer.profile")
                )

            elif role == UserRole.STAFF:

                return redirect(
                    url_for("staff.dashboard")
                )

            elif role == UserRole.SUPERVISOR:

                return redirect(
                    url_for("staff.dashboard")
                )

            elif role == UserRole.CUSTOMER:

                return redirect(
                    url_for("customer.dashboard")
                )

            return redirect(
                url_for("home")
            )

        flash(
            message,
            "danger"
        )

    return render_template(
        "auth/change_password.html",
        form=form
    )


# ===================================================
# LOGOUT
# ===================================================

@auth.route("/logout")
@login_required
def logout():

    if session.get("user_id"):

        ActivityLogService.log(
            user_id=session["user_id"],
            activity="Logged out of the system",
            module="Authentication"
        )

        LoginHistoryService.record_logout(
            session["user_id"]
        )

    AuthService.logout()

    flash(
        "You have successfully logged out.",
        "info"
    )

    return redirect(
        url_for("home")
    )