from datetime import datetime

from extensions import db


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    activity = db.Column(
        db.String(255),
        nullable=False
    )

    module = db.Column(
        db.String(100),
        nullable=False
    )

    ip_address = db.Column(
        db.String(100)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="activity_logs"
    )

    def __repr__(self):
        return (
            f"<ActivityLog "
            f"User={self.user_id} "
            f"Module={self.module} "
            f"Activity={self.activity}>"
        )