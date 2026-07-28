from datetime import datetime
import random

from extensions import db

from models.complaint import Complaint

from services.intelligent import IntelligentEngine
from services.history_service import HistoryService


class ComplaintService:
    """
    Handles all complaint-related business logic.
    """

    @staticmethod
    def submit(
        customer_id,
        form,
        meter_number,
        location
    ):
        """
        Create and save a new complaint.

        Returns:
            (True, message) on success
            (False, message) on failure
        """

        try:

            title = form.subject.data.strip()
            description = form.description.data.strip()

            # ==========================================
            # Detect Category
            # ==========================================

            category_id = IntelligentEngine.detect_category(
                description
            )

            # Use category selected by the user if
            # automatic detection fails.
            if category_id is None:
                category_id = form.category.data

            # ==========================================
            # Assign Priority
            # ==========================================

            priority = IntelligentEngine.assign_priority(
                description
            )

            # ==========================================
            # Duplicate Detection
            # ==========================================

            duplicate = IntelligentEngine.is_duplicate(
                customer_id,
                meter_number,
                description
            )

            # ==========================================
            # Generate Complaint Number
            # ==========================================

            complaint_number = (
                f"CMP-{datetime.now():%Y%m%d%H%M%S}-"
                f"{random.randint(1000, 9999)}"
            )

            # ==========================================
            # Create Complaint
            # ==========================================

            complaint = Complaint(
                complaint_number=complaint_number,
                customer_id=customer_id,
                category_id=category_id,
                meter_number=meter_number,
                title=title,
                description=description,
                location=location,
                priority=priority,
                duplicate=duplicate,
                status="Pending"
            )

            db.session.add(complaint)

            # Flush so complaint.id is available
            db.session.flush()

            # ==========================================
            # Save Complaint History
            # ==========================================

            HistoryService.log(
                complaint_id=complaint.id,
                action="Complaint Submitted",
                previous_status=None,
                new_status="Pending",
                remarks="Customer submitted complaint.",
                performed_by=customer_id
            )

            # ==========================================
            # Commit Everything Once
            # ==========================================

            db.session.commit()

            return (
                True,
                "Complaint submitted successfully."
            )

        except Exception as e:

            db.session.rollback()

            return (
                False,
                f"Failed to submit complaint: {str(e)}"
            )