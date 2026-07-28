from datetime import datetime

from extensions import db

from models.user import User
from models.complaint import Complaint

from services.history_service import HistoryService
from services.notification_service import NotificationService


class AssignmentService:
    """
    Service for assigning complaints to staff members.
    """

    # =====================================================
    # Get Assignable Staff
    # =====================================================

    @staticmethod
    def get_staff():

        return (

            User.query

            .filter(

                User.role.in_(

                    [
                        "staff",
                        "engineer",
                        "technician",
                        "support"
                    ]

                )

            )

            .filter(

                User.is_active == True

            )

            .order_by(

                User.full_name.asc()

            )

            .all()

        )

    # =====================================================
    # Assign Complaint
    # =====================================================

    @staticmethod
    def assign_complaint(

        complaint_id,
        staff_id,
        admin_id

    ):

        try:

            complaint = Complaint.query.get_or_404(
                complaint_id
            )

            staff = User.query.get_or_404(
                staff_id
            )

            allowed_roles = [

                "staff",
                "engineer",
                "technician",
                "support"

            ]

            if staff.role not in allowed_roles:

                return (

                    False,

                    "Selected user cannot receive complaint assignments.",

                    None

                )

            if complaint.assigned_to == staff.id:

                return (

                    False,

                    "Complaint is already assigned to this staff member.",

                    complaint

                )

            previous_status = complaint.status

            complaint.assigned_to = staff.id
            complaint.assigned_at = datetime.utcnow()
            complaint.status = "Assigned"

            HistoryService.log(

                complaint_id=complaint.id,

                action="Complaint Assigned",

                previous_status=previous_status,

                new_status="Assigned",

                remarks=f"Assigned to {staff.full_name}",

                performed_by=admin_id

            )

            NotificationService.create(

                user_id=staff.id,

                title="New Complaint Assigned",

                message=(

                    f"You have been assigned complaint "

                    f"{complaint.complaint_number}."

                ),

                notification_type="Assignment"

            )

            NotificationService.create(

                user_id=complaint.customer_id,

                title="Complaint Assigned",

                message=(

                    f"Your complaint "

                    f"{complaint.complaint_number} "

                    f"has been assigned to our support team."

                ),

                notification_type="Status"

            )

            db.session.commit()

            return (

                True,

                "Complaint assigned successfully.",

                complaint

            )

        except Exception as e:

            db.session.rollback()

            return (

                False,

                str(e),

                None

            )