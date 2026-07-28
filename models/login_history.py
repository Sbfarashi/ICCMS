from datetime import datetime

from extensions import db


class LoginHistory(db.Model):
    __tablename__ = "login_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    ip_address = db.Column(
        db.String(100),
        nullable=False
    )

    browser = db.Column(
        db.String(255)
    )

    operating_system = db.Column(
        db.String(255)
    )

    login_time = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    logout_time = db.Column(
        db.DateTime
    )

    login_status = db.Column(
        db.String(20),
        default="Success",
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="login_history"
    )

    def __repr__(self):

        return (
            f"<LoginHistory "
            f"{self.user_id} "
            f"{self.login_time}>"
        )