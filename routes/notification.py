from flask import Blueprint, render_template, session, redirect, url_for

from models.notification import Notification
from models.database import db

notification = Blueprint(
    "notification",
    __name__,
    url_prefix="/notification"
)


@notification.route("/")
def index():

    if not session.get("logged_in"):
        return redirect(url_for("auth.login"))

    notifications = (
        Notification.query
        .filter_by(user_id=session["user_id"])
        .order_by(Notification.created_at.desc())
        .all()
    )

    return render_template(
        "notification/index.html",
        notifications=notifications
    )


@notification.route("/read/<int:id>")
def mark_read(id):

    notification_item = Notification.query.get_or_404(id)

    if notification_item.user_id == session["user_id"]:

        notification_item.is_read = True

        db.session.commit()

    return redirect(url_for("notification.index"))


@notification.route("/read-all")
def read_all():

    Notification.query.filter_by(
        user_id=session["user_id"],
        is_read=False
    ).update(
        {"is_read": True}
    )

    db.session.commit()

    return redirect(url_for("notification.index"))