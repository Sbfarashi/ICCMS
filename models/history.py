from datetime import datetime
from extensions import db


class ComplaintHistory(db.Model):

    __tablename__ = "complaint_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=False
    )

    updated_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    old_status = db.Column(
        db.String(30)
    )

    new_status = db.Column(
        db.String(30)
    )

    remarks = db.Column(
        db.Text
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    complaint = db.relationship(
        "Complaint",
        back_populates="history"
    )

    user = db.relationship(
        "User"
    )