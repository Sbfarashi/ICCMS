from datetime import datetime

from extensions import db


class Department(db.Model):
    __tablename__ = "departments"

    # =====================================================
    # Basic Information
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # Relationships
    # =====================================================

    users = db.relationship(
        "User",
        back_populates="department",
        lazy=True
    )

    def __repr__(self):
        return f"<Department {self.name}>"