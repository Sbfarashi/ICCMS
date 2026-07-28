from datetime import datetime

from extensions import db
from constants.roles import UserRole


class User(db.Model):
    __tablename__ = "users"

    # =====================================================
    # Primary Key
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # Basic Information
    # =====================================================

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    employee_id = db.Column(
        db.String(20),
        unique=True,
        nullable=True
    )

    designation = db.Column(
        db.String(100),
        nullable=True
    )

    profile_picture = db.Column(
        db.String(255),
        nullable=True,
        default="default_avatar.png"
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
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

    # =====================================================
    # Department
    # =====================================================

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=True
    )

    department = db.relationship(
        "Department",
        back_populates="users"
    )

    # =====================================================
    # Account
    # =====================================================

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    last_login = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # =====================================================
    # Customer Complaints
    # =====================================================

    complaints = db.relationship(
        "Complaint",
        foreign_keys="Complaint.customer_id",
        back_populates="customer",
        cascade="all, delete-orphan",
        lazy=True
    )

    # =====================================================
    # Assigned Complaints
    # =====================================================

    assigned_complaints = db.relationship(
        "Complaint",
        foreign_keys="Complaint.assigned_to",
        back_populates="staff",
        lazy=True
    )

    # =====================================================
    # Engineer Field Visits
    # =====================================================

    field_visits = db.relationship(
        "FieldVisit",
        foreign_keys="FieldVisit.engineer_id",
        back_populates="engineer",
        lazy=True
    )

    # =====================================================
    # Complaint History
    # =====================================================

    history = db.relationship(
        "ComplaintHistory",
        foreign_keys="ComplaintHistory.performed_by",
        back_populates="user",
        lazy=True
    )

    # =====================================================
    # Notifications
    # =====================================================

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    # =====================================================
    # Login History
    # =====================================================

    login_history = db.relationship(
        "LoginHistory",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    # =====================================================
    # Activity Logs
    # =====================================================

    activity_logs = db.relationship(
        "ActivityLog",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    # =====================================================
    # Helper Methods
    # =====================================================

    def is_admin(self):
        return self.role == UserRole.ADMIN

    def is_customer(self):
        return self.role == UserRole.CUSTOMER

    def is_staff(self):
        return self.role in UserRole.STAFF_ROLES

    def is_engineer(self):
        return self.role == UserRole.ENGINEER

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def update_last_login(self):
        self.last_login = datetime.utcnow()

    # =====================================================
    # Display
    # =====================================================

    def __repr__(self):
        return (
            f"<User("
            f"id={self.id}, "
            f"name='{self.full_name}', "
            f"role='{self.role}', "
            f"employee_id='{self.employee_id}')>"
        )