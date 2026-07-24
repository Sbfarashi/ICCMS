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

    action = db.Column(
        db.String(100),
        nullable=False
    )

    previous_status = db.Column(
        db.String(30)
    )

    new_status = db.Column(
        db.String(30)
    )

    remarks = db.Column(
        db.Text
    )

    performed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # ==========================================
    # Relationships
    # ==========================================

    complaint = db.relationship(
        "Complaint",
        back_populates="history"
    )

    user = db.relationship(
        "User",
        foreign_keys=[performed_by]
    )

    def __repr__(self):
        return (
            f"<ComplaintHistory "
            f"Complaint={self.complaint_id} "
            f"Action={self.action}>"
        )