from datetime import datetime

from extensions import db

from models.user import User
from models.complaint import Complaint

from services.history_service import HistoryService


class AssignmentService:

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

            .order_by(

                User.full_name.asc()

            )

            .all()

        )

    @staticmethod
    def assign_complaint(

        complaint_id,

        staff_id,

        admin_id

    ):

        try:

            complaint = Complaint.query.get(

                complaint_id

            )

            if complaint is None:

                return (

                    False,

                    "Complaint not found."

                )

            staff = User.query.get(

                staff_id

            )

            if staff is None:

                return (

                    False,

                    "Selected staff does not exist."

                )

            complaint.assigned_to = staff.id

            complaint.assigned_at = datetime.utcnow()

            HistoryService.log(

                complaint_id=complaint.id,

                action="Complaint Assigned",

                previous_status=complaint.status,

                new_status=complaint.status,

                remarks=f"Assigned to {staff.full_name}",

                performed_by=admin_id

            )

            db.session.commit()

            return (

                True,

                "Complaint assigned successfully."

            )

        except Exception as e:

            db.session.rollback()

            return (

                False,

                str(e)

            )