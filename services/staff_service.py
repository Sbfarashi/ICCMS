from datetime import datetime

from extensions import db

from models.complaint import Complaint

from services.history_service import HistoryService


class StaffService:
    """
    Handles staff operations on complaints.
    """

    @staticmethod
    def get_assigned_complaints(staff_id):
        """
        Return all complaints assigned to a staff member.
        """

        return (
            Complaint.query
            .filter_by(assigned_to=staff_id)
            .order_by(Complaint.created_at.desc())
            .all()
        )

    @staticmethod
    def get_dashboard_statistics(staff_id):
        """
        Return dashboard statistics for the logged-in staff.
        """

        complaints = Complaint.query.filter_by(
            assigned_to=staff_id
        ).all()

        return {
            "total": len(complaints),
            "pending": sum(1 for c in complaints if c.status == "Pending"),
            "in_progress": sum(1 for c in complaints if c.status == "In Progress"),
            "resolved": sum(1 for c in complaints if c.status == "Resolved"),
            "closed": sum(1 for c in complaints if c.status == "Closed"),
        }

    @staticmethod
    def update_complaint(
        complaint_id,
        status,
        resolution,
        staff_id
    ):
        """
        Update complaint status and resolution.
        """

        try:

            complaint = Complaint.query.get(complaint_id)

            if complaint is None:
                return (
                    False,
                    "Complaint not found."
                )

            previous_status = complaint.status

            complaint.status = status

            if resolution:
                complaint.resolution = resolution.strip()

            # Set closed date automatically
            if status == "Closed":
                complaint.closed_at = datetime.utcnow()

            # Record history
            HistoryService.log(
                complaint_id=complaint.id,
                action="Status Updated",
                previous_status=previous_status,
                new_status=status,
                remarks=resolution,
                performed_by=staff_id
            )

            db.session.commit()

            return (
                True,
                "Complaint updated successfully."
            )

        except Exception as e:

            db.session.rollback()

            return (
                False,
                f"Failed to update complaint: {str(e)}"
            )

    @staticmethod
    def get_complaint(complaint_id):
        """
        Return a single complaint.
        """

        return Complaint.query.get(complaint_id)