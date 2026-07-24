from datetime import datetime

from extensions import db


class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    complaint_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id")
    )

    meter_number = db.Column(
        db.String(50),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.String(200)
    )

    priority = db.Column(
        db.String(20),
        default="Medium",
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending",
        nullable=False
    )

    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    # Date and time when the complaint was assigned
    assigned_at = db.Column(
        db.DateTime
    )

    duplicate = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    escalation_level = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    resolution = db.Column(
        db.Text
    )

    closed_at = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # ==========================================
    # Relationships
    # ==========================================

    customer = db.relationship(
        "User",
        foreign_keys=[customer_id],
        back_populates="complaints"
    )

    category = db.relationship(
        "Category",
        back_populates="complaints"
    )

    staff = db.relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="assigned_complaints"
    )

    history = db.relationship(
        "ComplaintHistory",
        back_populates="complaint",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return (
            f"<Complaint("
            f"Number={self.complaint_number}, "
            f"Status={self.status}, "
            f"Priority={self.priority})>"
        )