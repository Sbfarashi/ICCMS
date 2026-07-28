from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from services.activity_log_service import ActivityLogService
from decorators.auth import login_required
from constants.roles import UserRole

activity_log = Blueprint(
    "activity_log",
    __name__,
    url_prefix="/activity-log"
)


# ======================================================
# View Activity Logs
# ======================================================

@activity_log.route("/")
@login_required
def index():

    role = session.get("role")

    if role == UserRole.ADMIN:

        logs = ActivityLogService.get_all_logs()

    else:

        logs = ActivityLogService.get_user_logs(
            session["user_id"]
        )

    return render_template(
        "activity_log/index.html",
        logs=logs
    )