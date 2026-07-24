from datetime import datetime

from extensions import db

from models.complaint import Complaint
from services.history_service import HistoryService


class AdminUpdateService:
    """
    Service for administrators to update complaints.
    """

    @staticmethod
    def get_complaint(complaint_id):
        """
        Retrieve a complaint by its ID.
        """
        return Complaint.query.get(complaint_id)

    @staticmethod
    def update_complaint(complaint_id, form, admin_id):
        """
        Update complaint details.
        """

        complaint = Complaint.query.get(complaint_id)

        if not complaint:
            return None

        previous_status = complaint.status

        # Update complaint fields
        complaint.status = form.status.data
        complaint.resolution = form.resolution.data

        # Automatically set closed date
        if form.status.data == "Closed":
            complaint.closed_at = datetime.utcnow()

        # Log history
        HistoryService.log(
            complaint_id=complaint.id,
            action="Complaint Updated by Administrator",
            previous_status=previous_status,
            new_status=complaint.status,
            remarks=form.resolution.data,
            performed_by=admin_id
        )

        db.session.commit()

        return complaint