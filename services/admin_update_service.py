from datetime import datetime

from extensions import db

from models.complaint import Complaint

from services.history_service import HistoryService
from services.notification_service import NotificationService


class AdminUpdateService:
    """
    Service for administrators to update complaints.
    """

    # =====================================================
    # Get Complaint
    # =====================================================

    @staticmethod
    def get_complaint(complaint_id):

        return Complaint.query.get_or_404(
            complaint_id
        )

    # =====================================================
    # Update Complaint
    # =====================================================

    @staticmethod
    def update_complaint(
        complaint_id,
        form,
        admin_id
    ):

        complaint = Complaint.query.get_or_404(
            complaint_id
        )

        previous_status = complaint.status

        # ==========================================
        # Update Complaint
        # ==========================================

        complaint.status = form.status.data
        complaint.resolution = form.resolution.data

        # ==========================================
        # Automatically record closure time
        # ==========================================

        if complaint.status == "Closed":

            if complaint.closed_at is None:
                complaint.closed_at = datetime.utcnow()

        else:

            complaint.closed_at = None

        # ==========================================
        # Save History
        # ==========================================

        HistoryService.log(

            complaint_id=complaint.id,

            action="Complaint Updated by Administrator",

            previous_status=previous_status,

            new_status=complaint.status,

            remarks=form.resolution.data,

            performed_by=admin_id

        )

        # ==========================================
        # General Status Notification
        # ==========================================

        NotificationService.create(

            user_id=complaint.customer_id,

            title="Complaint Status Updated",

            message=(
                f"Your complaint "
                f"{complaint.complaint_number} "
                f"is now '{complaint.status}'."
            ),

            notification_type="Status"

        )

        # ==========================================
        # Resolution Notification
        # ==========================================

        if complaint.status == "Resolved":

            NotificationService.create(

                user_id=complaint.customer_id,

                title="Complaint Resolved",

                message=(
                    f"Your complaint "
                    f"{complaint.complaint_number} "
                    f"has been resolved successfully."
                ),

                notification_type="Resolution"

            )

        # ==========================================
        # Closure Notification
        # ==========================================

        elif complaint.status == "Closed":

            NotificationService.create(

                user_id=complaint.customer_id,

                title="Complaint Closed",

                message=(
                    f"Your complaint "
                    f"{complaint.complaint_number} "
                    f"has been closed."
                ),

                notification_type="Closure"

            )

        db.session.commit()

        return complaint