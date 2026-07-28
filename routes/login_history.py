from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from decorators.auth import login_required
from services.login_history_service import LoginHistoryService


login_history = Blueprint(
    "login_history",
    __name__,
    url_prefix="/login-history"
)


# ==========================================================
# USER LOGIN HISTORY
# ==========================================================

@login_history.route("/")
@login_required
def index():

    history = LoginHistoryService.get_user_history(
        session["user_id"]
    )

    return render_template(
        "login_history/index.html",
        history=history
    )