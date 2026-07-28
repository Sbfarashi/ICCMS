from datetime import datetime

from extensions import db


class FieldVisit(db.Model):
    __tablename__ = "field_visits"

    # =====================================================
    # Primary Key
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # Foreign Keys
    # =====================================================

    complaint_id = db.Column(
        db.Integer,
        db.ForeignKey("complaints.id"),
        nullable=False
    )

    engineer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # =====================================================
    # Visit Information
    # =====================================================

    visit_date = db.Column(
        db.Date,
        nullable=False
    )

    arrival_time = db.Column(
        db.Time
    )

    departure_time = db.Column(
        db.Time
    )

    # =====================================================
    # Visit Details
    # =====================================================

    observations = db.Column(db.Text)

    root_cause = db.Column(db.Text)

    work_done = db.Column(db.Text)

    materials_used = db.Column(db.Text)

    recommendation = db.Column(db.Text)

    # =====================================================
    # Meter Replacement
    # =====================================================

    meter_replaced = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    old_meter_number = db.Column(
        db.String(100)
    )

    new_meter_number = db.Column(
        db.String(100)
    )

    # =====================================================
    # Evidence
    # =====================================================

    before_photo = db.Column(
        db.String(255)
    )

    after_photo = db.Column(
        db.String(255)
    )

    customer_signature = db.Column(
        db.String(255)
    )

    # =====================================================
    # Audit
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # =====================================================
    # Relationships
    # =====================================================

    complaint = db.relationship(
        "Complaint",
        back_populates="field_visits"
    )

    engineer = db.relationship(
        "User",
        foreign_keys=[engineer_id]
    )

    # =====================================================
    # Display
    # =====================================================

    def __repr__(self):
        return (
            f"<FieldVisit "
            f"id={self.id}, "
            f"complaint_id={self.complaint_id}, "
            f"engineer_id={self.engineer_id}>"
        )