from datetime import datetime

from extensions import db
from constants.roles import UserRole


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default=UserRole.CUSTOMER,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    last_login = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ==========================================
    # Complaints Submitted by Customer
    # ==========================================

    complaints = db.relationship(
        "Complaint",
        foreign_keys="Complaint.customer_id",
        back_populates="customer",
        cascade="all, delete-orphan",
        lazy=True
    )

    # ==========================================
    # Complaints Assigned to Staff
    # ==========================================

    assigned_complaints = db.relationship(
        "Complaint",
        foreign_keys="Complaint.assigned_to",
        back_populates="staff",
        lazy=True
    )

    # ==========================================
    # Complaint History
    # ==========================================

    history = db.relationship(
        "ComplaintHistory",
        foreign_keys="ComplaintHistory.performed_by",
        back_populates="user",
        lazy=True
    )

    # ==========================================
    # Notifications
    # ==========================================

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.full_name}>"